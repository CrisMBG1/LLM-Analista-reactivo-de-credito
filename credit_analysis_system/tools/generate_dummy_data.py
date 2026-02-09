import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

DATA_DIR = '../data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def create_credit_application():
    data = {
        'Campo': [
            'Nombre del Cliente', 'NIT/Identificación', 'Ingresos Mensuales (COP)', 
            'Monto Solicitado (COP)', 'Plazo (Meses)', 'Propósito', 'Deudas Actuales (COP)'
        ],
        'Valor': [
            'Empresa Sólida S.A.S.', '900.123.456-7', '120,000,000', 
            '450,000,000', '24', 'Expansión de inventario y maquinaria', '35,000,000'
        ]
    }
    # Create DataFrame
    df = pd.DataFrame(data)
    filepath = os.path.join(DATA_DIR, 'solicitud_credito.xlsx')
    df.to_excel(filepath, index=False)
    print(f"Created {filepath}")

def create_macro_data():
    data = {
        'Indicador': ['Tasa de Interés Referencia (BanRep)', 'Inflación Anual (IPC)', 'Crecimiento PIB Sector Comercio', 'TRM (USD/COP)'],
        'Valor Actual': [12.75, 7.74, 1.2, 3950.00],
        'Tendencia': ['Estable', 'A la baja', 'Lenta', 'Volátil']
    }
    df = pd.DataFrame(data)
    filepath = os.path.join(DATA_DIR, 'datos_macro.xlsx')
    df.to_excel(filepath, index=False)
    print(f"Created {filepath}")

def create_company_report_pdf():
    filepath = os.path.join(DATA_DIR, 'reporte_empresa.pdf')
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, "Reporte Anual de Situación Financiera")
    c.drawString(100, 730, "Empresa Sólida S.A.S.")
    c.drawString(100, 700, "Resumen Ejecutivo:")
    c.drawString(100, 680, "La empresa ha mantenido un crecimiento sostenido del 12% en ventas nacionales.")
    c.drawString(100, 660, "Los márgenes de utilidad operativa se sitúan en el 18%.")
    c.drawString(100, 640, "La compañía opera principalmente en Bogotá, Medellín y Cali.")
    c.drawString(100, 600, "Balance General Simplificado (Cifras en COP):")
    c.drawString(100, 580, "Activos Totales: $1,250,000,000")
    c.drawString(100, 560, "Pasivos Totales: $380,000,000")
    c.drawString(100, 540, "Patrimonio: $870,000,000")
    c.drawString(100, 500, "Nota del Auditor:")
    c.drawString(100, 480, "Estados financieros preparados bajo NIIF para PYMES.")
    c.save()
    print(f"Created {filepath}")

if __name__ == "__main__":
    create_credit_application()
    create_macro_data()
    create_company_report_pdf()
