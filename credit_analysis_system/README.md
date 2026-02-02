# Sistema de Análisis de Crédito con IA

Este proyecto automatiza el análisis de solicitudes de crédito empresarial utilizando un LLM local (Ollama). Integra datos de excel, reportes en PDF y datos macroeconómicos para generar una recomendación de riesgo.

## 📋 Características
- **Ingesta Muti-fuente**: Lee Excel (solicitudes, datos macro) y PDF (reportes anuales).
- **Análisis con IA Local**: Usa Ollama (Llama 3 u otros) para privacidad y control.
- **Reportes Automáticos**: Genera un archivo Markdown con el análisis de riesgo.

## 🚀 Instalación y Uso

### Prerrequisitos
1.  **Python 3.8+** ([Descargar](https://www.python.org/downloads/)) - *Asegúrate de marcar "Add to PATH" al instalar*.
2.  **Ollama** ([Descargar](https://ollama.com)) - Con el modelo `llama3` descargado (`ollama pull llama3`).

### Configuración Rápida (Windows)
Simplemente ejecuta el archivo **`setup.bat`** incluido en la carpeta. Este script:
1.  Verifica tu instalación de Python.
2.  Instala las librerías necesarias (`pandas`, `openpyxl`, `openai`, etc.).
3.  Genera datos de prueba si no existen.

### Ejecución Manual
1.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
2.  Generar datos de prueba (opcional):
    ```bash
    python tools/generate_dummy_data.py
    ```
3.  **Correr el análisis**:
    ```bash
    python main.py
    ```
    El reporte se guardará en `src/reporting/credit_report.md`.

## 📂 Estructura del Código

```text
credit_analysis_system/
├── data/                   # Archivos de entrada (Excel, PDF)
├── src/
│   ├── analysis/           # Lógica de conexión con el LLM
│   │   └── llm_client.py
│   ├── ingestion/          # Scripts para leer archivos
│   │   ├── loaders.py      # Lee Excel/CSV
│   │   └── pdf_processor.py # Extrae texto de PDFs
│   └── reporting/          # Carpeta de salida de reportes
├── tools/
│   └── generate_dummy_data.py # Generador de datos ficticios
├── main.py                 # Script principal (Orquestador)
├── requirements.txt        # Lista de dependencias
└── setup.bat               # Autoconfiguración para Windows
```

## 🛠 Solución de Problemas COMMON

| Error | Solución |
|-------|----------|
| `'python' no se reconoce...` | Reinstala Python y marca **"Add Python to PATH"**. Reinicia tu PC. |
| `model 'llama3' not found` | Abre una terminal y ejecuta `ollama pull llama3`. |
| `Connection refused` | Asegúrate de que Ollama esté corriendo (icono en la barra de tareas). |

---
**Nota**: Para una explicación más técnica del flujo de datos, consulta el archivo `EXPLICACION_CODIGO.md`.
