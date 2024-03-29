from cgi import test
import altair as alt
import pandas as pd
import streamlit as st

# Set wide format for the columns
#st.set_page_config(layout="wide")

# Debugging streamlit

# Load data
@st.cache
def load_data():
    everything = pd.read_csv("https://media.githubusercontent.com/media/ktan8/sra_dashboard/main/data/data_date.csv")
    return everything
everything = load_data()

#Title
st.write("## SRA Database Explorer")




#define Figure A functions

# total number of basepairs vs time (year level, year range with 2008 as default lower bound)
def cumulative_yearly_counts(start, end, df):

  # initialize dfs to hold results
  Years = list(range(start,end+1))
  cumulative = pd.DataFrame(Years, columns=['Year'])
  yearly = pd.DataFrame(Years, columns=['Year'])

  # subset df to desired year range
  sub_df = df[df.Year.isin(Years)]

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
  bases_yearly_counts = []

  reads_cumu_total = 0
  reads_cumulative_counts = []
  reads_yearly_counts = []
  m = start # year marker

  # loop through all months, starting with January (1)
  while m <end+1:
    bases_year_total = 0 # gets reinitialized with each new year
    reads_year_total = 0 # gets reinitialized with each new year
    sub_df2 = sub_df[sub_df['Year'] == m] # subset to current year

    bases_year_total = int(sub_df2['Bases'].sum()) # add up basepairs for particular year (this is a str for some reason)
    reads_year_total = int(sub_df2['Spots'].sum()) # same for reads

    bases_cumu_total += bases_year_total # add yearly total to cumulative total
    bases_cumulative_counts.append(bases_cumu_total) # append value to cumulative list
    bases_yearly_counts.append(bases_year_total) # append value to yearly list

    reads_cumu_total += reads_year_total # add yearly total to cumulative total
    reads_cumulative_counts.append(reads_cumu_total) # append value to cumulative list
    reads_yearly_counts.append(reads_year_total) # append value to yearly list

    m +=1 # increment m up, move onto next year
  
  # add lists of counts as new columns in dfs
  cumulative['Billion_Basepairs_sequenced'] = bases_cumulative_counts
  cumulative['Million_Reads_sequenced'] = reads_cumulative_counts
  yearly['Billion_Basepairs_sequenced'] = bases_yearly_counts
  yearly['Million_Reads_sequenced'] = reads_yearly_counts

  return cumulative, yearly

# function to count unique organisms sequenced each month
def count_species_year(start, end, df):

  # initialize dfs to hold results
  Years = list(range(start,end+1))
  cumulative = pd.DataFrame(Years, columns=['Year'])
  yearly = pd.DataFrame(Years, columns=['Year'])

  # subset df to desired year range
  sub_df = df[df.Year.isin(Years)]

  # intialize values/lists for loop
  total_seen = [] # list of SpeciesID already seen total, doesn't get reset
  cumu_count = 0 # doesn't get reset with each month
  year_result = []
  cumu_result =[]
  m = start # year marker

  # loop through all years in range
  while m <end+1:

    #initialize yearly stuff
    year_seen = [] # list of SpeciesID already seen this year
    year_count = 0

    # subset to current month
    sub_df2 = sub_df[sub_df['Year'] == m] 

    #loop through each value in SpeciesID
    for i in sub_df2["SpeciesID"]:
      if i not in year_seen:
        year_count += 1
        year_seen.append(i)
      if i not in total_seen:
        cumu_count +=1
        total_seen.append(i)

    # when done looping through all rows for that year, append count results to lists
    year_result.append(year_count)
    cumu_result.append(cumu_count)

    # increment m up, move onto next year
    m +=1 

  # add lists of counts as new columns in dfs
  cumulative['Unique_Species_Sequenced'] = cumu_result
  yearly['Unique_Species_Sequenced'] = year_result

  return cumulative, yearly

########################################################
########################################################
  
  
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
  sub_df = df[df['Year'] <= year]

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


# Figure B Visualization

# call rankings function
st.header("Top 20 sequencing centers, species, and platforms")
year_ranks = st.slider('Select Year ranks', 2008, 2022, 2021)
ranks = rankings(year_ranks, everything)

# PLOT

# Top Centers
chart7 =  alt.Chart(ranks[0]).mark_bar().encode(
    y=alt.Y("Center", sort=None),
    x=alt.X("Entries:Q"),
    tooltip=["Center","Entries:Q"]
).properties(
    title="Top Centers by Entries", width=160, height=500
)



# Top Species
chart8 =  alt.Chart(ranks[1]).mark_bar().encode(
    y=alt.Y("Species", sort=None),
    x=alt.X("Entries:Q"),
    tooltip=["Species","Entries:Q"]
).properties(
    title="Top Species by Entries", width=160, height=500
)



# Top Platforms
chart9 =  alt.Chart(ranks[2]).mark_bar().encode(
    y=alt.Y("Platform", sort=None),
    x=alt.X("Entries:Q"),
    tooltip=["Platform","Entries:Q"]
).properties(
    title="Top Platforms by Entries", width=160, height=500
)

#st.altair_chart(chart7) | st.altair_chart(chart8) | st.altair_chart(chart9)


st.altair_chart(chart7 | chart8 | chart9)
  
  
  
  




##########################################################################
##########################################################################
# Define Figure A user iteractive selection options

st.header("Yearly sequencing trends for selected library preps")


#Year slider
year = st.slider('Select Year', 2008, 2022, 2015)
#subset = everything[everything["Year"] == year]
#print(subset.Month)

# Platform multiselector
all_platforms = ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
#platform = st.multiselect('Select Sequencing Platform', pd.unique(everything["Machine"]), ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS'])
#machines list: ['ILLUMINA', 'LS454', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ', 'CAPILLARY', 'HELICOS', 'COMPLETE_GENOMICS']
#sel1 = everything[everything['Machine'].isin(platform)]
sel1 = everything[everything['Machine'].isin(all_platforms)]

# Center multiselector, top 20, GEO and NVAL are generic labels
top_20_centers = ['GEO', 'Wellcome Sanger Institute', 'SC', 'CDC-OAMD', 'NVAL', 'BI', 'EDLB-CDC', 'UCSDMI', 'WGSC', 'Respiratory Virus Unit, Microbiology Services Coli', 'Originating lab: Wales Specialist Virology Centre', 'Broad_GCID', 'BGI', 'PHE', 'BCM', 'IPK-Gatersleben', 'JGI', 'Leibniz Institute of Plant Genetics and Crop Plant', 'UCSD']
#center = st.multiselect('Select Center', top_20_centers, top_20_centers)
#sel2 = sel1[sel1['Center'].isin(center)]
sel2 = sel1[sel1['Center'].isin(top_20_centers)]

# # Study Type multiselector
study = st.multiselect('Select Study Type', pd.unique(everything["HowSequenced"]), pd.unique(everything["HowSequenced"]))
sel3 = sel2[sel2['HowSequenced'].isin(study)]
#sel3 = everything[everything['HowSequenced'].isin(study)]

# Figure A Visualization 

# Call Figure A functions on user selection subset
subset = cumulative_yearly_counts(2008, year, sel3)
subset2 = count_species_year(2008, year, sel3)

# PLOT

# Side-by-side plots: BASEPAIRS
chart1 =  alt.Chart(subset[0]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Billion_Basepairs_sequenced:Q"),
    tooltip=["Year:O","Billion_Basepairs_sequenced:Q"]
).properties(
    title="Cumulative Basepairs Sequenced", width=250, height=150
)


chart2 = alt.Chart(subset[1]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Billion_Basepairs_sequenced:Q"),
    tooltip=["Year:O","Billion_Basepairs_sequenced:Q"]
).properties(
    title="Basepairs Sequenced per Year", width=250, height=150
)




# Side-by-side plots: READS
chart3 =  alt.Chart(subset[0]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Million_Reads_sequenced:Q"),
    tooltip=["Year:O","Million_Reads_sequenced:Q"]
).properties(
    title="Cumulative Reads Generated", width=250, height=150
)


chart4 = alt.Chart(subset[1]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Million_Reads_sequenced:Q"),
    tooltip=["Year:O","Million_Reads_sequenced:Q"]
).properties(
    title="Reads Generated per Year", width=250, height=150
)




# Side-by-side plots: SPECIES
chart5 =  alt.Chart(subset2[0]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Unique_Species_Sequenced:Q"),
    tooltip=["Year:O","Unique_Species_Sequenced:Q"]
).properties(
    title="Cumulative Species Sequenced", width=250, height=150
)


chart6 = alt.Chart(subset2[1]).mark_line(
    point=alt.OverlayMarkDef(color='red')
).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Unique_Species_Sequenced:Q"),
    tooltip=["Year:O","Unique_Species_Sequenced:Q"]
).properties(
    title="Species Sequenced per Year", width=250, height=150
)

st.altair_chart(chart2 | chart4 | chart6)
st.altair_chart(chart1 | chart3 | chart5)

# col1, col2, col3 = st.beta_columns((1,1,1))

# with col1:
	# chart2
# with col2:
	# chart4
# with col3:
	# chart6


#st.altair_chart(chart5 | chart6)



##########################################################################
##########################################################################




###############################
###############################


# Clean dataframe and remove runs without any spots and bases values
everything_clean = everything[everything["Bases"] != "-"]
everything_clean = everything_clean[everything_clean["Spots"] != "-"]

everything_clean["Bases"] = pd.to_numeric(everything_clean["Bases"])
everything_clean["Spots"] = pd.to_numeric(everything_clean["Spots"])

species_top1000 = everything_clean["Species"].value_counts(dropna=False)[0:100]

df1 = everything_clean.groupby(['Year', 'Species', 'Machine']).sum().reset_index()


########################
# create a drop-down cancer selector
species = species_top1000.keys().tolist()
species = species[1:len(species)] # drop the NAN value
species_dropdown = alt.binding_select(options=species)
species_select = alt.selection_single(
    # add your code here
    fields=["Species"], bind=species_dropdown, name="Species"
)

# only compare several selected platforms
platforms = ['LS454', 'ILLUMINA', 'HELICOS', 'ABI_SOLID', 'ION_TORRENT',
       'PACBIO_SMRT', 'COMPLETE_GENOMICS', 'OXFORD_NANOPORE', 'CAPILLARY',
       'BGISEQ']
df1 = df1[df1['Machine'].isin(platforms)]
df1 = df1[df1['Species'].isin(species)] # Keep only top 1000 species

########################
# create line charts
base = alt.Chart(df1
 ).mark_line().encode(
    x=alt.X('Year:Q', axis=alt.Axis(tickMinStep=1)),
    y='Bases:Q',
    color='Machine:N',
    tooltip='Machine:N'
)


########################
# add the drop-down selection to the chart (P2.1)
chart = base.add_selection(
    species_select
).transform_filter(
    species_select
).properties(
    width=600,
    height=200
)


########################
# add brush
brush = alt.selection_interval( encodings=['x'])

upper = chart.encode(
    alt.X('Year:Q', scale=alt.Scale(domain=brush), 
	axis=alt.Axis(tickMinStep=1))
)

lower = chart.properties(
    height=60
).add_selection(brush)


st.header("Yearly sequencing trends for each species")
upper & lower



#####################################################################
#####################################################################

st.header("Yearly trends in sequencing platforms used")
df2 = everything_clean.groupby(['Year', 'Machine']).sum().reset_index()
select_platforms = st.multiselect('Select Sequencing Platform', options=all_platforms, default=['ILLUMINA', 'ABI_SOLID', 'ION_TORRENT', 'PACBIO_SMRT', 'OXFORD_NANOPORE', 'BGISEQ'])
df2_filtered = df2[df2['Machine'].isin(select_platforms)]

base = alt.Chart(df2_filtered
 ).mark_line().encode(
    x='Year:O',
    y=alt.Y('Bases:Q',
        scale=alt.Scale(type="log")),
    color='Machine:N',
).properties(
    width=600,
    height=300
)

base.encoding.y.title = 'Number of bases sequenced'

spots = alt.Chart(df2_filtered
 ).mark_line().encode(
    x='Year:O',
    y=alt.Y('Spots:Q',
        scale=alt.Scale(type="log")),
    color='Machine:N',
).properties(
    width=600,
    height=300
)
spots.encoding.y.title = 'Number of reads sequenced'


base & spots
