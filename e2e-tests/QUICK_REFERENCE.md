# HTTP Test Files Quick Reference

## Quick Start (3 Steps)

1. **Install Extension**: Search "REST Client" in VS Code Extensions
2. **Open File**: Open any `.http` file from `e2e-tests/` directory  
3. **Send Request**: Click "Send Request" link above any HTTP request

## File Purpose Guide

| File | Purpose | Auth Required |
|------|---------|--------------|
| `health-check.http` | Verify all services are running | ❌ No |
| `auth.http` | User registration and login | ⚠️ Some endpoints |
| `articles.http` | Article management | ⚠️ Delete only |
| `sources.http` | RSS source management | ✅ Yes (Admin) |
| `crawler.http` | Crawler orchestration | ✅ Yes (Admin) |
| `recommendation.http` | AI recommendations | ❌ No |
| `summary.http` | AI summarization | ❌ No |
| `complete-workflow.http` | Full E2E test | ⚠️ Some endpoints |

## Testing Sequence

### 1️⃣ First Time Setup
```
health-check.http → auth.http (register + login)
```

### 2️⃣ Daily Testing
```
health-check.http → complete-workflow.http
```

### 3️⃣ Feature Specific
```
- Testing articles? → articles.http
- Testing crawler? → crawler.http (need admin)
- Testing AI? → recommendation.http + summary.http
```

## Common Variables

Update these in each file before testing:

```http
@username = your_username
@email = your_email@example.com
@password = your_password
@accessToken = YOUR_ACCESS_TOKEN_HERE  # Get from login
```

## Environment Switching

**Status Bar** (bottom right) → Click environment name → Select:
- `local` - Default (localhost)
- `dev` - Development server
- `production` - Production server

## Common Request Patterns

### 📝 Register New User
```http
POST {{baseUrl}}/api/v1/auth/register HTTP/1.1
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### 🔑 Login & Get Token
```http
# @name login
POST {{baseUrl}}/api/v1/auth/login HTTP/1.1
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123"
}

###
# Auto-extract token
@accessToken = {{login.response.body.access_token}}
```

### 🔒 Authenticated Request
```http
GET {{baseUrl}}/api/v1/auth/users/me HTTP/1.1
Authorization: Bearer {{accessToken}}
```

### 📄 GET with Query Params
```http
GET {{baseUrl}}/api/v1/articles?page=1&per_page=10&source_id=1 HTTP/1.1
```

### ➕ POST with JSON Body
```http
POST {{baseUrl}}/api/v1/sources HTTP/1.1
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
  "name": "VnExpress",
  "url": "https://vnexpress.net/rss/tin-moi-nhat.rss",
  "category": "News"
}
```

### ✏️ PUT to Update
```http
PUT {{baseUrl}}/api/v1/sources/1 HTTP/1.1
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
  "is_active": false
}
```

### ❌ DELETE Resource
```http
DELETE {{baseUrl}}/api/v1/articles/123 HTTP/1.1
Authorization: Bearer {{accessToken}}
```

## Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Send Request | `Ctrl+Alt+R` | `Cmd+Alt+R` |
| Send Request (selection) | `Ctrl+Alt+R` | `Cmd+Alt+R` |
| Cancel Request | `Ctrl+Alt+K` | `Cmd+Alt+K` |
| Re-run Last Request | `Ctrl+Alt+L` | `Cmd+Alt+L` |
| History | `Ctrl+Alt+H` | `Cmd+Alt+H` |

## Response Features

### View Response
- **Status**: HTTP status code (200, 404, etc.)
- **Headers**: Response headers
- **Body**: JSON response (formatted)
- **Time**: Request duration

### Save Response
Right-click response → "Save Response" or "Save Response Body"

### Copy Response
Click "Copy Response" or "Copy Response Body" links

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ❌ Connection refused | Start services: `docker-compose up -d` |
| ❌ 401 Unauthorized | Login again to get fresh token |
| ❌ 404 Not Found | Check resource ID exists |
| ❌ 400 Bad Request | Verify JSON format is correct |
| ❌ Variables not working | Check `.vscode/settings.json` exists |

## Tips & Tricks

### 💡 Tip 1: Chain Requests
Extract values from previous responses:
```http
# @name createSource
POST {{baseUrl}}/api/v1/sources HTTP/1.1
...

###
@sourceId = {{createSource.response.body.id}}
```

### 💡 Tip 2: Test Error Cases
Include invalid data to test error handling:
```http
# Should return 401
POST {{baseUrl}}/api/v1/auth/login HTTP/1.1
Content-Type: application/json

{
  "username": "invalid",
  "password": "wrong"
}
```

### 💡 Tip 3: Use Comments
Document what each test does:
```http
###
# Test Case: List articles with pagination
# Expected: 200 OK with array of articles
# Page size should be 10 items
GET {{baseUrl}}/api/v1/articles?page=1&per_page=10 HTTP/1.1
```

### 💡 Tip 4: Multiple Environments
Keep different tokens per environment:
```http
# Local token
@localToken = eyJhbGc...

# Dev token  
@devToken = eyJhbGc...

# Use based on environment
Authorization: Bearer {{accessToken}}
```

### 💡 Tip 5: Request History
View all previous requests:
- Press `Ctrl+Alt+H` (Windows/Linux)
- Press `Cmd+Alt+H` (macOS)
- Re-run any previous request

## Next Steps

1. ✅ Start services: `docker-compose up -d`
2. ✅ Run health checks: `health-check.http`
3. ✅ Register & login: `auth.http`
4. ✅ Test features: Choose specific `.http` files
5. ✅ Full E2E test: `complete-workflow.http`

## Resources

- 📖 [Full Documentation](README.md)
- 🔍 [Validation Report](VALIDATION.md)
- 🏗️ [API Examples](../API_EXAMPLES.md)
- 📚 [REST Client Docs](https://github.com/Huachao/vscode-restclient)

---

**Ready to test?** Open `health-check.http` and click "Send Request"! 🚀
