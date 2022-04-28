use strict;
use warnings;
use XML::Simple qw(:strict);
use Data::Dumper;

my $file = $ARGV[0];
my $xs = XML::Simple->new();
my $config = $xs->XMLin($file, ForceArray => 0, KeyAttr => []);


#print Dumper($config);

# Get accession
my $accession = $config->{EXPERIMENT}->{accession};

# Get Genomic
my $library_source = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_SOURCE};

# Get selection approach
my $library_selection = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_SELECTION};

# Get paired
my $a = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_LAYOUT};
my @library_layout = keys %$a;
my $library_layout_val = $library_layout[0];

# Library strat
my $library_strategy = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_STRATEGY};

# Library name
my $library_name = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_NAME};
unless(length $library_name){
	$library_name = "NA"
}

# Library protocol
my $library_protocol = $config->{EXPERIMENT}->{DESIGN}->{LIBRARY_DESCRIPTOR}->{LIBRARY_CONSTRUCTION_PROTOCOL};
unless(length $library_protocol){
	$library_protocol = "NA"
}

# Get platform names
my $platform_hash = $config->{EXPERIMENT}->{PLATFORM};
my @platform_key = keys %$platform_hash;
my $platform_val = $platform_hash->{$platform_key[0]};
my $platform_name = $platform_key[0];
my $instrument_name = $platform_val->{INSTRUMENT_MODEL};


my @result = ($file, $accession, $library_source, $library_selection, $library_layout_val, $library_strategy, $library_name,
$library_protocol, $platform_name, $instrument_name);
print join("\t", @result) . "\n";


