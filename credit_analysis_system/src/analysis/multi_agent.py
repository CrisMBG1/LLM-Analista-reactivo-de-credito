from openai import OpenAI

class CreditCommittee:
    def __init__(self, base_url="http://localhost:11434/v1"):
        self.api_key = "ollama"
        self.base_url = base_url
    
    def _call_model(self, model_name, system_prompt, user_prompt):
        """Helper to call any Ollama model with specific instructions."""
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al consultar modelo {model_name}: {str(e)}"

    def get_analyst_opinion(self, model_name, data_prompt):
        """
        Gets an initial analysis from a junior analyst model (Deepseek/Gemma).
        """
        sys_prompt = """
        Eres un Analista de Riesgo Crediticio Junior.
        Tu trabajo es revisar los datos y dar una opinión técnica, enfocada en los números y hechos.
        Sé crítico y directo. Responde SIEMPRE en Español.
        """
        return self._call_model(model_name, sys_prompt, data_prompt)

    def get_manager_decision(self, model_name, data_prompt, opinion_a, opinion_b):
        """
        Gets the final decision from the senior manager model (Llama3).
        Synthesizes the opinions A and B.
        """
        sys_prompt = """
        Eres el Gerente de Aprobación de Créditos Senior.
        Tu trabajo es leer los reportes de tus dos analistas y los datos originales para emitir el DICTAMEN FINAL.
        Debes decidir si se APRUEBA o RECHAZA el crédito.
        Genera un reporte muy profesional, bien estructurado en Markdown.
        Responde SIEMPRE en Español.
        """
        
        final_prompt = f"""
        # DATOS DE LA SOLICITUD
        {data_prompt}

        ---
        # REPORTE ANALISTA 1 (Deepseek)
        {opinion_a}

        ---
        # REPORTE ANALISTA 2 (Gemma)
        {opinion_b}

        ---
        # TU TAREA
        1. Evalúa la consistencia entre los dos analistas.
        2. Decide si otorgar el crédito.
        3. Escribe el Reporte Final Oficial de la empresa.
        """
        
        return self._call_model(model_name, sys_prompt, final_prompt)
