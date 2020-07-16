### Metagenomic_Quast
##### QUAST results were obtained from metagenomic assembly using SPAdes and MetaSPAdes. Each microbiome (CORAL & GUT) folder contain 6 tsv files each with assembly metrics & their values as columns. Program allows user to choose which microbiome and specific QUAST metric to assess. Then the program will create a bar graph representing that metric across both tools and kmer sizes.
##### Make sure the directory path is the path where CORAL and GUT folders are located. Ex: /Users/punitsundar/Documents/Metagenomic_Data

Example of output:
number of contigs (bp >= 0) |  number of contigs
:-------------------------:|:-------------------------:
<img width="375" alt="no_contigs_0" src="https://user-images.githubusercontent.com/30707159/87715414-29c94480-c762-11ea-8462-b27ad6e1e798.png"> | <img width="369" alt="no_contigs_only" src="https://user-images.githubusercontent.com/30707159/87715432-3188e900-c762-11ea-9ca0-e9e4cac24420.png">
