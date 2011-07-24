#!/usr/bin/perl
#Coded by : simula67
#Extract links for images of any query from Google
use LWP 5.64;
use URI;

if( @ARGV < 1 ) {
	die "Usage $0 <query string>\n";
}
my $query_string = "@ARGV";
my $page = 1;

my $browser = LWP::UserAgent->new;
$browser->agent('Mozilla/5.0');
my $url = URI->new( 'http://www.google.co.in/search' );
my $value = ($page - 1) * 20;
$url->query_form(
    'q' => ''.$query_string,
    'tbm' => 'isch',
    'sout' => '1',
    'safe' => 'off',
    'start' => ''.$value,
);
my $response = $browser->get($url);
my @lines = split /\n/, $response->decoded_content;
foreach my $line (@lines) {
	while( $line =~ m/imgurl\\x3d(\S*?\.jpg)/g) {
		print "$1\n";
	}
}

