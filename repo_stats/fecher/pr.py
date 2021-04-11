from gql import gql
from gql.transport.exceptions import TransportQueryError

from repo_stats.fecher.common import GraphAPIResponse


async def fetch_pr_info(
    session, response: GraphAPIResponse, repo_owner: str, repo_name: str, limit=50
) -> None:
    query = gql(
        """
        query getPRStats($name: String!, $owner: String!, $limit: Int) {
            repository(name: $name, owner: $owner) {
                pullRequests(last: $limit) {
                nodes {
                    author {
                    login
                    }
                    commits(last: $limit) {
                    nodes {
                        commit {
                        author {
                            user {
                            login
                            }
                        }
                        }
                    }
                    }
                    comments(last: $limit) {
                    nodes {
                        author {
                        login
                        }
                    }
                    }
                    reviews(last: $limit) {
                    nodes {
                        author {
                        login
                        }
                    }
                    }
                }
                }
            }
            }
        """
    )
    params = {
        "name": repo_name,
        "owner": repo_owner,
        "limit": limit,
    }
    try:
        result = await session.execute(document=query, variable_values=params)
        response.update_status("SUCCESS")
        response.result = result
    except TransportQueryError:
        response.update_status("NOT_FOUND")
