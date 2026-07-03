from pathlib import Path
import yaml


def load_jobs():
    """
    Read config/jobs.yaml and return the list of jobs.
    """

    project_root = Path(__file__).resolve().parents[3]

    jobs_file = project_root / "config" / "jobs.yaml"

    with open(jobs_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data["jobs"]