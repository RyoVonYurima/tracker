Code Explained (for myself and fellow dummies)

This file explains what study.py does, section by section, without assuming you remember anything about it in six months.

The goal of the script is simple:

Track real study time, subtract gaming time, and log the truth locally.

No cloud, no accounts, no “productivity psychology.”

High-level overview

study.py is a command-line tool that can:

Start a study session

Stop a study session

Run a Pomodoro workflow

Detect if games are running during study

Subtract gaming time from study time

Log everything to a local Markdown file

Show daily and weekly summaries

The script is designed to be:

Local-first

Transparent

Simple enough to audit

Hard to lie to yourself with

Imports (what libraries are used and why)
from datetime import datetime
from pathlib import Path
import sys
import time
import threading
import psutil
import tkinter as tk
from tkinter import messagebox, simpledialog


Why these exist:

datetime – timestamps, dates, durations

Path – clean file handling

sys – command-line arguments

time – sleep and timers

threading – track gaming without blocking study

psutil – detect running processes (games)

tkinter – popup dialogs for Pomodoro mode

No web libraries. No telemetry. No APIs.

Configuration section
LOG_FILE = Path(r"C:\Users\ryovo\Documents\Obsidian\study-log.md")
SESSION_FILE = Path(".current_session")


LOG_FILE
Where study sessions are permanently stored.
Markdown so it works inside Obsidian.

SESSION_FILE
Temporary file used to remember that a study session is active.
Prevents double-starts and allows recovery if the script crashes.

Targets and thresholds
DAILY_TARGET = 180
DAILY_THRESHOLD = 120
WEEKLY_TARGET = 1260
WEEKLY_THRESHOLD = 840


Used only for evaluation and feedback.
Nothing is enforced. No punishment. Just reporting.

Pomodoro configuration
POMODORO_STUDY = 20
POMODORO_BREAK = 5


Minutes per cycle. Easy to change.

Gaming detection configuration
GAMING_CHECK_INTERVAL = 5


Every 5 seconds, the script checks whether a known game process is running.

GAMING_PROCESSES = {
    "hollow_knight.exe",
    "factorygamesteam.exe",
    "factorygamesteam-win64-shipping.exe",
}


This is intentionally explicit.
If a game isn’t listed here, it doesn’t count.

Global session state (runtime memory)
session_start_ts = None
gaming_overlap_seconds = 0
gaming_stop_event = None
gaming_thread = None


These variables exist only while the script is running.

session_start_ts – when the study session began

gaming_overlap_seconds – accumulated gaming time

gaming_stop_event – tells the gaming thread to stop

gaming_thread – background thread that tracks gaming

If Python crashes, this state disappears, which is why timestamps are also written to disk.

Gaming detection logic
is_gaming_active()

Checks all running processes and returns True if any process name matches the known games.

Uses psutil.process_iter().

This is passive detection. Nothing is blocked or killed.

track_gaming_overlap(stop_event)

Runs in a background thread while studying.

Every few seconds:

Checks if gaming is active

If yes, adds time to gaming_overlap_seconds

This allows:

Studying and gaming detection to happen simultaneously

The main program to remain responsive

Log parsing and totals
calculate_totals()

Reads the Markdown log file and calculates:

Today’s total study time

This week’s total study time

It does this by:

Tracking which date section it’s in

Parsing start and end times

Summing minutes

No external database. Just text parsing.

evaluate(total, threshold, target)

Returns:

"ideal"

"acceptable"

"missed"

Used only for human-readable feedback.

Popup helpers (Pomodoro UI)
ask_popup(message)

Shows a Yes/No popup that:

Forces itself to the foreground

Avoids getting lost behind other windows

Used for:

Starting study sessions

Starting breaks

ask_subject()

Prompts the user for what they’re studying.

This avoids hardcoding subjects into batch files.

Core commands
start(subject, device)

What happens when you start studying:

Checks if a session is already active

Writes .current_session with timestamp, subject, device

Resets gaming counters

Starts the gaming detection thread

Prints confirmation

This does not write to the log yet.
Logging happens only when you stop.

stop()

What happens when you stop studying:

Stops the gaming detection thread

Reads the session start time from disk

Calculates total session duration

Calculates gaming overlap

Computes effective study time

Appends a new entry to the Markdown log

Deletes .current_session

Prints daily and weekly totals

This is the most important function in the script.

summary()

Prints:

Today’s total study time

Weekly total study time

Does not modify anything.

pomodoro(device)

Runs a loop that:

Asks for subject

Prompts to start study

Runs a timed study session

Stops and logs it

Prompts for break

Repeats until cancelled

Uses the same start() and stop() functions.
No duplicate logic.

Entry point (command-line interface)
if __name__ == "__main__":


Reads the command provided and routes to the correct function:

start

stop

summary

pomodoro

Anything invalid shows the help text.

Final notes

This script is intentionally boring.

No GUI dashboards

No streaks

No scoring system

No cloud sync

Just:

timestamps

process detection

honest subtraction

If it says you studied 25 minutes, you studied 25 minutes.

That’s the whole point.