from pathlib import Path

import yaml

from rcsm.models.job import SyncJob


def load_jobs():

    project_root = Path(__file__).resolve().parents[3]

    jobs_file = project_root / "config" / "jobs.yaml"

    with open(jobs_file, "r", encoding="utf-8") as file:

        data = yaml.safe_load(file)

    jobs = []

    required_fields = [
        "id",
        "name",
        "group",
        "remote",
        "local",
        "mode",
    ]

    valid_modes = {
        "bisync",
        "download",
        "upload",
    }

    exclude_dir = (
        project_root
        / "config"
        / "excludes"
    )

    for item in data["jobs"]:

        for field in required_fields:

            if field not in item or item[field] in (None, ""):
                raise ValueError(
                    f"Configuration error: "
                    f"Job is missing required field '{field}'."
                )

        if item["mode"] not in valid_modes:
            raise ValueError(
                f"Configuration error: "
                f"Job '{item['name']}' has invalid mode "
                f"'{item['mode']}'. "
                f"Valid modes: bisync, download, upload."
            )

        if item.get("exclude"):

            exclude_file = (
                exclude_dir
                / item["exclude"]
            )

            if not exclude_file.exists():
                raise ValueError(
                    f"Configuration error: "
                    f"Job '{item['name']}' references "
                    f"missing exclude file "
                    f"'{item['exclude']}'."
                )

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