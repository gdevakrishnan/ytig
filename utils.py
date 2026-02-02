import win32gui
import win32process
import psutil
import time

BROWSERS = ["chrome.exe", "firefox.exe", "msedge.exe", "brave.exe", "opera.exe"]

def get_active_window_info():
    """
    Returns the active window's title and process name.
    If no window is active, returns (None, None).
    """
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return None, None

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        proc = psutil.Process(pid)
        process_name = proc.name().lower()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        process_name = None

    title = win32gui.GetWindowText(hwnd)

    return title, process_name


def is_browser(process_name):
    """Check if the process belongs to a browser"""
    return process_name in BROWSERS


def is_instagram(window_title):
    """Check if the active window is Instagram"""
    if not window_title:
        return False
    return "instagram" in window_title.lower()


if __name__ == "__main__":
    print("Starting continuous monitor... Press Ctrl + C to stop.\n")

    while True:
        title, process = get_active_window_info()

        if not title or not process:
            print("No active window detected")
            time.sleep(2)
            continue

        print("\nWindow title:", title)
        print("Process:", process)

        if is_browser(process):
            print("User is in a browser")
        else:
            print("Not a browser")

        if is_instagram(title):
            print("User is on Instagram")
        else:
            print("Not Instagram")

        time.sleep(2)
