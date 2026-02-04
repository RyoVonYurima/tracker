### Study Tracker

A local-first study tracking system built to answer one question honestly:

Where did my time actually go?

This project began as a personal tool during medical school. I wanted a way to track study time without relying on yet another Pomodoro app, paid productivity service, or cloud-based dashboard.

Over time, it evolved into a small but capable system with session logging, Pomodoro mode, gaming overlap detection, and visual analytics.

No cloud.
No accounts.
No behavioral manipulation.
Just timestamps and receipts.

### Why this exists

I didn’t want:
- another Pomodoro app
- another productivity SaaS
- another dashboard gamifying discipline with streaks and confetti

I wanted:
- exact start and stop times
- a clear record of how long I actually studied
- detection of when I was “studying” but actively gaming
- simple, honest visual summaries
- full control over my data

So I built it.

This project is open source so anyone can read the code, understand how it works, fork it, or adapt it to their own workflow.

### Features

### Core tracking:
 - Manual start and stop of study sessions
 - Logs sessions to a local Markdown file (Obsidian-compatible)
 - Automatic daily and weekly summaries
### Pomodoro
 - Pomodoro mode
 - Popup-based prompts (no cluttered terminal windows)
 - Customizable study and break durations
 - Runs quietly in the backgroun
### Game Detection
 - Gaming overlap detection (PC)
 - Detects active game processes during study sessions
 - Tracks time spent gaming while a study session is active
 - Logs effective study time vs gaming time



### Analytics (separate repository)
  Daily study consistency heatmap
  Weekly time-of-day heatmap

All visualizations generated locally as PNG files

### Project structure:

```text
study-tracker/
├── study.py              # Main tracker logic
├── start-study.bat       # Start a study session
├── stop-study.bat        # Stop a study session
├── pomodoro.bat          # Pomodoro mode
├── summary.bat           # Daily / weekly summary
├── requirements.txt
└── README.md

```
Analytics scripts live in a separate repository: study-analytics.

### Setup

  ## Requirements
    Windows
    Python 3.10 or newer
    Git (optional, but recommended)


Install dependencies
pip install -r requirements.txt


## Dependencies are minimal:
```
  psutil – process detection
  matplotlib, numpy – analytics and heatmaps
  Tkinter is included with Python on Windows.
```
### Usage

## Start a study session  
```
  py study.py start <subject> <pc|phone>
```

Example:
  py study.py start Physiology pc


## Stop a session
```
  py study.py stop
```

This logs the session and reports:
  - total session time
  - effective study time
  - gaming overlap (if any)


## Pomodoro mode
```
    py study.py pomodoro <pc|phone>
```

  Prompts for subject
  Uses popup dialogs
  Alternates study and break cycles

## View summary
```
   py study.py summary
```
Shows:
  - today’s total
  - weekly total
  - target status

Batch files are included for quick access.

### Data & privacy
  All data is stored locally
  No internet access required
  No telemetry
  No external services


Study sessions are logged in plain text Markdown files that you fully control.
  If you delete the files, the data is gone.
  No backups, no copies, no surprises.

### Roadmap

Planned or under consideration:
  
 - Gaming overlap analytics visualization
 - Anki integration (design phase)
 - GitHub Actions for automated heatmap generation
 - Standalone desktop app (no Python dependency)
 - Android companion app (research phase)
 - Configurable UI instead of batch files

Nothing here is guaranteed.
This is a personal project, not a product.

### Final note

  This isn’t about productivity hacks.
  It’s about knowing the truth about your time.

Use it, modify it, or ignore it.
The data doesn’t lie, even when we do.
