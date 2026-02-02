import pandas as pd
import json

class DataLoader:
    @staticmethod
    def load_credit_application(filepath):
        """
        Reads the credit application Excel file.
        Expected format: Two columns 'Campo' and 'Valor'.
        Returns a dictionary of the application data.
        """
        try:
            df = pd.read_excel(filepath)
            # Normalize column names just in case
            df.columns = [c.strip() for c in df.columns]
            
            # Convert to dictionary (Campo -> Valor)
            # Assuming the excel has key-value pairs structure
            if 'Campo' in df.columns and 'Valor' in df.columns:
                return dict(zip(df['Campo'], df['Valor']))
            else:
                # Fallback: return record list
                return df.to_dict(orient='records')
        except Exception as e:
            return {"error": f"Failed to load credit application: {str(e)}"}

    @staticmethod
    def load_macro_data(filepath):
        """
        Reads the macroeconomic data Excel file.
        Returns a string representation (markdown table) for the prompt.
        """
        try:
            df = pd.read_excel(filepath)
            return df.to_markdown(index=False)
        except Exception as e:
            return f"Error loading macro data: {str(e)}"
