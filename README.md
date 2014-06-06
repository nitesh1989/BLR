Code for experiment contains 3 files:

1. splitGenome.py :

   Contains the code to split genome in to d-divisions, along with other helper functions.
   
  
2. runBowtie.py

   run_bowtie_build : Builds the bowtie index and moves to bowtie/indexes
   
   run_fastq_generator : Runs mason fastq generator
   
   run_bowtie_align : Runs bowtie alignement on each of the broken genomes with the 
   		    simulated fastq

3. plotStats.R

   Plots the time time taken in R using ggplot2