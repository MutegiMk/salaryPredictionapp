import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

""" This function will look into the data and select country where
    the limit cutoff is not reached and group  them to a column
    called others
"""
def shorten_categories(categories, cutoff):
  categorical_map = {}
  for i in range(len(categories)):
    if categories.values[i] >= cutoff:
      categorical_map[categories.index[i]] = categories.index[i]
    else:
      categorical_map[categories.index[i]] = 'Others'
  return categorical_map

""" This function will convert years of experience
to float and remove wording
"""
def clean_experience(x):
  if x == "More than 50 years":
    return 50
  if x == 'Less than 1 year':
    return 0.5
  return float(x)

""" This function will take education column
and print just meangful names as directed
"""
def clean_education(x):
  if "Bachelor’s degree" in x:
    return "Bachelor's degree"
  if "Master’s degree" in x:
    return "Masters's degree"
  if "Professional degree" in x or "Other doctoral" in x:
    return "post grad"
  return "Less than a Bachelors"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment",axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    #drop the others column
    df = df[df['Country'] != 'Others']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""
        ### Stack Overflow DeveloperSurvey 2020
        """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Number of data from different countries""")

    st.pyplot(fig1)

    st.write("""
    #### Mean Salary Based On Country
    """)

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """#### Mean Salary Based On Experience
        """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)


