#!/usr/bin/env python3
"""
Attune Task Bridge - Cross-platform notifications.

Sends notifications when tasks are available for implementation.
Supports macOS Notification Center and terminal output.
"""

import subprocess
import sys
import os
import platform
from typing import Optional


def notify_macos(title: str, message: str, sound: bool = True) -> bool:
    """Send macOS notification using osascript."""
    try:
        script = f'display notification "{message}" with title "{title}"'
        if sound:
            script += ' sound name "Glass"'
        
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True
        )
        return True
    except Exception as e:
        print(f"macOS notification failed: {e}", file=sys.stderr)
        return False


def notify_linux(title: str, message: str) -> bool:
    """Send Linux notification using notify-send."""
    try:
        subprocess.run(
            ["notify-send", title, message],
            check=True,
            capture_output=True
        )
        return True
    except Exception as e:
        print(f"Linux notification failed: {e}", file=sys.stderr)
        return False


def notify_terminal(title: str, message: str, urgent: bool = False) -> None:
    """Print notification to terminal with formatting."""
    width = 60
    border = "═" * width
    
    print()
    if urgent:
        print(f"\033[1;31m{border}\033[0m")  # Red bold
        print(f"\033[1;31m  🔔 {title.upper()}\033[0m")
    else:
        print(f"\033[1;36m{border}\033[0m")  # Cyan bold
        print(f"\033[1;36m  🔔 {title}\033[0m")
    
    print(f"\033[0m  {message}\033[0m")
    
    if urgent:
        print(f"\033[1;31m{border}\033[0m")
    else:
        print(f"\033[1;36m{border}\033[0m")
    print()


def notify_task_available(task_title: str, task_id: str, priority: str = "medium") -> bool:
    """
    Notify that a task is available for implementation.
    
    Args:
        task_title: Title of the task
        task_id: Task ID for reference
        priority: Task priority (low, medium, high, critical)
    
    Returns:
        True if any notification was sent successfully
    """
    system = platform.system()
    
    # Format message
    title = "🎯 Attune Task Waiting"
    message = f"'{task_title}' is ready for implementation"
    
    # Determine urgency
    urgent = priority.lower() in ["high", "critical"]
    
    results = []
    
    # Terminal notification (always)
    notify_terminal(title, message, urgent=urgent)
    results.append(True)
    
    # Platform-specific notification
    if system == "Darwin":  # macOS
        results.append(notify_macos(title, message, sound=urgent))
    elif system == "Linux":
        results.append(notify_linux(title, message))
    
    return any(results)


def notify_no_tasks() -> None:
    """Notify that no tasks are currently available."""
    title = "Attune Task Bridge"
    message = "No tasks currently in progress. You're all caught up!"
    
    notify_terminal(title, message, urgent=False)
    
    # Also send platform notification
    system = platform.system()
    if system == "Darwin":
        notify_macos(title, message, sound=False)
    elif system == "Linux":
        notify_linux(title, message)


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Send notifications")
    parser.add_argument("--title", default="Test Notification")
    parser.add_argument("--message", default="This is a test message")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--no-tasks", action="store_true", help="Show 'no tasks' notification")
    
    args = parser.parse_args()
    
    if args.no_tasks:
        notify_no_tasks()
    else:
        notify_task_available(args.title, "test-123", args.priority)


if __name__ == "__main__":
    main()
