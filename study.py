from datetime import datetime
from pathlib import Path
import sys
import time
import threading
import psutil
import tkinter as tk
from tkinter import messagebox, simpledialog

# =========================
# CONFIG
# =========================

LOG_FILE = Path(r"C:\Users\ryovo\Documents\Obsidian\study-log.md")
SESSION_FILE = Path(".current_session")

DAILY_TARGET = 180
DAILY_THRESHOLD = 120
WEEKLY_TARGET = 1260
WEEKLY_THRESHOLD = 840

POMODORO_STUDY = 20
POMODORO_BREAK = 5

GAMING_CHECK_INTERVAL = 5  # seconds

GAMING_PROCESSES = {
    "hollow_knight.exe",
    "factorygamesteam.exe",
    "factorygamesteam-win64-shipping.exe",
}

# =========================
# GLOBAL SESSION STATE
# =========================

session_start_ts = None
gaming_overlap_seconds = 0

gaming_stop_event = None
gaming_thread = None

# =========================
# HELPERS
# =========================

def is_gaming_active():
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            name = proc.info["name"]
            if name and name.lower() in GAMING_PROCESSES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def track_gaming_overlap(stop_event):
    global gaming_overlap_seconds

    while not stop_event.is_set():
        if is_gaming_active():
            gaming_overlap_seconds += GAMING_CHECK_INTERVAL
        time.sleep(GAMING_CHECK_INTERVAL)


def calculate_totals():
    if not LOG_FILE.exists():
        return 0, 0

    lines = LOG_FILE.read_text().splitlines()
    today = datetime.now().date()
    week_start = today.fromisocalendar(today.year, today.isocalendar()[1], 1)

    daily_total = 0
    weekly_total = 0
    current_date = None

    for line in lines:
        if line.startswith("##"):
            current_date = datetime.strptime(line[3:], "%Y-%m-%d").date()
            continue

        if not line.startswith("-") or not current_date:
            continue

        try:
            time_part = line.split("|")[0].strip("- ").strip()
            start_str, end_str = time_part.split("-")

            start = datetime.strptime(start_str, "%H:%M")
            end = datetime.strptime(end_str, "%H:%M")
            minutes = (end - start).seconds // 60

            if current_date == today:
                daily_total += minutes
            if current_date >= week_start:
                weekly_total += minutes
        except Exception:
            continue

    return daily_total, weekly_total


def evaluate(total, threshold, target):
    if total >= target:
        return "ideal"
    elif total >= threshold:
        return "acceptable"
    else:
        return "missed"


# =========================
# POPUPS
# =========================

def ask_popup(message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.focus_force()
    root.update()

    result = messagebox.askyesno("Pomodoro", message, parent=root)
    root.destroy()
    return result


def ask_subject():
    root = tk.Tk()
    root.withdraw()
    subject = simpledialog.askstring("Pomodoro", "What are you studying?")
    root.destroy()
    return subject


# =========================
# COMMANDS
# =========================

def start(subject, device):
    global session_start_ts, gaming_overlap_seconds
    global gaming_stop_event, gaming_thread

    if SESSION_FILE.exists():
        print("A study session is already running.")
        return

    SESSION_FILE.write_text(
        f"{datetime.now().isoformat()}|{subject}|{device}"
    )

    session_start_ts = time.time()
    gaming_overlap_seconds = 0

    gaming_stop_event = threading.Event()
    gaming_thread = threading.Thread(
        target=track_gaming_overlap,
        args=(gaming_stop_event,),
        daemon=True
    )
    gaming_thread.start()

    print(f"Started studying {subject} on {device}.")

def safe_minutes_since(start_dt):
    """Fallback duration if runtime state is missing."""
    return int((datetime.now() - start_dt).total_seconds() // 60)


def stop():
    global gaming_stop_event, gaming_thread
    global session_start_ts, gaming_overlap_seconds

    if not SESSION_FILE.exists():
        print("No active study session.")
        return

    if gaming_stop_event:
        gaming_stop_event.set()
        gaming_thread.join(timeout=1)

    start_time, subject, device = SESSION_FILE.read_text().split("|")
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.now()

    if session_start_ts is not None:
        total_minutes = int((time.time() - session_start_ts) // 60)
    else:
        # fallback: compute from timestamps
        total_minutes = safe_minutes_since(start_dt)
    gaming_minutes = gaming_overlap_seconds // 60
    effective_minutes = max(total_minutes - gaming_minutes, 0)

    entry_date = start_dt.strftime("%Y-%m-%d")
    entry_line = (
        f"- {start_dt.strftime('%H:%M')}-{end_dt.strftime('%H:%M')} | "
        f"{subject} | {device} | "
        f"study {effective_minutes}m | gaming {gaming_minutes}m\n"
    )

    if not LOG_FILE.exists():
        LOG_FILE.write_text("# Study Log\n\n")

    content = LOG_FILE.read_text()
    header = f"\n## {entry_date}\n"
    if header not in content:
        content += header

    content += entry_line
    LOG_FILE.write_text(content)
    SESSION_FILE.unlink()

    daily, weekly = calculate_totals()

    print(f"Logged study session: {subject}")
    print(f"Today: {daily} min ({evaluate(daily, DAILY_THRESHOLD, DAILY_TARGET)})")
    print(f"This week: {weekly} min ({evaluate(weekly, WEEKLY_THRESHOLD, WEEKLY_TARGET)})")


def summary():
    daily, weekly = calculate_totals()
    print("=== Study Summary ===")
    print(f"Today: {daily} min")
    print(f"This week: {weekly} min")


def pomodoro(device):
    subject = ask_subject()
    if not subject:
        return

    while True:
        if not ask_popup(f"Start {POMODORO_STUDY}-minute study session?"):
            break

        start(subject, device)
        time.sleep(POMODORO_STUDY * 60)
        stop()

        if not ask_popup(f"Start {POMODORO_BREAK}-minute break?"):
            break

        time.sleep(POMODORO_BREAK * 60)


def help():
    print(
        "Usage:\n"
        "  py study.py start <subject> <pc|phone>\n"
        "  py study.py stop\n"
        "  py study.py summary\n"
        "  py study.py pomodoro <pc|phone>"
    )


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start" and len(sys.argv) == 4:
        start(sys.argv[2], sys.argv[3])
    elif command == "stop":
        stop()
    elif command == "summary":
        summary()
    elif command == "pomodoro" and len(sys.argv) == 3:
        pomodoro(sys.argv[2])
    else:
        help()
