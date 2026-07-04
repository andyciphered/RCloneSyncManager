# RCloneSyncManager

A professional cross-platform cloud synchronization manager powered by rclone.

---

# Current Status

Version: v1.0.0-beta

Current Milestone:
Achieve feature parity with the existing Windows batch workflow.

---

# Version 1 Goals

## Feature 007
- [ ] Execution Modes
  - Normal
  - Resync
  - Force
  - Automatic Resync Recovery

## Feature 008
- [ ] Sync All

## Feature 009
- [ ] Logging
  - Timestamp
  - Job name
  - Exit code
  - Output log

## Feature 010
- [ ] Polish
  - Cleaner menus
  - Better summaries
  - Error handling
  - Version cleanup

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
- [x] Git repository
- [x] GitHub repository
- [x] Codex integration

---

# Version 2 (Future)

These features are intentionally postponed until Version 1 ships.

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

- [ ] Feature 007 complete
- [ ] Feature 008 complete
- [ ] Feature 009 complete
- [ ] Feature 010 complete
- [ ] README updated
- [ ] .gitignore cleaned
- [ ] Version 1 released