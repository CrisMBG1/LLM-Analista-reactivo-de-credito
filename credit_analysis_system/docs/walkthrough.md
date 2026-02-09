# Guía de Ejecución: Sistema de Análisis de Crédito

## Prerrequisitos
1. **Python 3.8+** instalado.
   > [!IMPORTANT]
   > **Si ves el error "no se encontró Python"**:
   > 1. Descarga Python desde [python.org](https://www.python.org/downloads/).
   > 2. Ejecuta el instalador.
   > 3. **MUY IMPORTANTE**: Marca la casilla **"Add Python to PATH"** antes de dar clic en Install.
   > 4. Reinicia tu terminal (cierra y vuelve a abrir VS Code).

2. **Ollama** instalado y corriendo.
   > [!TIP]
   > **Configuración de Ollama**:
   > 1. Descarga e instala desde [ollama.com](https://ollama.com).
   > 2. Abre tu terminal (PowerShell o CMD).
   > 3. Descarga el modelo (ej. Llama3): `ollama pull llama3`
   > 4. El servicio suele correr en segundo plano automáticamente. Para verificar, visita `http://localhost:11434` en tu navegador (debería decir "Ollama is running").

## Pasos para probar el sistema

### 1. Instalación Automática
Ejecuta el archivo **`setup.bat`** (doble clic) para instalar librerías y generar datos.

### 2. Ejecutar el Dashboard (Web)
La forma más fácil es hacer doble clic en el archivo:
👉 **`run_dashboard.bat`**

Si prefieres usar la terminal manualmente:
```bash
python -m streamlit run src/dashboard/app.py
```

### 3. Ejecutar Análisis por Consola (Opcional)
Si prefieres solo el archivo de texto:
```bash
python main.py
```
El reporte se guardará en `src/reporting/credit_report.md`.
