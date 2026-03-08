# FastAPI Learning Tasks

## Phase 1: Authentication & Security 🔐

### JWT Authentication Setup

- [x] Install required packages:
        `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
- [ ] Create `app/core/security.py` with password hashing utilities (using bcrypt)
- [ ] Create `app/core/auth.py` with JWT token creation and verification functions
- [ ] Add JWT secret key and algorithm settings to `app/core/config.py`
- [ ] Create `app/schemas/token.py` with Token and TokenData schemas

### Authentication Router

- [ ] Create `app/routers/auth.py` with login endpoint
- [ ] Implement POST `/auth/login` endpoint that returns JWT access token
- [ ] Hash passwords before storing in database (update users router)
- [ ] Create OAuth2 password bearer dependency for protected routes
- [ ] Add current user dependency function to validate JWT tokens

### Protect Existing Routes

- [ ] Add authentication to POST `/posts` (create post)
- [ ] Add authentication to PUT `/posts/{post_id}` (update post)
- [ ] Add authentication to DELETE `/posts/{post_id}` (delete post)
- [ ] Add authentication to POST `/comments` (create comment)
- [ ] Add authentication to PUT/DELETE comment endpoints
- [ ] Ensure users can only update/delete their own posts and comments

### Register Missing Routers

- [ ] Include `users.router` in `app/main.py`
- [ ] Include `comments.router` in `app/main.py`
- [ ] Include `auth.router` in `app/main.py`

## Phase 2: Advanced Features 🚀

### Pagination & Filtering

- [ ] Add pagination to GET `/posts` (limit, skip parameters)
- [ ] Add search functionality to posts (by title or content)
- [ ] Add filtering by user_id to posts endpoint
- [ ] Add pagination to GET `/comments`
- [ ] Create reusable pagination dependency

### Relationships & Complex Queries

- [ ] Include post owner data in PostOut schema
- [ ] Include comment count in PostOut schema
- [ ] Add endpoint to get all posts by a specific user
- [ ] Add endpoint to get all comments by a specific user
- [ ] Include comment author data in CommentOut schema

### Voting/Likes System

- [ ] Create `app/models/vote.py` for post likes/votes
- [ ] Create vote schema in `app/schemas/vote.py`
- [ ] Add POST `/posts/{post_id}/vote` endpoint
- [ ] Add DELETE `/posts/{post_id}/vote` endpoint (unlike)
- [ ] Include vote count in PostOut schema
- [ ] Ensure users can only vote once per post

## Phase 3: Data Validation & Error Handling 🛡️

### Enhanced Validation

- [ ] Add minimum/maximum length validation to post title and content
- [ ] Add minimum length validation to comment content
- [ ] Add username validation (alphanumeric, min/max length)
- [ ] Create custom validators for password strength
- [ ] Add email verification format validation

### Better Error Handling

- [ ] Create custom exception classes in `app/core/exceptions.py`
- [ ] Implement global exception handler
- [ ] Add proper error messages for duplicate email/username
- [ ] Add validation error responses with detailed field errors
- [ ] Handle database connection errors gracefully

## Phase 4: Testing 🧪

### Unit Tests

- [ ] Set up pytest and pytest-asyncio
- [ ] Create `tests/conftest.py` with test database fixture
- [ ] Write tests for user CRUD operations
- [ ] Write tests for post CRUD operations
- [ ] Write tests for comment CRUD operations
- [ ] Write tests for authentication (login, token validation)

### Integration Tests

- [ ] Test complete user registration and login flow
- [ ] Test creating posts with authentication
- [ ] Test unauthorized access attempts
- [ ] Test cascade deletion (user deletion removes their posts/comments)
- [ ] Test voting system edge cases

## Phase 5: Documentation & Code Quality 📚

### API Documentation

- [ ] Add detailed docstrings to all endpoint functions
- [ ] Add request/response examples to key endpoints
- [ ] Document all error responses with examples
- [ ] Add tags and descriptions to all routers
- [ ] Create README.md with setup and usage instructions

### Code Organization

- [ ] Create dependency file `app/core/dependencies.py` for reusable dependencies
- [ ] Refactor database queries into repository pattern (`app/repositories/`)
- [ ] Add type hints to all function parameters and returns
- [ ] Configure pre-commit hooks (black, flake8, mypy)
- [ ] Add logging configuration in `app/core/logging.py`

## Phase 6: Advanced Topics 🎓

### Background Tasks

- [ ] Implement email sending for user registration (background task)
- [ ] Add welcome email after user registration
- [ ] Create email templates directory

### Caching

- [ ] Install Redis and python redis client
- [ ] Add caching to GET `/posts` endpoint
- [ ] Implement cache invalidation on post create/update/delete
- [ ] Add rate limiting using Redis

### File Upload

- [ ] Add profile picture upload for users
- [ ] Add image upload for posts
- [ ] Implement file validation (size, type)
- [ ] Store uploaded files properly (local or cloud storage)

### Database Migrations

- [ ] Install Alembic
- [ ] Initialize Alembic configuration
- [ ] Create initial migration from current models
- [ ] Practice creating and applying migrations
- [ ] Add migration scripts to version control

### WebSockets

- [ ] Create WebSocket endpoint for real-time notifications
- [ ] Implement real-time comment notifications
- [ ] Add connection manager for WebSocket clients

## Phase 7: Production Ready 🌐

### Environment & Configuration

- [ ] Create `.env.example` file with all required variables
- [ ] Add environment-specific configurations (dev, staging, prod)
- [ ] Implement proper secrets management
- [ ] Add health check endpoint

### Performance

- [ ] Add database connection pooling optimization
- [ ] Implement query optimization (select specific columns, join optimization)
- [ ] Add database indexes for frequently queried fields
- [ ] Profile slow endpoints and optimize

### Deployment

- [ ] Create `Dockerfile` for the application
- [ ] Create `docker-compose.yml` with app and database
- [ ] Add GitHub Actions CI/CD pipeline
- [ ] Deploy to a cloud platform (Heroku, Railway, or DigitalOcean)
- [ ] Set up monitoring and logging (Sentry or similar)

### Security Hardening

- [ ] Add HTTPS/TLS in production
- [ ] Implement rate limiting on auth endpoints
- [ ] Add CORS configuration for production
- [ ] Implement refresh token functionality
- [ ] Add account lockout after failed login attempts
- [ ] Sanitize user inputs to prevent injection attacks

## Bonus Challenges 🎯

- [ ] Implement password reset functionality (email with token)
- [ ] Add social media authentication (OAuth with Google/GitHub)
- [ ] Create admin role and admin-only endpoints
- [ ] Implement soft delete for posts and users
- [ ] Add full-text search with PostgreSQL
- [ ] Create API versioning (v1, v2)
- [ ] Add GraphQL endpoint alongside REST API
- [ ] Implement audit logging for all changes
- [ ] Create automated API documentation generation
- [ ] Add support for multiple languages (i18n)

---

## Getting Started

**Recommended order:** Complete Phase 1 first (especially JWT authentication), then move through phases 2-4. Phases 5-7 can be done in any order based on your interests.

**Tip:** After completing each major feature, test it thoroughly and commit your changes!
