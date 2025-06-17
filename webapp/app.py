# Imports
import streamlit as st
import requests
import os
from loguru import logger

PORT = os.environ.get('PORT', 8000)
BACKEND_URL = os.environ.get('BACKEND_URL', f"http://localhost:{PORT}")

# Récupérer l'input de l'utilisateur
st.write("### Would you survive the Titanic?")

name = st.text_input("Enter your name:", value="John Doe")
gender = st.selectbox("Select your Gender:", options=["male", "female"])
age = st.slider("Select your Age:", min_value=0, max_value=100, value=30)
class_ = st.selectbox("Select your Class:", options=[1, 2, 3])
embarked_options = {
    "Cherbourg": "C",
    "Queenstown": "Q",
    "Southampton": "S"
}
embarked = st.selectbox("Select your Embarked Port:", options=list(embarked_options.keys()))
fare = st.slider("Select your ticket fare:", min_value=0.0, max_value=512.40, value=32.20, step=0.1)

# Quand il click sur un bouton, Faire une requête au backend
if st.button("Would you survive ?"):
    params = {
        "Name": name,   # Nom de l'utilisateur
        "Sex": gender,
        "Age": age,
        "Pclass": class_,
        "Embarked": embarked_options[embarked],
        "Fare": fare
    }
    logger.info(f"Sending request with params: {params}")
    answer = requests.get(f"{BACKEND_URL}/predict", params=params)
    logger.info(f"Received response: {answer}")
    if answer.status_code != 200:
        st.error(f"🔥 Error on prediction: {answer} 🔥")
    else:
        # En fonction de la réponse afficher survie ou non
        if answer.json()['survived']:
            st.markdown("You would have survived the Titanic!")
            for _ in range(10):
                st.balloons()
        else:
            st.markdown("💀💀💀 You are dead... 💀💀💀")
            for _ in range(10):
                st.snow()