"""Hospital-themed Streamlit styling and reusable UI helpers."""

import streamlit as st
from PIL import Image

PRIMARY = "#2563EB"
SECONDARY = "#10B981"
BG = "#F8FAFC"
TEXT = "#0F172A"
MUTED = "#64748B"
CARD_BG = "#FFFFFF"
ACCENT_BG = "#E0F2FE"

FIELD_LABELS = {
    "pregnancies": {"Français": "Grossesses", "English": "Pregnancies"},
    "glucose": {"Français": "Glycémie (Glucose)", "English": "Glucose"},
    "blood_pressure": {"Français": "Pression artérielle", "English": "Blood Pressure"},
    "skin_thickness": {"Français": "Épaisseur de peau", "English": "Skin Thickness"},
    "insulin": {"Français": "Insuline", "English": "Insulin"},
    "bmi": {"Français": "IMC (BMI)", "English": "BMI"},
    "dpf": {"Français": "Antécédents familiaux (DPF)", "English": "Diabetes Pedigree Function"},
    "age": {"Français": "Âge", "English": "Age"},
}


def field_label(key: str, lang: str) -> str:
    return FIELD_LABELS[key][lang]


def inject_medical_styles() -> None:
    st.markdown(
        f"""
        <style>
            .block-container {{
                padding-top: 1.75rem;
                padding-bottom: 2.5rem;
                max-width: 1150px;
            }}
            [data-testid="stSidebar"] {{
                background-color: {BG};
                border-right: 1px solid #CBD5E1;
            }}
            [data-testid="stSidebar"] .stRadio label {{
                font-weight: 500;
                font-size: 0.95rem;
            }}
            .medical-disclaimer {{
                background-color: {ACCENT_BG};
                border-left: 4px solid {PRIMARY};
                border-radius: 8px;
                padding: 0.9rem 1.2rem;
                margin-bottom: 1.5rem;
                color: {TEXT};
                font-size: 1rem;
            }}
            .medical-card {{
                background-color: {CARD_BG};
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 1.5rem 1.75rem;
                margin-bottom: 1.25rem;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            }}
            .medical-card h3 {{
                color: {PRIMARY};
                margin-top: 0;
                margin-bottom: 0.85rem;
                font-size: 1.35rem;
            }}
            .medical-metric {{
                background-color: {ACCENT_BG};
                border-radius: 10px;
                padding: 1.1rem;
                text-align: center;
                border: 1px solid #BAE6FD;
            }}
            .medical-metric .value {{
                font-size: 2rem;
                font-weight: 700;
                color: {PRIMARY};
            }}
            .medical-metric .label {{
                font-size: 0.95rem;
                color: {MUTED};
                margin-top: 0.35rem;
            }}
            .medical-metric .hint {{
                font-size: 0.8rem;
                color: {MUTED};
                margin-top: 0.25rem;
            }}
            div[data-testid="stForm"] {{
                background-color: {CARD_BG};
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 1.5rem;
            }}
            .stButton > button {{
                background-color: {PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 0.6rem 1rem;
            }}
            .stButton > button:hover {{
                background-color: #1D4ED8;
                color: white;
            }}
            h1 {{
                color: {TEXT};
                font-size: 2rem;
            }}
            h2, h3 {{
                color: {TEXT};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(lang: str) -> None:
    if lang == "Français":
        text = (
            "⚕️ <strong>Avis médical :</strong> cet outil est une aide à la décision à titre indicatif "
            "et ne remplace pas un diagnostic médical professionnel."
        )
    else:
        text = (
            "⚕️ <strong>Medical notice:</strong> this tool provides decision support for informational "
            "purposes only and does not replace professional medical diagnosis."
        )
    st.markdown(f'<div class="medical-disclaimer">{text}</div>', unsafe_allow_html=True)


def render_sidebar_logo(logo_path, lang: str) -> None:
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, width=110)
    except FileNotFoundError:
        st.sidebar.warning("Logo introuvable." if lang == "Français" else "Logo not found.")


def render_result_card(lang: str, prediction: int, prob: float) -> None:
    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Résultat de la prédiction" if lang == "Français" else "### 📈 Prediction Result")

    st.markdown(
        f'<div class="medical-metric"><div class="value">{prob:.1%}</div>'
        f'<div class="label">{"Probabilité estimée de diabète" if lang == "Français" else "Estimated diabetes probability"}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    if prediction == 1:
        st.error(
            "🚨 Le modèle indique que le patient est probablement **diabétique**."
            if lang == "Français"
            else "🚨 The model suggests the patient is likely **diabetic**."
        )
    else:
        st.success(
            "✅ Le modèle indique que le patient est probablement **non diabétique**."
            if lang == "Français"
            else "✅ The model suggests the patient is likely **non-diabetic**."
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard_metrics(lang: str) -> None:
    if lang == "Français":
        metrics = [
            ("96 %", "ROC AUC", "Modèle GBDT"),
            ("91 %+", "Précision", "Jeu d'entraînement"),
            ("768", "Enregistrements", "Dataset Pima"),
            ("8", "Variables", "Entrées cliniques"),
        ]
    else:
        metrics = [
            ("96%", "ROC AUC", "GBDT model"),
            ("91%+", "Accuracy", "Training set"),
            ("768", "Records", "Pima dataset"),
            ("8", "Features", "Clinical inputs"),
        ]

    cols = st.columns(4)
    for col, (value, label, hint) in zip(cols, metrics):
        with col:
            col.markdown(
                f'<div class="medical-metric">'
                f'<div class="value">{value}</div>'
                f'<div class="label">{label}</div>'
                f'<div class="hint">{hint}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
