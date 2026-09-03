import shutil
import subprocess
from pathlib import Path

def check_rclone():

    return shutil.which("rclone") is not None


def check_remote(remote):

    remote_name = remote.split(":", 1)[0]

    result = subprocess.run(
        ["rclone", "listremotes"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return False

    remotes = [
        line.strip().rstrip(":")
        for line in result.stdout.splitlines()
    ]

    return remote_name in remotes

def check_remotes(jobs):

    result = subprocess.run(
        ["rclone", "listremotes"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    remotes = {
        line.strip().rstrip(":")
        for line in result.stdout.splitlines()
    }

    missing = []

    for job in jobs:

        remote_name = job.remote.split(":", 1)[0]

        if remote_name not in remotes:
            missing.append(
                (job.name, remote_name)
            )

    return missing

def check_local_paths(jobs):

    missing = []
    invalid = []

    for job in jobs:

        local = Path(job.local).expanduser()

        if not local.exists():
            missing.append(
                (job.name, str(local))
            )

        elif not local.is_dir():
            invalid.append(
                (job.name, str(local))
            )

    return missing, invalid

def validate_job(job):

    local = Path(job.local).expanduser()

    if local.exists() and not local.is_dir():
        return False, f"Local path is not a directory: {local}"

    if not check_remote(job.remote):
        remote_name = job.remote.split(":", 1)[0]
        return False, f"Remote is not available: {remote_name}"

    return True, ""
