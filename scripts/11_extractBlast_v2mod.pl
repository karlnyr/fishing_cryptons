#!/usr/bin/perl


use strict;
use warnings;
use List::Util qw(max min);	#Loading the math modules "max" and "min"

# Input parameters
# If you want to have more parameters, just add more lines,
# starting with "my" and $some_name=$ARGV[next number];
# Note that the when you run the script you need to input the
# files in exactly this order.
my $BLASTLIST = $ARGV[0];
my $ASSEMBLY = $ARGV[1];
my $OUTFILE = $ARGV[2];
#my $LISTOFSP = $ARGV[3];	#Needed for extracting blast hits

my $flank = ARGV[3];
my $maxhitdist = 10000;
my $frac = 0.8;

#Make a hash of the sequences
my %seqHash = ();

#Make file handle for output file
open(OUT, ">".$OUTFILE);

#Save the ONLY
my $tempNames = "tempNames.out";
system("cut -f2 $BLASTLIST |uniq >$tempNames");


open(IN, $tempNames);
while(<IN>) {
	chomp($_);
	$seqHash{$_}="";
}
close(IN);


# This part is just for making it possible to input a
# zipped file (checks if the file ends with ".gz")
#if ($ASSEMBLY =~ /\.gz$/) {
#	open(FILE, "zcat $ASSEMBLY |");
#}
# If the file isn't compressed (default way of opening file handle)
#else {
open(FILE, $ASSEMBLY);
#}

print "Saving Genome sequences...\n";


while(<FILE>) {		#The <> means that we read one line at the time

	#Found a header
	if($_ =~ m/^>/) {
		chomp($_);

		my $head = $_;
		$head =~ s/>//;

		if(defined $seqHash{$head}) {

			my $seq = ();
			my $next = <FILE>;
			while ($next !~ m/^>/) {
				chomp($next),
				$seq.= $next;
				if(eof(FILE)) {
					last;
				}
				$next = <FILE>;
			}
			seek(FILE, -length($next), 1);

			$seqHash{$head} = $seq;
		}
	}
}
close(IN);


print "...Done!\n";

#Close the file handle
close(FILE);

print "Going through the hits...\n";
open(IN, $tempNames);
while(<IN>) {
	chomp($_);

	my $tempRows = "temp.out";

	system("awk '(\$2==\"$_\"){print}' $BLASTLIST |cut -f1,2,9,10 |sort -k3n >$tempRows");

	#Change the sequence header to the file name, and remove the latin name
	#Now when we open a new file while still having the other file ("IN")
	#open, we cannot use the default parameter "$_" for the line, but instead
	#create a parameter for it, here called "$line"
	open(TMP, $tempRows);
	my ($head, $fullName, $start, $stop);
	my ($plus, $minus) = (0,0);
	my $cnt = 0;
	my $suffix = "";
	my $compl="";
	while(my $line = <TMP>) {
		#First line - just save for comparison
		if($cnt==0) {
			($head, $fullName, $start, $stop) = split(/\s+/, $line);
			if($stop>$start) {
				$plus++;
			}
			else {
				$minus++;
				my $temp=$start;
				$start=$stop;
				$stop=$temp;
			}
#			print "DEBUG:Looking at the first line with start $start\n";
		}
		#All other lines
		else {
			my @thisline = split(/\s+/, $line);


			#If the line should be merged with the previous
			if(min($thisline[2],$thisline[3])-max($stop,$start)<=$maxhitdist) {
					$start = min($start,$stop,$thisline[2],$thisline[3]);
					$stop = max($start,$stop,$thisline[2],$thisline[3]);


					if($thisline[3]>$thisline[2]) {
						$plus++;
					}
					else {
						$minus++;
					}
			}
			#if not, print previous result and save this line to compare with
			else {
				#First, we need to remove spaces from the header etc
				my @tab = split(/#/, $fullName);
				$fullName = $tab[0];
				#(In Blast output the spaces are replaced by "#", we want to remove
				#any spaces and what comes after it, therefore we split on "#" and
				#save only what preceeds it)


				#Check that a majority of the hits has the same direction
				if(max($plus, $minus)/($plus+$minus) < $frac) {
					print STDERR "Ambiguous orientation of blast hits for ".$fullName.": ".$plus." +, ".$minus." -\n";
					$suffix = "_Ambiguous_orientation";
				}


				#define sequence
				my $sequence = $seqHash{$fullName};

				#Call the sub routine
				my $substr = &extractFromFasta($start-$flank,$stop+$flank,$sequence);

				#Check if we need to reverse complement
				if($minus>$plus) {
					$substr=&revComp($substr);
					$compl="_RC";
				}


				print OUT ">".$fullName."_".$start."-".$stop.$suffix.$compl."\n".$substr;
				$suffix="";
				$compl="";

				#Save this line:
				($head, $fullName, $start, $stop) = split(/\s+/, $line);
				if($stop>$start) {
					$plus=1;
				}
				else {
					$minus=1;
					my $temp=$start;
					$start=$stop;
					$stop=$temp;
				}

			}
		}
		$cnt++;
	}
	#print the last line (same code as within "while")
	if(max($plus, $minus)/($plus+$minus) < $frac) {
		print STDERR "Ambiguous orientation of blast hits for ".$fullName.": ".$plus." +, ".$minus." -\n";
		$suffix = "_Ambiguous_orientation";
	}
	my $sequence = $seqHash{$fullName};
	my $substr = &extractFromFasta($start-$flank,$stop+$flank,$sequence);
	if($minus>$plus) {
		$substr=&revComp($substr);
		$compl="_RC";
	}

	print OUT ">".$fullName."_".$start."-".$stop.$suffix.$compl."\n".$substr;

	close(TMP);
}
close(IN);
print "...Done!\n";


# EXTRACT SEQUENCE FROM A FASTA FILE
# I copied this code from the "extractFromFasta" script
# and modified it a bit.
sub extractFromFasta {

	my $start = shift;
	my $end = shift;
	my $seq = shift;

#	 print "DEBUG: Inside subroutine!\n";		#Uncomment this line for display

	my $noOfBases = $end-$start+1;
	my $rowlength = 80;		#How many bases per row



	# "substr" is a function which is pre-defined in perl
	my $substr = substr($seq, $start-1, $noOfBases);
	my @seqParts = split(/(.{$rowlength})/, $substr);
	my $substr2 = "";
	for my $seqs (@seqParts) {
		unless($seqs eq "") {
			$substr2 = $substr2.$seqs."\n";
		}
	}

	return $substr2;

}

# REVERSE COMPLEMENT A SEQUENCE
sub revComp {

	my $DNAstring = shift;

	$DNAstring =~ s/\n//g;

	my $output = "";
	my @a = split(//, $DNAstring);

	for(@a) {
		$_ =~ tr/[A,T,C,G,R,Y,K,M,B,D,H,V,a,t,c,g,r,y,k,m,b,d,h,v]/[T,A,G,C,Y,R,M,K,V,H,D,B,t,a,g,c,y,r,m,k,v,h,d,b]/;
		$output = $_ . $output;
	}

	my @seqParts = split(/(.{80})/, $output);
	my $substr2 = "";
	for my $seqs (@seqParts) {
		unless($seqs eq "") {
			$substr2 = $substr2.$seqs."\n";
		}
	}

	return $substr2;
}




