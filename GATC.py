#!/usr/bin/env python3

from Bio import SeqIO
from datetime import datetime

def log(msg):
    """Print a message with a timestamp for debugging."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Input FASTA (GRCh38)
fasta_file = "/mnt/bioadhoc/Groups/RaoLab/wzhao/reference_genome/GCF_000001405.40_GRCh38.p14_genomic.fna"

# Output bedGraph file
bedgraph_file = "/mnt/bioadhoc/Groups/RaoLab/wzhao/reference_genome/A_GATC.bedGraph"

# The motif we are looking for
motif = "GATC"

def find_motif_in_sequence(seq, motif):
    """
    Generator function that yields the start indices of all 
    occurrences of 'motif' in 'seq' (both are strings).
    """
    start = 0
    while True:
        index = seq.find(motif, start)
        if index == -1:
            break
        yield index
        start = index + 1

def main():
    """
    1) Parse FASTA
    2) Find GATC
    3) Write bedGraph lines for the 'A' position in GATC with score=1
    """
    log("Opening bedGraph output file...")
    with open(bedgraph_file, "w") as bg:
        bg.write(f"track type=bedGraph name='A_in_GATC' description='Positions of A in GATC' visibility=2\n")
        
        log(f"Parsing FASTA: {fasta_file}")
        total_hits = 0
        
        for record in SeqIO.parse(fasta_file, "fasta"):
            chr_id = record.id
            seq_str = str(record.seq)
            length_chr = len(seq_str)
            
            if length_chr < 4:
                # No GATC possible in sequences shorter than 4
                continue
            
            # Find all 'A' positions in GATC
            a_positions = []
            for motif_start in find_motif_in_sequence(seq_str, motif):
                # 'A' is at motif_start+1 (0-based)
                a_pos = motif_start + 1
                a_positions.append(a_pos)
            
            # Write each position to bedGraph as a 1 bp region with a score of 1.
            # bedGraph is 0-based, half-open, so we do [start, start+1) for a single base.
            for pos in a_positions:
                # Safeguard: ensure pos+1 <= length of the chromosome
                if pos >= 0 and pos < length_chr:
                    # Format: chrom, start, end, value
                    # Example: chr1  100  101  1
                    bg.write(f"{chr_id}\t{pos}\t{pos+1}\t1\n")
            
            total_hits += len(a_positions)
            log(f"{chr_id}: wrote {len(a_positions)} bedGraph lines.")
        
        log(f"Finished writing bedGraph. Total 'A in GATC' positions: {total_hits}")
        log(f"bedGraph file: {bedgraph_file}")

if __name__ == "__main__":
    main()

