# Blog API Tests

Complete test suite for the FastAPI Blog API application.

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_users.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## Test Coverage

**48 tests total** covering all endpoints and edge cases:
- **Users** (13 tests): CRUD operations, validation, password hashing
- **Posts** (14 tests): CRUD operations, foreign key constraints, cascade deletes
- **Comments** (19 tests): CRUD operations, relationships, filtering
- **Main** (2 tests): Root endpoint, API documentation

## Key Features

- **Isolated tests**: In-memory SQLite database per test
- **Comprehensive fixtures**: Sample data and test helpers in `conftest.py`
- **Password security**: Bcrypt hashing tested automatically
- **Foreign keys**: SQLite constraints enforced in tests
- **Edge cases**: Invalid data, duplicates, not-found scenarios

## Fixtures

- `client` - FastAPI test client
- `db_session` - Fresh in-memory database
- `create_test_user` - User factory fixture
- `create_test_post` - Post factory fixture
- `sample_*_data` - Test data dictionaries
