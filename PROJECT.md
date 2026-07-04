# CloudSync Manager

## Vision

A professional cloud synchronization manager powered by rclone.

---

## Current Version

v0.5.0

---

## Completed

- [x] Python project
- [x] Virtual environment
- [x] Rich terminal UI
- [x] Health check
- [x] YAML configuration
- [x] SyncJob model
- [x] Interactive menu
- [x] Command preview

---

## Current Milestone

Build the rclone execution engine.

---

## Roadmap

### Core Engine

- [ ] Execute rclone
- [ ] Dry Run
- [ ] Progress display
- [ ] Error handling

### Logging

- [ ] Sync history
- [ ] SQLite database
- [ ] Statistics

### User Experience

- [ ] Favorites
- [ ] Search jobs
- [ ] Settings
- [ ] Notifications

### Automation

- [ ] Scheduler
- [ ] Startup sync
- [ ] Automatic updates

---

## Design Rules

- Keep app.py small.
- One responsibility per file.
- Configuration belongs in YAML.
- No hardcoded sync commands.
- Every milestone must compile.
- Commit after every completed milestone.