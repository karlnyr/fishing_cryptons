/proj/sllstore2017073/private/

### 02-09-19
```bash
$ module load bioinfo-tools
$ module load blast/2.7.1+

# includes tblastn which will be used for the start of the fishing expedition. 
# for more information on how tblastn can be used through CLI follow:
# https://www.ncbi.nlm.nih.gov/books/NBK279684/

$ tblastn -h
USAGE
  tblastn [-h]v984kbncq75r1xf [-help] [-import_search_strategy filename]
    [-export_search_strategy filename] [-task task_name] [-db database_name]
    [-dbsize num_letters] [-gilist filename] [-seqidlist filename]
    [-negative_gilist filename] [-negative_seqidlist filename]
    [-entrez_query entrez_query] [-db_soft_mask filtering_algorithm]
    [-db_hard_maTraditional BLASTN requiring an exact match of 11
sk filtering_algorithm] [-subject subject_input_file]
    [-subject_loc range] [-query input_file] [-out output_file]
    [-evalue evalue] [-word_size int_value] [-gapopen open_penalty]
    [-gapextend extend_penalty] [-qcov_hsp_perc float_value]
    [-max_hsps int_value] [-xdrop_ungap float_value] [-xdrop_gap float_value]
    [-xdrop_gap_final float_value] [-searchsp int_value]
    [-sum_stats bool_value] [-db_gencode int_value] [-ungapped]
    [-max_intron_length length] [-seg SEG_options]
    [-soft_masking soft_masking] [-matrix matrix_name]
    [-threshold float_value] [-culling_limit int_value]
    [-best_hit_overhang float_value] [-best_hit_score_edge float_value]
    [-window_size int_value] [-lcase_masking] [-query_loc range]
    [-parse_deflines] [-outfmt format] [-show_gis]
    [-num_descriptions int_value] [-num_alignments int_value]
    [-line_length line_length] [-html] [-max_target_seqs num_sequences]
    [-num_threads int_value] [-remote] [-comp_based_stats compo]
    [-use_sw_tback] [-in_pssm psi_chkpt_file] [-version]

```

At glance tblastn seems pretty straight forward, you have in and out, different cutofs then a ton of min maxing one could add to the search. The program does require a database, and if you want to create on of these you can use makeblastdb which creates a db out of a fasta file, so we could simply add sequences to a fasta file format and create a database to be queried. We want to perform an iterative tblast of the matches of cryptonts, meaning that if we get a match for a crypton, that has not been notified yet in other searches then we take that make and query it to the genome it was found in, this is to find possible degenerated sequences of the same crypton in the genome. 

Trying simply to tblastn the kirc fasta, which is as follows:

>PaWa53m.gene.004562|Kirc|CDS| PaWa53m_chromosome_3
MPRKKSPQEFFRRGKDRGSENCTEGIDGSAVHKKITDKVMKGYQRMVDLWSQYAEDHPGASPYDLKTLKDFVKDIAFGIDGAEDNSDPAEGTVMVYWKQFMAGWRRENDAIPKNITLSVTNFIKYELPDILRTEGKEILKNKRPRRFGTKNHFLHLGRQLWGNDWVVCDKPATRVYDWADLLAIVCSSARVGEYIESTCRAGSGRGLYYRNVTFGVFLNEHGNAEFAVQLVRDAKGMTDNPAKRPEHSLYEGLGEMPLICNPMLPILAILIGTKAFKDYETIEDLLNIQPSEGEMIHLQWKESVLDLPFFKSMSARGTPGKIETATAFSKRLRLLGFRAGYSRPPTIHDFRAEGLYWIDKLYSVAQRMKHAGQKDPNTYNNHYQPNNSGTDGQGSYFGLDVRNIANDLFRGLTLARNPQLWQTLPAEKQEEFQNSPEFSKIENKLATLQGQRDTDSVTRRRNLYAERRRLTEKEVRKYQKAQTLRPSGDRFLQCYHRCIFDRVRFLMPERDRLASTLFEIHALRSPTGLSALRDMVALCEKDAEVEFRPGLEPEKCHCSSRPHQRKLVKSTDSNIKTQSFYDWKHIYRCYKNSHTDFAELCFLCNNWFFGEAQWSSHCQAHLNCPETLPI

So we will do it as follows: 

 * tblastn crypton sequence of interest
 * gather species with > 5 hits
 * download these genomes 
 * try to find a consensus sequence of the crypton used. 
 * rince and repeat for multiple cryptons

### 03-09-19
Trying to extract fasta header and putting them into a csv file, seems to be working now. This is to document what species that has already been analyzed, so when getting blast hits we will be able to remove the already reported hits.

So, trial run of Kirc into tblastn:
in total, without limiting it, we get about 176 sequence hits into the nt database. 

Gathering those with 5 or more hits:

* 7 hits - Gaeumannomyces tritici R3-111a-1
* 6 hits - Pyricularia oryzae 70-15
* 12 hits - Exophiala oligosperma
* 8 hits - Cyphellophora europaea CBS 101466
* 5 hits - Aspergillus nidulans FGSC A4

Then I guess we would like to see if an of these has had Kirc found in them before? As reference we are using the repbase database. Using the host name we can see if there are any records of the cryptons of our interest in the host:

* Gaeumannomyces tritici R3-111a-1 - Not documentation
* Pyricularia oryzae - No documentation
* Exophiala oligosperma - No documentation
* Cyphellophora europaea - No documentation
* Aspergillus nidulans - No documentation

Concerning? We cannot expect kirc to be present in any of the species, but the fact that we got good homologous searches which indicate sequence preserverence. 

to do now:

* retrieve sequences from genomes by using  the output 6 format from blast through the script extract_flanks on uppmax
* get genomes to uppmax, use the shortenScaffoldnames.pl to remove spaces in the genomes
* use MAFFT, either server or local to align the sequences, to then draw a consensus sequence by viewing the new alignment to the genome the sequences came from

Folder for the project:

/proj/sllstore2017073/private/

there seems to be and issue with the tblastn on uppmax, the job never seems to be starting for some odd reason.

### 04-09-19
Tried to simply create my own blastdb and it seems to be working, think if there are other issues at hand here? goinga to try to increase the cores as well as the time even further, don't know why this should be such a heavy task. 

Bash script for tblastn is now working, possible to perform something fancy as a larger script that would search iterably over a sequence of interest? 

created script to extract fasta sequences after their header, extracted crypton_V due to few hits for Kirc, could be due to that Kirc is degenerated. We did find three hits in the P.Anserina species, which apparantly is an homologue to kirc. 

"final" tblastn script created, needs to be edited for every run, please streamline this...

### 05-09-19
Today we will try to extract flanking sequences with Alex's script. For this we need the genome, and only from those organisms with a couple of hits that are not reported in repbase.

Currently all blast queries through command line is with default settings.
created script to separate the model sequences from the genomic sequences. Debating if I should create a script to extract taxonomy name, or if I should make a list and simply use online resources and later process it

Trying to make the accession numbers to compress, and only if the have more that x amount of hits then we add the to the final list that we can use to find the taxa name through either 3rd party programme or not. 


### 06-09-19
downloaded the accession2taxid files [from](ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid). By using grep and awk I imagine I could extract the taxa name and respective ACN.

```shell
fgrep -w -f research_training_19/blast_queries/kirc_tblastn_020919_acn <accession2taxid> | awk -F "\t" '{print $3}' 
```

this oneliner above does extract column 2 from the output of the grep line above. The file structure of accession2taxid is build so that the accession version nr, which is what we get out of the blast hit, is kept in column 2. Searching the whole line through Gbs is inefficient so first I will use awk to extract column 2 and column 3 has the respective taxID. Then we also need to parse this through a taxid 2 taxaname db to find the actual taxa name, to then check if it is found already in the organism or not.

```shell
fgrep -w -f <out_from_script_above> nu 
```

Acc_nr -> taxid -> tax_name

### 09-09-19
Should probably make the script to get taxa also save the conversion file. Would be nice to have a final tabe of the structure $ACN $TAXID $TAXA_NAME. Should not be 2 complicated, simply print the row of the one file in combo with the other. 

### 11-09-19
Previous day consisted of reading articles and waiting for blast hits to return. Today the goal is to actually use the perl script to extract flanking sequences for a blast hit and then try to put these into and aligner, either bioedit or aliview. 

```shell
$ head -n 20 extractBlast_v2mod_1kbflanks.pl
#!/usr/bin/perl


use strict;
use warnings;
use List::Util qw(max min); #Loading the math modules "max" and "min" 

# Input parameters 
# If you want to have more parameters, just add more lines,
# starting with "my" and $some_name=$ARGV[next number];
# Note that the when you run the script you need to input the 
# files in exactly this order. 
my $BLASTLIST = $ARGV[0];
my $ASSEMBLY = $ARGV[1];
my $OUTFILE = $ARGV[2];
#my $LISTOFSP = $ARGV[3];   #Needed for extracting blast hits

my $flank = 1000;
my $maxhitdist = 10000;
my $frac = 0.8;
```

Script is very descriptive, don't really know if I need the 4th argument in extracting the sequences but I will try to run it simply using a blast hit for a genome that is downloaded on the uppmax service. 

All ACN -> tid -> count_filter -> taxa_name -> check_taxa_named -> extractFlanks_X.pl -> Alignment tool

### 12-09-19
Very close on finishing the starting pipeline. Thus I would have a way of easily blasting a sequence and retrieving the taxa names with a good number of hits.

taxa id and scientific name was extracted on the 12-09-19 by:
```shell
awk -F "|" '$4~/scientific name/ {print $1"\t"$2}' $namesdump_path > taxa_id_name 
```

### 16-09-19
sorted the taxa_id-name file, to be used later on in the join to be performed.

```shell
sort -k1 -o sorted_taxa_id_name taxa_id_name 

# Then the ids filtered where joined with the names by using join

join -t $'\t' \
    -1 1 -2 1 \
    -o 1.1,1.2,2.1 \
    filtered_acn_tid sorted_taxa_id_name | sort -nk1 > filtered_blast_hits
```

### 19-09-19
Mainly been trying to perfect the pipeline. Came up with new ideas how to do it properly. Current status is to blast, then see if one sequence matches to the same taxa more then 5 times. The next step will be to then check if these proteins are discovered in this taxa, and if not, I want to retrieve their lines from the fmt6 file to then extract the sequences from the target genome. 

### 25-09-19
preparing some data of information for the symposium. 

```shell
$ cut -f1,13 crypt_v_180919_filt_fmt6 | uniq | wc -l
113
# meaning that if take the number of probable novel crypton hits and filter for query and taxa we get 113 newly found combinations
$ cut -f1 <(cut -f1,13 crypt_v_180919_filt_fmt6 | uniq) | uniq
CryptonV-10_CFl_1p
CryptonV-11_CFl_1p
CryptonV-12_CFl_1p
CryptonV-1_BTa_1p
CryptonV-1_CFl_1p
CryptonV-1_CGi_1p
# There are 6 probable cryptons that has seen homology, resulting in 113 probable novel hosts
cut -f1,13 crypt_v_180919_filt_fmt6 | uniq | grep 'CryptonV-1_CGi_1p'
CryptonV-1_CGi_1p   Danio rerio
CryptonV-1_CGi_1p   Oryzias latipes
CryptonV-1_CGi_1p   Scophthalmus maximus
CryptonV-1_CGi_1p   Lateolabrax maculatus
CryptonV-1_CGi_1p   Danio rerio
CryptonV-1_CGi_1p   Dicentrarchus labrax
CryptonV-1_CGi_1p   Oryzias latipes
CryptonV-1_CGi_1p   Cyprinus carpio
CryptonV-1_CGi_1p   Parambassis ranga
CryptonV-1_CGi_1p   Betta splendens
CryptonV-1_CGi_1p   Anabas testudineus
CryptonV-1_CGi_1p   Denticeps clupeoides
CryptonV-1_CGi_1p   Mastacembelus armatus
CryptonV-1_CGi_1p   Sparus aurata
CryptonV-1_CGi_1p   Scleropages formosus
CryptonV-1_CGi_1p   Takifugu rubripes
CryptonV-1_CGi_1p   Salarias fasciatus
CryptonV-1_CGi_1p   Sphaeramia orbicularis
CryptonV-1_CGi_1p   Gadus morhua
CryptonV-1_CGi_1p   Coregonus sp. 'balchen'
CryptonV-1_CGi_1p   Chanos chanos
# For instance, CryptonV-1_CGI has 5 or more hits to these 21 species.
```

###01-10-19
To download multiple genomes one can make use of the wget tool to do the following:

```shell
$ for file in `for file in `cut -f2,13 blast_queries/genome_hits/crypt_v_180919_filt_fmt6 | sort -k2 | uniq | grep 'Takifugu' | cut -f1`; do wget -O ~/genomes/vertebrate/species/$file 'https://www.ncbi.nlm.nih.gov/search/api/sequence/'$file'/?report=fasta'; done
```

extract fmt6 format by species spec

```shell
for name in `cut -f1 blast_queries/genome_hits/crypt_v_180919_filt_fmt6 | sort -k1 | uniq`; do awk -F "\t" '$1~/'$name'/ && $13~/Gadus morhua/ {print $0}' blast_queries/genome_hits/crypt_v_180919_filt_fmt6 > blast_queries/crypton_hits/crypt_v/gadus_morhua/$name'_fmt6' ; done
```

### 14-10-19
trying to group sequences by simularity. using a cut-off at 95% simularity to group the two

```python
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

calculator = DistanceCalculator('identity')
dm = calculator.get_distance(align)

align = AlignIO.read('input.fasta', 'fasta')

for item in range(len(dm.matrix)):
     for perc in range(len(dm.matrix[item])):
             if dm.matrix[item][perc] <= 0.05:
                     print(dm.matrix[item][perc])
                     print(dm.names[item])
```
might have to alter this cut-of. 95% yields a very small amount of sequences, and we ned at least 3 for a consensus to be made. 

### 22-10-19
common mafft online profile that could be used for commandline one day is shown below:

```shell
$ mafft --thread 8 --threadtb 5 --threadit 0 --reorder --adjustdirection --anysymbol --auto input > output
```

### 23-10-19

RaxMl reference:  "RAxML Version 8: A tool for Phylogenetic Analysis and Post-Analysis of Large Phylogenies". In Bioinformatics, 2014, open access.

CryptonH - found in Danio Rerio(zebrafish) and is a YR encoding DNA transposon. distantly related to Crypton-V, and is distributed amoun anomals such as fish cnidarians. Will be used to get a close relationship to the CryptonV.

CryptonV do in some cases leave TSD, CryptonV-1_DR leaves 11bp TIRs, but a few of them tend to insert into TG microsatellites.

### 25-09-19
animalia phylogeny from: https://www.annualreviews.org/doi/10.1146/annurev-ecolsys-120213-091627

fish phylogeny picture from: https://www.pnas.org/content/115/24/6249/tab-figures-data

### 30-10-19
after aligning with math, cluster with python script, then create consensus by majority rule. After this we used ORF-finder to find longest orf and if significantly large ones where found(similar to the largest in size) two ORFs where taken, marked with L for longeset and S for shortest. After, coding sequences for all novel and reported cryptonV's from repbase where aligned again using mafft, this was done to ensure that the ORFs taken from ORF-finder was somewhat aligning at all to the reported cryptonV's. This alignment was then followed by an mafft --add alignment(using the novel cryptonV and reported cryptonV from above as seed) of all reported CryptonH in repbase, in repbase reports they are not to divergent from to the cryptonV's, and atleast two of each other reported cryptonfamily in repbase, except for CryptonI which only had one entry in the database at the time.

To construct the phylogenetic tree the substitution model was decided using MEGA model estimation, which uses maximum likelihood tests of multiple models. The one with the lowest BIC-score is deemed to be the best fit for the data, which in this case is WAG + G + F. Phylogenetic tree is produced using the WAG+G+F and 500 bootstraps. 

### 1-11-19
Model decided in MEGA, model run in raxml, trees summarized by sumtree and then imaged by figtree. great.
