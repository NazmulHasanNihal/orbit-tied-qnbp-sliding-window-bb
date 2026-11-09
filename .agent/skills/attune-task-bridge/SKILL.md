---
name: attune-task-bridge
description: Check for and notify about pending Attune tasks waiting for implementation. Use when Kimi needs to (1) Check if there are tasks in "In Progress" column, (2) Get notified when new tasks become available, (3) Poll for tasks continuously, (4) View task details before implementation, or (5) Stay synchronized with the Attune Task Board. Integrates with the Attune FastAPI backend Task Board API.
---

# Attune Task Bridge

Bridge between Kimi and the Attune Task Board. Notifies when tasks are moved to "In Progress" and ready for implementation.

## Quick Start

**Option A: Push Notifications (Recommended)**
```bash
# Terminal 1: Start WebSocket bridge (receives push notifications)
python3 .agent/skills/attune-task-bridge/scripts/ws_bridge.py

# Now when you move a task to "In Progress", you'll get instant notification!
```

**Option B: Manual Check**
```bash
python3 .agent/skills/attune-task-bridge/scripts/check_tasks.py
```

**Option C: Polling Mode**
```bash
python3 .agent/skills/attune-task-bridge/scripts/poll_tasks.py
```

## Scripts

### ws_bridge.py ⭐ RECOMMENDED

**Push-based notifications via WebSocket.** Connects to the Attune Task Board and instantly notifies when tasks move to "in_progress".

**Why use this instead of polling?**
- ✅ Instant notification (no delay)
- ✅ No wasted API calls
- ✅ Shows task move events in real-time
- ✅ Auto-reconnects on connection loss

**Usage:**
```bash
# Start bridge (keeps running)
python3 scripts/ws_bridge.py

# With explicit API key
python3 scripts/ws_bridge.py --api-key your-key

# No auto-reconnect (single attempt)
python3 scripts/ws_bridge.py --no-reconnect
```

**What happens:**
1. Connects to WebSocket endpoint
2. Listens for `task_moved` events
3. When task → "in_progress":
   - Shows macOS notification (if on macOS)
   - Prints formatted task details in terminal
   - Automatically fetches full task info via API

**Events tracked:**
- `task_moved` - Task moved between columns
- `task_executing` - Task ready for execution
- `task_completed` - Task finished
- `agent_status` - Connection status updates

### check_tasks.py

Query the Task Board API for tasks in "in_progress" status.

**Usage:**
```bash
# Check all in-progress tasks
python3 scripts/check_tasks.py

# Get specific task
python3 scripts/check_tasks.py --task-id <task-id>

# JSON output for parsing
python3 scripts/check_tasks.py --format json

# Custom API URL
ATTUNE_API_URL=http://localhost:8000 python3 scripts/check_tasks.py
```

**Output:** Formatted task list with title, feature, impact, priority, effort estimate.

### notify.py

Send cross-platform notifications (macOS Notification Center + Terminal).

**Usage:**
```bash
# Test notification
python3 scripts/notify.py --title "Test" --message "Hello"

# Task available notification
python3 scripts/notify.py --title "New Task" --message "Implement feature" --priority high

# No tasks notification
python3 scripts/notify.py --no-tasks
```

**Features:**
- macOS Notification Center with sound for urgent tasks
- Terminal output with color coding
- Priority-based urgency (high/critical = red, normal = cyan)

### poll_tasks.py

Continuous polling mode for background task monitoring.

**Usage:**
```bash
# Poll every 30 seconds (default)
python3 scripts/poll_tasks.py

# Custom interval
python3 scripts/poll_tasks.py --interval 60

# Repeat notifications for same tasks
python3 scripts/poll_tasks.py --notify-repeat
```

**Behavior:**
- Remembers notified tasks (won't spam)
- Cleans up when tasks move out of in_progress
- Ctrl+C to stop

## Workflow

### Mode 1: Push Notifications (Best Experience) ⭐

**Setup (run once per session):**
```bash
# Terminal 1: Start WebSocket bridge
python3 .agent/skills/attune-task-bridge/scripts/ws_bridge.py
```

**How it works:**
1. Bridge connects to backend WebSocket
2. You work normally in another terminal
3. When someone moves a task to "In Progress":
   - Instant notification appears
   - Task details are shown
   - You can immediately start implementing

**Perfect for:** Development workflows where you want instant feedback.

### Mode 2: Manual Check

When user asks about tasks or you want to check:

```python
import subprocess
result = subprocess.run(
    ["python3", ".agent/skills/attune-task-bridge/scripts/check_tasks.py", "--format", "json"],
    capture_output=True,
    text=True
)
# Parse JSON and present tasks to user
```

### Mode 3: Continuous Polling (Fallback)

For long-running sessions without WebSocket:

```bash
# Terminal 1: Start poller
python3 .agent/skills/attune-task-bridge/scripts/poll_tasks.py --interval 30

# Terminal 2: Normal work
# Notifications appear when tasks arrive
```

## API Reference

See [references/api.md](references/api.md) for complete Task Board API documentation.

## Configuration

Environment variables:
- `ATTUNE_API_URL` - Base URL (default: http://localhost:8000)
- `ATTUNE_ADMIN_API_KEY` - Admin API key for authentication

### API Authentication

The Task Board API requires authentication. Two methods are supported:

1. **API Key** (recommended for CLI/tools):
   ```bash
   export ATTUNE_ADMIN_API_KEY="your-secret-key"
   python3 scripts/check_tasks.py
   ```

2. **Command line**:
   ```bash
   python3 scripts/check_tasks.py --api-key "your-secret-key"
   ```

To set up the API key in the backend, add to `.env`:
```
ADMIN_API_KEY=your-secret-key
```

## Response Handling

When tasks are found, present them clearly:

```
🚀 2 task(s) waiting for implementation:

1. 🎯 Task: Implement OAuth flow
   ID: task-abc-123
   Feature: User Authentication
   Impact: HIGH
   Priority: HIGH | Effort: M

2. 🎯 Task: Fix navigation bug
   ...
```

Ask user: "Soll ich einen dieser Tasks implementieren?" or "Welchen Task möchtest du als nächstes bearbeiten?"

## Integration with Kimi

### Automatic Trigger on Task Move

The WebSocket bridge (`ws_bridge.py`) enables true push notifications:

```
User moves task to "In Progress" in browser
           ↓
Backend sends WebSocket event
           ↓
ws_bridge.py receives event instantly
           ↓
Terminal shows: 🔔 Task 'X' ready!
           ↓
User sees notification and asks: "Soll ich implementieren?"
```

### Starting the Bridge

```bash
# In a separate terminal or background:
python3 ~/.config/agents/skills/attune-task-bridge/scripts/ws_bridge.py
```

The bridge will:
1. Show connection status
2. Display all task movements
3. **Instantly notify** when tasks enter "in_progress"
4. Auto-reconnect if connection drops

### Example Output

```
🔌 Connecting to ws://localhost:8000/api/v1/admin/ws/tasks...
✅ Connected! Kimi agents online: 1

📦 Task moved: Enhance Weekly Insights (todo → in_progress)
🔔 Task moved to In Progress: Enhance Weekly Insights

════════════════════════════════════════════════════════════
  🔔 🎯 ATTUNE TASK WAITING
════════════════════════════════════════════════════════════
  'Enhance Weekly Insights' is ready for implementation
════════════════════════════════════════════════════════════

📋 Task Details:
🎯 Task: Enhance Weekly Insights with Qualitative Trend Analysis
   ID: task_003
   Feature: weekly_insights
   ...
```
