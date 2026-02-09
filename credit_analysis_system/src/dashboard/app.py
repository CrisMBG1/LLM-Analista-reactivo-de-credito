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
from src.analysis.multi_agent import CreditCommittee
from src.reporting.pdf_generator import PDFReportGenerator

# Configuración de la página
st.set_page_config(
    page_title="Comité de Crédito IA",
    page_icon="🤖",
    layout="wide"
)

# Título
st.title("🤖 Comité de Crédito Multi-Agente")
st.markdown("---")

# Sidebar
st.sidebar.header("Configuración del Comité")
st.sidebar.info("Este sistema utiliza 3 modelos de IA trabajando en equipo.")

model_a_name = st.sidebar.text_input("Analista A (Numérico)", value="deepseek-r1:8b")
model_b_name = st.sidebar.text_input("Analista B (Cualitativo)", value="gemma3:1b")
model_boss_name = st.sidebar.text_input("Gerente (Decisor)", value="llama3")

# Rutas de datos
DATA_DIR = os.path.join(parent_dir, 'data')
credit_app_path = os.path.join(DATA_DIR, 'solicitud_credito.xlsx')
macro_data_path = os.path.join(DATA_DIR, 'datos_macro.xlsx')
report_pdf_path = os.path.join(DATA_DIR, 'reporte_empresa.pdf')

def load_data():
    if not os.path.exists(credit_app_path):
        st.error("No se encontraron los datos. Por favor ejecuta 'generate_dummy_data.py'.")
        return None, None, None, None
    
    credit_data = DataLoader.load_credit_application(credit_app_path)
    macro_md = DataLoader.load_macro_data(macro_data_path)
    
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
    # --- Vista Ejecutiva de Datos ---
    st.subheader("� Información del Cliente y Contexto")
    
    # Contenedor superior
    c_info, c_macro = st.columns([3, 2])
    
    with c_info:
        st.markdown("**Solicitud de Crédito**")
        if isinstance(credit_data, dict):
            # Formatear bonito como tabla HTML o st.dataframe limpio
            df_cred = pd.DataFrame(list(credit_data.items()), columns=["Concepto", "Detalle"])
            st.dataframe(df_cred, hide_index=True, use_container_width=True)
        else:
            st.write(credit_data)

    with c_macro:
        st.markdown("**Indicadores Económicos (Colombia)**")
        st.dataframe(macro_df, hide_index=True, use_container_width=True)
        
        st.markdown("**Resumen Reporte Anual**")
        st.caption(f"{pdf_text[:300]}...") # Mostrar un fragmento pequeño


    # --- Sección de Análisis ---
    st.markdown("### 🧠 Sala de Decisiones")
    
    # Helper para extraer conclusión
    def extract_conclusion(text):
        if "=== CONCLUSIÓN ===" in text:
            parts = text.split("=== CONCLUSIÓN ===")
            return parts[0], parts[1].strip()
        return text, "No se encontró una conclusión explícita."

    
    analyze_btn = st.button("Iniciar Sesión del Comité", type="primary", use_container_width=True)

    if analyze_btn:
        committee = CreditCommittee()
        
        # Construir Prompt Base
        bureau_score = 680
        base_prompt = f"""
        # DATOS DE ENTRADA
        - Solicitud: {credit_data}
        - Buró Score: {bureau_score}
        - Macroeconomía: {macro_md_text}
        - Reporte Anual: {pdf_text[:2000]}...
        """

        # 1. Analista A (Deepseek)
        with st.status(f"Analizando con {model_a_name}...", expanded=True) as status:
            raw_opinion_a = committee.get_analyst_opinion(model_a_name, base_prompt)
            body_a, conclusion_a = extract_conclusion(raw_opinion_a)
            status.update(label=f"{model_a_name} terminó", state="complete", expanded=False)
        
        # 2. Analista B (Gemma)
        with st.status(f"Analizando con {model_b_name}...", expanded=True) as status:
            raw_opinion_b = committee.get_analyst_opinion(model_b_name, base_prompt)
            body_b, conclusion_b = extract_conclusion(raw_opinion_b)
            status.update(label=f"{model_b_name} terminó", state="complete", expanded=False)

        # Mostrar Opiniones Preliminares
        st.subheader("🔎 Análisis Preliminares")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"**Modelo:** {model_a_name}")
            with st.expander("Ver Análisis Completo"):
                st.markdown(body_a)
            st.info(f"**Conclusión:**\n\n{conclusion_a}")
            
        with col_b:
            st.markdown(f"**Modelo:** {model_b_name}")
            with st.expander("Ver Análisis Completo"):
                st.markdown(body_b)
            st.info(f"**Conclusión:**\n\n{conclusion_b}")

        st.divider()

        # 3. Gerente (Llama3) - Síntesis
        with st.spinner(f"Generando Dictamen Final ({model_boss_name})..."):
            final_raw = committee.get_manager_decision(model_boss_name, base_prompt, raw_opinion_a, raw_opinion_b)
            body_final, conclusion_final = extract_conclusion(final_raw)
            
            st.header("🏆 Dictamen Final")
            
            # Recuadro de Conclusión Final (Más destacado)
            st.success(f"### � DECISIÓN FINAL\n\n{conclusion_final}")
            
            with st.expander("Leer Dictamen Completo", expanded=True):
                st.markdown(body_final)
            
            # Generar PDF (Usamos el texto completo)
            pdf_filename = "Dictamen_Final.pdf"
            pdf_path = os.path.join(parent_dir, 'src', 'reporting', pdf_filename)
            
            # Ensure dir exists
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            
            PDFReportGenerator.create_pdf(pdf_path, final_raw)
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Descargar Dictamen en PDF",
                    data=f,
                    file_name="Dictamen_Credito_Final.pdf",
                    mime="application/pdf"
                )

else:
    st.warning("Esperando datos...")
