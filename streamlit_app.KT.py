import altair as alt
import pandas as pd
import streamlit as st

# Load data

@st.cache
def load_data():
    everything = pd.read_csv("https://media.githubusercontent.com/media/ktan8/sra_dashboard/main/data/data_date.csv")
    return everything
everything = load_data()

#Title
st.write("## SRA Database Explorer")

#Year slider
year = st.slider('Select Year', 2008, 2022, 2008)
subset = everything[everything["Year"] == year]

print(subset.Month)

#Species multiselector
#species = st.multiselect('Select Species', pd.unique(everything["Species"]))
#subset = subset[subset["Species"].isin(species)]

#Center multiselector, top 20, GEO and NVAL are generic labels
#center = st.multiselect('Select Center', pd.unique(everything["Center"]), ['GEO', 'Wellcome Sanger Institute', 'SC', 'CDC-OAMD', 'NVAL', 'BI', 'EDLB-CDC', 'UCSDMI', 'WGSC', 'Respiratory Virus Unit, Microbiology Services Coli', 'Originating lab: Wales Specialist Virology Centre', 'Broad_GCID', 'BGI', 'PHE', 'BCM', 'IPK-Gatersleben', 'JGI', 'Leibniz Institute of Plant Genetics and Crop Plant', 'UCSD'])
#subset = subset[subset["Center"].isin(center)]

#machines list: ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
#study type list: ['cDNA' 'ChIP' 'RANDOM' 'RANDOM PCR' 'unspecified' 'PCR' 'size fractionation' 'other' 'Restriction Digest' 'PolyA' 'Inverse rRNA''Oligo-dT' 'Hybrid Selection' 'RT-PCR' 'Reduced Representation''repeat fractionation' 'DNase' 'MBD2 protein methyl-CpG binding domain''MNase' 'MDA' 'RACE' 'padlock probes capture method''5-methylcytidine antibody' 'CAGE' 'ChIP-Seq']

#Visualization
chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("sum_spots:Q"),
).transform_aggregate(
    sum_spots='sum(Spots)',
    groupby=["Month"]
).properties(
    title="test plot"
)

st.altair_chart(chart, use_container_width=True)
