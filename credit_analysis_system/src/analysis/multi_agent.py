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
        Eres un sistema de análisis de riesgo crediticio avanzado.
        Tu trabajo es revisar los datos y dar una opinión técnica objetiva.
        
        IMPORTANTE:
        1. No saludes ni te presentes.
        2. Al final de tu respuesta, DEBES incluir una línea exacta que diga "=== CONCLUSIÓN ===" seguida de un resumen de 2 líneas.
        3. Responde SIEMPRE en Español.
        """
        return self._call_model(model_name, sys_prompt, data_prompt)

    def get_manager_decision(self, model_name, data_prompt, opinion_a, opinion_b):
        """
        Gets the final decision.
        Synthesizes the opinions A and B.
        """
        sys_prompt = """
        Eres un sistema de decisión de créditos.
        Tu trabajo es sintetizar los reportes y los datos para emitir el dictamen final.
        Analiza objetivamente sin roles ni teatro.
        
        IMPORTANTE:
        1. No incluyas firmas, nombres de cargos (como "Gerente") ni despedidas.
        2. Al final de tu respuesta, DEBES incluir una línea exacta que diga "=== CONCLUSIÓN ===" seguida de la decisión final clara (Aprobado/Rechazado) y el motivo principal.
        3. Responde SIEMPRE en Español.
        """
        
        final_prompt = f"""
        # DATOS DE LA SOLICITUD
        {data_prompt}

        ---
        # REPORTE 1 (Análisis Numérico)
        {opinion_a}

        ---
        # REPORTE 2 (Análisis Cualitativo)
        {opinion_b}

        ---
        # TU TAREA
        1. Evalúa la consistencia entre los análisis.
        2. Decide si otorgar el crédito.
        3. Genera el Dictamen Final sin adornos personales.
        """
        
        return self._call_model(model_name, sys_prompt, final_prompt)
