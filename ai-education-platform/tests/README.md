# AI Education Platform - Tests

## Unit Tests
Location: `tests/unit/`

## Integration Tests
Location: `tests/integration/`

## E2E Tests
Location: `tests/e2e/`

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test type
pytest tests/unit/ -v
pytest tests/integration/ -v
```