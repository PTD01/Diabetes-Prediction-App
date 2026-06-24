"""Static pages used during the thesis presentation."""

import streamlit as st

from ui.components import render_page_header


def show_about_project(lang: str) -> None:
    if lang == "Français":
        render_page_header(
            "À propos du projet",
            "Une plateforme académique d'estimation du risque de diabète destinée à la démonstration.",
        )
        overview = {
            "Problématique": "Le dépistage précoce du diabète repose sur plusieurs indicateurs cliniques qui peuvent être difficiles à interpréter rapidement.",
            "Objectif": "Présenter une estimation du risque à partir de huit variables médicales courantes.",
            "Intérêt": "Illustrer comment le machine learning peut soutenir l'analyse de données de santé dans un cadre académique.",
            "Usage": "Tester un patient, consulter le résultat, explorer les données et présenter les performances du modèle.",
        }
        limits = "Cette application soutient une soutenance et une démonstration. Elle ne fournit pas de diagnostic clinique."
        examples_title = "Cas de démonstration"
        example_columns = ["Scénario", "Glycémie", "IMC", "Âge", "Lecture attendue"]
        example_rows = [
            ["Risque élevé", 180, 33, 50, "Risque probablement élevé"],
            ["Risque faible", 85, 22, 25, "Risque probablement faible"],
        ]
    else:
        render_page_header(
            "About the project",
            "An academic diabetes risk estimation platform designed for demonstration.",
        )
        overview = {
            "Problem": "Early diabetes screening relies on several clinical indicators that can be difficult to interpret quickly.",
            "Objective": "Present a risk estimate based on eight common medical variables.",
            "Value": "Illustrate how machine learning can support health data analysis in an academic setting.",
            "Use": "Test one patient, review the result, explore data and present model performance.",
        }
        limits = "This application supports a thesis presentation and demonstration. It does not provide a clinical diagnosis."
        examples_title = "Demonstration cases"
        example_columns = ["Scenario", "Glucose", "BMI", "Age", "Expected reading"]
        example_rows = [
            ["High risk", 180, 33, 50, "Probably higher risk"],
            ["Low risk", 85, 22, 25, "Probably lower risk"],
        ]

    cols = st.columns(2)
    for col, (title, text) in zip(cols * 2, overview.items()):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {title}")
                st.write(text)

    st.info(limits)
    st.subheader(examples_title)
    st.dataframe(
        {column: [row[index] for row in example_rows] for index, column in enumerate(example_columns)},
        width="stretch",
        hide_index=True,
    )


def show_researcher_info(lang: str) -> None:
    if lang == "Français":
        render_page_header(
            "Équipe de recherche",
            "Projet de thèse sur la prédiction du risque de diabète.",
        )
        fields = {
            "Étudiants": "David Ben Zaza, Darryl Momo",
            "Encadrants": "Pr Mve et Pr Bediang",
            "Institution": "CHUY et HGOPY",
            "Département": "Gynécologie-obstétrique",
        }
    else:
        render_page_header(
            "Research Team",
            "Thesis project on diabetes risk prediction.",
        )
        fields = {
            "Students": "David Ben Zaza, Darryl Momo",
            "Supervisors": "Pr Mve and Pr Bediang",
            "Institution": "CHUY and HGOPY",
            "Department": "Obstetrics and Gynecology",
        }

    with st.container(border=True):
        for label, value in fields.items():
            st.markdown(f"**{label} :** {value}" if lang == "Français" else f"**{label}:** {value}")


def show_how_it_works(lang: str) -> None:
    if lang == "Français":
        render_page_header(
            "Fonctionnement du système",
            "Le parcours existant, de la saisie patient à l'affichage du résultat.",
        )
        steps = [
            ("1", "Saisie", "Huit variables cliniques sont renseignées dans le formulaire."),
            ("2", "Préparation", "Les valeurs saisies sont normalisées avant l'analyse."),
            ("3", "Analyse", "Le modèle calcule le risque estimé et la probabilité."),
            ("4", "Présentation", "L'interface affiche le risque estimé et les recommandations."),
        ]
    else:
        render_page_header(
            "How the system works",
            "The existing journey from patient input to result display.",
        )
        steps = [
            ("1", "Input", "Eight clinical variables are entered in the form."),
            ("2", "Preparation", "The entered values are normalized before analysis."),
            ("3", "Analysis", "The model computes the estimated risk and probability."),
            ("4", "Presentation", "The interface displays the estimated risk and recommendations."),
        ]

    cols = st.columns(4)
    for col, (number, title, text) in zip(cols, steps):
        with col:
            with st.container(border=True):
                st.caption(f"ÉTAPE {number}" if lang == "Français" else f"STEP {number}")
                st.markdown(f"#### {title}")
                st.write(text)


def show_demo_guide(lang: str) -> None:
    if lang == "Français":
        render_page_header(
            "Guide de démonstration",
            "Un parcours court pour présenter l'application en cinq à sept minutes.",
        )
        sections = [
            ("1. Connexion", "Connectez-vous avec le compte de démonstration, puis présentez l'accueil."),
            ("2. Ouvrir Prédiction", "Accédez au formulaire principal depuis la barre latérale."),
            ("3. Saisir les valeurs", "Utilisez un cas ci-contre et conservez les autres valeurs par défaut."),
            ("4. Lancer l'estimation", "Cliquez sur Estimer le risque pour interroger le modèle existant."),
            ("5. Examiner le résultat", "Montrez la probabilité, le niveau de risque et les recommandations."),
            ("6. Présenter les données", "Ouvrez Explorations et Performance ; le test CSV est également disponible."),
        ]
        credentials = "**Utilisateur :** `admin`  \n**Mot de passe :** `daikii123`"
        talking_points = "Expliquez l'objectif académique, les huit variables, le flux de prédiction et les limites médicales."
        access_title = "Accès démo"
        talking_title = "Points à présenter"
        samples_title = "Cas d'essai"
        samples = [
            ("Risque élevé", "Glycémie 180 · IMC 33 · Âge 50"),
            ("Risque faible", "Glycémie 85 · IMC 22 · Âge 25"),
        ]
    else:
        render_page_header(
            "Demo guide",
            "A short journey for presenting the application in five to seven minutes.",
        )
        sections = [
            ("1. Login", "Sign in with the demo account, then introduce the dashboard."),
            ("2. Open Prediction", "Access the main form from the sidebar."),
            ("3. Enter values", "Use one of the sample cases and keep the other default values."),
            ("4. Run the estimate", "Select Estimate risk to query the existing model."),
            ("5. Review the result", "Show the probability, risk level and recommendations."),
            ("6. Present the data", "Open Data Visualisation and Model Performance; CSV testing is also available."),
        ]
        credentials = "**Username:** `admin`  \n**Password:** `daikii123`"
        talking_points = "Explain the academic objective, eight variables, prediction flow and medical limitations."
        access_title = "Demo access"
        talking_title = "Talking points"
        samples_title = "Sample cases"
        samples = [
            ("High risk", "Glucose 180 · BMI 33 · Age 50"),
            ("Low risk", "Glucose 85 · BMI 22 · Age 25"),
        ]

    left, right = st.columns([2, 1])
    with left:
        for title, text in sections:
            with st.container(border=True):
                st.markdown(f"#### {title}")
                st.write(text)
    with right:
        with st.container(border=True):
            st.markdown(f"#### {access_title}")
            st.markdown(credentials)
        with st.container(border=True):
            st.markdown(f"#### {talking_title}")
            st.write(talking_points)
        with st.container(border=True):
            st.markdown(f"#### {samples_title}")
            for label, values in samples:
                st.markdown(f"**{label}**  \n{values}")
