# PassworkClient Test Suite

This document provides instructions for running and extending the test suite for the PassworkClient library.

## Test Structure

The test suite is organized as follows:

- `tests/unit/`: Unit tests for isolated components
  - `test_crypto.py`: Tests for cryptographic functions
  - `test_item.py`: Tests for the Item module functionality
- `tests/mock_data/`: Real API response data for testing
  - `item_response.json`: Sample password item response
  - `user_keys_response.json`: Sample user encryption keys

## Prerequisites

Ensure you have installed the required dependencies:

```bash
pip install -r requirements.txt
```

The dependencies include pytest, pytest-mock, pytest-cov, and other development tools needed for testing.

## Running Tests

### Run all tests

```bash
python -m pytest
```

### Run with different verbosity

```bash
python -m pytest -v  # verbose output
python -m pytest -q  # quiet output
```

### Run specific test files

```bash
# Run crypto tests
python -m pytest tests/unit/test_crypto.py

# Run item tests
python -m pytest tests/unit/test_item.py
```

### Run specific test methods

```bash
# Run a specific test method
python -m pytest tests/unit/test_crypto.py::TestCrypto::test_encrypt_decrypt_aes
```

### Run tests with coverage reporting

```bash
python -m pytest --cov=passwork_client
```

For a detailed HTML coverage report:

```bash
python -m pytest --cov=passwork_client --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage details.

## Test Fixtures

The test suite includes several fixtures defined in `tests/conftest.py`:

- `mock_response`: Creates mock HTTP responses
- `mock_client`: Provides a PassworkClient with mocked request methods
- `mock_encrypted_client`: Similar to `mock_client` but with encryption enabled
- `load_mock_data`: Loads data from JSON files in the mock_data directory
- `vault_mock_data`: Provides sample vault data
- `password_mock_data`: Provides sample password data

## Adding New Tests

When adding functionality to the library, follow these guidelines:

1. Add unit tests for new functions or methods
2. Use the existing fixtures when possible
3. For API interaction tests, create or update mock data in the `mock_data` directory
4. Follow the existing test style and organization
5. Include tests for normal operation and error cases

### Testing Cryptographic Functions

When testing cryptographic functions:

- Use known test vectors where possible
- Test encryption/decryption roundtrips
- Verify compatibility with the Passwork API expectations

### Testing API Interactions

When testing API interactions:

- Use the provided mock client fixtures
- Mock API responses using real response structures
- Test both encrypted and unencrypted modes

## Security Considerations

- Tests should never include real credentials or API keys
- Use only mock data in the test suite
- When testing with real mock API responses, sanitize any sensitive information 