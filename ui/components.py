"""Small reusable display components for the Streamlit interface."""

import streamlit as st


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-intro">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards(cards: list[tuple[str, str, str, str]]) -> None:
    cols = st.columns(len(cards))
    for col, (number, title, description, status) in zip(cols, cards):
        col.markdown(
            f"""
            <div class="feature-card">
                <span class="feature-number">{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
                <span class="status-label">{status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_dashboard_metrics(lang: str) -> None:
    metrics = (
        [
            ("96 %", "ROC AUC", "Modèle GBDT"),
            ("91 % +", "Précision", "Résultat présenté"),
            ("768", "Observations", "Dataset Pima"),
            ("8", "Variables", "Entrées cliniques"),
        ]
        if lang == "Français"
        else [
            ("96%", "ROC AUC", "Presented model"),
            ("91% +", "Accuracy", "Presented result"),
            ("768", "Records", "Pima dataset"),
            ("8", "Features", "Clinical inputs"),
        ]
    )

    cols = st.columns(4)
    for col, (value, label, hint) in zip(cols, metrics):
        col.markdown(
            f"""
            <div class="medical-metric">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
                <div class="hint">{hint}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_result_card(lang: str, prediction: int, probability: float) -> None:
    high_risk = prediction == 1
    if lang == "Français":
        risk_label = "Risque estimé élevé" if high_risk else "Risque estimé faible"
        explanation = (
            "Le modèle recommande une évaluation par un professionnel de santé."
            if high_risk
            else "Le modèle n'indique pas de risque élevé pour les valeurs saisies."
        )
        probability_label = "Probabilité estimée"
        notice = "Résultat de démonstration : il ne remplace pas le jugement médical."
    else:
        risk_label = "Estimated high risk" if high_risk else "Estimated low risk"
        explanation = (
            "The model suggests an assessment by a healthcare professional."
            if high_risk
            else "The model does not indicate high risk for the values entered."
        )
        probability_label = "Estimated probability"
        notice = "Demo result: it does not replace professional medical judgment."

    risk_class = "risk-high" if high_risk else "risk-low"
    st.markdown(
        f"""
        <div class="result-card {risk_class}">
            <div>
                <span class="result-kicker">{probability_label}</span>
                <div class="result-value">{probability:.1%}</div>
            </div>
            <div class="result-summary">
                <h3>{risk_label}</h3>
                <p>{explanation}</p>
                <small>{notice}</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_summary(items: list[tuple[str, object]]) -> None:
    cols = st.columns(4)
    for index, (label, value) in enumerate(items):
        cols[index % 4].metric(label, value)
