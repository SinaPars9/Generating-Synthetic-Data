import os

import gradio as gr
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI

from generator import SyntheticDataGenerator
from prompts import PromptBuilder


load_dotenv(override=True)


MODELS = {
    "Nemotron 3 Super": "nvidia/nemotron-3-super-120b-a12b:free",
    "Step 3.7 Flash": "stepfun/step-3.7-flash:free",
}

FALLBACK_MODEL = "kilo-auto/free"

BASE_URL = "https://api.kilo.ai/api/gateway"
API_KEY = os.getenv("KILOCODE_API_KEY")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


prompt_builder = PromptBuilder()


def generate_with_model(
    model_id,
    description,
    columns,
    rows,
    style,
    columns_count
):

    generator = SyntheticDataGenerator(
        client,
        model_id,
        prompt_builder
    )

    if style == "random":

        return generator.generate(
            rows=rows,
            style="random",
            columns_count=columns_count
        )

    return generator.generate(
        description=description,
        columns=columns,
        rows=rows,
        style=style
    )


def generate_data(
    description,
    columns,
    rows,
    style,
    columns_count,
    model
):

    try:

        rows = int(rows)

        if rows <= 0:
            raise ValueError(
                "Rows must be greater than 0."
            )

        if style == "random":

            columns_count = int(columns_count)

            if columns_count <= 0:
                raise ValueError(
                    "Columns Count must be greater than 0."
                )

        else:

            if not description.strip():
                raise ValueError(
                    "Description is required."
                )

            columns = [
                column.strip()
                for column in columns.split(",")
                if column.strip()
            ]

            if not columns:
                raise ValueError(
                    "At least one column is required."
                )

        model_id = MODELS[model]

        try:

            data = generate_with_model(
                model_id=model_id,
                description=description,
                columns=columns,
                rows=rows,
                style=style,
                columns_count=columns_count
            )

        except Exception:

            gr.Warning(
                f"{model} is unavailable. "
                "Switching to Auto Free..."
            )

            data = generate_with_model(
                model_id=FALLBACK_MODEL,
                description=description,
                columns=columns,
                rows=rows,
                style=style,
                columns_count=columns_count
            )

            gr.Info(
                "Dataset generated using Auto Free."
            )

        return pd.DataFrame(data)

    except ValueError as error:

        raise gr.Error(str(error))

    except Exception as error:

        raise gr.Error(
            f"Generation failed: {error}"
        )


def update_inputs(style):

    if style == "random":

        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True)
        )

    return (
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=False)
    )


with gr.Blocks() as app:

    gr.Markdown("# Synthetic Data Generator")

    description = gr.Textbox(
        label="Description",
        placeholder="Describe the dataset you want to generate..."
    )

    columns = gr.Textbox(
        label="Columns",
        placeholder="name, age, city, salary"
    )

    rows = gr.Number(
        label="Rows",
        value=5,
        precision=0
    )

    style = gr.Dropdown(
        choices=[
            "realistic",
            "business",
            "random"
        ],
        label="Style",
        value="realistic"
    )

    columns_count = gr.Number(
        label="Columns Count",
        value=5,
        precision=0,
        visible=False
    )

    model = gr.Dropdown(
        choices=list(MODELS.keys()),
        label="Model",
        value="Nemotron 3 Super"
    )

    generate_button = gr.Button(
        "Generate"
    )

    output = gr.Dataframe(
        label="Generated Data"
    )

    style.change(
        fn=update_inputs,
        inputs=style,
        outputs=[
            description,
            columns,
            columns_count
        ]
    )

    generate_button.click(
        fn=generate_data,
        inputs=[
            description,
            columns,
            rows,
            style,
            columns_count,
            model
        ],
        outputs=output
    )


app.launch()