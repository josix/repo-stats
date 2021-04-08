import asyncio
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import FastAPI

from repo_stats.fecher.commit import fetch_pr_commits
from repo_stats.fecher.graphql_client import graphql_connection

load_dotenv()

app = FastAPI()


@app.get("/commits/{repo_owner}/{repo_name}")
async def get_commit(
    repo_owner: str, repo_name: str, last: int = 100, csv: bool = False
):
    response: dict = defaultdict(None)
    async with graphql_connection() as session:
        fetch_pr_commits_task = asyncio.create_task(
            fetch_pr_commits(
                session,
                response,
                repo_owner=repo_owner,
                repo_name=repo_name,
                limit=last,
            )
        )
        await asyncio.gather(fetch_pr_commits_task)
    pull_requests = response["result"]["repository"]["pullRequests"]["nodes"]
    return pull_requests
