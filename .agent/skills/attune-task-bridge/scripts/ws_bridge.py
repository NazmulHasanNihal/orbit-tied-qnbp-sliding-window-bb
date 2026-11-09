#!/usr/bin/env python3
"""
Attune Task Bridge - WebSocket Bridge for Push Notifications.

Connects to the Attune Task Board WebSocket and triggers notifications
when tasks are moved to "in_progress". This provides real-time push
notifications instead of polling.

Usage:
    python3 ws_bridge.py                    # Connect with auto-reconnect
    python3 ws_bridge.py --no-reconnect     # Single connection attempt
    python3 ws_bridge.py --execute          # Auto-execute tasks (advanced)
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from typing import Optional
from urllib.parse import urljoin

import websockets
from websockets.exceptions import ConnectionClosed


# Default configuration
DEFAULT_WS_URL = "ws://localhost:8000/api/v1/admin/ws/tasks"
DEFAULT_API_URL = "http://localhost:8000"
CLIENT_ID = "kimi_task_bridge"


class TaskWebSocketBridge:
    """
    WebSocket bridge that listens for task events and triggers notifications.
    
    Features:
    - Connects to Attune Task Board WebSocket
    - Listens for task_moved events
    - Triggers notifications when tasks enter "in_progress"
    - Auto-reconnects on connection loss
    """
    
    def __init__(
        self,
        ws_url: str = DEFAULT_WS_URL,
        api_url: str = DEFAULT_API_URL,
        api_key: str = None,
        auto_reconnect: bool = True,
        reconnect_delay: int = 5,
    ):
        self.ws_url = ws_url
        self.api_url = api_url
        self.api_key = api_key or os.getenv("ATTUNE_ADMIN_API_KEY", "")
        self.auto_reconnect = auto_reconnect
        self.reconnect_delay = reconnect_delay
        self.ws = None
        self.connected = False
        self.running = False
        self.last_task_id: Optional[str] = None
    
    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            # Build connection URL with query params
            url = f"{self.ws_url}?client_id={CLIENT_ID}&kimi_agent=true"
            
            print(f"🔌 Connecting to {self.ws_url}...")
            self.ws = await websockets.connect(url)
            
            # Wait for connection confirmation (can be 'connected' or 'agent_status')
            response = await self.ws.recv()
            data = json.loads(response)
            
            msg_type = data.get("type")
            if msg_type in ("connected", "agent_status"):
                self.connected = True
                kimi_count = data.get("kimi_agents_online", 0)
                print(f"✅ Connected! Kimi agents online: {kimi_count}")
                return True
            else:
                print(f"⚠️  Unexpected response: {data}")
                return False
                
        except ConnectionRefusedError:
            print(f"❌ Connection refused. Is the server running at {self.api_url}?")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Close WebSocket connection."""
        if self.ws:
            await self.ws.close()
            self.connected = False
            print("👋 Disconnected from WebSocket")
    
    def trigger_notification(self, task_data: dict):
        """
        Trigger notification when task is ready.
        
        This calls the notify.py script to send:
        - macOS Notification Center alert
        - Terminal output
        """
        task_title = task_data.get("title", "Untitled")
        task_id = task_data.get("id", "unknown")
        priority = task_data.get("priority", "medium")
        
        print(f"\n🔔 Task moved to In Progress: {task_title}")
        
        # Build command to notify.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        notify_script = os.path.join(script_dir, "notify.py")
        
        try:
            subprocess.run([
                "python3", notify_script,
                "--title", task_title,
                "--message", f"Task {task_id} is ready for implementation",
                "--priority", priority.lower()
            ], check=True)
        except Exception as e:
            print(f"⚠️  Notification failed: {e}")
        
        # Also fetch full task details via check_tasks.py
        self.fetch_task_details(task_id)
    
    def fetch_task_details(self, task_id: str):
        """Fetch and display detailed task information."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        check_script = os.path.join(script_dir, "check_tasks.py")
        
        env = os.environ.copy()
        if self.api_key:
            env["ATTUNE_ADMIN_API_KEY"] = self.api_key
        
        try:
            result = subprocess.run(
                ["python3", check_script, "--task-id", task_id],
                capture_output=True,
                text=True,
                env=env
            )
            if result.returncode == 0:
                print("\n📋 Task Details:")
                print(result.stdout)
            else:
                print(f"⚠️  Could not fetch task details: {result.stderr}")
        except Exception as e:
            print(f"⚠️  Error fetching details: {e}")
    
    async def handle_message(self, message: str):
        """Process incoming WebSocket message."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "task_moved":
                from_col = data.get("from_column")
                to_col = data.get("to_column")
                task_id = data.get("task_id")
                task_title = data.get("task_title")
                
                print(f"📦 Task moved: {task_title} ({from_col} → {to_col})")
                
                # Trigger notification if moved to in_progress
                if to_col == "in_progress":
                    task_data = data.get("task", {})
                    task_data["id"] = task_id
                    task_data["title"] = task_title
                    self.trigger_notification(task_data)
                    self.last_task_id = task_id
            
            elif msg_type == "task_executing":
                # Direct notification from backend
                task_title = data.get("task_title")
                task_id = data.get("task_id")
                print(f"🚀 Task executing: {task_title}")
                
                task_data = data.get("task", {})
                self.trigger_notification(task_data)
                self.last_task_id = task_id
            
            elif msg_type == "task_completed":
                task_title = data.get("task_title")
                print(f"✅ Task completed: {task_title}")
            
            elif msg_type == "agent_status":
                status = data.get("status")
                message = data.get("message")
                print(f"👤 Agent status: {status} - {message}")
            
            elif msg_type == "connected":
                # Already handled in connect()
                pass
            
            else:
                # Unknown message type, print for debugging
                print(f"ℹ️  {msg_type}: {data.get('message', '')}")
                
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON: {message[:100]}")
        except Exception as e:
            print(f"⚠️  Error handling message: {e}")
    
    async def send_ping(self):
        """Send periodic ping to keep connection alive."""
        while self.connected and self.running:
            try:
                if self.ws:
                    await self.ws.send(json.dumps({"type": "ping"}))
                await asyncio.sleep(30)  # Ping every 30 seconds
            except Exception:
                break
    
    async def listen(self):
        """Main listen loop."""
        self.running = True
        
        while self.running:
            if not self.connected:
                success = await self.connect()
                if not success:
                    if self.auto_reconnect:
                        print(f"⏳ Retrying in {self.reconnect_delay}s...")
                        await asyncio.sleep(self.reconnect_delay)
                        continue
                    else:
                        print("❌ Connection failed. Exiting.")
                        break
            
            # Start ping task
            ping_task = asyncio.create_task(self.send_ping())
            
            try:
                # Listen for messages
                async for message in self.ws:
                    await self.handle_message(message)
            
            except ConnectionClosed:
                print("⚠️  Connection closed")
                self.connected = False
            
            except Exception as e:
                print(f"⚠️  Error: {e}")
                self.connected = False
            
            finally:
                ping_task.cancel()
                try:
                    await ping_task
                except asyncio.CancelledError:
                    pass
            
            # Reconnect logic
            if self.auto_reconnect and self.running:
                print(f"⏳ Reconnecting in {self.reconnect_delay}s...")
                await asyncio.sleep(self.reconnect_delay)
            else:
                break
    
    def stop(self):
        """Stop the bridge."""
        self.running = False
        print("\n🛑 Stopping WebSocket bridge...")


async def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="WebSocket bridge for Attune Task Board push notifications"
    )
    parser.add_argument(
        "--ws-url",
        default=os.getenv("ATTUNE_WS_URL", DEFAULT_WS_URL),
        help="WebSocket URL (default: ws://localhost:8000/api/v1/admin/ws/tasks)"
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("ATTUNE_API_URL", DEFAULT_API_URL),
        help="REST API URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("ATTUNE_ADMIN_API_KEY", ""),
        help="Admin API key (or set ATTUNE_ADMIN_API_KEY env var)"
    )
    parser.add_argument(
        "--no-reconnect",
        action="store_true",
        help="Don't auto-reconnect on connection loss"
    )
    parser.add_argument(
        "--reconnect-delay",
        type=int,
        default=5,
        help="Seconds to wait before reconnect (default: 5)"
    )
    
    args = parser.parse_args()
    
    bridge = TaskWebSocketBridge(
        ws_url=args.ws_url,
        api_url=args.api_url,
        api_key=args.api_key,
        auto_reconnect=not args.no_reconnect,
        reconnect_delay=args.reconnect_delay,
    )
    
    # Handle Ctrl+C gracefully
    try:
        await bridge.listen()
    except KeyboardInterrupt:
        bridge.stop()
    finally:
        await bridge.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
