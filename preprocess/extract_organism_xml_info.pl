use strict;
use warnings;
use XML::Simple qw(:strict);
use Data::Dumper;

my $file = $ARGV[0];
my $xs = XML::Simple->new();
my $config = $xs->XMLin($file, ForceArray => 0, KeyAttr => []);


#print Dumper($config);

my $taxon_ID = $config->{'SAMPLE'}->{'SAMPLE_NAME'}->{'TAXON_ID'};
if(not defined $taxon_ID){
	$taxon_ID = "NA"
}

my $scientific_name = $config->{'SAMPLE'}->{'SAMPLE_NAME'}->{'SCIENTIFIC_NAME'};
if(not defined $scientific_name){
        $scientific_name = "NA"
}


# Get accession
my $accession = $config->{SAMPLE}->{accession};


my @result = ($file, $accession, $taxon_ID, $scientific_name);
print join("\t", @result) . "\n";


