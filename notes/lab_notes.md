### 02-09-19
```bash
$ module load bioinfo-tools
$ module load blast/2.7.1+

# includes tblastn which will be used for the start of the fishing expedition. 
# for more information on how tblastn can be used through CLI follow:
# https://www.ncbi.nlm.nih.gov/books/NBK279684/

$ tblastn -h
USAGE
  tblastn [-h] [-help] [-import_search_strategy filename]
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
fgrep -w -f research_training_19/blast_queries/kirc_tblastn_020919_acn <accession2taxid> | awk 'F="\t" {print $3}' 
```

this oneliner above does extract column 2 from the output of the grep line above. The file structure of accession2taxid is build so that the accession version nr, which is what we get out of the blast hit, is kept in column 2. Searching the whole line through Gbs is inefficient so first I will use awk to extract column 2 and column 3 has the respective taxID. Then we also need to parse this through a taxid 2 taxaname db to find the actual taxa name, to then check if it is found already in the organism or not.

```shell
fgrep -w -f <out_from_script_above> nu 
```

Acc_nr -> taxid -> tax_name

