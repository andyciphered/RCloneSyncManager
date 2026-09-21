# RCloneSyncManager

A personal macOS cloud synchronization manager powered by rclone.

---

# Current Status

Version: v1.0.0

Current Milestone:

Version 1 feature set complete.

Final cleanup and project hardening in progress.

---

# Version 1 Goals

## Feature 007 — Execution Modes

- [x] Normal
- [x] Resync
- [x] Force
- [x] Automatic Resync Recovery

## Feature 008 — Sync All

- [x] Sync all applicable jobs
- [x] Shared execution mode selection
- [x] Job summary
- [x] Success and failure reporting
- [x] Total execution time

## Feature 009 — Logging & Sync History

- [x] Timestamp
- [x] Job name
- [x] Status
- [x] Duration
- [x] Sync history display
- [x] History limited to latest 20 entries

## Feature 010 — Polish & Stabilization

- [x] Cleaner menus
- [x] Progress display
- [x] Better summaries
- [x] Error reporting
- [x] Version cleanup
- [x] Regression testing

## Feature 011 — Reliability & Safety

- [x] Configuration validation
- [x] Remote validation
- [x] Local path validation
- [x] Pre-flight checks
- [x] Job-aware execution modes
- [x] Safe handling of non-bisync jobs

---

# Completed

- [x] Python project structure
- [x] Virtual environment
- [x] Rich terminal UI
- [x] Health check
- [x] YAML configuration
- [x] SyncJob model
- [x] Interactive menu
- [x] Command preview
- [x] Rclone execution
- [x] Execution modes
- [x] Automatic Resync Recovery
- [x] Sync All
- [x] Logging
- [x] Sync History
- [x] Configuration validation
- [x] Remote validation
- [x] Local path validation
- [x] Pre-flight checks
- [x] macOS launcher
- [x] Git repository
- [x] GitHub repository

---

# Version 2 (Future)

These features are intentionally postponed until Version 1 is complete.

- Dashboard
- SQLite
- Statistics
- Scheduler
- Favorites
- Search
- Notifications
- Automatic updates

---

# Design Principles

- Keep the architecture simple.
- Prefer small incremental changes.
- One completed feature at a time.
- Every feature must compile before moving on.
- Configuration belongs in YAML.
- Never hardcode sync commands.
- Commit after every completed feature.

---

# Release Checklist

- [x] Feature 007 complete
- [x] Feature 008 complete
- [x] Feature 009 complete
- [x] Feature 010 complete
- [x] Feature 011 complete
- [x] README updated
- [x] .gitignore cleaned
- [x] Version 1 released

## Feature 012 — macOS Application Bundle

- Finder-launchable RCloneSyncManager.app
- Custom macOS application icon
- Opens Terminal and starts RCloneSyncManager
- Existing RCloneSyncManager.command retained as fallback