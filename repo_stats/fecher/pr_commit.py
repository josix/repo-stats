from gql import gql


async def fetch_pr_commits(
    session, response, repo_owner: str, repo_name: str, limit=50
) -> None:
    query = gql(
        """
        query getPRCommits($name: String!, $owner: String!, $limit: Int) {
            repository(name: $name, owner: $owner) {
                pullRequests(last: $limit) {
                nodes {
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
    result = await session.execute(document=query, variable_values=params)
    response["result"] = result
