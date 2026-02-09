# Explicación Técnica: Sistema de Análisis de Crédito

Este documento describe la estructura y funcionamiento del código fuente del sistema.

## 1. Arquitectura General
El sistema sigue un flujo lineal de 3 pasos principales:
1.  **Ingesta**: Lectura de archivos (Excel, PDF) desde la carpeta `data/`.
2.  **Construcción del Prompt**: Unificación de toda la información en un solo texto coherente.
3.  **Análisis (LLM)**: Envío de la información a la Inteligencia Artificial Local (Ollama) para obtener evaluar el riesgo.

## 2. Descripción de Archivos

### `main.py` (El cerebro)
Es el archivo principal que coordina todo.
- **Función**: Verifica que existan los archivos, llama a los lectores de datos, prepara el "prompt" (la pregunta larga para la IA) e imprime el reporte final.
- **Flujo**:
    1. Define las rutas de los archivos.
    2. Llama a `DataLoader` y `PDFProcessor`.
    3. Combina los textos extraídos.
    4. Envía todo a `LocalLLMClient`.
    5. Guarda el resultado en `credit_report.md`.

### `src/ingestion/loaders.py`
Encargado de leer archivos Excel.
- **`load_credit_application`**: Usa `pandas` para leer la solicitud de crédito y la convierte en un diccionario simple (clave-valor) para que la IA la entienda fácil.
- **`load_macro_data`**: Lee los indicadores económicos y los convierte a una tabla en formato texto (Markdown).

### `src/ingestion/pdf_processor.py`
Encargado de leer PDFs.
- **`extract_text_from_pdf`**: Usa la librería `pypdf`. Abre el archivo, recorre cada página y extrae el texto puro. Esto es necesario porque la IA no "mira" el PDF, sino que "lee" su contenido textual.

### `src/analysis/llm_client.py`
El puente con la Inteligencia Artificial.
- **Módulo `LocalLLMClient`**: Se conecta a tu servidor local de Ollama (generalmente en el puerto 11434).
- **Método `analyze_credit`**: Envía el mensaje con instrucciones de "actuar como analista de riesgo" y devuelve la respuesta generada.

### `tools/generate_dummy_data.py`
Un script auxiliar que no es parte del sistema principal, pero sirve para crear archivos de prueba (`solicitud_credito.xlsx`, `reporte_empresa.pdf`) automáticamente si no tienes datos reales.

## 3. Flujo de Datos

```mermaid
graph TD
    A[Archivos: Excel, PDF] -->|Extractores| B(Texto Crudo)
    B -->|Preprocesamiento| C{Main Prompt}
    C -->|Envío HTTP| D[Ollama / Local LLM]
    D -->|Respuesta Texto| E[Reporte Final (.md)]
```

## 4. Personalización
- **Cambiar el Modelo**: En `main.py`, busca la línea `llm = LocalLLMClient(model="llama3")` y cambia "llama3" por otro modelo que tengas (ej. "mistral").
- **Ajustar Reglas**: Si quieres que la IA sea más estricta, edita el texto dentro de la variable `prompt` en `main.py`.
