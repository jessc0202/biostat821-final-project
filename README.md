# Dream Survey Processor
group member: Sizhe
A Python library for processing messy, multi-wave survey data from different sources and producing clean, standardized datasets.

## Features

- Load data from CSV and Excel files
- Map different column schemas to a unified format
- Align survey waves across datasets and labeled groups
- Basic data validation and cleaning
- Command-line interface for general survey directories

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
combined_data = processor.process_data_groups(
    {
        "USA": "path/to/usa/data",
        "Argentina": "path/to/argentina/data",
    }
)

validation_results = processor.validate_data()
print(validation_results)

summary = processor.get_summary()
print(summary)
```

### Customize schema mapping

```python
custom_mapping = {
    "response_id": ["ResponseId", "Response ID", "id"],
    "start_date": ["StartDate", "Start Date"],
    "age": ["Demo_Age", "Age"],
}

processor = SurveyProcessor(default_mapping=custom_mapping)
```

### Command Line

```bash
dream-survey-processor --input-dir USA=./USA --input-dir Argentina=./Argentina --output processed_data.csv --validate
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

The library supports directories containing CSV and Excel files. Each directory is treated as a labeled group and files are processed in sorted order.

## Generative AI Usage

We used ChatGPT to help with:
- brainstorming the project structure
- drafting initial test cases
- debugging Ruff, Black, and pytest errors
- improving README wording

All code was reviewed, edited, and tested by me before submission.
## License

MIT License
