# Genomic pipeline

I have 100 FASTQ files from a sequencing run. I need to calculate the k-mer frequency (k=8) for each file to identify potential adapter contamination or sequence bias.
`kmer_serial.py` is provided to do this.

## Data download
Example subset of the E. coli dataset from the European Nucleotide Archive (https://www.ebi.ac.uk/ena/browser/view/SRR000001) can be downloaded with the following code:
```
mkdir -p data && cd data
# Downloading 3 sample files (approx 30MB each)
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR000/SRR000001/SRR000001.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR000/SRR000001/SRR000001_1.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR000/SRR000001/SRR000001_2.fastq.gz
cd ..
```
