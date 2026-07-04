from pathlib import Path

import yaml

from rcsm.models.job import SyncJob


def load_jobs():

    project_root = Path(__file__).resolve().parents[3]

    jobs_file = project_root / "config" / "jobs.yaml"

    with open(jobs_file, "r", encoding="utf-8") as file:

        data = yaml.safe_load(file)

    jobs = []

    for item in data["jobs"]:

        jobs.append(
            SyncJob(
                id=item["id"],
                name=item["name"],
                group=item["group"],
                remote=item["remote"],
                local=item["local"],
                mode=item["mode"],
                exclude=item.get("exclude"),
            )
        )

    return jobs