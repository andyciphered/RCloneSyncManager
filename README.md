# RCloneSyncManager

A personal macOS cloud synchronization manager powered by rclone.

## Features

- Bisync
- Upload
- Download
- Sync All
- Execution Modes

  - Normal
  - Resync
  - Force
- Automatic Resync Recovery
- YAML Configuration
- Rich Terminal UI
- Progress Display
- Logging & Sync History
- Configuration Validation
- Remote & Local Path Validation
- Pre-flight Checks
- macOS Launcher

## Requirements

- macOS
- Python 3.13+
- rclone

## Usage

### Launch from Terminal

From the project directory:

```bash
python -m rcsm
```

### Launch with the macOS launcher

Double-click:

```text
RCloneSyncManager.command
```

The launcher activates the project's virtual environment and starts RCloneSyncManager.

## Configuration

Sync jobs are configured in:

```text
config/jobs.yaml
```

Exclude files are stored in:

```text
config/excludes/
```

## Project Structure

```text
RCloneSyncManager/
├── config/
│   ├── excludes/
│   └── jobs.yaml
├── src/
│   └── rcsm/
├── logs/
├── RCloneSyncManager.command
├── PROJECT.md
├── README.md
└── pyproject.toml
```

## Notes

RCloneSyncManager is designed for personal use on macOS and uses rclone for all cloud synchronization operations.
