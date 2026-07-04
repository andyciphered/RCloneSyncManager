from pathlib import Path

from rcsm.models.job import SyncJob


def build_command(job: SyncJob) -> list[str]:
    """
    Build the rclone command for a sync job.
    Returns the command as a list, ready for subprocess.run().
    """

    local = str(Path(job.local).expanduser())
    remote = job.remote

    if job.mode == "bisync":
        command = [
            "rclone",
            "bisync",
            local,
            remote,
        ]

    elif job.mode == "download":
        command = [
            "rclone",
            "sync",
            remote,
            local,
        ]

    elif job.mode == "upload":
        command = [
            "rclone",
            "sync",
            local,
            remote,
        ]

    else:
        raise ValueError(f"Unknown mode: {job.mode}")

    if job.exclude:
        command.extend([
            "--exclude-from",
            f"config/excludes/{job.exclude}"
        ])

    return command