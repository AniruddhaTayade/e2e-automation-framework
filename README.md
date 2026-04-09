# E2E Automation Framework

A complete Selenium + Python + pytest end-to-end automation framework for [SauceDemo](https://www.saucedemo.com) using the Page Object Model (POM) pattern.

## Features

- Page Object Model design pattern
- Headless Chrome support (CI/CD ready)
- HTML test reports via pytest-html
- GitHub Actions CI/CD pipeline
- Cross-browser support (Chrome & Firefox)
- React SPA compatible form interactions

## Project Structure

```
e2e-automation-framework/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions pipeline
├── config/
│   └── config.py               # Base URL, users, timeout settings
├── pages/
│   ├── base_page.py            # Base class with shared helper methods
│   ├── login_page.py           # Login page interactions
│   ├── inventory_page.py       # Inventory/products page interactions
│   └── cart_page.py            # Cart and checkout page interactions
├── tests/
│   ├── test_login.py           # Login flow tests (6 tests)
│   ├── test_inventory.py       # Inventory and sorting tests (10 tests)
│   └── test_cart.py            # Cart and checkout tests (7 tests)
├── utils/
│   └── driver_factory.py       # WebDriver factory (Chrome/Firefox)
├── conftest.py                 # Pytest fixtures
├── pytest.ini                  # Pytest configuration
└── requirements.txt            # Python dependencies
```

## Test Coverage

| Module | Tests | Scenarios |
|--------|-------|-----------|
| Login | 6 | Valid login, invalid credentials, empty fields, locked user |
| Inventory | 10 | Product count, A-Z/Z-A sort, price sort, cart badge |
| Cart | 7 | Add/remove items, full checkout flow, URL progression |
| **Total** | **23** | |

## Prerequisites

- Python 3.11+
- Google Chrome browser

## Installation

```bash
git clone https://github.com/AniruddhaTayade/e2e-automation-framework.git
cd e2e-automation-framework
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests (headed)
pytest

# Run all tests in headless mode
pytest --headless

# Run a specific test file
pytest tests/test_login.py --headless

# Run on Firefox
pytest --browser firefox --headless

# Run with HTML report
pytest --headless --html=reports/report.html --self-contained-html
```

## Test Report

An HTML report is automatically generated at `reports/report.html` after every run. In CI, it is uploaded as a downloadable artifact on every push and pull request.

## CI/CD

The GitHub Actions pipeline runs on every push and pull request to `main`:

1. Sets up Python 3.11
2. Installs dependencies
3. Runs all 23 tests in headless Chrome
4. Uploads the HTML report as an artifact (retained for 30 days)

## Test Users

SauceDemo provides the following built-in test users (password: `secret_sauce`):

| Username | Behaviour |
|----------|-----------|
| `standard_user` | Normal user |
| `locked_out_user` | Cannot log in |
| `problem_user` | UI bugs |
| `performance_glitch_user` | Slow responses |
