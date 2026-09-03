from datetime import datetime
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
LOG_FILE = LOG_DIR / "sync.log"


def log_sync(job_name, result, duration):
    """
    Write a sync execution result to the log file.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    status = "SUCCESS" if result == 0 else f"FAILED ({result})"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"{timestamp} | "
        f"{job_name} | "
        f"{status} | "
        f"{duration:.1f}s\n"
    )

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(entry)

def get_sync_history():
    """
    Read sync history from the log file.
    """

    if not LOG_FILE.exists():
        return []

    history = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = [part.strip() for part in line.split("|")]

            if len(parts) != 4:
                continue

            timestamp, job_name, status, duration = parts

            history.append(
                {
                    "timestamp": timestamp,
                    "job_name": job_name,
                    "status": status,
                    "duration": duration,
                }
            )

    return history