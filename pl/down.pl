#!/usr/bin/perl
use IO::Socket;
my $url = shift;
die "Usage : $0 <url>\n" unless( defined($url) );
my $output_file ="";;
if($url !~ m|/|)   {
    $output_file = "index.html";
}
elsif( ($output_file) = ($url =~ m|.*/(.*)$|) ) {
    
    if( "$output_file" eq ""  ) {
	$output_file = "index.html";
    }
}
my $hostname;
my $dont_care;
my $res_path;
if( ($dont_care, $hostname) = ( $url =~ m|^(http://)?([^/]*)| ) ) {
    if( "$hostname" eq "" ) {
	die "Cannot extract hostname\n";
    }
}
if( ($res_path) = ( $url =~ m|$dont_care$hostname(.*)| ) ) {
    if( "$res_path" eq "" ) {
	$res_path = "/";
    }
}

print "Hostname : $hostname\n";
print "Resource path : $res_path\n";
my $sock = new IO::Socket::INET (
    PeerAddr => "$hostname",
    PeerPort => '80',
    Proto => 'tcp',
    );
die "Could not create socket: $!\n" unless $sock;
my $request = "GET $res_path HTTP/1.1\r\nHost: $hostname\r\n\r\n";
print $sock "$request";
my $bytes;
my $content_len = 0;
my $line = "";
while( 1 ) {
    $bytes = sysread($sock,$buf,1);
    if( $bytes == 0 ) {
	last;
    }
    $line .= "$buf";
    
    if($line =~ m|^\r\n|) {
	last;
    }
    if($line =~ m|\r\n$|s) {
#	print "$line";
	$line = "";
    }
    if( $line =~ m|Content-Length: (\d*)| ) {	
	$content_len = $1
    }
}
if ( $content_len == 0 ) {
    die "Cannot extract content length\n";
}
print "Content Length: $content_len\n";
open OUT, ">$output_file" or die "Cannot open $output_file\n";
for( $i=0; $i < $content_len; $i++ ) {
    sysread($sock,$buf,1);
    print OUT "$buf";
}
