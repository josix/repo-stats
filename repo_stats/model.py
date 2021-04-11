from typing import List

from pydantic import BaseModel


class PullRequestStats(BaseModel):
    author: List[str]
    pull_request: List[int]
    comment: List[int]
    commit: List[int]


class Message(BaseModel):
    message: str
