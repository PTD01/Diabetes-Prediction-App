import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from utils.predict import predict_diabetes
from PIL import Image

from ui.theme import (
    ACCENT_BG,
    BG,
    PRIMARY,
    SECONDARY,
    field_label,
    inject_medical_styles,
    render_dashboard_metrics,
    render_disclaimer,
    render_result_card,
    render_sidebar_logo,
)
from ui.presentation_pages import show_about_project, show_researcher_info

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
    st.markdown(
        f'<div class="medical-card" style="max-width: 480px; margin: 2rem auto; background-color: {ACCENT_BG};">',
        unsafe_allow_html=True,
    )
    st.title(translations["login_title"][LANG])
    username_input = st.text_input(translations["username_label"][LANG])
    password_input = st.text_input(translations["password_label"][LANG], type="password")

    if st.button(translations["login_button"][LANG], use_container_width=True):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error(translations["login_failed"][LANG])
    st.markdown("</div>", unsafe_allow_html=True)


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
    render_dashboard_metrics(LANG)
    st.markdown("")

    col_img, col_text = st.columns([1, 2])

    with col_img:
        try:
            logo = Image.open(LOGO_PATH)
            st.image(logo, width=110)
        except FileNotFoundError:
            st.warning("Logo non chargé." if LANG == "Français" else "Logo not loaded.")

    with col_text:
        if LANG == "Français":
            st.subheader("Bienvenue 👋")
            st.markdown(
                """
                Cette application a été conçue pour **prédire le risque de diabète**
                à partir de données médicales simples.

                **Parcours recommandé pour la démonstration :**
                1. 🎓 Lire la présentation du projet
                2. 🤖 Saisir les données d'un patient et lancer une prédiction
                3. 📈 Consulter le résultat et les recommandations
                4. 🏥 Présenter les performances du modèle
                """
            )
        else:
            st.subheader("Welcome 👋")
            st.markdown(
                """
                This application is designed to **predict the risk of diabetes**
                from basic medical data.

                **Suggested demo flow:**
                1. 🎓 Read the project overview
                2. 🤖 Enter patient data and run a prediction
                3. 📈 Review the result and recommendations
                4. 🏥 Present model performance
                """
            )


def show_prediction_form():
    st.subheader("🧾 Formulaire de Prédiction" if LANG == "Français" else "🧾 Prediction Form")
    st.markdown(
        "Veuillez remplir les informations médicales ci-dessous :"
        if LANG == "Français"
        else "Please fill in the medical information below:"
    )

    threshold = st.slider(
        "🔧 Seuil de décision (0 = très sensible, 1 = très précis)"
        if LANG == "Français"
        else "🔧 Decision threshold (0 = sensitive, 1 = precise)",
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

    st.markdown("---")
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            pregnancies = st.number_input(field_label("pregnancies", LANG), 0, 20, 1)
            glucose = st.number_input(field_label("glucose", LANG), 0, 200, 100)
            blood_pressure = st.number_input(field_label("blood_pressure", LANG), 0, 150, 70)
            skin_thickness = st.number_input(field_label("skin_thickness", LANG), 0, 100, 20)

        with col2:
            insulin = st.number_input(field_label("insulin", LANG), 0, 900, 80)
            bmi = st.number_input(field_label("bmi", LANG), 0.0, 70.0, 25.0, step=0.1)
            dpf = st.number_input(field_label("dpf", LANG), 0.0, 2.5, 0.5, step=0.01)
            age = st.number_input(field_label("age", LANG), 1, 120, 30)

        submit_button = st.form_submit_button(
            "🔍 Prédire" if LANG == "Français" else "🔍 Predict",
            use_container_width=True,
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

        st.success("✅ Prédiction effectuée !" if LANG == "Français" else "✅ Prediction completed!")
        render_result_card(LANG, prediction, prob)


def show_prediction_result():
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


def show_recommendations():
    if "last_prediction" not in st.session_state:
        st.warning(
            "⚠️ Veuillez d'abord effectuer une prédiction pour afficher les recommandations."
            if LANG == "Français"
            else "⚠️ Please make a prediction first to display recommendations."
        )
        return

    prediction = st.session_state["last_prediction"]
    st.subheader("💡 Recommandations" if LANG == "Français" else "💡 Recommendations")

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if prediction == 1:
        if LANG == "Français":
            st.error("🩺 Le patient présente un risque élevé de diabète.")
            st.markdown(
                """
                **Conseils pour la gestion du diabète :**
                - 🥗 Adoptez une alimentation équilibrée à faible indice glycémique
                - 🏃‍♂️ Faites de l'exercice régulièrement (30 min/jour)
                - 💧 Hydratez-vous correctement
                - 🚫 Réduisez les sucres rapides et les aliments transformés
                - 📅 Effectuez des contrôles réguliers chez un professionnel
                - 💊 Respectez les traitements médicaux si prescrits
                """
            )
        else:
            st.error("🩺 The patient shows a high risk of diabetes.")
            st.markdown(
                """
                **Tips for managing diabetes:**
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
            st.success("😊 Le patient semble en bonne santé.")
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
            st.success("😊 The patient appears to be healthy.")
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

    if LANG == "Français":
        st.subheader("📊 Visualisation des Données")
        st.markdown("Explorez le jeu de données utilisé pour entraîner le modèle.")
    else:
        st.subheader("📊 Data Visualisation")
        st.markdown("Explore the dataset used to train the model.")

    st.markdown("### 📌 Distribution de la variable cible (Outcome)")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x="Outcome", ax=ax1, palette=chart_palette)
    ax1.set_xticklabels(
        ["Non diabétique", "Diabétique"] if LANG == "Français" else ["Non-diabetic", "Diabetic"]
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
    sns.boxplot(x="Outcome", y=var, data=df, palette=chart_palette, ax=ax4)
    ax4.set_xticklabels(
        ["Non diabétique", "Diabétique"] if LANG == "Français" else ["Non-diabetic", "Diabetic"]
    )
    ax4.set_title(
        f"{var} selon l'état de santé" if LANG == "Français" else f"{var} by health status"
    )
    ax4.set_facecolor(BG)
    fig4.patch.set_facecolor(BG)
    st.pyplot(fig4)
    plt.close(fig4)


def show_model_performance():
    st.subheader(
        "🏥 Performance du modèle" if LANG == "Français" else "🏥 Model Performance"
    )
    st.markdown(
        "Comparaison des performances du modèle **Gradient Boosting (GBDT)** avec d'autres algorithmes."
        if LANG == "Français"
        else "Performance comparison of the **Gradient Boosting (GBDT)** model with other algorithms."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "#### 📊 Accuracy & AUC"
            if LANG == "Français"
            else "#### 📊 Accuracy & AUC"
        )
        try:
            st.image(str(PERF_CHART_PATH), use_container_width=True)
        except Exception:
            st.warning("Image de performance introuvable." if LANG == "Français" else "Performance image not found.")

    with col2:
        st.markdown("#### 📈 Courbes ROC" if LANG == "Français" else "#### 📈 ROC Curves")
        try:
            st.image(str(ROC_CHART_PATH), use_container_width=True)
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
    st.subheader("📤 Prédiction en lot" if LANG == "Français" else "📤 Bulk Prediction via CSV")

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
        st.dataframe(df, use_container_width=True)

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
    st.subheader("🆘 Aide / Contact" if LANG == "Français" else "🆘 Help / Contact")

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if LANG == "Français":
        st.markdown(
            """
            ### ℹ️ À propos de l'application
            Cette application utilise un modèle de Machine Learning (Gradient Boosting) pour prédire le **risque de diabète** à partir de données médicales simples.

            Elle n'a **pas vocation à remplacer un avis médical** et doit être utilisée à titre indicatif.

            ### 📧 Contact
            - Développeur : **Darryl MOMO**
            - Email : darrylmomo237@gmail.com
            - LinkedIn : [Voir le profil](https://www.linkedin.com/in/darryl-momo)
            - GitHub : [Accéder au dépôt](https://github.com/Darryl237/Diabetes-Prediction-App)

            ### 📝 Conseils d'utilisation
            - Utilisez des valeurs réalistes dans le formulaire
            - Exportez vos résultats pour en discuter avec un professionnel
            - Ne pas utiliser sur des données sensibles sans chiffrement
            """
        )
    else:
        st.markdown(
            """
            ### ℹ️ About this App
            This application uses a Gradient Boosting Machine Learning model to predict the **risk of diabetes** from simple medical data.

            It is **not intended to replace medical advice** and should be used for informational purposes only.

            ### 📧 Contact
            - Developer: **Darryl MOMO**
            - Email: darrylmomo237@gmail.com
            - LinkedIn: [View profile](https://www.linkedin.com/in/darryl-momo)
            - GitHub: [Access repository](https://github.com/Darryl237/Diabetes-Prediction-App)

            ### 📝 Usage Tips
            - Use realistic values in the prediction form
            - Export results to discuss with your doctor
            - Do not use on sensitive data without encryption
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# LOGIQUE D'AFFICHAGE DES PAGES
# -------------------------
PAGE_HANDLERS = {
    0: show_home,
    1: lambda: show_about_project(LANG),
    2: lambda: show_researcher_info(LANG),
    3: show_prediction_form,
    4: show_prediction_result,
    5: show_recommendations,
    6: show_data_viz,
    7: show_model_performance,
    8: show_bulk_prediction,
    9: show_help,
}

page_index = menu_options[LANG].index(page)
PAGE_HANDLERS[page_index]()
