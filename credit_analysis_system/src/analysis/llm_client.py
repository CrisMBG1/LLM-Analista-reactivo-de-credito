from openai import OpenAI
import os

class LocalLLMClient:
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama", model="llama3"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def analyze_credit(self, prompt):
        """
        Sends the prompt to the local LLM and retrieves the analysis.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior credit risk analyst. Your goal is to evaluate credit applications based on provided data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying LLM: {str(e)}"
