import os
import re
import time

__author__ = 'niteshturaga'

# Set working directory
os.chdir("/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/")


def run_bowtie_build(path):
    """
    Using bowtie-1.0.1, build index
    """
    bowtie_path = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/bowtie-1.0.1/"
    new_dir = "BrokenGenomeIndex"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    # Bowtie call
    inp = [f for f in os.listdir(path) if f.endswith('.fa')]
    for i in xrange(len(inp)):
        in_file = path + inp[i]
        out_file = os.path.join(new_dir, re.sub(".fa", "", inp[i])) + " > " + \
                   os.path.join(new_dir, re.sub(".fa", "", inp[i])) + ".pyout"
        bt = "" + bowtie_path + "bowtie-build" + " --ftabchars 6 " + in_file + " " + out_file
        # print "bowtie command: ", bt
        os.system(bt)

    #After running bowtie build move to bowtie indexes folder
    move_indexes = "mv " + new_dir + "/*.ebwt " + os.path.join(bowtie_path, "indexes")
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
    bowtie_path = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/bowtie-1.0.1/bowtie"
    new_dir = os.path.join("AlignFastqWithIndex")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    inp = [f for f in os.listdir(index_path) if f.startswith('chr')]
    inp = list(set([(re.sub("\.(.*)", "", f)) for f in inp]))

    for i in xrange(len(inp)):

        out_file = os.path.join(new_dir, inp[i]) + ".res"
        align = bowtie_path + " -t " + inp[i] + " " + fastq_file + " > " + out_file
        os.system(align)
    return "Aligning with bowtie index done"


def main():
    run_bowtie_build("/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/BrokenGenome24/")

    # FastQ generator is run only once
    # run_fastq_generator("/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/cElegansGenome")

    indexes_path = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/bowtie-1.0.1/indexes"
    fastq_path = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/cElegansGenome/chr_all_1.fastq"

    # TIME IT
    t0 = time.time()
    run_bowtie_align(indexes_path, fastq_path)
    print "seconds wall time", time.time() - t0

    return


if __name__ == "__main__":
    main()