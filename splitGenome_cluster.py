import os
import re
import time

__author__ = "niteshturaga"

"""
Script used to divide the genome of given organism into multiple
files, with overlap of a 100 nucleotides.

Nitesh Turaga
Email:nturaga1@jhmi.edu
"""

# Set working directory
os.chdir("/home/jhmi/nturaga1/BLR/data")


def length_fasta(filename):
    """
    This function gets the length of the FastA file, i.e,
    the number of nucleotides in each chromosome of the
    organisms genome
    :param filename: name of the fasta file
    """
    nucleotides = 0
    lines = 0
    with open(filename, 'rb') as f:
        next(f)
        for line in f:
            nucleotides += len(line[:-1])
            lines += 1
    return nucleotides, lines


def read_whole_genome(folder):
    """
    Get dimensions of all files in directory of fasta files
    :param folder:  the path of the fasta files for the genome
    """
    fasta_files = []
    fasta_files += [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.fa')]
    # results = []
    results = (fasta_files, map(length_fasta, fasta_files))
    return results


def create_file_name(fasta_identifier, count, path):
    """
    Creates new path name only with fasta identifiers
    :param fasta_identifier:
    :param count
    :param path
    """
    filename = re.sub(">", "", fasta_identifier) + "_" + str(count) + ".fa"
    return os.path.join(path, filename)


def split_genome(folder, overlap_size, d):
    """
    split_genome divides the whole genome of the organism into multiple
    smaller sets.
    :param folder: the path of the fasta files for the genome
    :param overlap_size: Size of the overlap
    :param d: the number of divisions of the genome with a minimum overlap of 100bp
    """
    # Make a new directory
    f_name = "BrokenGenome" + str(d)
    new_dir = os.path.join(folder, f_name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # Use read_whole_genome helper function
    genome_info = read_whole_genome(folder)
    # Path of each file , Size(characters,number of lines) information
    fasta_files, size_info = genome_info[0], genome_info[1]

    for i in xrange(len(fasta_files)):  # for each fasta file

        lines = size_info[i][1]  # number of lines in the fasta file
        break_size = int(lines/d)

        with open(fasta_files[i], 'rb') as f:
            header = next(f)  # >chrI -- fasta identifier
            genome = ""
            genome += header
            break_count = 0  # TO append in the broken genome filename
            for index, line in enumerate(f, start=1):
                if index in [break_size*i for i in range(1, d+1)]:
                    break_count += 1
                    fn = create_file_name(header.strip(), break_count, new_dir)

                    with open(fn, 'wb') as out:
                        out.write(genome)

                    g = genome.splitlines()
                    x = len(g)
                    overlap = "\n".join(g[x - 2:x])
                    assert(len(overlap)-1 == overlap_size)
                    genome = header + overlap + "\n" # reset to blank file with fasta identifier

                else:
                    genome += line
    return "Genome is Split"


def main():
    """
    Call the functions and give it the needed parameters
    """
    # test_file = "/Users/niteshturaga/Documents/BenLangmeadResearch/CE_FMIndex/data/chrI.fa"
    folder = "/home/jhmi/nturaga1/BLR/data/cElegansGenome"

    start = time.clock()
    split_genome(folder, 100, 2)
    split_genome(folder, 100, 4)
    split_genome(folder, 100, 8)
    split_genome(folder, 100, 12)
    split_genome(folder, 100, 16)
    split_genome(folder, 100, 20)
    split_genome(folder, 100, 24)
    split_genome(folder, 100, 30)
    split_genome(folder, 100, 50)
    split_genome(folder, 100, 80)
    end = time.clock()
    the_time = end-start
    print split_genome.__name__, the_time
    return


if __name__ == "__main__":
    main()




