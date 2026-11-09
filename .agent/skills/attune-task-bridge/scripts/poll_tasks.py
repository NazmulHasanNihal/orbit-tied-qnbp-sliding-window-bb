#!/usr/bin/env python3
"""
Attune Task Bridge - Continuous polling mode.

Polls the Task Board API at regular intervals and notifies
when new tasks enter the "in_progress" column.
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Set

import httpx

from check_tasks import TaskBridgeClient, DEFAULT_API_URL
from notify import notify_task_available, notify_no_tasks


class TaskPoller:
    """Polls for tasks and tracks which have been notified."""
    
    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        api_key: str = None,
        interval: int = 30,
        notify_once: bool = True
    ):
        self.client = TaskBridgeClient(api_url, api_key)
        self.interval = interval
        self.notify_once = notify_once
        self.notified_tasks: Set[str] = set()
        self.running = False
    
    async def close(self):
        await self.client.close()
    
    async def check_and_notify(self) -> int:
        """
        Check for tasks and send notifications.
        
        Returns:
            Number of new tasks found
        """
        tasks = await self.client.get_in_progress_tasks()
        current_task_ids = {t["id"] for t in tasks}
        
        new_count = 0
        
        for task in tasks:
            task_id = task["id"]
            
            # Skip if already notified and notify_once is enabled
            if self.notify_once and task_id in self.notified_tasks:
                continue
            
            # Send notification
            notify_task_available(
                task_title=task.get("title", "Untitled"),
                task_id=task_id,
                priority=task.get("priority", "medium")
            )
            
            self.notified_tasks.add(task_id)
            new_count += 1
        
        # Clean up notified_tasks (remove IDs that are no longer in_progress)
        if self.notify_once:
            self.notified_tasks &= current_task_ids
        
        return new_count
    
    async def run(self):
        """Run the polling loop."""
        self.running = True
        
        print(f"🔍 Task Poller started")
        print(f"   API: {self.client.base_url}")
        print(f"   Interval: {self.interval}s")
        print(f"   Notify once per task: {self.notify_once}")
        print(f"   Press Ctrl+C to stop\n")
        
        # Initial check
        try:
            count = await self.check_and_notify()
            if count == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No tasks waiting")
        except Exception as e:
            print(f"Error during initial check: {e}", file=sys.stderr)
        
        # Polling loop
        while self.running:
            try:
                await asyncio.sleep(self.interval)
                count = await self.check_and_notify()
                
                if count > 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {count} new task(s)")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error during polling: {e}", file=sys.stderr)
    
    def stop(self):
        """Stop the polling loop."""
        self.running = False


async def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Poll for Attune tasks continuously"
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("ATTUNE_API_URL", DEFAULT_API_URL),
        help="Base URL of the Attune API"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Polling interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--notify-repeat",
        action="store_true",
        help="Notify repeatedly for same tasks (default: notify once)"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("ATTUNE_ADMIN_API_KEY", ""),
        help="Admin API key for authentication (or set ATTUNE_ADMIN_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    poller = TaskPoller(
        api_url=args.api_url,
        api_key=args.api_key,
        interval=args.interval,
        notify_once=not args.notify_repeat
    )
    
    try:
        await poller.run()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping poller...")
        poller.stop()
    finally:
        await poller.close()


if __name__ == "__main__":
    asyncio.run(main())
