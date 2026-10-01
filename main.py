import os
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI

from generator import SyntheticDataGenerator
from prompts import PromptBuilder


load_dotenv(override=True)

models = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "stepfun/step-3.7-flash:free",
]
base_url_kilo = "https://api.kilo.ai/api/gateway"
api_key_kilo = os.getenv("KILOCODE_API_KEY")

client = OpenAI(
    api_key=api_key_kilo,
    base_url=base_url_kilo
)

prompt_builder = PromptBuilder()

for model in models:
    generator = SyntheticDataGenerator(
        client,
        model,
        prompt_builder
    ) 
    data = generator.generate(
        description="Employees of a technology company",
        columns=[
            "name",
            "position",
            "department",
            "salary",
            "working_hours",
            "overtime_hours",
            "years_of_experience"
        ],
        rows=5,
        style="business"
    )
    df = pd.DataFrame(data)
    print(f'{model} :')
    print(df)