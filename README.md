# En construcción

## Propuesta de estructura inicial del proyecto:

```bash
computer_vision_G5/
├── backend/               # Código backend (API, DB, lógica del modelo)
│   ├── app/
│   │   ├── routes/        # Endpoints
│   │   ├── services/      # Lógica del modelo, base de datos
│   │   └── utils/         # Funciones auxiliares
│   ├── models/            # Modelos entrenados (en gitignore)
│   └── main.py
│
├── frontend/              # Código frontend (Streamlit, Gradio, Next.js, etc.)
│
├── data/                  # Dataset de imágenes y vídeos (en gitignore)
│   ├── raw/
│   ├── processed/
│   └── annotations/
│
├── notebooks/             # Pruebas, EDA, prototipos
│
├── reports/               # Resultados, gráficos, informes
│
├── tests/                 # Tests unitarios o de integración
│
├── requirements.txt
└── README.md
```
