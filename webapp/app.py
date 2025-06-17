import streamlit as st
import pandas as pd
from titanic.data import load_data, prepare_data, upload_data
import matplotlib.pyplot as plt
import seaborn as sns
import requests

st.title("Welcome to the Streamlit App")

st.markdown("""
# This is a simple Streamlit app.
## It serves as a template for your web application.
### You can add more content here.
- Use **Markdown** for formatting.
- Add **widgets** like buttons, sliders, and text inputs.
- Display **data** using tables and charts.
""")


amount = st.slider("Select a number", min_value=0, max_value=100, value=50)
if st.button("Click Me!") : 
    params = {"amount": amount}
    answer = requests.get(url = f"http://127.0.0.1:8000/love", params=params)
    if answer.status_code == 200:
        st.success(f"❤️ {answer.json()['love']}")

"### Add more functionality as needed."
" # Dataframe Example"

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 30, 22],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
st.dataframe(df)

@st.cache_data
def load_data_app():
    """
    Load the Titanic dataset.
    
    Returns:
        pd.DataFrame: The Titanic dataset.
    """
    print("Dataframe loaded successfully!")
    return load_data()

df = load_data_app()

st.write("### Seaborn")
f = plt.figure(figsize=(10, 6))
sns.histplot(df['Age'], kde=True, bins=30)
st.pyplot(f)

st.write("### Matplotlib")
fig, ax = plt.subplots()
ax.plot(df['Age'], df['Fare'], 'o')
st.pyplot(fig)

st.write('Plotly Express')
import plotly.express as px
fig = px.scatter(df, x='Age', y='Fare', color='Survived', title='Age vs Fare')
st.plotly_chart(fig)



st.write("### Would you survive the Titanic?")

name = st.text_input("Enter your name:", value="John Doe")
gender = st.selectbox("Select your Gender:", options=["Male", "Female", "Other"])
age = st.slider("Select your Age:", min_value=0, max_value=100, value=30)
class_ = st.selectbox("Select your Class:", options=["1st", "2nd", "3rd"])
embarked = st.selectbox("Select your Embarked Port:", options=["Cherbourg", "Queenstown", "Southampton"])
fare = st.selectbox("Select your Ticket Fare:", options=["Low", "Medium", "High"])

if st.button("Check if you would survive"):
    st.write("You would have survived the Titanic!")
    st.balloons()

