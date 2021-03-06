import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, StreamingResponse

from repo_stats.fecher.common import GraphAPIResponse
from repo_stats.fecher.graphql_client import graphql_connection
from repo_stats.fecher.pr import fetch_pr_info
from repo_stats.fecher.issue import fetch_issue_info
from repo_stats.model import Message, PullRequestStats, IssueStats
from repo_stats.stats import PRStatsCounter, IssueStatsCounter

load_dotenv()

app = FastAPI()

@app.get(
    '/issues/{repo_owner}/{repo_name}',
    response_model=IssueStats,
    responses={
        404: {"model": Message},
        503: {"model": Message},
        500: {"model": Message},
    },
)
async def get_issue_stats(
    repo_owner: str, repo_name: str, last: int = 100, csv: bool = False
):
    response: GraphAPIResponse = GraphAPIResponse(
        result=dict(),
    )
    async with graphql_connection() as session:
        fetch_issue_info_task = asyncio.create_task(
            fetch_issue_info(
                session,
                response,
                repo_owner=repo_owner,
                repo_name=repo_name,
                limit=last,
            )
        )
        await asyncio.gather(fetch_issue_info_task)
    if response.status == "SUCCESS":
        result = response.result
        issues = result["repository"]["issues"]["nodes"]
        stats = IssueStatsCounter()
        for issue in issues:
            author, comments = (
                issue["author"]["login"],
                issue["comments"]["nodes"],
            )
            stats.update_issue(author)
            for comment in comments:
                login = comment["author"]["login"]
                stats.update_comment(login)
        if csv:
            return StreamingResponse(
                stats.csv(),
                media_type="text/csv",
                headers={"Content-Disposition": "filename=issue_stats.csv"},
            )
        else:
            return stats.json()
    elif response.status == "NOT_FOUND":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Resource not found"},
        )
    elif response.status == "UNAVAILABLE":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "GitHub Graph API is unavailable"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error"},
        )

@app.get(
    "/pull_requests/{repo_owner}/{repo_name}",
    response_model=PullRequestStats,
    responses={
        404: {"model": Message},
        503: {"model": Message},
        500: {"model": Message},
    },
)
async def get_pull_request_stats(
    repo_owner: str, repo_name: str, last: int = 100, csv: bool = False
):
    response: GraphAPIResponse = GraphAPIResponse(
        result=dict(),
    )
    async with graphql_connection() as session:
        fetch_pr_info_task = asyncio.create_task(
            fetch_pr_info(
                session,
                response,
                repo_owner=repo_owner,
                repo_name=repo_name,
                limit=last,
            )
        )
        await asyncio.gather(fetch_pr_info_task)
    if response.status == "SUCCESS":
        result = response.result
        pull_requests = result["repository"]["pullRequests"]["nodes"]
        stats = PRStatsCounter()
        for pull_request in pull_requests:
            author, commits, comments, reviews = (
                pull_request["author"]["login"],
                pull_request["commits"]["nodes"],
                pull_request["comments"]["nodes"],
                pull_request["reviews"]["nodes"],
            )
            stats.update_pull_request(author)
            for commit in commits:
                if commit["commit"]["author"]["user"]:
                    login = commit["commit"]["author"]["user"]["login"]
                    stats.update_commit(login)
            for review in reviews:
                login = review["author"]["login"]
                stats.update_review(login)
            for comment in comments:
                login = comment["author"]["login"]
                stats.update_comment(login)
        if csv:
            return StreamingResponse(
                stats.csv(),
                media_type="text/csv",
                headers={"Content-Disposition": "filename=pull_request_stats.csv"},
            )
        else:
            return stats.json()
    elif response.status == "NOT_FOUND":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Resource not found"},
        )
    elif response.status == "UNAVAILABLE":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "GitHub Graph API is unavailable"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error"},
        )
