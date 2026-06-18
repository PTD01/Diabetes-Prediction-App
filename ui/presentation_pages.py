"""Presentation-only pages for thesis/demo (static content, no backend logic)."""

import streamlit as st


def show_about_project(lang: str) -> None:
    st.subheader("🎓 À propos du projet" if lang == "Français" else "🎓 About the Project")

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if lang == "Français":
        st.markdown(
            """
            ### Objectif
            Cette application est une **aide à la décision clinique** qui estime le risque de diabète
            à partir de huit mesures médicales courantes (glycémie, IMC, âge, etc.).

            ### Problématique
            Le diabète de type 2 est une pathologie fréquente. Un outil simple permettant d'évaluer
            rapidement un risque peut soutenir le travail du clinicien lors d'un dépistage précoce.

            ### Approche technique
            - **Dataset :** Pima Indians Diabetes (768 enregistrements)
            - **Prétraitement :** StandardScaler
            - **Modèle retenu :** Gradient Boosting (GBDT)
            - **Interface :** Application web Streamlit bilingue (FR / EN)

            ### Limites
            L'outil est **indicatif** et ne remplace pas un diagnostic médical. Il sert à la
            démonstration académique et à l'exploration de données cliniques.
            """
        )
    else:
        st.markdown(
            """
            ### Objective
            This application is a **clinical decision-support tool** that estimates diabetes risk
            from eight common medical measurements (glucose, BMI, age, etc.).

            ### Problem
            Type 2 diabetes is widespread. A simple risk assessment tool can support clinicians
            during early screening.

            ### Technical approach
            - **Dataset:** Pima Indians Diabetes (768 records)
            - **Preprocessing:** StandardScaler
            - **Selected model:** Gradient Boosting (GBDT)
            - **Interface:** Bilingual Streamlit web app (FR / EN)

            ### Limitations
            The tool is **informational only** and does not replace medical diagnosis. It is
            intended for academic demonstration and clinical data exploration.
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    st.markdown("### 🧪 Exemples pour la démonstration" if lang == "Français" else "### 🧪 Demo examples")
    if lang == "Français":
        st.markdown(
            """
            | Scénario | Glycémie | IMC | Âge | Résultat attendu |
            |----------|----------|-----|-----|------------------|
            | Risque élevé | 180 | 33 | 50 | Probablement diabétique |
            | Risque faible | 85 | 22 | 25 | Probablement non diabétique |

            Utilisez la page **Prédiction** pour tester ces valeurs (autres champs : valeurs par défaut).
            """
        )
    else:
        st.markdown(
            """
            | Scenario | Glucose | BMI | Age | Expected outcome |
            |----------|---------|-----|-----|------------------|
            | High risk | 180 | 33 | 50 | Likely diabetic |
            | Low risk | 85 | 22 | 25 | Likely non-diabetic |

            Use the **Prediction** page to test these values (other fields: default values).
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)


def show_researcher_info(lang: str) -> None:
    st.subheader("👨‍⚕️ Équipe de recherche" if lang == "Français" else "👨‍⚕️ Research Team")

    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    if lang == "Français":
        st.markdown(
            """
            ### Projet académique
            **Titre :** Conception et implémentation d'une plateforme de prédiction du risque de diabète

            **Domaine :** Santé numérique · Machine Learning · Aide à la décision clinique

            ### Équipe
            | Rôle | Nom |
            |------|-----|
            | Développeur / Chercheur | **Darryl MOMO** |
            | Encadrant / Médecin référent | *[À compléter pour la soutenance]* |
            | Institution | *[Hôpital / Université — à compléter]* |

            ### Contact
            - Email : darrylmomo237@gmail.com
            - LinkedIn : [Profil](https://www.linkedin.com/in/darryl-momo)
            - GitHub : [Dépôt du projet](https://github.com/Darryl237/Diabetes-Prediction-App)
            """
        )
    else:
        st.markdown(
            """
            ### Academic project
            **Title:** Design and implementation of a diabetes risk prediction platform

            **Field:** Digital health · Machine Learning · Clinical decision support

            ### Team
            | Role | Name |
            |------|------|
            | Developer / Researcher | **Darryl MOMO** |
            | Supervisor / Referring physician | *[To complete for defense]* |
            | Institution | *[Hospital / University — to complete]* |

            ### Contact
            - Email: darrylmomo237@gmail.com
            - LinkedIn: [Profile](https://www.linkedin.com/in/darryl-momo)
            - GitHub: [Project repository](https://github.com/Darryl237/Diabetes-Prediction-App)
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)
