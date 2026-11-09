#!/usr/bin/env python3
"""
Attune Task Bridge - Check for pending tasks via API.

This script queries the Attune backend for tasks that are "In Progress"
and waiting for implementation.
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

import httpx


# Default API configuration
DEFAULT_API_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
DEFAULT_API_KEY = ""  # Set via ATTUNE_ADMIN_API_KEY env var


class TaskBridgeClient:
    """Client for the Attune Task Board API."""
    
    def __init__(self, base_url: str = DEFAULT_API_URL, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("ATTUNE_ADMIN_API_KEY", DEFAULT_API_KEY)
        
        # Setup headers with API key if available
        headers = {}
        if self.api_key:
            headers["X-Admin-API-Key"] = self.api_key
        
        self.client = httpx.AsyncClient(timeout=10.0, headers=headers)
    
    async def close(self):
        await self.client.aclose()
    
    async def health_check(self) -> bool:
        """Check if the API is running."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False
    
    async def get_in_progress_tasks(self) -> List[dict]:
        """Get all tasks currently in 'in_progress' column."""
        url = f"{self.base_url}{API_PREFIX}/admin/tasks"
        try:
            response = await self.client.get(url)
            
            if response.status_code == 403:
                print("⚠️  API returned 403 Forbidden - authentication may be required", file=sys.stderr)
                print("   Returning empty task list", file=sys.stderr)
                return []
            
            response.raise_for_status()
            data = response.json()
            
            # Filter for in_progress tasks
            tasks = data.get("tasks", [])
            in_progress = [
                task for task in tasks 
                if task.get("status") == "in_progress"
            ]
            return in_progress
        except Exception as e:
            print(f"Error fetching tasks: {e}", file=sys.stderr)
            return []
    
    async def get_task_by_id(self, task_id: str) -> Optional[dict]:
        """Get details for a specific task."""
        url = f"{self.base_url}{API_PREFIX}/admin/tasks/{task_id}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching task {task_id}: {e}", file=sys.stderr)
            return None


def format_task_for_display(task: dict) -> str:
    """Format a task for human-readable display."""
    lines = []
    lines.append(f"🎯 Task: {task.get('title', 'Untitled')}")
    lines.append(f"   ID: {task.get('id', 'N/A')}")
    
    # Feature can be a string or dict
    feature = task.get('feature')
    if feature:
        if isinstance(feature, dict):
            lines.append(f"   Feature: {feature.get('title', 'N/A')}")
            if feature.get('impact'):
                lines.append(f"   Impact: {feature.get('impact')}")
        else:
            lines.append(f"   Feature: {feature}")
    
    # Rationale often contains useful context
    rationale = task.get('rationale', '')
    if rationale:
        lines.append(f"   Rationale: {rationale[:100]}...")
    
    priority = task.get('priority', 'medium')
    effort = task.get('estimated_effort', task.get('effort_estimate', 'unknown'))
    lines.append(f"   Priority: {priority.upper()} | Effort: {effort}")
    
    return "\n".join(lines)


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check for pending Attune tasks"
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("ATTUNE_API_URL", DEFAULT_API_URL),
        help="Base URL of the Attune API"
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--task-id",
        help="Get specific task by ID"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("ATTUNE_ADMIN_API_KEY", DEFAULT_API_KEY),
        help="Admin API key for authentication (or set ATTUNE_ADMIN_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    client = TaskBridgeClient(args.api_url, args.api_key)
    
    try:
        # Health check
        if not await client.health_check():
            print("❌ Attune API is not running", file=sys.stderr)
            sys.exit(1)
        
        if args.task_id:
            # Get specific task
            task = await client.get_task_by_id(args.task_id)
            if task:
                if args.format == "json":
                    import json
                    print(json.dumps(task, indent=2))
                else:
                    print(format_task_for_display(task))
            else:
                print(f"Task {args.task_id} not found", file=sys.stderr)
                sys.exit(1)
        else:
            # Get all in-progress tasks
            tasks = await client.get_in_progress_tasks()
            
            if args.format == "json":
                import json
                print(json.dumps({
                    "count": len(tasks),
                    "tasks": tasks,
                    "timestamp": datetime.now().isoformat()
                }, indent=2))
            else:
                if not tasks:
                    print("✅ No tasks currently in progress")
                else:
                    print(f"🚀 {len(tasks)} task(s) waiting for implementation:\n")
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {format_task_for_display(task)}")
                        print()
    
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
