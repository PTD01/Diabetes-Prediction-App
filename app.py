import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from utils.predict import predict_diabetes
from ui.components import (
    render_dashboard_metrics,
    render_feature_cards,
    render_input_summary,
    render_page_header,
    render_result_card,
)
from ui.theme import (
    BG,
    PRIMARY,
    SECONDARY,
    field_label,
    inject_medical_styles,
    render_disclaimer,
    render_sidebar_logo,
)
from ui.presentation_pages import (
    show_about_project,
    show_demo_guide,
    show_how_it_works,
    show_researcher_info,
)

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "assets" / "Diabetes_app_image.png"
PERF_CHART_PATH = BASE_DIR / "assets" / "PE_diabetes.jpeg"
ROC_CHART_PATH = BASE_DIR / "assets" / "roc_diabetes.jpeg"
DATA_PATH = BASE_DIR / "data" / "diabetes.csv"

# -------------------------
# CONFIGURATION GÉNÉRALE STREAMLIT
# -------------------------
st.set_page_config(
    page_title="Détection Diabète / Diabetes Detection",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_medical_styles()

# Charger les identifiants
USERNAME = st.secrets["APP_USERNAME"]
PASSWORD = st.secrets["APP_PASSWORD"]

# -------------------------
# LANGUE (sélecteur + dictionnaire)
# -------------------------
lang_options = ["Français", "English"]
selected_lang = st.sidebar.selectbox("🌐 Language / Langue", lang_options)
LANG = selected_lang

translations = {
    "login_title": {
        "Français": "🔐 Authentification requise",
        "English": "🔐 Login Required",
    },
    "username_label": {
        "Français": "Nom d'utilisateur",
        "English": "Username",
    },
    "password_label": {
        "Français": "Mot de passe",
        "English": "Password",
    },
    "login_button": {
        "Français": "Se connecter",
        "English": "Log in",
    },
    "login_failed": {
        "Français": "❌ Identifiants incorrects.",
        "English": "❌ Incorrect credentials.",
    },
}

# -------------------------
# AUTHENTIFICATION
# -------------------------
def authenticate():
    render_page_header(
        translations["login_title"][LANG],
        "Accès sécurisé à la démonstration clinique."
        if LANG == "Français"
        else "Secure access to the clinical demonstration.",
    )
    username_input = st.text_input(translations["username_label"][LANG])
    password_input = st.text_input(translations["password_label"][LANG], type="password")

    if st.button(translations["login_button"][LANG], width="stretch"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error(translations["login_failed"][LANG])


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    authenticate()
    st.stop()

# -------------------------
# TITRE / BANNIÈRE D'ACCUEIL
# -------------------------
if LANG == "Français":
    st.title("🩺 Application de Prédiction du Diabète")
else:
    st.title("🩺 Diabetes Prediction Application")

render_disclaimer(LANG)

# -------------------------
# MENU LATÉRAL DE NAVIGATION
# -------------------------
menu_options = {
    "Français": [
        "🏠 Accueil",
        "🎓 À propos du projet",
        "⚙️ Fonctionnement",
        "📋 Guide démo",
        "👨‍⚕️ Équipe de recherche",
        "🤖 Prédiction",
        "📈 Résultat",
        "💡 Recommandations",
        "📊 Explorations",
        "🏥 Performance du modèle",
        "📤 Prédictions par CSV",
        "🆘 Aide / Contact",
    ],
    "English": [
        "🏠 Home",
        "🎓 About the Project",
        "⚙️ How It Works",
        "📋 Demo Guide",
        "👨‍⚕️ Research Team",
        "🤖 Prediction",
        "📈 Result",
        "💡 Recommendations",
        "📊 Data Visualisation",
        "🏥 Model Performance",
        "📤 Bulk Predictions (CSV)",
        "🆘 Help / Contact",
    ],
}

st.sidebar.title("🧭 Navigation")
render_sidebar_logo(LOGO_PATH, LANG)

page = st.sidebar.radio(
    "Choisissez une page / Select a page",
    menu_options[LANG],
)


# -------------------------
# ROUTAGE DE PAGES
# -------------------------
def show_home():
    if LANG == "Français":
        render_page_header(
            "Tableau de bord clinique",
            "Une interface de démonstration pour explorer et présenter l'estimation du risque de diabète.",
        )
        cards = [
            ("01", "Estimation du risque", "Tester un patient à partir de huit variables cliniques.", "Disponible"),
            ("02", "Saisie patient", "Utiliser un formulaire guidé et bilingue.", "Disponible"),
            ("03", "Performance", "Présenter les résultats et courbes du modèle.", "Présentation"),
            ("04", "Test CSV", "Évaluer plusieurs lignes dans un fichier structuré.", "Disponible"),
        ]
        steps = """
        1. Ouvrez **Prédiction** et saisissez les informations du patient.
        2. Consultez **Résultat**, puis les **Recommandations**.
        3. Terminez avec la page **Performance du modèle** ou le test **CSV**.
        """
        section_title = "Comment tester la démonstration"
    else:
        render_page_header(
            "Clinical dashboard",
            "A demonstration interface for exploring and presenting diabetes risk estimation.",
        )
        cards = [
            ("01", "Risk estimation", "Test one patient using eight clinical variables.", "Available"),
            ("02", "Patient input", "Use a guided bilingual form.", "Available"),
            ("03", "Performance", "Present the model results and curves.", "Presentation"),
            ("04", "CSV testing", "Evaluate multiple rows in a structured file.", "Available"),
        ]
        steps = """
        1. Open **Prediction** and enter the patient information.
        2. Review **Result**, followed by **Recommendations**.
        3. Finish with **Model Performance** or the **CSV** test.
        """
        section_title = "How to test the demonstration"

    render_feature_cards(cards)
    st.markdown("")
    with st.container(border=True):
        st.subheader(section_title)
        st.markdown(steps)
    st.markdown("")
    render_dashboard_metrics(LANG)


def show_prediction_form():
    render_page_header(
        "Formulaire de prédiction" if LANG == "Français" else "Prediction form",
        "Renseignez les huit variables cliniques utilisées par le modèle."
        if LANG == "Français"
        else "Enter the eight clinical variables used by the model.",
    )

    threshold = st.slider(
        "Seuil de référence (affichage indicatif)"
        if LANG == "Français"
        else "Reference threshold (display only)",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.01,
    )
    st.caption(
        "ℹ️ La classification finale utilise la logique de décision par défaut du modèle entraîné. "
        "Le curseur est affiché à titre indicatif."
        if LANG == "Français"
        else "ℹ️ The final classification uses the trained model's default decision logic. "
        "The slider is shown for reference only."
    )

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Profil patient" if LANG == "Français" else "#### Patient profile")
            pregnancies = st.number_input(field_label("pregnancies", LANG), 0, 20, 1)
            age = st.number_input(field_label("age", LANG), 1, 120, 30)
            dpf = st.number_input(field_label("dpf", LANG), 0.0, 2.5, 0.5, step=0.01)
            bmi = st.number_input(field_label("bmi", LANG), 0.0, 70.0, 25.0, step=0.1)

        with col2:
            st.markdown("#### Mesures cliniques" if LANG == "Français" else "#### Clinical measurements")
            glucose = st.number_input(field_label("glucose", LANG), 0, 200, 100)
            blood_pressure = st.number_input(field_label("blood_pressure", LANG), 0, 150, 70)
            skin_thickness = st.number_input(field_label("skin_thickness", LANG), 0, 100, 20)
            insulin = st.number_input(field_label("insulin", LANG), 0, 900, 80)

        submit_button = st.form_submit_button(
            "Estimer le risque" if LANG == "Français" else "Estimate risk",
            width="stretch",
        )

    if submit_button:
        input_data = {
            "Pregnancies": pregnancies,
            "Glucose": glucose,
            "BloodPressure": blood_pressure,
            "SkinThickness": skin_thickness,
            "Insulin": insulin,
            "BMI": bmi,
            "DiabetesPedigreeFunction": dpf,
            "Age": age,
        }

        prob, prediction = predict_diabetes(input_data, threshold=threshold)

        st.session_state["last_prediction"] = prediction
        st.session_state["last_proba"] = prob
        st.session_state["last_threshold"] = threshold
        st.session_state["last_input_data"] = input_data

        st.success("✅ Prédiction effectuée !" if LANG == "Français" else "✅ Prediction completed!")
        render_result_card(LANG, prediction, prob)


def show_prediction_result():
    render_page_header(
        "Dernier résultat" if LANG == "Français" else "Latest result",
        "Retrouvez ici la dernière estimation effectuée pendant cette session."
        if LANG == "Français"
        else "Review the latest estimate made during this session.",
    )
    if "last_prediction" not in st.session_state or "last_proba" not in st.session_state:
        st.warning(
            "⚠️ Aucune prédiction n'a encore été effectuée. Veuillez remplir le formulaire."
            if LANG == "Français"
            else "⚠️ No prediction made yet. Please fill out the form."
        )
        return

    render_result_card(
        LANG,
        st.session_state["last_prediction"],
        st.session_state["last_proba"],
    )

    input_data = st.session_state.get("last_input_data")
    if input_data:
        st.subheader("Valeurs du patient" if LANG == "Français" else "Patient values")
        summary = [
            (field_label("pregnancies", LANG), input_data["Pregnancies"]),
            (field_label("glucose", LANG), input_data["Glucose"]),
            (field_label("blood_pressure", LANG), input_data["BloodPressure"]),
            (field_label("skin_thickness", LANG), input_data["SkinThickness"]),
            (field_label("insulin", LANG), input_data["Insulin"]),
            (field_label("bmi", LANG), input_data["BMI"]),
            (field_label("dpf", LANG), input_data["DiabetesPedigreeFunction"]),
            (field_label("age", LANG), input_data["Age"]),
        ]
        render_input_summary(summary)


def show_recommendations():
    render_page_header(
        "Recommandations" if LANG == "Français" else "Recommendations",
        "Conseils généraux associés au niveau de risque estimé."
        if LANG == "Français"
        else "General guidance associated with the estimated risk level.",
    )
    if "last_prediction" not in st.session_state:
        st.warning(
            "⚠️ Veuillez d'abord effectuer une prédiction pour afficher les recommandations."
            if LANG == "Français"
            else "⚠️ Please make a prediction first to display recommendations."
        )
        return

    prediction = st.session_state["last_prediction"]
    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if prediction == 1:
        if LANG == "Français":
            st.error("Le modèle indique un risque estimé élevé pour les valeurs saisies.")
            st.markdown(
                """
                **Conseils généraux :**
                - 🥗 Adoptez une alimentation équilibrée à faible indice glycémique
                - 🏃‍♂️ Faites de l'exercice régulièrement (30 min/jour)
                - 💧 Hydratez-vous correctement
                - 🚫 Réduisez les sucres rapides et les aliments transformés
                - 📅 Effectuez des contrôles réguliers chez un professionnel
                - 💊 Respectez les traitements médicaux si prescrits
                """
            )
        else:
            st.error("The model indicates a high estimated risk for the values entered.")
            st.markdown(
                """
                **General guidance:**
                - 🥗 Follow a low-glycemic balanced diet
                - 🏃‍♂️ Exercise regularly (30 min/day)
                - 💧 Stay hydrated
                - 🚫 Avoid processed and sugary foods
                - 📅 Schedule regular check-ups
                - 💊 Follow medical prescriptions if any
                """
            )
    else:
        if LANG == "Français":
            st.success("Le modèle indique un risque estimé faible pour les valeurs saisies.")
            st.markdown(
                """
                **Conseils pour conserver une bonne santé :**
                - 🥦 Mangez varié et évitez les excès de sucre
                - 🚶‍♀️ Marchez régulièrement
                - 📉 Surveillez votre poids et votre IMC
                - 🧘 Réduisez le stress
                - 🩺 Consultez votre médecin pour un suivi annuel
                """
            )
        else:
            st.success("The model indicates a low estimated risk for the values entered.")
            st.markdown(
                """
                **Tips to maintain good health:**
                - 🥦 Eat a varied diet and limit sugar
                - 🚶‍♀️ Walk regularly
                - 📉 Monitor your weight and BMI
                - 🧘 Reduce stress
                - 🩺 Visit your doctor for annual checkups
                """
            )
    st.markdown("</div>", unsafe_allow_html=True)


def show_data_viz():
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error("❌ Fichier 'diabetes.csv' introuvable dans le dossier 'data/'.")
        return

    chart_palette = [PRIMARY, SECONDARY]

    render_page_header(
        "Exploration des données" if LANG == "Français" else "Data exploration",
        "Explorez le jeu de données utilisé pour entraîner le modèle."
        if LANG == "Français"
        else "Explore the dataset used to train the model.",
    )

    st.markdown("### 📌 Distribution de la variable cible (Outcome)")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.countplot(
        data=df,
        x="Outcome",
        hue="Outcome",
        ax=ax1,
        palette=chart_palette,
        legend=False,
    )
    ax1.set_xticks(
        [0, 1],
        ["Non diabétique", "Diabétique"]
        if LANG == "Français"
        else ["Non-diabetic", "Diabetic"],
    )
    ax1.set_title("Répartition des cas" if LANG == "Français" else "Case distribution")
    ax1.set_facecolor(BG)
    fig1.patch.set_facecolor(BG)
    st.pyplot(fig1)
    plt.close(fig1)

    st.markdown("### 🔥 Corrélations entre les variables")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="GnBu", ax=ax2)
    ax2.set_title("Matrice de corrélation" if LANG == "Français" else "Correlation matrix")
    st.pyplot(fig2)
    plt.close(fig2)

    st.markdown("### 🔍 Exploration d'une variable")
    var = st.selectbox(
        "Choisissez une variable" if LANG == "Français" else "Choose a variable",
        df.columns[:-1],
    )

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.histplot(df[var], kde=True, ax=ax3, color=PRIMARY)
    ax3.set_title(f"Distribution de {var}" if LANG == "Français" else f"Distribution of {var}")
    ax3.set_facecolor(BG)
    fig3.patch.set_facecolor(BG)
    st.pyplot(fig3)
    plt.close(fig3)

    st.markdown("### 🧪 Boxplot par classe")
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sns.boxplot(
        x="Outcome",
        y=var,
        hue="Outcome",
        data=df,
        palette=chart_palette,
        legend=False,
        ax=ax4,
    )
    ax4.set_xticks(
        [0, 1],
        ["Non diabétique", "Diabétique"]
        if LANG == "Français"
        else ["Non-diabetic", "Diabetic"],
    )
    ax4.set_title(
        f"{var} selon l'état de santé" if LANG == "Français" else f"{var} by health status"
    )
    ax4.set_facecolor(BG)
    fig4.patch.set_facecolor(BG)
    st.pyplot(fig4)
    plt.close(fig4)


def show_model_performance():
    render_page_header(
        "Performance du modèle" if LANG == "Français" else "Model performance",
        "Comparaison des performances du modèle **Gradient Boosting (GBDT)** avec d'autres algorithmes."
        if LANG == "Français"
        else "Performance comparison of the **Gradient Boosting (GBDT)** model with other algorithms.",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "#### 📊 Accuracy & AUC"
            if LANG == "Français"
            else "#### 📊 Accuracy & AUC"
        )
        try:
            st.image(str(PERF_CHART_PATH), width="stretch")
        except Exception:
            st.warning("Image de performance introuvable." if LANG == "Français" else "Performance image not found.")

    with col2:
        st.markdown("#### 📈 Courbes ROC" if LANG == "Français" else "#### 📈 ROC Curves")
        try:
            st.image(str(ROC_CHART_PATH), width="stretch")
        except Exception:
            st.warning("Image ROC introuvable." if LANG == "Français" else "ROC image not found.")

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if LANG == "Français":
        st.markdown(
            """
            **Points clés :**
            - 🏆 Le modèle GBDT obtient une **ROC AUC ≈ 96 %**
            - ✅ Précision supérieure à **91 %**
            - 📌 Meilleure séparation des classes par rapport à RF et XGBoost
            """
        )
    else:
        st.markdown(
            """
            **Key highlights:**
            - 🏆 GBDT achieves **ROC AUC ≈ 96%**
            - ✅ Accuracy above **91%**
            - 📌 Strongest class separation compared to RF and XGBoost
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)


def show_bulk_prediction():
    render_page_header(
        "Prédiction en lot" if LANG == "Français" else "Bulk prediction via CSV",
        "Importez un fichier structuré avec les huit variables attendues."
        if LANG == "Français"
        else "Upload a structured file containing the eight expected variables.",
    )

    uploaded_file = st.file_uploader(
        "📁 Importez un fichier CSV avec les données des patients"
        if LANG == "Français"
        else "📁 Upload a CSV file with patient data",
        type=["csv"],
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(
                f"Erreur de lecture du fichier : {e}"
                if LANG == "Français"
                else f"Error reading file: {e}"
            )
            return

        expected_columns = [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age",
        ]
        if list(df.columns) != expected_columns:
            st.error(
                "❌ Le fichier doit contenir les colonnes exactes suivantes :"
                if LANG == "Français"
                else "❌ The file must contain the following exact columns:"
            )
            st.code(", ".join(expected_columns))
            return

        from utils.predict import scaler, model

        X_scaled = scaler.transform(df)
        predictions = model.predict(X_scaled)

        df["Prediction"] = predictions
        df["Prediction_Label"] = df["Prediction"].map(
            {
                0: "Non diabétique" if LANG == "Français" else "Non-diabetic",
                1: "Diabétique" if LANG == "Français" else "Diabetic",
            }
        )

        st.success("✅ Prédictions générées !" if LANG == "Français" else "✅ Predictions generated!")
        st.dataframe(df, width="stretch")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger les résultats" if LANG == "Français" else "📥 Download Results",
            data=csv,
            file_name="predictions_result.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "📌 Veuillez importer un fichier pour commencer."
            if LANG == "Français"
            else "📌 Please upload a file to begin."
        )


def show_help():
    render_page_header(
        "Aide et contact" if LANG == "Français" else "Help and contact",
        "Repères rapides pour utiliser l'application pendant la démonstration."
        if LANG == "Français"
        else "Quick guidance for using the application during the demonstration.",
    )

    if LANG == "Français":
        about = "Le modèle Gradient Boosting estime un risque à partir de huit variables. Son résultat reste indicatif."
        tips = [
            "Utilisez des valeurs réalistes dans le formulaire.",
            "Consultez Résultat après chaque nouvelle estimation.",
            "N'importez pas de données patients sensibles pendant la démonstration.",
        ]
    else:
        about = "The Gradient Boosting model estimates risk from eight variables. Its result remains informational."
        tips = [
            "Use realistic values in the form.",
            "Open Result after each new estimate.",
            "Do not upload sensitive patient data during the demonstration.",
        ]

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("#### Application")
            st.write(about)
            for tip in tips:
                st.markdown(f"- {tip}")
    with right:
        with st.container(border=True):
            st.markdown("#### Contact")
            st.markdown(
                "**Darryl MOMO**  \n"
                "darrylmomo237@gmail.com  \n"
                "[LinkedIn](https://www.linkedin.com/in/darryl-momo) · "
                "[GitHub](https://github.com/Darryl237/Diabetes-Prediction-App)"
            )


# -------------------------
# LOGIQUE D'AFFICHAGE DES PAGES
# -------------------------
PAGE_HANDLERS = {
    0: show_home,
    1: lambda: show_about_project(LANG),
    2: lambda: show_how_it_works(LANG),
    3: lambda: show_demo_guide(LANG),
    4: lambda: show_researcher_info(LANG),
    5: show_prediction_form,
    6: show_prediction_result,
    7: show_recommendations,
    8: show_data_viz,
    9: show_model_performance,
    10: show_bulk_prediction,
    11: show_help,
}

page_index = menu_options[LANG].index(page)
PAGE_HANDLERS[page_index]()
