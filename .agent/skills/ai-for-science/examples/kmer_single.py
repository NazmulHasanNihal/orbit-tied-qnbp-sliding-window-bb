import sys
import gzip
from collections import Counter
from pathlib import Path

def count_kmers(file_path, k=8):
    """Counts k-mers in a gzipped FASTQ file."""
    kmers = Counter()
    try:
        # Open gzipped file
        with gzip.open(file_path, "rt") as f:
            for i, line in enumerate(f):
                # FASTQ files: sequence is every 4th line
                if i % 4 == 1:
                    seq = line.strip()
                    for j in range(len(seq) - k + 1):
                        kmers[seq[j:j+k]] += 1
        return sum(kmers.values())
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python kmer_single.py <fastq_file>")
        sys.exit(1)
        
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    print(f"Processing {file_path.name}...")
    count = count_kmers(file_path)
    print(f"File: {file_path.name}, Total k-mers: {count}")

if __name__ == "__main__":
    main()
