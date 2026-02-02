import streamlit as st
import pandas as pd
import os
import sys

# Add parent dir to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from src.ingestion.loaders import DataLoader
from src.ingestion.pdf_processor import PDFProcessor
from src.analysis.llm_client import LocalLLMClient

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Análisis de Crédito",
    page_icon="🏦",
    layout="wide"
)

# Título y Header
st.title("🏦 Sistema Ejecutivo de Análisis de Crédito")
st.markdown("---")

# Sidebar
st.sidebar.header("Panel de Control")
st.sidebar.info("Este sistema utiliza modelos de IA locales para analizar riesgos crediticios.")
model_name = st.sidebar.text_input("Modelo LLM", value="llama3")

# Rutas de datos
DATA_DIR = os.path.join(parent_dir, 'data')
credit_app_path = os.path.join(DATA_DIR, 'solicitud_credito.xlsx')
macro_data_path = os.path.join(DATA_DIR, 'datos_macro.xlsx')
report_pdf_path = os.path.join(DATA_DIR, 'reporte_empresa.pdf')

def load_data():
    if not os.path.exists(credit_app_path):
        st.error("No se encontraron los datos. Por favor ejecuta 'generate_dummy_data.py'.")
        return None, None, None
    
    credit_data = DataLoader.load_credit_application(credit_app_path)
    macro_md = DataLoader.load_macro_data(macro_data_path)
    
    # Load macro as DF for display
    try:
        macro_df = pd.read_excel(macro_data_path)
    except:
        macro_df = pd.DataFrame()

    pdf_text = ""
    if os.path.exists(report_pdf_path):
        pdf_text = PDFProcessor.extract_text_from_pdf(report_pdf_path)
    
    return credit_data, macro_df, pdf_text, macro_md

# Cargar datos
credit_data, macro_df, pdf_text, macro_md_text = load_data()

if credit_data:
    # --- Layout Principal ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📄 Solicitud de Crédito")
        # Mostrar datos del cliente como tabla key-value
        if isinstance(credit_data, dict):
            df_display = pd.DataFrame(list(credit_data.items()), columns=["Campo", "Valor"])
            st.table(df_display)
        else:
            st.write(credit_data)

    with col2:
        st.subheader("📈 Contexto Macroeconómico")
        st.dataframe(macro_df, hide_index=True)
        
        st.subheader("📑 Documentación Anexa")
        st.info(f"Reporte PDF procesado ({len(pdf_text)} caracteres extraídos).")
        with st.expander("Ver contenido extraído del PDF"):
            st.text(pdf_text)

    # --- Sección de Análisis ---
    st.markdown("---")
    st.header("🤖 Análisis de Riesgo (IA)")

    col_btn, col_status = st.columns([1, 4])
    
    analyze_btn = col_btn.button("Generar Informe", type="primary", use_container_width=True)

    if analyze_btn:
        with st.spinner('Analizando datos con Inteligencia Artificial...'):
            try:
                # Construir Prompt
                bureau_score = 680 # Simulado
                prompt = f"""
                # Credit Admission Request Analysis

                ## 1. Applicant Profile
                {credit_data}

                ## 2. Bureau Score
                Score: {bureau_score} (Scale: 300-850, >650 is generally good)

                ## 3. Macroeconomic Context
                {macro_md_text}

                ## 4. Company Annual Report Summary
                {pdf_text[:3000]}...

                ## Task
                Analyze the above information to determine if the credit should be approved.
                Generate a professional executive report.
                """
                
                # Ejecutar LLM
                llm = LocalLLMClient(model=model_name)
                report = llm.analyze_credit(prompt)
                
                st.success("¡Análisis Completado!")
                st.markdown("### Reporte Ejecutivo")
                st.markdown(report)
                
                # Opción de Descarga
                st.download_button(
                    label="Descargar Reporte",
                    data=report,
                    file_name="reporte_credito.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error durante el análisis: {e}")

else:
    st.warning("Esperando datos...")
