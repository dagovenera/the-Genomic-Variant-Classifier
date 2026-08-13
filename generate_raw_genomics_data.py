import numpy as np
import pandas as pd

print("🧬 Initializing VCF Data Simulator (Target: 3,000 Records)...")

num_records = 3000
np.random.seed(42) #for reproducible results

# 1. Human Genome Mapping Matrix (Chromosomes & Base-Pair Ranges)
gene_reference = {
    "MTHFR": {"chrom": "1",  "start": 11785721,  "end": 11806102},
    "EGFR":  {"chrom": "7",  "start": 55115566,  "end": 55324313},
    "CFTR":  {"chrom": "7",  "start": 117465784, "end": 117680153},
    "KRAS":  {"chrom": "12", "start": 25205166,  "end": 25250436},
    "TP53":  {"chrom": "17", "start": 7661779,   "end": 7687550},
    "BRCA1": {"chrom": "17", "start": 43044295,  "end": 43125483},
    "APOE":  {"chrom": "19", "start": 44905791,  "end": 44909393},
    "ALDH2": {"chrom": "12", "start": 111766890, "end": 111817532}
}

gene_list = list(gene_reference.keys())

# 2. Simulate genetic attributes and clinical significance
simulated_genes = np.random.choice(gene_list, num_records)
alleles = ["A", "C", "G", "T", "."]
significances = ["Benign", "Pathogenic", "Drug-Resistant"]
filters = ['PASS', 'LowQual', 'q20', 'STRAND_BIAS']

# 3. Write out VCF format layout
output_path = "raw_genetic_variants.txt"
with open(output_path, "w") as f:
    # Standard VCF Metadata Headers
    f.write("##fileformat=VCFv4.2\n")
    f.write("##fileDate=20260810\n")
    f.write("##source=Synthetic_HighThroughput_Generator\n")
    f.write("##INFO=<ID=GENE,Number=1,Type=String,Description=\"Gene Symbol\">\n")
    f.write("##INFO=<ID=SIG,Number=1,Type=String,Description=\"Clinical Significance Tag\">\n")
    # Standard VCF Column Header Row
    f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    
    for i in range(num_records):
        gene = simulated_genes[i]
        chrom = gene_reference[gene]["chrom"]
        
        # Pick a base-pair position within the gene's boundaries
        pos = np.random.randint(gene_reference[gene]["start"], gene_reference[gene]["end"])

        qual = np.random.randint(100)

        #ref allele is randomly selected from letters (not ".") in allele list
        #create list of options for alt allele: removing ref & leaving "."
        #alt allele is randomly selected from options, having 18% chance of getting "."
        ref = np.random.choice(alleles[:4])
        alt_options = alleles.copy()
        alt_options.remove(ref)
        alt = np.random.choice(alt_options, p=[0.3, 0.3, 0.3, 0.1])

        #Simulate filters with rejection rate of 20%
        filter = np.random.choice(filters, p=[0.85, 0.05, 0.05, 0.05])

        # Link clinical significance probabilities to specific genes to give ML model a pattern to learn
        if gene in ["BRCA1", "TP53", "KRAS"]:
            sig = np.random.choice(significances, p=[0.1, 0.7, 0.2])
        elif gene in ["EGFR", "CFTR"]:
            sig = np.random.choice(significances, p=[0.2, 0.2, 0.6])
        else:
            sig = np.random.choice(significances, p=[0.7, 0.2, 0.1])


        # VCF rows use INFO column for annotations like Gene names and clinical tags
        f.write(f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t{qual}\t{filter}\tGENE={gene};SIG={sig}\n")

print(f"🎉 Success! Generated {num_records} messy VCF records inside '{output_path}'")
