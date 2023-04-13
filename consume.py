import streamlit as st
# from utils import PrepProcesor, columns
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pickle
pickled_model = pickle.load(open('model.pkl', 'rb'))
pickled_scaler = pickle.load(open('scaler.pkl', 'rb'))
st.title('Does he/she survived from Titantic? :ship:')
st.write('we gonna using the model we trained to predict if the passenger survived.')
st.subheader('Fill the form below make prediction')

form = st.form(key='my-form')

# Name
Name = form.text_input('Name')
# First feature : Pclass
Pclass = form.selectbox(
    'Passenger Class [1st = Upper,2nd = Middle,3rd = Lower]', options=[1, 2, 3])
# Second feature : Sex
sex = form.selectbox('Sex', options=['Male', 'Female'])
# Third feature : Age
Age = form.number_input('Age', min_value=1, max_value=100, value=1, step=1)
# Fourth feature : number of siblings/spouses aboard the Titanic
SibSp = form.number_input('Number of siblings/spouses aboard the Titanic',
                          min_value=0, max_value=10, value=0, step=1)
# Fifth feature : number of parents/children aboard the Titanic
Parch = form.number_input('Number of parents/children aboard the Titanic',
                          min_value=0, max_value=10, value=0, step=1)
# Sixth feature :
embarked = form.selectbox('Port of Embarkation', options=[
                          'Cherbourg', 'Queenstown', 'Southampton'])
predict = form.form_submit_button('Predict')

if predict:
    # convert sex to 0 and 1
    Sex = 0 if sex == "Male" else 1
    embarked_dict = {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2}
    Embarked = embarked_dict[embarked]
    row = [Pclass, Sex, Age, SibSp, Parch, Embarked]
    columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked']
    row_df = pd.DataFrame([row], columns=columns)
    # use transform instead of fit_transform
    normalized_row = pickled_scaler.transform(row_df.values)
    prediction = pickled_model.predict(normalized_row)
    st.subheader("Prediction Result")
    if prediction == 0:
        st.error(f'{Name} did not survive', icon="🚨")
    else:
        st.success(f'{Name} survived', icon="✅")
