import os
import re
import time

__author__ = 'niteshturaga'
__email__ = "nturaga1@jhmi.edu"


# Set working directory
os.chdir("/home/jhmi/nturaga1/BLR/data/")


def run_bowtie_build(path):
    """
    Using bowtie-1.0.1, build index
    """
    bowtie_path = "/home/jhmi/nturaga1/BLR/bowtie-1.0.1/"
    new_dir = "BrokenGenomeIndex" + re.findall(r'\d+',path)[1]
    print new_dir
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    # Bowtie call
    inp = [f for f in os.listdir(path) if f.endswith('.fa')]
    for i in xrange(len(inp)):
        in_file = path + inp[i]
        fasta_file = os.path.join(new_dir, re.sub(".fa", "", inp[i]))
        out_file = fasta_file + " > " + \
                   fasta_file + ".out" + " 2>" + fasta_file + ".std.err"
        bt = "" + bowtie_path + "bowtie-build" + " --ftabchars 6 " + in_file + " " + out_file
        #print "bowtie command: ", bt
        os.system(bt)

    #After running bowtie build move to bowtie indexes folder
    if not os.path.exists(os.path.join(bowtie_path,"indexes",new_dir)):
        os.makedirs(os.path.join(bowtie_path,"indexes",new_dir))
    move_indexes = "mv " + new_dir + "/*.ebwt " + os.path.join(bowtie_path, "indexes",new_dir)
    #print move_indexes
    os.system(move_indexes)
    
    return "Index Built and Moved to Bowtie Index Folder"


def run_fastq_generator(genome_path):
    """
    Run mason fastq generator (Mason)
    """
    new_dir = os.path.join("RefGenomeArtificialFastq")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    # concatenate
    complete_fasta = os.path.join(genome_path, "chr_all.fasta")
    cat_call = "cat " + genome_path + "/*.fa > " + complete_fasta
    os.system(cat_call)

    #run mason
    complete_fastq = os.path.join(genome_path, "chr_all.fastq")
    mason = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/seqan-trunk-build/release/bin/mason illumina " \
            "-n 100 -N 100000 -sq -mp -o  " + complete_fastq + " " + complete_fasta

    os.system(mason)
    return "All fastQ generated"


def run_bowtie_align(index_path, fastq_file):
    """
    Run bowtie alignment with the artificially genrated fastq files
    """
    bowtie_path = "/home/jhmi/nturaga1/BLR/bowtie-1.0.1/bowtie"

    new_dir = os.path.join("AlignFastqWithIndex")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    inp = [f for f in os.listdir(index_path) if f.startswith('chr')]
    inp = list(set([(re.sub("\.(.*)", "", f)) for f in inp]))
    print inp
    for i in xrange(len(inp)):
        name = os.path.join(new_dir, inp[i])
        out_file = name + ".res" + " 2> " + name + ".std.err"
        align = bowtie_path + " -t " + os.path.join(index_path,inp[i]) + " " + fastq_file + " > " + out_file
#        print align
        os.system(align)
    return "Aligning with bowtie index done"


def main():
    run_bowtie_build("/home/jhmi/nturaga1/BLR/data/cElegansGenome/BrokenGenome4/")

    # FastQ generator is run only once
    # run_fastq_generator("/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/cElegansGenome")

    indexes_path = "/home/jhmi/nturaga1/BLR/bowtie-1.0.1/indexes/BrokenGenomeIndex4"
    fastq_path = "/home/jhmi/nturaga1/BLR/data/cElegansGenome/chr_all_1.fastq"

    # TIME IT
    t0 = time.time()
    run_bowtie_align(indexes_path, fastq_path)
    print indexes_path
    print "seconds wall time", time.time() - t0

    return


if __name__ == "__main__":
    main()
