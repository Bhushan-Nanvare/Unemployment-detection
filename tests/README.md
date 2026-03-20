# Tests

Add unit and integration tests here using **pytest**.

## Suggested structure

```
tests/
├── conftest.py          # Shared fixtures (e.g. sample data, API client)
├── test_data_loader.py
├── test_preprocessing.py
├── test_forecasting.py
├── test_shock_scenario.py
├── test_api.py          # FastAPI endpoint tests
└── ...
```

## Running tests

```bash
pip install pytest requests
pytest tests/ -v
```

## Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```
