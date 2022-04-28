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

#Species multiselector
species = st.multiselect('Select Species', pd.unique(everything["Species"]))
subset = subset[subset["Species"].isin(species)]

#Center multiselector, top 20, GEO and NVAL are generic labels
center = st.multiselect('Select Center', pd.unique(everything["Center"]), ['GEO', 'Wellcome Sanger Institute', 'SC', 'CDC-OAMD', 'NVAL', 'BI', 'EDLB-CDC', 'UCSDMI', 'WGSC', 'Respiratory Virus Unit, Microbiology Services Coli', 'Originating lab: Wales Specialist Virology Centre', 'Broad_GCID', 'BGI', 'PHE', 'BCM', 'IPK-Gatersleben', 'JGI', 'Leibniz Institute of Plant Genetics and Crop Plant', 'UCSD'])
subset = subset[subset["Center"].isin(center)]

#machines list: ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
#study type list: ['cDNA' 'ChIP' 'RANDOM' 'RANDOM PCR' 'unspecified' 'PCR' 'size fractionation' 'other' 'Restriction Digest' 'PolyA' 'Inverse rRNA''Oligo-dT' 'Hybrid Selection' 'RT-PCR' 'Reduced Representation''repeat fractionation' 'DNase' 'MBD2 protein methyl-CpG binding domain''MNase' 'MDA' 'RACE' 'padlock probes capture method''5-methylcytidine antibody' 'CAGE' 'ChIP-Seq']

def cumulative_monthly_counts(df):

    # initialize dfs to hold results
    Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    cumulative = pd.DataFrame(Months, columns=['Month'])
    monthly = pd.DataFrame(Months, columns=['Month'])

    # remove rows with '-' bases, convert 'Bases' column values to numeric, 
    sub_df = sub_df[pd.to_numeric(sub_df['Bases'], errors='coerce').notnull()]
    sub_df['Bases'] = sub_df['Bases'].astype('int')

    # convert 'Spots' column values to numeric, 
    sub_df['Spots'] = sub_df['Spots'].astype('int')

    # convert 'Bases' to Billions of bps by dividing by 1,000,000,000
    sub_df['Bases'] = sub_df['Bases'].div(100000000)

    # convert 'Spots' to Millions of reads by dividing by 1,000,000
    sub_df['Spots'] = sub_df['Spots'].div(100000)

    # intialize values/lists for loop
    bases_cumu_total = 0
    bases_cumulative_counts = []
    bases_monthly_counts = []

    reads_cumu_total = 0
    reads_cumulative_counts = []
    reads_monthly_counts = []
    m = 1 # month

    # loop through all months, starting with January (1)
    while m <13:
        bases_month_total = 0 # gets reinitialized with each new month
        reads_month_total = 0 # gets reinitialized with each new month
        sub_df2 = sub_df[sub_df['Month'] == m] # subset to current month

        bases_month_total = int(sub_df2['Bases'].sum()) # add up basepairs for particular month (this is a str for some reason)
        reads_month_total = int(sub_df2['Spots'].sum()) # same for reads

        bases_cumu_total += bases_month_total # add monthly total to cumulative total
        bases_cumulative_counts.append(bases_cumu_total) # append value to cumulative list
        bases_monthly_counts.append(bases_month_total) # append value to monthly list

        reads_cumu_total += reads_month_total # add monthly total to cumulative total
        reads_cumulative_counts.append(reads_cumu_total) # append value to cumulative list
        reads_monthly_counts.append(reads_month_total) # append value to monthly list

        m +=1 # increment m up, move onto next month
  
    # add lists of counts as new columns in dfs
    cumulative['Billion_Basepairs_sequenced'] = bases_cumulative_counts
    cumulative['Million_Reads_sequenced'] = reads_cumulative_counts
    monthly['Billion_Basepairs_sequenced'] = bases_monthly_counts
    monthly['Million_Reads_sequenced'] = reads_monthly_counts

    return cumulative, monthly

# call count function on subsetted df
cumulative, monthly = cumulative_monthly_counts(subset)




#Visualization
#chart = alt.Chart(subset).mark_rect().encode(
#    x=alt.X("Age", sort=ages),
#    y=alt.Y("Country"),
#    color=alt.Color("Rate",scale=alt.Scale(type='log', domain=(0.01, 1000), clamp=True), legend=alt.Legend(title="Mortality rate per 100k")),
#    tooltip=["Rate"],
#).properties(
#    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
#)
### P2.5 ###

#st.altair_chart(chart, use_container_width=True)