#!/usr/bin/env perl
use strict;
use warnings;
use autodie;

# Genomic VCF Data Parser
# Extract nucleotide variant markers that pass quality controls

print "🧬 Launching Genomic Variant Extraction Engine...\n";

my $input_file  = "raw_genetic_variants.txt";
my $output_file = "clean_mutations.csv";

# Open input and output files securely
open my $in,  '<', $input_file;
open my $out, '>', $output_file;

# Print the headers for relational tabular layout on output file
print $out "Gene_ID,Chromosome,Position,Reference_Allele,Mutant_Allele,Clinical_Significance\n";

my $processed_records = 0;

while (my $line = <$in>) {
    chomp $line;
    
    # Skip standard metadata, comment headers, or space-only lines, common in genomic files
    next if $line =~ /^#/;
    next if $line =~ /^\s*$/;
    
    # Split the tab-delimited matrix of variants
    my @fields = split(/\t/, $line);

    # Skip records that do not meet quality standards
    next if ($fields[5] < 20 || $fields[6] ne "PASS");
    
    # Feature Extraction
    my $chromosome = $fields[0];
    my $position   = $fields[1];
    my $ref_allele = $fields[3];
    my $mut_allele = $fields[4];
    my $info_field = $fields[7]; # Column 8 holds "GENE=BRCA1;SIG=Pathogenic"
    
    #Filter out incomplete or unsequenced variant frames with missing allele data
    next if ($ref_allele eq '.' || $mut_allele eq '.');

    # Extract features from INFO field string
    my ($gene_id)     = $info_field =~ /GENE=([^;]+)/;
    my ($significance) = $info_field =~ /SIG=([^;]+)/;

    # Write extracted features as a row in tabular layout of output file
    print $out "$gene_id,$chromosome,$position,$ref_allele,$mut_allele,$significance\n";
    $processed_records++;
}

close $in;
close $out;

print "🎉 Perl processing complete! Successfully extracted $processed_records quality records.\n";
print "📁 Parsed data written to file: clean_mutations.csv\n";
