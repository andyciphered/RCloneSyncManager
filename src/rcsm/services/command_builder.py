from pathlib import Path

from rcsm.models.job import SyncJob


CONFLICT_RESOLVE_VALUES = {
    "push": "newer",
    "pull": "older",
}


def build_command(
    job: SyncJob,
    execution_mode: str = "normal",
    conflict: str | None = None,
    dry_run: bool = False,
) -> list[str]:
    """
    Build the rclone command for a sync job.
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
        command.extend(
            [
                "--exclude-from",
                f"config/excludes/{job.exclude}",
                "--exclude-from",
                str(exclude_file),
            ]
        )

# Execution mode modifiers

    if execution_mode == "resync":
        command.append("--resync")

    elif execution_mode == "force":

        command.append("--force")

        if conflict:
            command.extend(
                [
                    "--conflict-resolve",
                    CONFLICT_RESOLVE_VALUES.get(conflict, conflict),
                ]
            )

    if dry_run:
        command.append("--dry-run")

    return command
