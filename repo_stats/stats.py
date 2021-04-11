from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class StatsCounterBase:
    author: List[str] = field(default_factory=list)
    comment: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def update_author(self, login) -> None:
        if login not in set(self.author):
            self.author.append(login)

    def update_comment(self, login, count=1) -> None:
        self.update_author(login)
        self.comment[login] += count

    def json(self) -> dict:
        return NotImplemented

    def csv(self) -> dict:
        return NotImplemented


@dataclass
class PRStatsCounter(StatsCounterBase):
    review: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    commit: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    pull_request: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def update_pull_request(self, login, count=1):
        self.update_author(login)
        self.pull_request[login] += count

    def update_commit(self, login, count=1):
        self.update_author(login)
        self.commit[login] += count

    def update_review(self, login, count=1):
        self.update_author(login)
        self.review[login] += count

    def json(self):
        return {
            "author": self.author,
            "pull_request": [self.pull_request[author] for author in self.author],
            "comment": [self.comment[author] for author in self.author],
            "commit": [self.commit[author] for author in self.author],
            "review": [self.review[author] for author in self.author],
        }

    def csv(self):
        header = ",".join(["Author", "#Pull Request", "#Comment", "#Commit", "#Review"])
        content = [
            ",".join(
                [
                    author,
                    str(self.pull_request[author]),
                    str(self.comment[author]),
                    str(self.commit[author]),
                    str(self.review[author]),
                ]
            )
            for author in self.author
        ]
        return "\n".join([header, *content])
