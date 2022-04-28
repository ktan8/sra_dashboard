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
subset = everything[everything["Year"] == year]

#Species multiselector
species = st.multiselect('Select Species', pd.unique(everything["Species"]))
subset = subset[subset["Species"].isin(species)]

#Center multiselector, top 20, GEO and NVAL are generic labels
center = st.multiselect('Select Center', pd.unique(everything["Center"]), ['GEO', 'Wellcome Sanger Institute', 'SC', 'CDC-OAMD', 'NVAL', 'BI', 'EDLB-CDC', 'UCSDMI', 'WGSC', 'Respiratory Virus Unit, Microbiology Services Coli', 'Originating lab: Wales Specialist Virology Centre', 'Broad_GCID', 'BGI', 'PHE', 'BCM', 'IPK-Gatersleben', 'JGI', 'Leibniz Institute of Plant Genetics and Crop Plant', 'UCSD'])
subset = subset[subset["Center"].isin(center)]

#machines list: ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
#study type list: ['cDNA' 'ChIP' 'RANDOM' 'RANDOM PCR' 'unspecified' 'PCR' 'size fractionation' 'other' 'Restriction Digest' 'PolyA' 'Inverse rRNA''Oligo-dT' 'Hybrid Selection' 'RT-PCR' 'Reduced Representation''repeat fractionation' 'DNase' 'MBD2 protein methyl-CpG binding domain''MNase' 'MDA' 'RACE' 'padlock probes capture method''5-methylcytidine antibody' 'CAGE' 'ChIP-Seq']

### P2.3 ###
#countries = st.multiselect('Select Countries', pd.unique(df["Country"]), ['Austria', 'Germany','Iceland', 'Spain','Sweden', 'Thailand','Turkey'])
#subset = subset[subset["Country"].isin(countries)]

### P2.4 ###
# replace with st.selectbox
#cancer = st.selectbox('Select Cancer', pd.unique(df["Cancer"]))
#subset = subset[subset["Cancer"] == cancer]

#Visualization
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