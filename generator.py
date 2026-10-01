import json

from altair import value
class SyntheticDataGenerator:
    def __init__(self,client,model,prompt_builder):
        self.client = client
        self.model = model
        self.prompt_builder = prompt_builder
    def generate(self, rows,style,description=None, columns= None,columns_count = None):
        if style =='random':
            prompt = self.prompt_builder.build_random(
                rows,
                columns_count
            ) 
        else:
            prompt = self.prompt_builder.build(
                description,
                columns,
                rows,
                style
            )
    

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        full_response = ""

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)
                full_response += content

        data =  json.loads(full_response)
        if len(data) != rows:
            raise ValueError(
                f"Expected {rows} rows, but got {len(data)}"
            )

        if style == "random":           
            for item in data:
                if len(item.keys()) != columns_count:
                    raise ValueError(
                        f"Expected {columns_count} columns, "
                        f"but got {len(item.keys())}"
                    )
            expected_columns = set(data[0].keys())
            for item in data:
                if set(item.keys()) != expected_columns:
                    raise ValueError(
                        f"Inconsistent columns. "
                        f"Expected {expected_columns}, "
                        f"but got {set(item.keys())}"
                    )
        else:
            if columns is None:
                raise ValueError(
                    'columns is required for realistic and business styles'
                )
            expected_columns = set(columns)
            for item in data:
                if set(item.keys()) != expected_columns:
                    raise ValueError(
                        f"Expected columns {expected_columns}, "
                        f"but got {set(item.keys())}"
                    )

        return data

