#!/usr/bin/env python

"""
randomize-fasta-headers.py

Replace the headers of a FASTA file with random letters and numbers, and create
a TSV file containing the old headers and the new headers.

Dependencies: python=3.11.0, biopython=1.80
Other package versions may work but are untested.
"""

__author__ = "Liam Brown"
__email__ = "pcrxn@proton.me"
__license__ = "MIT"

import os
import sys
import argparse
import random
import string
from Bio import SeqIO

#-------------------------------------------------------------------------------
# parse_arguments()
#-------------------------------------------------------------------------------

def parse_arguments():
    """
    Parse command-line arguments.
    :returns args: List of parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description = """
        Replace the headers of a FASTA file with random letters and numbers, and
        create a TSV file containing the old headers and the new headers.        
        """)

    # Required arguments
    required_args = parser.add_argument_group('Required')
    required_args.add_argument('-i', '--input', type = str, required = True,
        help = """
        Path to a FASTA file with headers to replace.
        """)
    required_args.add_argument('-o', '--outdir', type = str, required = True,
        help = """
        Path to directory where the new FASTA file and TSV file will be saved.
        """)

    # Optional arguments
    optional_args = parser.add_argument_group('Optional')

    optional_args.add_argument('-l', '--length', type = str,
        default = 18,
        help = """
        Length of new FASTA headers to create.
        Default: 18
        """)

    # If no arguments provided:
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

#-------------------------------------------------------------------------------
# Other functions
#-------------------------------------------------------------------------------

def randomheader(length):
    """
    Generate a random string of letters and numbers of length x, where there are
    x/3 numbers in the string.

    :param length: Length of random string to generate.
    :type length: int
    :returns new_header: Random string to be used as new FASTA header.
    :rtype new_header: str
    """
    # One-third of the length will be numbers
    num_numbers = round(length/3)
    num_letters = length - num_numbers
    letters = string.ascii_uppercase
    numbers = string.digits
    s = "".join(random.choice(letters) for i in range(num_letters)) + \
    "".join(random.choice(numbers) for i in range(num_numbers))
    new_header = "".join(random.sample(s, len(s)))

    return new_header

def parse_and_write(fasta_file, outdir, length):
    """
    Read each record in the input FASTA file line-by-line, and for each record:
    replace the old header with a new random header; write the new record to a
    new FASTA file; write the old header and new header to a new TSV file.

    :param fasta_file: Path to the input FASTA file.
    :type fasta_file: str
    :param length: Length of random string to generate.
    :type length: int
    """

    # If the input FASTA file name is "test.fa", the output name will be
    # "test.M.fa"
    outfasta_file = outdir + os.path.splitext(os.path.basename(fasta_file))[0] + '.M' + \
        os.path.splitext(os.path.basename(fasta_file))[1]

    outtsv_file = outfasta_file + ".tsv"

    # For each FASTA record:
    for record in SeqIO.parse(fasta_file, "fasta"):

        new_header = randomheader(length)
        old_header = record.id
        record.id = new_header
        record.description = ""

        # Write out new FASTA and TSV file
        with open(outfasta_file, 'a') as outfasta_handle:
            with open(outtsv_file, 'a') as outtsv_handle:
                outfasta_handle.write(record.format("fasta"))
                outtsv_handle.write(f"{old_header}\t{new_header}\n")

#-------------------------------------------------------------------------------
# main()
#-------------------------------------------------------------------------------

def main(args):
    parse_and_write(fasta_file = args.input, outdir = args.outdir, 
    length = args.length)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)