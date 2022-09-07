import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data =load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    countries = (
        "United States of America",                            
        "Germany",                                                 
        "United Kingdom of Great Britain and Northern Ireland",    
        "India",                                                   
        "Canada",                                                  
        "France",                                                
        "Brazil",                                                
        "Spain",                                                    
        "Netherlands",                                              
        "Australia",                                                
        "Italy",                                                    
        "Poland",                                                   
        "Sweden",                                                   
        "Russian Federation",                                       
        "Switzerland"        
    )

    education = (
        "Masters's degree", 
        "Bachelor's degree", 
        "Less than a Bachelors",
        "post grad"
    )
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    experience = st.slider("Years of Experience", 0, 50,3)

    click = st.button("Calculate Salary")
    if click:
        X = np.array([[country, education,experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The Estimated Salary Is ${salary[0]:.2f}")



