# Dream Survey Processor

A Python library for processing messy, multi-wave survey data from different sources and producing clean, standardized datasets.

## Features

- Load data from CSV and Excel files
- Map different column schemas to a unified format
- Align survey waves across datasets
- Basic data validation and cleaning
- Command-line interface for batch processing

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e .[dev]
```

## Usage

### As a Library

```python
from dream_survey_processor import SurveyProcessor

processor = SurveyProcessor()
combined_data = processor.process_all_data(
    usa_dir='path/to/usa/data',
    argentina_dir='path/to/argentina/data'
)

# Validate the data
validation_results = processor.validate_data()
print(validation_results)

# Get summary
summary = processor.get_summary()
print(summary)
```

### Command Line

```bash
dream-survey-processor --usa-dir ./USA --argentina-dir ./Argentina --output processed_data.csv --validate
```

## Project Structure

```
src/dream_survey_processor/
├── __init__.py
├── loader.py          # Data loading from files
├── mapper.py          # Schema mapping and standardization
├── aligner.py         # Wave alignment across datasets
├── validator.py       # Data validation
├── cleaner.py         # Basic data cleaning
├── processor.py       # Main processing pipeline
└── cli.py            # Command-line interface

tests/
├── test_*.py         # Unit tests

.github/workflows/
└── ci.yml            # GitHub Actions CI
```

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check src/ tests/
```

### Formatting

```bash
black src/ tests/
```

## Data Format

The library expects survey data in the following structure:

- **USA**: CSV files in a directory, one per wave (e.g., `Dream Initial Survey_*.csv`, `Dream Follow Up 1_*.csv`, etc.)
- **Argentina**: Excel files in a directory, one per form (e.g., `DATA FORM 1_*.xlsx`, `DATA FORM 2_*.xlsx`, etc.)

The library maps various column names to unified names and standardizes data types.

## License

MIT License