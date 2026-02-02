import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

DATA_DIR = '../data/'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def create_credit_application():
    data = {
        'Campo': [
            'Nombre del Cliente', 'RFC/Identificación', 'Ingresos Mensuales', 
            'Monto Solicitado', 'Plazo (Meses)', 'Propósito', 'Deudas Actuales'
        ],
        'Valor': [
            'Empresa Sólida S.A. de C.V.', 'ESO123456789', '500000', 
            '2000000', '24', 'Expansión de inventario', '150000'
        ]
    }
    # df = pd.read_json(pd.io.json.dumps(data)) # Removed deprecated call
    df = pd.DataFrame(data)
    filepath = os.path.join(DATA_DIR, 'solicitud_credito.xlsx')
    df.to_excel(filepath, index=False)
    print(f"Created {filepath}")

def create_macro_data():
    data = {
        'Indicador': ['Tasa de Interés Referencia', 'Inflación Anual', 'Crecimiento PIB Sector Comercio', 'Tipo de Cambio (USD/MXN)'],
        'Valor Actual': [11.25, 4.5, 2.3, 17.50],
        'Tendencia': ['Estable', 'A la baja', 'Moderada', 'Volátil']
    }
    df = pd.DataFrame(data)
    filepath = os.path.join(DATA_DIR, 'datos_macro.xlsx')
    df.to_excel(filepath, index=False)
    print(f"Created {filepath}")

def create_company_report_pdf():
    filepath = os.path.join(DATA_DIR, 'reporte_empresa.pdf')
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, "Reporte Anual de Situación Financiera")
    c.drawString(100, 730, "Empresa Sólida S.A. de C.V.")
    c.drawString(100, 700, "Resumen Ejecutivo:")
    c.drawString(100, 680, "La empresa ha mantenido un crecimiento sostenido del 15% en ventas.")
    c.drawString(100, 660, "Los márgenes de utilidad operativa se sitúan en el 20%.")
    c.drawString(100, 640, "No se reportan litigios pendientes ni problemas laborales significativos.")
    c.drawString(100, 600, "Balance General Simplificado:")
    c.drawString(100, 580, "Activos Totales: $5,000,000 MXN")
    c.drawString(100, 560, "Pasivos Totales: $1,200,000 MXN")
    c.drawString(100, 540, "Capital Contable: $3,800,000 MXN")
    c.drawString(100, 500, "Nota del Auditor:")
    c.drawString(100, 480, "Estados financieros presentados razonablemente en todos los aspectos importantes.")
    c.save()
    print(f"Created {filepath}")

if __name__ == "__main__":
    create_credit_application()
    create_macro_data()
    create_company_report_pdf()
