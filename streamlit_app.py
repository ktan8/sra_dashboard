import altair as alt
import pandas as pd
import streamlit as st

# Load data

@st.cache
def load_data():
    everything = pd.read_csv("https://media.githubusercontent.com/media/ktan8/sra_dashboard/main/data/data.csv")
    return everything
everything = load_data()

#Title
st.write("## SRA Database Explorer")

#Year slider
year = st.slider('Select Year', 2008, 2022, 2008)
subset = df[df["Year"] == year]

#Species multiselector? Need to change this
sex = st.radio( "Sex", ('M', 'F'))
subset = subset[subset["Sex"] == sex]

### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
#countries = [
#    "Austria",
#    "Germany",
#    "Iceland",
#   "Spain",
#    "Sweden",
#    "Thailand",
#    "Turkey",
#]
#subset = subset[subset["Country"].isin(countries)]
### P2.3 ###
countries = st.multiselect('Select Countries', pd.unique(df["Country"]), ['Austria', 'Germany','Iceland', 'Spain','Sweden', 'Thailand','Turkey'])
subset = subset[subset["Country"].isin(countries)]

### P2.4 ###
# replace with st.selectbox
cancer = st.selectbox('Select Cancer', pd.unique(df["Cancer"]))
subset = subset[subset["Cancer"] == cancer]

### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country"),
    color=alt.Color("Rate",scale=alt.Scale(type='log', domain=(0.01, 1000), clamp=True), legend=alt.Legend(title="Mortality rate per 100k")),
    tooltip=["Rate"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
