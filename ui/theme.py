"""Hospital-themed colors and global Streamlit styling."""

import streamlit as st
from PIL import Image

PRIMARY = "#2563EB"
SECONDARY = "#10B981"
BG = "#F8FAFC"
TEXT = "#0F172A"
MUTED = "#64748B"
CARD_BG = "#FFFFFF"
ACCENT_BG = "#E0F2FE"
BORDER = "#E2E8F0"
SIDEBAR_BG = "#F1F7FB"
DANGER = "#DC2626"

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
            :root {{
                --medical-primary: {PRIMARY};
                --medical-secondary: {SECONDARY};
                --medical-bg: {BG};
                --medical-text: {TEXT};
                --medical-muted: {MUTED};
                --medical-card: {CARD_BG};
                --medical-border: {BORDER};
            }}
            [data-testid="stAppViewContainer"] {{
                background-color: {BG};
            }}
            [data-testid="stHeader"] {{
                background: rgba(248, 250, 252, 0.88);
                border-bottom: 1px solid rgba(216, 227, 238, 0.8);
                backdrop-filter: blur(10px);
            }}
            .block-container {{
                padding-top: 1.25rem;
                padding-bottom: 2.25rem;
                max-width: 1120px;
            }}
            [data-testid="stSidebar"] {{
                background-color: {SIDEBAR_BG};
                border-right: 1px solid {BORDER};
                box-shadow: 8px 0 24px rgba(15, 23, 42, 0.04);
            }}
            [data-testid="stSidebar"]::before {{
                content: "";
                display: block;
                height: 5px;
                background-color: {PRIMARY};
            }}
            [data-testid="stSidebar"] .stRadio label {{
                font-weight: 500;
                font-size: 0.95rem;
                color: #334155;
                border-radius: 9px;
                padding: 0.35rem 0.55rem;
                transition: background-color 160ms ease, color 160ms ease, transform 160ms ease;
            }}
            [data-testid="stSidebar"] .stRadio label:hover {{
                color: {PRIMARY};
                background-color: rgba(255, 255, 255, 0.72);
                transform: translateX(2px);
            }}
            [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
                color: {PRIMARY};
                background-color: {CARD_BG};
                box-shadow: 0 4px 14px rgba(37, 99, 235, 0.10);
            }}
            .medical-disclaimer {{
                background-color: {ACCENT_BG};
                border-left: 4px solid {PRIMARY};
                border-radius: 8px;
                padding: 0.9rem 1.2rem;
                margin-bottom: 1.5rem;
                color: {TEXT};
                font-size: 1rem;
                box-shadow: 0 4px 16px rgba(37, 99, 235, 0.06);
            }}
            .medical-card {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-top: 3px solid {PRIMARY};
                border-radius: 12px;
                padding: 1.35rem 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .medical-card:empty {{
                display: none;
            }}
            .medical-card h3 {{
                color: {PRIMARY};
                margin-top: 0;
                margin-bottom: 0.85rem;
                font-size: 1.35rem;
            }}
            .page-intro {{
                margin: 0.25rem 0 1.35rem;
            }}
            .page-intro h2 {{
                margin: 0 0 0.35rem;
                color: {TEXT};
                font-size: 1.55rem;
            }}
            .page-intro p {{
                margin: 0;
                color: {MUTED};
                font-size: 1rem;
                max-width: 760px;
            }}
            .feature-card {{
                display: flex;
                flex-direction: column;
                min-height: 148px;
                height: 100%;
                padding: 1.1rem 1.15rem;
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .feature-number {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 26px;
                height: 26px;
                border-radius: 7px;
                background-color: {ACCENT_BG};
                color: {PRIMARY};
                font-weight: 700;
                font-size: 0.82rem;
            }}
            .feature-card h3 {{
                margin: 0.7rem 0 0.35rem;
                color: {TEXT};
                font-size: 1rem;
            }}
            .feature-card p {{
                margin: 0 0 0.85rem;
                color: {MUTED};
                font-size: 0.88rem;
                line-height: 1.45;
            }}
            .status-label {{
                display: inline-block;
                align-self: flex-start;
                margin-top: auto;
                padding: 0.18rem 0.5rem;
                border-radius: 999px;
                background-color: #ECFDF5;
                color: #047857;
                font-size: 0.72rem;
                font-weight: 600;
            }}
            .medical-metric {{
                background-color: {CARD_BG};
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
                border: 1px solid {BORDER};
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .result-card {{
                display: grid;
                grid-template-columns: minmax(160px, 0.7fr) 2fr;
                gap: 1.5rem;
                align-items: center;
                margin-top: 1.1rem;
                padding: 1.35rem 1.5rem;
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-left: 5px solid {SECONDARY};
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .result-card.risk-high {{
                border-left-color: {DANGER};
            }}
            .result-kicker {{
                color: {MUTED};
                font-size: 0.82rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }}
            .result-value {{
                color: {PRIMARY};
                font-size: 2.4rem;
                font-weight: 750;
                line-height: 1.1;
                margin-top: 0.25rem;
            }}
            .result-summary h3 {{
                margin: 0 0 0.35rem;
                font-size: 1.2rem;
            }}
            .result-summary p {{
                margin: 0 0 0.5rem;
                color: #334155;
            }}
            .result-summary small {{
                color: {MUTED};
            }}
            .medical-metric .value {{
                font-size: 1.8rem;
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
                border: 1px solid {BORDER};
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            [data-testid="stNumberInput"] input,
            [data-testid="stTextInput"] input,
            [data-testid="stSelectbox"] > div > div {{
                border-radius: 8px;
            }}
            [data-testid="stNumberInput"] input:focus,
            [data-testid="stTextInput"] input:focus {{
                border-color: {PRIMARY};
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
            }}
            .stButton > button,
            .stDownloadButton > button,
            [data-testid="stFormSubmitButton"] > button {{
                background-color: {PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 0.55rem 1rem;
                transition: background-color 150ms ease;
            }}
            .stButton > button:hover,
            .stDownloadButton > button:hover,
            [data-testid="stFormSubmitButton"] > button:hover {{
                background-color: #1D4ED8;
                color: white;
            }}
            [data-testid="stAlert"] {{
                border-radius: 10px;
                border: 1px solid {BORDER};
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
            }}
            [data-testid="stDataFrame"],
            [data-testid="stFileUploader"] section {{
                border: 1px solid {BORDER};
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.88);
            }}
            hr {{
                border-color: {BORDER};
            }}
            h1 {{
                color: {TEXT};
                font-size: 2rem;
                letter-spacing: -0.025em;
            }}
            h2, h3 {{
                color: {TEXT};
            }}
            h1::after {{
                content: "";
                display: block;
                width: 72px;
                height: 4px;
                margin-top: 0.65rem;
                border-radius: 999px;
                background-color: {PRIMARY};
            }}
            .st-key-login_card {{
                max-width: 760px;
                margin: 8vh auto 0;
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-top: 3px solid {PRIMARY};
                border-radius: 14px;
                padding: 1.85rem 2rem 1.6rem;
                box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
            }}
            .st-key-login_card [data-testid="stImage"] {{
                display: flex;
                justify-content: flex-start;
            }}
            .st-key-login_card [data-testid="stImage"] img {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 14px;
                padding: 8px;
            }}
            .st-key-login_card [data-testid="stColumn"]:last-child {{
                border-left: 1px solid {BORDER};
                padding-left: 1.75rem;
            }}
            .st-key-login_card [data-testid="column"]:last-child {{
                border-left: 1px solid {BORDER};
                padding-left: 1.75rem;
            }}
            .login-title {{
                font-size: 1.25rem;
                font-weight: 700;
                color: {TEXT};
                margin-top: 0.7rem;
            }}
            .login-subtitle {{
                font-size: 0.9rem;
                color: {MUTED};
                margin: 0.2rem 0 0;
            }}
            .st-key-login_card label {{
                font-weight: 500;
                font-size: 0.88rem;
                color: {TEXT};
            }}
            .st-key-login_card input {{
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }}
            .st-key-login_card [data-testid="stButton"] {{
                margin-top: 0.4rem;
            }}
            .st-key-login_card [data-testid="stButton"] button {{
                padding: 0.65rem 1rem;
                font-size: 0.97rem;
            }}
            .login-disclaimer {{
                text-align: center;
                font-size: 0.78rem;
                color: {MUTED};
                margin-top: 1.1rem;
                padding-top: 0.9rem;
                border-top: 1px solid {BORDER};
            }}
            @media (max-width: 768px) {{
                .block-container {{
                    padding-top: 1.25rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }}
                .medical-card {{
                    padding: 1.15rem;
                }}
                .medical-metric .value {{
                    font-size: 1.55rem;
                }}
                .feature-card {{
                    min-height: auto;
                    margin-bottom: 0.5rem;
                }}
                .result-card {{
                    grid-template-columns: 1fr;
                    gap: 0.9rem;
                }}
                h1 {{
                    font-size: 1.65rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(lang: str) -> None:
    if lang == "Français":
        text = (
            "<strong>Avis médical :</strong> cet outil est une aide à la décision à titre indicatif "
            "et ne remplace pas un diagnostic médical professionnel."
        )
    else:
        text = (
            "<strong>Medical notice:</strong> this tool provides decision support for informational "
            "purposes only and does not replace professional medical diagnosis."
        )
    st.markdown(f'<div class="medical-disclaimer">{text}</div>', unsafe_allow_html=True)


def render_sidebar_logo(logo_path, lang: str) -> None:
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, width=90)
    except FileNotFoundError:
        st.sidebar.warning("Logo introuvable." if lang == "Français" else "Logo not found.")
