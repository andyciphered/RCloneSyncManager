from dataclasses import dataclass


@dataclass
class SyncJob:
    id: str
    name: str
    group: str
    remote: str
    local: str
    mode: str
    exclude: str | None = None