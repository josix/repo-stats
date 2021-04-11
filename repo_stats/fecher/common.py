from dataclasses import dataclass


@dataclass
class GraphAPIResponse:
    result: dict
    status: str = "PENDING"
    _all_status = frozenset(
        {"NOT_FOUND", "INVALID", "SUCCESS", "PENDING", "UNAVAILABLE"}
    )

    def update_status(self, new_status: str):
        if new_status not in self._all_status:
            raise ValueError("Invalid status")
        self.status = new_status
