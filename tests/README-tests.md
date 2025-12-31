# Tests Directory

This directory contains all test files for your project.

## What Goes Here?

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Test fixtures and mock data
- Test utilities and helpers

## Suggested Structure

```
tests/
├── README-tests.md         # This file
├── unit/                   # Unit tests
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/            # Integration tests
│   ├── api/
│   └── database/
├── e2e/                    # End-to-end tests
│   └── scenarios/
├── fixtures/               # Test data
│   ├── users.json
│   └── products.json
└── utils/                  # Test utilities
    ├── setup.js
    └── helpers.js
```

## Testing Best Practices

### Write Testable Code
- Keep functions small and focused
- Avoid tight coupling
- Use dependency injection
- Separate business logic from infrastructure

### Good Test Characteristics (F.I.R.S.T.)
- **Fast**: Tests should run quickly
- **Independent**: Tests should not depend on each other
- **Repeatable**: Same results every time
- **Self-validating**: Clear pass/fail
- **Timely**: Write tests as you code

### Test Structure (Arrange-Act-Assert)
```javascript
describe('Calculator', () => {
  it('should add two numbers correctly', () => {
    // Arrange
    const calculator = new Calculator();
    const a = 5;
    const b = 3;
    
    // Act
    const result = calculator.add(a, b);
    
    // Assert
    expect(result).toBe(8);
  });
});
```

## Testing by Technology Stack

### Node.js/TypeScript
```bash
# Install testing frameworks
npm install --save-dev jest @types/jest
npm install --save-dev supertest @types/supertest

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

**Example test** (`tests/unit/calculator.test.ts`):
```typescript
import { Calculator } from '../../src/calculator';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(calculator.add(2, 3)).toBe(5);
    });

    it('should add negative numbers', () => {
      expect(calculator.add(-2, -3)).toBe(-5);
    });
  });
});
```

### Python
```bash
# Install testing framework
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/
```

**Example test** (`tests/unit/test_calculator.py`):
```python
import pytest
from src.calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()
    
    def test_add_positive_numbers(self):
        assert self.calc.add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        assert self.calc.add(-2, -3) == -5
```

### Go
```bash
# Run tests
go test ./...

# Run with coverage
go test -cover ./...
```

**Example test** (`calculator_test.go`):
```go
package calculator

import "testing"

func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Rust
```bash
# Run tests
cargo test

# Run with coverage (requires tarpaulin)
cargo tarpaulin --out Html
```

**Example test** (`src/calculator.rs`):
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive_numbers() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative_numbers() {
        assert_eq!(add(-2, -3), -5);
    }
}
```

## Integration Testing

### API Testing Example (Node.js + Supertest)
```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('API Endpoints', () => {
  describe('GET /health', () => {
    it('should return 200 OK', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);
      
      expect(response.body).toEqual({ status: 'ok' });
    });
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const newUser = {
        name: 'John Doe',
        email: 'john@example.com'
      };

      const response = await request(app)
        .post('/api/users')
        .send(newUser)
        .expect(201);
      
      expect(response.body).toHaveProperty('id');
      expect(response.body.name).toBe(newUser.name);
    });
  });
});
```

## Running Tests in Docker

Add to your `Makefile`:
```makefile
test:
	docker-compose run --rm api npm test

test-coverage:
	docker-compose run --rm api npm test -- --coverage
```

Or in `docker-compose.yml`:
```yaml
services:
  api:
    # ... existing config
  
  test:
    build: .
    command: npm test
    environment:
      - NODE_ENV=test
    depends_on:
      - postgres
      - redis
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          docker-compose run --rm api npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Coverage Goals

Aim for:
- **Critical paths**: 100% coverage
- **Business logic**: 90%+ coverage
- **Overall**: 80%+ coverage

Remember: 100% coverage doesn't mean bug-free code!

## Mocking External Services

### Example: Mocking HTTP requests (Node.js)
```typescript
import nock from 'nock';

describe('External API', () => {
  it('should fetch user data', async () => {
    nock('https://api.example.com')
      .get('/users/1')
      .reply(200, { id: 1, name: 'John' });

    const result = await fetchUser(1);
    expect(result.name).toBe('John');
  });
});
```

## Load Testing

### Using k6 (example script)
```javascript
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
};

export default function() {
  let res = http.get('http://localhost:8080/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Go Testing Package](https://golang.org/pkg/testing/)
- [Rust Testing Guide](https://doc.rust-lang.org/book/ch11-00-testing.html)

---

**Remember**: Good tests are an investment in code quality and developer confidence!
