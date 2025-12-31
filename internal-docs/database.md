# Internal Documentation

This directory is for internal team documentation that should not be publicly shared.

## What Goes Here?

- Internal architecture decisions
- Database schemas and migration notes
- Infrastructure details
- Security procedures
- Internal APIs and services
- Team processes and workflows
- Incident response procedures
- Access credentials documentation

## ⚠️ Security Notice

**Do NOT commit sensitive information:**
- API keys or tokens
- Passwords or connection strings
- Private keys or certificates
- Personal data
- Proprietary business logic

Use environment variables and secret management tools for sensitive data.

## Suggested Structure

```
internal-docs/
├── README.md               # This file
├── architecture/
│   ├── decisions.md        # Architecture decision records (ADRs)
│   └── infrastructure.md   # Infrastructure details
├── database/
│   ├── schema.md           # Database schema documentation
│   └── migrations.md       # Migration procedures
├── security/
│   ├── access-control.md   # Access control policies
│   └── incident-response.md # Incident response procedures
└── processes/
    ├── deployment.md       # Internal deployment procedures
    └── onboarding.md       # Team onboarding guide
```

## Example: Architecture Decision Record (ADR)

```markdown
# ADR-001: Use Docker for Local Development

## Status
Accepted

## Context
We need a consistent development environment across team members using different operating systems.

## Decision
Use Docker and Docker Compose for local development environment.

## Consequences
### Positive
- Consistent environment across all developers
- Easy onboarding for new team members
- Matches production environment closely

### Negative
- Initial setup takes time
- Requires learning Docker basics
- Resource intensive on older machines

## Alternatives Considered
- Virtual machines (rejected: too heavy)
- Native development (rejected: inconsistent)
```

## Example: Database Schema

```markdown
# Database Schema

## Users Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | User identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

## Indexes
- `idx_users_email` on `email` column

## Relations
- One-to-many with `sessions` table
```

---

**Remember**: This is internal documentation. Be thorough but keep sensitive information in secure vaults.
```

### 5. Update specific fields in a document
```bash
curl -X PATCH "https://db.chipatrade.com/api/firestore/collections/products/DOCUMENT_ID" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "price": 14.99,
    "inStock": false
  }'
```

### 6. Delete a document
```bash
curl -X DELETE "https://db.chipatrade.com/api/firestore/collections/products/DOCUMENT_ID" \
  -H "x-api-key: "
```

### 7. Batch operations
```bash
curl -X POST "https://db.chipatrade.com/api/firestore/batch" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {
        "type": "set",
        "collection": "products",
        "docId": "product1",
        "data": {"name": "Tea", "price": 8.99},
        "merge": true
      },
      {
        "type": "set",
        "collection": "products",
        "docId": "product2",
        "data": {"name": "Sugar", "price": 4.99},
        "merge": true
      }
    ]
  }'
```

---

## Authentication Examples

### 1. Create a new user
```bash
curl -X POST "https://db.chipatrade.com/api/auth/users" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePassword123!",
    "displayName": "Test User",
    "phoneNumber": "+1234567890"
  }'
```

### 2. Get user by email
```bash
curl -X GET "https://db.chipatrade.com/api/auth/users/email/testuser@example.com" \
  -H "x-api-key: "
```

### 3. List all users
```bash
curl -X GET "https://db.chipatrade.com/api/auth/users?maxResults=10" \
  -H "x-api-key: "
```

### 4. Update user information
```bash
curl -X PATCH "https://db.chipatrade.com/api/auth/users/USER_UID" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Updated Name",
    "phoneNumber": "+9876543210"
  }'
```

### 5. Set custom claims for a user (e.g., admin role)
```bash
curl -X POST "https://db.chipatrade.com/api/auth/users/USER_UID/claims" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "claims": {
      "admin": true,
      "role": "moderator",
      "accessLevel": 5
    }
  }'
```

### 6. Create custom token for a user
```bash
curl -X POST "https://db.chipatrade.com/api/auth/custom-token" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "USER_UID",
    "claims": {
      "premium": true
    }
  }'
```

### 7. Verify Firebase ID token
```bash
curl -X POST "https://db.chipatrade.com/api/auth/verify-token" \
  -H "x-api-key: " \
  -H "Content-Type: application/json" \
  -d '{
    "token": "FIREBASE_ID_TOKEN_HERE"
  }'
```

### 8. Get current user info (requires Firebase ID token)
```bash
curl -X GET "https://db.chipatrade.com/api/auth/me" \
  -H "x-api-key: " \
  -H "Authorization: Bearer FIREBASE_ID_TOKEN_HERE"
```

### 9. Revoke all refresh tokens for a user
```bash
curl -X POST "https://db.chipatrade.com/api/auth/users/USER_UID/revoke-tokens" \
  -H "x-api-key: "
```

### 10. Delete a user
```bash
curl -X DELETE "https://db.chipatrade.com/api/auth/users/USER_UID" \
  -H "x-api-key: "
```

---

## Health Check
```bash
curl -X GET "https://db.chipatrade.com/health"
```

## Get API Information
```bash
curl -X GET "https://db.chipatrade.com/"
```

---

## Notes

- Replace `DOCUMENT_ID` with actual document IDs from your Firestore
- Replace `USER_UID` with actual user UIDs from Firebase Auth
- Replace `FIREBASE_ID_TOKEN_HERE` with actual Firebase ID tokens
- The API key in these examples is `chipa-secret-key-change-this` - change this in production!
- All timestamps are automatically added (createdAt, updatedAt)

## Testing with Postman

You can also import these into Postman or use the Postman collection feature. Create a new environment with:
- `base_url`: https://db.chipatrade.com
- `api_key`: chipa-secret-key-change-this
