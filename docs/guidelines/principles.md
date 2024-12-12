# Python Development Guidelines

## General Principles
- Use Python 3.10+ features and patterns
- Always use type hints
- Always handle errors properly
- When raising errors, provide clear and detailed error messages to facilitate problem resolution

## Naming Conventions
- Use clear and consistent nomenclature for functions, classes, variables, and files
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Files: `kebab-case`

## Testing Guidelines

### General Testing Principles
- Always use pytest as the testing framework
- Test behavior, not implementation
- Cover different scenarios:
  - Positive cases
  - Negative cases
  - Edge cases
  - Boundary conditions

### Test Structure
- Name tests following the pattern:
  ```
  test_should_[expected_behavior]_when_[condition]_[additional_context]
  ```
- Isolate test units using fixtures
- Use parametrized tests with `pytest.mark.parametrize`

### Test Decorators and Utilities
- `@pytest.mark.skip`: Skip a test
- `@pytest.mark.skipif`: Skip a test under specific conditions
- `@pytest.mark.xfail`: Mark a test as expected to fail
- `@pytest.mark.usefixtures`: Use fixtures in a test

### Test Doubles
- Use stubs for replacing real objects withw test-specific behavior
- Use mocks for verifying interactions and behavior

