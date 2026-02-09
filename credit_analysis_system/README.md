# Sistema de Análisis de Crédito Multi-Agente 🤖🏦

Este sistema utiliza un **Comité de Inteligencia Artificial** para evaluar solicitudes de crédito empresarial.
Tres modelos (Deepseek, Gemma y Llama3) colaboran para analizar datos financieros, macroeconómicos y reportes PDF, emitiendo un dictamen final.

![Diagrama de Arquitectura](./Diagrama.png)

## 🌟 Características Principales
- **Arquitectura de Comité**:
    - **Analista A (Deepseek-r1:8b)**: Enfoque numérico/lógico.
    - **Analista B (Gemma3:1b)**: Enfoque cualitativo/resumen.
    - **Gerente (Llama3)**: Toma la decisión final y sintetiza.
- **Dashboard Interactivo**: Interfaz web (Streamlit) para visualizar el proceso de "pensamiento".
- **Generación de PDF**: Crea un dictamen oficial descargable.
- **Soporte Docker**: Contenerizado para ejecución aislada y fácil despliegue.

---

## 🚀 Guía de Ejecución Rápida

### Opción A: Windows (Sin instalar nada extra)
Si ya tienes Python y Ollama instalados en tu PC:

1.  **Ejecuta `setup.bat`** (Doble click) -> Instala librerías y genera datos.
2.  **Ejecuta `run_dashboard.bat`** (Doble click) -> Abre el sistema en tu navegador.

### Opción B: Docker (Recomendado para aislamiento)
Si tienes Docker Desktop instalado:

1.  Abre una terminal en esta carpeta.
2.  Construye y levanta el contenedor:
    ```bash
    docker-compose up --build
    ```
3.  Abre tu navegador en:
    👉 **http://localhost:8501**

> **Nota sobre Docker y Ollama**: El sistema está configurado para conectarse automáticamente a tu Ollama local (en Windows) a través de la red interna de Docker (`host.docker.internal`). No necesitas instalar Ollama dentro del contenedor.

---

## 📂 Estructura del Proyecto (Simplificada)

```text
credit_analysis_system/
├── app.py                  # APLICACIÓN PRINCIPAL (Dashboard)
├── data/                   # Datos de entrada (Excel, PDF)
├── src/
│   ├── analysis/           # Cerebro (Lógica Multi-Agente)
│   ├── ingestion/          # Lectores de datos
│   └── reporting/          # Generadores de PDF
├── tools/                  # Generador de datos ficticios
├── docs/                   # Documentación y Diagramas
├── Dockerfile              # Definición de la imagen Docker
├── docker-compose.yml      # Orquestación de servicios
└── requirements.txt        # Dependencias Python
```

## 🛠 Modelos Requeridos (Ollama)
Asegúrate de tener descargados estos modelos en tu terminal:
```bash
ollama pull deepseek-r1:8b
ollama pull gemma3:1b
ollama pull llama3
```
