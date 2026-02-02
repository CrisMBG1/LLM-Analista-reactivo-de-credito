# Plan de Implementación: Sistema de Reporte de Admisión de Crédito

## Objetivo
Desarrollar un sistema automatizado que ingente datos de múltiples fuentes y utilice un LLM local para analizar la viabilidad de créditos, visualizado en un Dashboard Web profesional.

## Revisión del Usuario Requerida
> [!IMPORTANT]
> **Dashboard**: Se utilizará **Streamlit** por su capacidad de crear interfaces de datos profesionales rápidamente utilizando Python puro.

## Componentes

### Estructura del Proyecto

#### Ingesta de Datos (`src/ingestion`)
- **Credit App Loader**: Leer `solicitud_credito.xlsx`.
- **Macro Data Parser**: Leer `datos_macro.xlsx`.
- **PDF Processor**: Extraer texto de `reporte_empresa.pdf`.

#### Análisis (`src/analysis`)
- **Local LLM Client**: Cliente OpenAI para Ollama.
- **Prompt Engineering**: Construcción del prompt unificado.

#### Dashboard (`src/dashboard`)
- **`app.py`**: Interfaz de usuario.
    - **Tablero Principal**: Muestra KPIs del cliente.
    - **Sección de Análisis**: Botón para ejecutar el LLM y mostrar el resultado en Markdown renderizado.
    - **Visor de Documentos**: Visualización de tablas de datos macro.

## Nuevas Dependencias
- `streamlit`

## Plan de Verificación
1. Ejecutar `streamlit run src/dashboard/app.py`.
2. Verificar que carga los Excels.
3. Probar el botón de análisis.
