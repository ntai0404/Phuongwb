# E2E API Testing with HTTP Files

This directory contains HTTP files for end-to-end testing of all API endpoints following **RFC 2616** (HTTP/1.1) protocol specification.

## Prerequisites

### 1. Install VS Code REST Client Extension

Install the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao in Visual Studio Code.

**Installation steps:**
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
3. Search for "REST Client"
4. Click Install on the extension by Huachao Mao

### 2. Start the Services

Before running the tests, ensure all services are running:

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or start individual services
# Core API Service: http://localhost:8080
# Recommendation Service: http://localhost:8001
# Summary Service: http://localhost:8002
```

## Environment Configuration

The `.vscode/settings.json` file contains environment variables for different environments:

- **local**: Default local development environment (localhost)
- **dev**: Development environment
- **production**: Production environment

### Switching Environments

1. Open any `.http` file
2. Click on the environment selector in the status bar (bottom right)
3. Select your desired environment (local, dev, production)

## HTTP Files Overview

### 1. `auth.http` - Authentication API
Tests for user authentication and management:
- User registration
- User login
- Token refresh
- Get current user profile
- List all users (Admin)
- Update user roles (Admin)

**Usage:**
1. Run "Register a new user" request
2. Run "Login" request - this automatically extracts the access token
3. Use the extracted token for authenticated requests

### 2. `articles.http` - Articles Management API
Tests for article operations:
- List articles with pagination
- Filter articles by source, date range
- Get article details
- Delete articles (Admin)

**All endpoints are public except DELETE which requires admin authentication.**

### 3. `sources.http` - RSS Sources Management API
Tests for RSS source management:
- List active RSS sources (Public)
- Add new RSS source (Admin)
- Update RSS source (Admin)
- Delete RSS source (Admin)

**Admin authentication required for POST, PUT, DELETE operations.**

### 4. `crawler.http` - Crawler Orchestration API
Tests for crawler management:
- Trigger immediate crawl for all sources (Admin)
- Trigger crawl for specific source (Admin)
- Get crawler schedule (Admin)
- Update crawler schedule (Admin)

**All endpoints require admin authentication.**

### 5. `recommendation.http` - Recommendation Service API
Tests for AI-powered recommendation features:
- Upsert articles for indexing
- Semantic search with natural language queries
- Get similar articles based on article ID

**Supports multilingual queries (Vietnamese, English, etc.).**

### 6. `summary.http` - Summary Service API
Tests for AI-powered text summarization:
- Generate summaries for articles
- Supports multilingual text (Vietnamese, English, etc.)

**Minimum text length: 50 characters.**

### 7. `health-check.http` - Health Check API
Quick health checks for all services:
- Core API Service health
- Recommendation Service health
- Summary Service health

## How to Use

### Basic Usage

1. Open any `.http` file in VS Code
2. Click "Send Request" above any HTTP request
3. View the response in the right panel

### Variable Usage

HTTP files use variables for reusability:

```http
@baseUrl = {{baseUrl}}
@accessToken = YOUR_ACCESS_TOKEN_HERE
```

- `{{baseUrl}}` - Automatically uses the environment variable from `.vscode/settings.json`
- Local variables (like `@accessToken`) can be updated manually or extracted from responses

### Automatic Token Extraction

The authentication flow automatically extracts tokens:

```http
# @name login
POST {{baseUrl}}/api/v1/auth/login HTTP/1.1
Content-Type: application/json
{
  "username": "testuser",
  "password": "securepassword123"
}

###
# Token is automatically extracted
@accessToken = {{login.response.body.access_token}}
@refreshToken = {{login.response.body.refresh_token}}
```

### Testing Workflow

#### Complete E2E Testing Flow:

1. **Start with health checks**
   ```
   Open: health-check.http
   Run: All health check requests
   Verify: All services return status 200
   ```

2. **Set up authentication**
   ```
   Open: auth.http
   Run: Register a new user
   Run: Login (token auto-extracted)
   Run: Get current user profile (to verify token works)
   ```

3. **Test RSS sources**
   ```
   Open: sources.http
   Run: List sources (public)
   Run: Create new source (requires admin token)
   Run: Update source
   ```

4. **Test article management**
   ```
   Open: articles.http
   Run: List all articles
   Run: Get specific article
   Run: Test filters (by source, date)
   ```

5. **Test crawler**
   ```
   Open: crawler.http
   Run: Get schedule
   Run: Trigger crawl for all sources
   Run: Update schedule
   ```

6. **Test recommendation service**
   ```
   Open: recommendation.http
   Run: Upsert articles for indexing
   Run: Semantic search
   Run: Get similar articles
   ```

7. **Test summary service**
   ```
   Open: summary.http
   Run: Generate summary for articles
   ```

## RFC 2616 Compliance

All HTTP files follow RFC 2616 specifications:

1. **Request Line**: Method, URI, HTTP Version
   ```
   GET /api/v1/articles HTTP/1.1
   ```

2. **Headers**: Properly formatted headers
   ```
   Content-Type: application/json
   Authorization: Bearer <token>
   ```

3. **Message Body**: JSON payloads for POST/PUT requests
   ```json
   {
     "username": "testuser",
     "password": "securepassword123"
   }
   ```

4. **Request Separation**: Triple hash separator (###)
   ```
   ###
   # Next request
   ```

## Tips and Best Practices

### 1. Use Request Names for Token Extraction
```http
# @name login
POST {{baseUrl}}/api/v1/auth/login HTTP/1.1
```
This allows you to reference the response later.

### 2. Update Variables Before Testing
Before running tests, update these variables in each file:
- `@username` - Your test username
- `@email` - Your test email
- `@password` - Your test password
- `@accessToken` - Admin token for admin-only endpoints

### 3. Chain Requests
Use extracted values from previous responses:
```http
@sourceId = {{createSource.response.body.id}}
```

### 4. Test Error Cases
Test validation and error handling:
- Invalid credentials
- Missing required fields
- Unauthorized access
- Not found resources

### 5. Use Comments
Add descriptive comments to document test cases:
```http
###
# Test Case: User login with valid credentials
# Expected: 200 OK with access_token
POST {{baseUrl}}/api/v1/auth/login HTTP/1.1
```

## Troubleshooting

### Connection Refused
- Ensure all services are running: `docker-compose ps`
- Check service logs: `docker-compose logs [service-name]`

### 401 Unauthorized
- Verify your access token is valid
- Login again to get a fresh token
- Ensure you have admin role for admin-only endpoints

### 404 Not Found
- Verify the resource ID exists in the database
- Check the API endpoint path

### Invalid JSON
- Ensure JSON payloads are properly formatted
- Check for missing commas or quotes

## Environment Variables Reference

Defined in `.vscode/settings.json`:

```json
{
  "rest-client.environmentVariables": {
    "local": {
      "baseUrl": "http://localhost:8080",
      "recommendationUrl": "http://localhost:8001",
      "summaryUrl": "http://localhost:8002"
    }
  }
}
```

## Additional Resources

- [VS Code REST Client Documentation](https://github.com/Huachao/vscode-restclient)
- [RFC 2616 - HTTP/1.1](https://www.ietf.org/rfc/rfc2616.txt)
- [API Examples](../API_EXAMPLES.md)
- [Project Architecture](../ARCHITECTURE.md)

## Contributing

When adding new endpoints:
1. Create appropriate `.http` file or add to existing file
2. Follow RFC 2616 format
3. Add descriptive comments
4. Include both success and error test cases
5. Update this README with new endpoints

## License

Same as the main project.
