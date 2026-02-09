# Diagrama de Arquitectura del Sistema

Este diagrama ilustra el flujo de datos desde la ingesta hasta la generación del dictamen final por el comité de IA.

```mermaid
graph TD
    %% Estilos
    classDef input fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef process fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef ai fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,stroke-dasharray: 5 5;
    classDef output fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

    subgraph "1. Fuentes de Datos (Data Layer)"
        A1[📄 Solicitud Crédito<br/>(Excel)]:::input
        A2[📈 Datos Macro<br/>(Excel)]:::input
        A3[📑 Reporte Anual<br/>(PDF)]:::input
    end

    subgraph "2. Ingesta y Procesamiento (Backend)"
        B1[Loaders (Pandas)]:::process
        B2[PDF Processor]:::process
        
        A1 --> B1
        A2 --> B1
        A3 --> B2
    end

    subgraph "3. Orquestador (Dashboard)"
        C1{{Streamlit App}}:::process
        B1 --> C1
        B2 --> C1
    end

    subgraph "4. Comité de IA (Multi-Agent System)"
        D1[🗣️ Analista A<br/>(Deepseek-r1)]:::ai
        D2[🗣️ Analista B<br/>(Gemma3)]:::ai
        D3[⚖️ Gerente Decisor<br/>(Llama3)]:::ai

        C1 -->|Contexto| D1
        C1 -->|Contexto| D2
        
        D1 -->|Opinión A| D3
        D2 -->|Opinión B| D3
        C1 -->|Datos Crudos| D3
    end

    subgraph "5. Salida (Reporting)"
        E1[📝 Reporte Ejecutivo<br/>(Markdown)]:::output
        E2[📄 Dictamen Oficial<br/>(PDF Descargable)]:::output
        
        D3 --> E1
        D3 --> E2
        E1 --> C1
    end
```

## Explicación del Flujo

1.  **Ingesta**: El sistema lee automáticamente los archivos Excel y PDF de la carpeta `data/`.
2.  **Dashboard**: La interfaz (`app.py`) presenta los datos al usuario y permite iniciar el análisis.
3.  **Comité (Fase 1)**: Se envían los datos a dos modelos "Junior" (Deepseek y Gemma) que analizan independientemente desde perspectivas numéricas y cualitativas.
4.  **Comité (Fase 2)**: El modelo "Senior" (Llama3) recibe las dos opiniones + los datos originales. Su trabajo es sintetizar, validar coherencia y tomar la decisión final.
5.  **Generación**: El veredicto final se compila en un documento PDF profesional listo para descargar.
