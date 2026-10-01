
# Synthetic Data Generator

A Python-based synthetic data generation tool that uses LLMs to create structured datasets from natural-language descriptions.

The application provides a Gradio interface where users can define a dataset, choose a generation style and model, and receive the generated data as a structured table.

## Features

- Generate synthetic datasets using LLMs
- Multiple generation styles:
  - **Realistic** — generates data based on user-defined columns and description
  - **Business** — generates realistic business-oriented datasets with relationships between fields
  - **Random** — lets the model choose the dataset topic, columns, and data types
- Configurable number of rows
- Configurable number of columns for random datasets
- Multiple LLM model options
- Automatic fallback to `kilo-auto/free` if the selected model is unavailable
- Output validation:
  - Row count validation
  - Column count validation
  - Column consistency validation
- Error handling for invalid input and generation failures
- Interactive Gradio web interface
- Environment-based API key configuration

## Example

For a business dataset, you can provide:

**Description:**

```text
Employees of a technology company
````

**Columns:**

```text
name, position, department, salary, working_hours, overtime_hours, years_of_experience
```

The application generates a structured dataset such as:

| name          | position                 | department  | salary | working_hours |
| ------------- | ------------------------ | ----------- | -----: | ------------: |
| Alex Martinez | Software Engineer        | Engineering |  95000 |            40 |
| Priya Patel   | Senior Software Engineer | Engineering | 150000 |            40 |
| Liam O'Connor | Data Scientist           | Data        | 115000 |            40 |

The exact output varies depending on the selected model.

## Project Structure

```text
synthetic_data/
│
├── app.py
├── main.py
├── generator.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### `app.py`

The main Gradio application.

It handles:

* User inputs
* Dataset generation
* Model selection
* Conditional UI behavior
* Error handling
* Fallback model logic
* Displaying generated datasets

### `generator.py`

Contains the `SyntheticDataGenerator` class.

It handles communication with the LLM and validates the generated JSON data.

### `prompts.py`

Contains the `PromptBuilder` class and the prompts used for the different dataset generation styles.

### `main.py`

A simple test script used to test the generator with different models without using the Gradio interface.

## Requirements

* Python 3.10+
* A Kilo Code API key

Python dependencies:

```text
openai
python-dotenv
gradio
pandas
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd synthetic_data
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
KILOCODE_API_KEY=your_kilo_api_key_here
```

You can use `.env.example` as a template.

The `.env` file is excluded from Git using `.gitignore`.

## Running the Application

Start the Gradio application:

```bash
python app.py
```

Gradio will provide a local URL where you can open the application in your browser.

## Model Fallback

The application supports multiple models.

If the selected model fails during generation, the application automatically attempts to generate the dataset using:

```text
kilo-auto/free
```

The user is notified when the fallback model is used.

## Validation

Generated data is validated before being displayed.

The application checks:

* Whether the requested number of rows was generated
* Whether the expected number of columns was generated
* Whether all records use the same columns
* Whether the generated data follows the requested schema

This helps prevent malformed LLM output from being passed directly to the user.

## License

This project is for educational and experimental purposes.
