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
    # --- Vista de Datos ---
    with st.expander("📂 Ver Datos de Entrada", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Datos Solicitud**")
            st.write(credit_data)
        with c2:
            st.write("**Datos Macro**")
            st.dataframe(macro_df, hide_index=True)

    # --- Sección de Análisis ---
    st.markdown("### 🧠 Sala de Decisiones")
    
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
        with st.status("Analista A pensando...", expanded=True) as status:
            st.write(f"Consultando a **{model_a_name}**...")
            opinion_a = committee.get_analyst_opinion(model_a_name, base_prompt)
            status.update(label="Analista A terminó", state="complete", expanded=False)
        
        # 2. Analista B (Gemma)
        with st.status("Analista B pensando...", expanded=True) as status:
            st.write(f"Consultando a **{model_b_name}**...")
            opinion_b = committee.get_analyst_opinion(model_b_name, base_prompt)
            status.update(label="Analista B terminó", state="complete", expanded=False)

        # Mostrar Opiniones Preliminares
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"### Opinión {model_a_name}")
            st.markdown(opinion_a)
        with col_b:
            st.info(f"### Opinión {model_b_name}")
            st.markdown(opinion_b)

        st.divider()

        # 3. Gerente (Llama3)
        with st.spinner(f"El Gerente ({model_boss_name}) está deliberando..."):
            final_verdict = committee.get_manager_decision(model_boss_name, base_prompt, opinion_a, opinion_b)
            
            st.success("### 🏆 Dictamen Final del Comité")
            st.markdown(final_verdict)
            
            # Generar PDF
            pdf_filename = "Dictamen_Final.pdf"
            pdf_path = os.path.join(parent_dir, 'src', 'reporting', pdf_filename)
            
            # Ensure dir exists
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            
            PDFReportGenerator.create_pdf(pdf_path, final_verdict)
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Descargar Dictamen en PDF",
                    data=f,
                    file_name="Dictamen_Credito_Final.pdf",
                    mime="application/pdf"
                )

else:
    st.warning("Esperando datos...")
