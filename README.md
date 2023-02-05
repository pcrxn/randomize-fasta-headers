# randomize-fasta-headers

A Python script to randomize the sequence header(s) of a FASTA or multi-FASTA file.
The headers of the old FASTA file will be replaced by random strings of length `x`, where the new string contains `x/3` numbers, and the remainder uppercase letters.
The length of `x` can be changed on the command-line using `-l/--length`.
A TSV file containing the old and new headers will be created in the output directory.

## Usage

- `-i/--input`: Path to a FASTA file with headers to replace.
- `-o/--outdir`: Path to directory where the new FASTA file and TSV file will be saved.
- `-l/--length`: Length of new FASTA headers to create. Default: `18`

For example, `python3 randomize-fasta-headers.py -i datadir/bacillus.fa -o outdir/ -l 23` will create a new FASTA file `outdir/bacillus.M.fa` with randomized FASTA headers of length 23, and will create a TSV file `outdir/bacillus.M.fa.tsv` with the old headers in the first column and the new headers in the second column.

## Dependencies

- python=3.11.0 
- biopython=1.80

Other Python and package versions may work but are untested.
