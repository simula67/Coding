#!/usr/bin/perl
#Coded by : simula67
#Extract links for images of any query from Google
use LWP 5.64;
use URI;
use CGI;
my $q = CGI->new;
print "Content-Type: text/html", "\n\n";
my $query_string = $q->param('q');
if( "$query_string" eq  "" ) {
    print "<html>\n";
    print "<head>\n";
    print "</head>\n";
    print "<title> Simplified Google Image Search </title>\n";
    print "<body>\n";
    print "<center>\n";
    print "<h1>Type something you want to search<h1>\n";
    print "</center>\n";
    print "<form action=\"save.pl\" method=GET>\n";
    print "<input type=\"text\" name=\"q\" style=\"width:100%\"><br />\n";
    print "<center>";
    print "<input type=\"submit\" value=\"Pull Images\">\n";
    print "</center>\n";
    print "</form>\n";
    print "</body>\n";
    print "</html>\n";
    exit 0;
}
my $page = $q->param('page');
if(!defined($page)) {
    $page = 1;
}
my $browser = LWP::UserAgent->new;
$browser->agent('Mozilla/5.0');
my $url = URI->new( 'http://www.google.com/search' );
my $value = ($page - 1) * 20;
$url->query_form(
    'q' => ''.$query_string,
    'tbm' => 'isch',
    'sout' => '1',
    'safe' => 'off',
    'start' => ''.$value,
    );
my $response = $browser->get($url);
if(!$response->is_success ) {
    print $response->status_line;
    die "Failed to fetch\n";
}
print "<html>\n"; 
print "<head>\n";
print "<title> $query_string </title>\n";
print "</head>\n";
print "<body>\n";
print "<center><h1><a href=\"save.pl\">Home</a></h1></center>";
my @lines = split /\n/, $response->decoded_content;
foreach my $line (@lines) {
    while( $line =~ m/imgurl\\x3d(\S*?\.jpg)/g) {
	print "<img src=\"$1\"><br />\n";
    }
}
print "<center><h1>";
for($i=$page;$i<=$page+10;$i++) {
    print "<a href=\"save.pl?q=$query_string&page=$i\">$i</a> &nbsp";
}
print "</h1></center>";
print "</body>\n";
print "</html>\n";
