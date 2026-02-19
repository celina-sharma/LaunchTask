import streamlit as st
import requests

#Config
st.set_page_config(page_title="Titanic Survival Prediction", layout="centered")
API_URL = "http://localhost:8000/predict"

st.title("Titanic Survival Prediction")
st.write("Enter passenger details and predict survival probability")

# UI Inputs
sex = st.selectbox("Sex", ["Male", "Female"])
fare = st.number_input("Fare", min_value=0.0, max_value=1000.0, value=32.2)
embarked_s = st.selectbox("Embarked from Southampton (S)", [0, 1])
embarked_q = st.selectbox("Embarked from Queenstown (Q)", [0, 1])
is_alone = st.selectbox("Is Alone", [0, 1])
age = st.number_input("Age", min_value=0, max_value=100, value=28)
sibsp = st.number_input("Siblings / Spouse aboard", min_value=0, max_value=10, value=1)
pclass = st.selectbox("Passenger Class", [1, 2, 3])

payload = {
    "Sex_male": 1 if sex == "Male" else 0,
    "Fare": fare,
    "Embarked_S": embarked_s,
    "Embarked_Q": embarked_q,
    "IsAlone": is_alone,
    "Age": age,
    "SibSp": sibsp,
    "Pclass": pclass
}

#Call FastAPI
if st.button("Predict Survival"):
    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            if result["prediction"] == 1:
                st.success(f"Survived (Probability: {round(result['probability'], 2)})")
            else:
                st.error(f"Not Survived (Probability: {round(result['probability'], 2)})")

        else:
            st.error("Prediction failed. Check FastAPI server.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
