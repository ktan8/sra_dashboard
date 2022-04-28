# Preprocess

## Download meta data from the SRA databases
We will download the required metadata from the SRA database.

`wget -b https://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/NCBI_SRA_Metadata_Full_20220319.tar.gz`
`wget -b https://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/SRA_Accessions.tab`

## Uncompress required files
The NCBI_SRA_Metadata_Full_20220319.tar.gz file contains more detailed annotations on the organisms and experimental platforms for each dataset. We will therefore extract the corresponding XML files for these datasets.

`tar -xf NCBI_SRA_Metadata_Full_20220319.tar.gz *.experiments.xml`
`tar -xf NCBI_SRA_Metadata_Full_20220319.tar.gz *.sample.xml`


## Extract organisms and experiment info from xml files
extract_experiment_xml_info.pl

`nohup bash -c "find $PWD -name "*.experiments.xml" | parallel -j 100 perl extract_experiment_xml_info.pl {} '>>' SRA.experiments.txt" &`
`nohup bash -c "find $PWD -name "*.sample.xml" | parallel -j 100 perl extract_organism_xml_info.pl {} '>>' SRA.organisms.txt" &`


## Sub-sample SRA datasets
As the SRA datasets is too big to work with and visualized in its entirety, we decided to randomly subset 5% of the full dataset. Even though we are not working with the full dataset, we expect the general temporal trends and top ranking results from the subsetted dataset to be largely concordant with the full dataset.

This was done using the following command:
`awk 'rand()<0.05' SRA_Accessions.RUN.tab >> SRA_Accessions.RUN.sample.tab`

## Merging tables
The three tables that we required was then merged into one using code in our collab notebook.


