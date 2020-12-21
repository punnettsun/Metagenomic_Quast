# Program: Evaluate_QUAST_Results
# Author: Punit Sundar
# Last Updated: December 21, 2020
# Description: Gut sample reads and Australian coral sample reads were assembled using SPAdes and MetaSPAdes 
#              after trimming. QUAST results were generated for kmer sizes 21, 33 and 55 for both SPAdes and 
#              MetaSPAdes. Program compiles all 6 TSV files (3 from SPAdes & 3 from MetaSPAdes for GUT or CORAL 
#              data) into one CSV file. This CSV file will be located inside the CORAL or GUT folder. Program then
#              provides bar graphs using the compiled CSV file for various QUAST metrics that the user can choose 
#              from to assess.

# Suggested input when running program:
# First input: CORAL
# Second input: *Provide full path to CORAL & GUT data folders* EX: /Users/punitsundar/Documents/Metagenomic_Quast/Metagenomic_Data
# Third input: 0
# *Check CORAL or GUT folder to examine generated CSV file*


# Bug FIX
# 1. Make sure all metrics match for QUAST results

import os
import pandas as pd
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt

class AnalyzeQUASTMetrics(object):
    
    def __init__(self):
        """ Microbiome, directory, number of tools, and which tools used are asked from user """
        
        try:
            self.microbiome = input("Which microbiome data do you want to compile results for (CORAL or GUT)?: ").upper() 
            self.directory = input("Full path to where CORAL and GUT folders are located in your computer: ")
        except FileNotFoundError:
            print("ERROR!:\nFile or directory does not exist. Recheck your directory path and try again.")
            # /Users/punitsundar/Documents/Metagenomic_Data
        self.no_of_tools = 2
        self.tools_list = ["MetaSPAdes","SPAdes"]
    
        
    
    def create_CSV(self):
        """ Combines all .tsv files from one microbiome (CORAL or GUT) folder into one CSV file """
        
        new_data_frame = pd.DataFrame() # New dataframe to add columns to from .tsv files
        
        for tool in self.tools_list: # 'MetaSPAdes'
            full_path = self.directory + "/" + self.microbiome + "/" + tool 
            # /Users/punitsundar/Documents/Metagenomic_Data/CORAL/MetaSPAdes
            os.chdir(full_path) 
            list_all_files = os.listdir(full_path) #MetaSPAdes_K21.tsv,MetaSPAdes_K33.tsv,etc.
            
            for filename in list_all_files: 
                if filename.endswith(".tsv"): 
                    length = len(filename)
                    mod_filename = filename[:length-4] # Remove the .tsv part of file name
                    my_file = pd.read_csv(filename,sep='\t',header=0, names=['Assembly Metrics',mod_filename])
                    new_data_frame[['Assembly Metrics']] = my_file[['Assembly Metrics']] 
                    new_data_frame[[mod_filename]] = my_file[[mod_filename]] # Adds column to the new data frame
        
        os.chdir(self.directory + "/" + self.microbiome) # changes directory to specific microbiome folder 
        new_data_frame.to_csv(self.microbiome + '_tool_results.csv',sep=',',index='FALSE') # Makes compiled CSV file
        
        print()
        print("Program has successfully created a CSV file for " + self.microbiome + " in the" + self.directory\
              + "/" + self.microbiome, "folder")



    def compare_single_metric(self, which_microbiome):
        """ Compares a single assembly metric from a microbiome (CORAL or GUT) data to compare tools and kmer sizes. """

        csv_directory = self.directory + "/" + self.microbiome + "/" + which_microbiome.upper()+"_tool_results.csv"
        
        try:
            all_metrics = pd.read_csv(csv_directory)
    
        except FileNotFoundError:
            print()
            print('ERROR in compare_single_metric method!:')
            print('Program trying to open a file that does not exist. Make sure the CSV file for ' \
                  + which_microbiome + ' is created prior to using the compare_single_metric method.')
                
        else:
            print()
            list_all_metrics = list(all_metrics['Assembly Metrics']) # # contigs, Duplication ratio, etc.
            list_all_metrics_dict = {}
            
            for i in range(len(list_all_metrics)): # 0
                list_all_metrics_dict[list_all_metrics[i]] = i # associates number with metric
                
            for metric in list_all_metrics_dict:
                print(metric, "--------------", list_all_metrics_dict[metric])

            try:
                num_choice = int(input("Type in the number associated with the metric you want to assess \
                                           from the dictionary above (0 suggested): "))
            except ValueError:
                print("Invalid number choice. Try again.")
            else:
                
                for key in list_all_metrics_dict:
                    if list_all_metrics_dict[key] == num_choice:
                        metric_choice = key
                    
                pd.set_option('display.expand_frame_repr', False)
                row = DataFrame(all_metrics.loc[all_metrics['Assembly Metrics']==metric_choice])
                columns = [column for column in all_metrics][2:]
                list_row_values = [row[tool_kmer].values for tool_kmer in columns]
            
                try:
                    row_values = [int(num) for value in list_row_values for num in value]
                except ValueError:
                    print("Insufficient data. This metric is not complete to assess. Try again with another metric.")
                else:
                    Data = {'Tool/kmer':columns, metric_choice: row_values}
                    df = DataFrame(Data, columns = ['Tool/kmer',metric_choice])
                    df.plot(x = 'Tool/kmer', y = metric_choice, kind = 'bar')
                    plt.show()
                        


if __name__=="__main__":
    try1 = AnalyzeQUASTMetrics()
    try1.create_CSV()
    try1.compare_single_metric('CORAL') # Should change to 'GUT' if assessing GUT results 

