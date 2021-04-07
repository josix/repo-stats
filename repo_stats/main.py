from fastapi import FastAPI
from fecher.commit import fetch_commits

app = FastAPI()


@app.get("/commits/{repo_owner}/{repo_name}")
async def get_commit(repo_owner: str, repo_name: str):
    await fetch_commits(repo_owner=repo_owner, repo_name=repo_name)
    return {"message": "Hello World"}
