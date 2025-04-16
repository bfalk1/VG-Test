# IAM Fullstack Challenge — Example Solution

This solution includes:

- `server.ts` — Express backend with mocked login + JWT + role-based dashboard
- `auth_component.tsx` — React frontend to log in, display token + dashboard
- Role-based authorization with JWT and minimal error handling
- Connects to Postgres DB with `users` table (via `seed.sql`)

## Setup

1. Ensure PostgreSQL is running and seed your DB with the provided `seed.sql`
2. Run the server:
   ```
   npm install
   ts-node server.ts
   ```

3. Run the React frontend normally or embed into your system
4. Interact with the login system using:
   - admin@example.com
   - user@example.com
   - (password can be mocked)

## Notes

- Error handling is implemented for invalid tokens, missing credentials, and unknown roles
- Extend this by adding hashed passwords, SCIM/OAuth2 integration, etc.