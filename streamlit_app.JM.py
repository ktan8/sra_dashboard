from cgi import test
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

#define Figure A functions

def cumulative_monthly_counts(year, df):

  """Takes a year (as int) and input df. Returns 2 new dfs. The first df called "cumulative"
  has  3 columns; 1)month (Jan - Dec) and 2) cumulative basepair count throughout the year,
  and 3) cumulative read counts throughout the year. The second df called "monthly" has 3 
  columns: 1) month, 2) total bp sequenced for that individual month (not a running total 
  across the year), and 3) total reads sequenced that month (not a running total)."""

  # initialize dfs to hold results
  Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  cumulative = pd.DataFrame(Months, columns=['Month'])
  monthly = pd.DataFrame(Months, columns=['Month'])
  
  # subset df to desired year
  sub_df = df[df['Year'] == year]
  
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

# function to count unique organisms sequenced each month
def count_species(year, df):
  """ will explain later"""

  # initialize dfs to hold results
  Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  cumulative = pd.DataFrame(Months, columns=['Month'])
  monthly = pd.DataFrame(Months, columns=['Month'])

  # subset df to desired year
  sub_df = df[df['Year'] == year]

  # intialize values/lists for loop
  year_seen = [] # list of SpeciesID already seen this year, doesn't get reset
  cumu_count = 0 # doesn't get reset with each month
  month_result = []
  cumu_result =[]
  m = 1 # month

  # loop through all months, starting with January (1)
  while m <13:

    #initialize monthly stuff
    month_seen = [] # list of SpeciesID already seen this month
    month_count = 0

    # subset to current month
    sub_df2 = sub_df[sub_df['Month'] == m] 

    #loop through each value in SpeciesID
    for i in sub_df2["SpeciesID"]:
      if i not in month_seen:
        month_count += 1
        month_seen.append(i)
      if i not in year_seen:
        cumu_count +=1
        year_seen.append(i)
    
    # when done looping through all rows for that month, append count results to lists
    month_result.append(month_count)
    cumu_result.append(cumu_count)

    # increment m up, move onto next month
    m +=1 


  # add lists of counts as new columns in dfs
  cumulative['Unique_Species_Sequenced'] = cumu_result
  monthly['Unique_Species_Sequenced'] = month_result

  return cumulative, monthly

# Define Figure A user iteractive selection options

#Year slider
year = st.slider('Select Year', 2008, 2022, 2008)
#subset = everything[everything["Year"] == year]
#print(subset.Month)

# Platform multiselector
platform = st.multiselect('Select Sequencing Platform', pd.unique(everything["Machine"]))
#machines list: ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
sel1 = everything[everything['Machine'].isin(platform)]

# Center multiselector, top 20, GEO and NVAL are generic labels
top_20_centers = ['GEO', 'Wellcome Sanger Institute', 'SC', 'CDC-OAMD', 'NVAL', 'BI', 'EDLB-CDC', 'UCSDMI', 'WGSC', 'Respiratory Virus Unit, Microbiology Services Coli', 'Originating lab: Wales Specialist Virology Centre', 'Broad_GCID', 'BGI', 'PHE', 'BCM', 'IPK-Gatersleben', 'JGI', 'Leibniz Institute of Plant Genetics and Crop Plant', 'UCSD']
center = st.multiselect('Select Center', top_20_centers )
sel2 = sel1[sel1['Center'].isin(center)]

# Study Type multiselector
study = st.multiselect('Select Study Type', pd.unique(everything["HowSequenced"]))
sel3 = sel2[sel2['HowSequenced'].isin(study)]




# Figure A Visualization 

# Call Figure A functions on user selection subset
subset = cumulative_monthly_counts(year, sel3)
subset2 = count_species(year, sel3)

# PLOT

# Side-by-side plots: BASEPAIRS
chart1 =  alt.Chart(subset[0]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Billion_Basepairs_sequenced:Q"),
).properties(
    title="Cumulative Basepairs Sequenced", width=500, height=300
)


chart2 = alt.Chart(subset[1]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Billion_Basepairs_sequenced:Q"),
).properties(
    title="Basepairs Sequenced per Month", width=500, height=300
)

st.altair_chart(chart1 | chart2)



# Side-by-side plots: READS
chart3 =  alt.Chart(subset[0]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Million_Reads_sequenced:Q"),
).properties(
    title="Cumulative Reads Generated", width=500, height=300
)


chart4 = alt.Chart(subset[1]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Million_Reads_sequenced:Q"),
).properties(
    title="Reads Generated per Month", width=500, height=300
)

st.altair_chart(chart3 | chart4)


# Side-by-side plots: SPECIES
chart5 =  alt.Chart(subset2[0]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Unique_Species_Sequenced:Q"),
).properties(
    title="Cumulative Species Sequenced", width=500, height=300
)


chart6 = alt.Chart(subset2[1]).mark_bar().encode(
    x=alt.X("Month:O"),
    y=alt.Y("Unique_Species_Sequenced:Q"),
).properties(
    title="Species Sequenced per Month", width=500, height=300
)

st.altair_chart(chart5 | chart6)


# FIGURE B: rankings

# define Figure B function
def rankings(year, df):
    
  """Takes a year (as int) and input df. Returns 3 new dfs. The first df called "Centers"
  has  3 columns; 1) Center name 2) cumulative entries count throughout the year,
  and 3) Rank. The second df called "Species" is the same except the first col
  holds species names. The 3rd df called "Platforms" is also the same except the
  first column holds sequencing platform names."""

  from pandas.core.algorithms import rank
  
  # subset df to desired year
  sub_df = df[df['Year'] == year]

  # Make Centers df(based on # entries, aka # rows)
  centers_ranked = sub_df['Center'].value_counts() # count rows per center
  if len(centers_ranked) >=20:
    top_centers = centers_ranked[:20] # take top 20 if there are at least 20 options
    c_ranks = list(range(1, 20+1)) # make list of ranks to add as col later
  else:
    top_centers = centers_ranked
    c_ranks = list(range(1,len(top_centers)+1)) 
  Centers = top_centers.to_frame() # convert to df
  Centers = Centers.rename_axis("name").reset_index() # make rownames into first col
  Centers.rename(columns = {'name':'Center', 'Center':'Entries'}, inplace = True) # change col names
  Centers["Rank"] = c_ranks # add rank list as 3rd column
  

  # Make Species df (based on # entries, aka # rows)
  species_ranked = sub_df['Species'].value_counts() # count rows per center
  if len(species_ranked) >=20:
    top_species = species_ranked[:20] # take top 20 if there are at least 20 options
    s_ranks = list(range(1, 20+1)) # make list of ranks to add as col later
  else:
    top_species = species_ranked
    s_ranks = list(range(1,len(top_species)+1)) 
  Species = top_species.to_frame() # convert to df
  Species = Species.rename_axis("name").reset_index() # make rownames into first col
  Species.rename(columns = {'name':'Species', 'Species':'Entries'}, inplace = True) # change col names
  Species["Rank"] = s_ranks # add rank list as 3rd column
  

  # Make Platform df (based on # entries, aka # rows)
  platforms_ranked = sub_df['Machine'].value_counts() # count rows per center
  if len(platforms_ranked) >=20:
    top_platforms = platforms_ranked[:20] # take top 20 if there are at least 20 options
    p_ranks = list(range(1, 20+1)) # make list of ranks to add as col later
  else:
    top_platforms = platforms_ranked # take however many there are
    p_ranks = list(range(1,len(top_platforms)+1)) # make rank list to match lenth
  Platforms = top_platforms.to_frame() # convert to df
  Platforms = Platforms.rename_axis("name").reset_index() # make rownames into first col
  Platforms.rename(columns = {'name':'Platform', 'Machine':'Entries'}, inplace = True) # change col names
  Platforms["Rank"] = p_ranks # add rank list as 3rd column

  return Centers, Species, Platforms


# set Figure B year slider

figB_year = st.slider('Select Year', 2008, 2022, 2008)

# Figure B Visualization

# call rankings function
ranks = rankings(figB_year, everything)

# PLOT

# Top Centers
chart7 =  alt.Chart(rankings[0]).mark_bar().encode(
    x=alt.X("Center:O"),
    y=alt.Y("Entries:Q"),
).properties(
    title="Top Centers by Entries", width=500, height=300
)

st.altair_chart(chart7)

# Top Species
chart8 =  alt.Chart(rankings[1]).mark_bar().encode(
    x=alt.X("Species:O"),
    y=alt.Y("Entries:Q"),
).properties(
    title="Top Species by Entries", width=500, height=300
)

st.altair_chart(chart8)

# Top Platforms
chart9 =  alt.Chart(rankings[2]).mark_bar().encode(
    x=alt.X("Platform:O"),
    y=alt.Y("Entries:Q"),
).properties(
    title="Top Platforms by Entries", width=500, height=300
)

st.altair_chart(chart9)


