# ObservaTurismo Certificado – UACh CER

Dashboard web y pipeline ETL que muestran la participación y distribución de alojamientos certificados en Chile, construido para el Centro de Estudios Regionales de la Universidad Austral de Chile.

## 🎯 Objetivos del proyecto
- Normalizar y combinar las fuentes oficiales de turismo certificado mediante un ETL modular (`funds_etl`).
- Exponer indicadores ejecutivos con visualizaciones interactivas (Highcharts + Plotly) en español y con modo claro/oscuro.
- Entregar una plantilla HTML fácil de compartir (`docs/index.html`) que agrupa las visualizaciones clave.

## 🗂️ Estructura principal
```
config/                # Parámetros del ETL
data/raw/              # CSV originales
data/processed/        # Salidas del ETL (manifest + tourism_metrics)
docs/                  # Dashboard HTML+CSS y visualizaciones standalone
notebooks/             # Exploración y prototipos Plotly
scripts/run_etl.py     # Entrada principal del pipeline
src/funds_etl/         # Librería ETL (extract-transform-load modular)
tests/                 # Pytest del pipeline y extractores
```

## ⚙️ Requisitos
- Python 3.10+
- Dependencias: `pip install -r requirements.txt`
- Para desarrollo avanzado: `pip install .[dev]`

## 🚀 Cómo ejecutar
1. **Procesar datos**
   ```bash
   python scripts/run_etl.py --config config/settings.yaml
   ```
   Genera datasets limpios en `data/processed/`, incluido `tourism_metrics.csv`.

2. **Explorar resultados**
   - Abre `docs/index.html` en tu navegador (o sirve la carpeta con `python -m http.server 8000`).
   - Usa la barra de navegación para alternar entre:
     - **Participación por tipologías** (`docs/participacion_alojamientos_donut.html`)
     - **Distribución de oferta** (`docs/distribucion_alojamientos_highcharts.html`)
   - Cada visualización incluye modo claro/oscuro sin dependencias externas adicionales.

## ✨ Visualizaciones destacadas
- **Donut “Participación de tipologías”**: top 10 tipologías con leyenda externa y toggle de tema.
- **Barras “Distribución de oferta”**: 13 tipos de alojamiento con etiquetas de valor y porcentajes.
- Ambas se renderizan de forma standalone (HTML puro) y se incrustan en la plantilla principal.

## 🧪 Calidad y pruebas
- Ejecuta la batería de tests del ETL: `pytest`
- Lint opcional con Ruff: `ruff check src tests`

## 📄 Documentación adicional
- `docs/architecture.md`: diseño del pipeline.
- `notebooks/turismo_certificado_insights.ipynb`: storytelling y exploración con Plotly.

## 🤝 Créditos
Proyecto desarrollado por el equipo de Ciencia de Datos del CER-UACh para Observa Los Ríos. Las visualizaciones reutilizables y el ETL pueden adaptarse a nuevas fuentes ajustando la configuración y los transformers existentes.
