class PromptBuilder:
    def build(self, description, columns, rows, style):
        if style == 'realistic':
            return f"""Generate a realistic synthetic dataset based on the following description:
        Description:
        {description}
        Generate {rows} records.
        Columns:
        {columns}
        The generated data should resemble real-world data. Values should be plausible, consistent with each other, and appropriate for the given context. Avoid unrealistic combinations, excessive repetition, and obviously fabricated patterns.
        Return ONLY a valid JSON array.
         Each object must contain exactly these fields:
        {columns}
        Do not include markdown, explanations, comments, or any text outside the JSON array.
        """
        if style == 'business':
            return f"""Generate a realistic synthetic business dataset for the following scenario:
        Business scenario:
        {description}
        Generate {rows} employee records.
        Columns:
        {columns}
        The data should represent a plausible company and should contain meaningful relationships between fields. For example, salary, working hours, overtime, experience, department, and job position should be reasonably consistent with each other.
        Use realistic ranges and avoid impossible or highly unusual values unless the scenario requires them.
        Return ONLY a valid JSON array.
        Each object must contain exactly these fields:
        {columns}
        Do not include markdown, explanations, comments, or any text outside the JSON array.
        """
    def build_random(self, rows, columns_count):
        return f"""Generate a creative and diverse synthetic dataset.
        You decide:
        * the dataset topic
        * the column names
        * the type of data
        * the relationships between the columns
        Generate exactly {columns_count} columns.
        Generate exactly {rows} records.
        Choose an interesting and coherent topic. The dataset should be internally consistent and contain meaningful variation between records.
        Do not use the same type of dataset every time. Explore different domains such as science, technology, business, entertainment, sports, geography, history, or any other interesting subject.
        Return ONLY a valid JSON array.
        Each object should represent one record and must contain exactly {columns_count} fields.
        All objects must use the same field names throughout the dataset.
        Do not include markdown, explanations, comments, or any text outside the JSON array.
        """