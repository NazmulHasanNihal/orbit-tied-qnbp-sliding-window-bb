# Attune Task Board API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

The Admin API supports two authentication methods:

### 1. API Key (for CLI/tools)

Add the `X-Admin-API-Key` header to all requests:

```bash
curl -H "X-Admin-API-Key: your-secret-key" \
     http://localhost:8000/api/v1/admin/board
```

**Setup:** Set `ADMIN_API_KEY` in the backend `.env` file.

### 2. Firebase JWT (for web clients)

Use Bearer token authentication:

```bash
curl -H "Authorization: Bearer <firebase-jwt>" \
     http://localhost:8000/api/v1/admin/board
```

## Endpoints

### GET /admin/tasks

List all tasks with optional filtering.

**Query Parameters:**
- `status` - Filter by status (todo, in_progress, done)
- `priority` - Filter by priority (low, medium, high, critical)
- `feature_id` - Filter by feature

**Response:**
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "Task title",
      "description": "Task description",
      "status": "in_progress",
      "priority": "high",
      "effort_estimate": "M",
      "feature": {
        "id": "uuid",
        "title": "Feature title",
        "impact": "HIGH"
      },
      "created_at": "2026-03-05T10:00:00",
      "updated_at": "2026-03-05T10:00:00"
    }
  ],
  "total": 10
}
```

### GET /admin/tasks/{task_id}

Get specific task details.

### POST /admin/tasks/{task_id}/move

Move task to different column.

**Body:**
```json
{
  "to_column": "done",
  "moved_by": "kimi_agent"
}
```

### WebSocket /api/v1/admin/ws/tasks

Real-time task updates.

**Connection:**
```
ws://localhost:8000/api/v1/admin/ws/tasks?client_id=kimi_main&kimi_agent=true
```

**Events:**
- `task_moved` - Task moved between columns
- `task_created` - New task created
- `task_updated` - Task modified

## Task Status Values

| Status | Description |
|--------|-------------|
| `todo` | Not started |
| `in_progress` | Ready for implementation |
| `done` | Completed |

## Priority Levels

| Priority | Description |
|----------|-------------|
| `low` | Nice to have |
| `medium` | Normal priority |
| `high` | Important |
| `critical` | Blocker/urgent |

## Effort Estimates

| Code | Description |
|------|-------------|
| `XS` | Extra small (< 1 hour) |
| `S` | Small (1-2 hours) |
| `M` | Medium (2-4 hours) |
| `L` | Large (4-8 hours) |
| `XL` | Extra large (> 8 hours) |
