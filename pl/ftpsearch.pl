#!/usr/bin/perl
#Prints all the files from an ftp site
# author : simula67 ( Joji Antony )
use Net::FTP;
$hostname = shift;
die "Usage : $0 <hostname> [username] [password]\n" unless (defined($hostname));
$user = shift;
$user = "anonymous" unless (defined($user));
$pass = shift;
$pass = "ftpsearch" unless (defined($pass));
my $conn = Net::FTP->new("$hostname", Debug => 0) or die "Cannot connect to $hostname: $@";
$conn->login("$user","$pass") or die "Cannot login ", $conn->message;
sub parse_path {
    my $path = shift;
    my $next_dir;
    my $file;
    unless( $conn->cwd("$path") ) {
	warn "Cannot change to $path\n";
	return;
    }
    my @directories = $conn->dir();
    foreach $dir (@directories) {
	if( $dir =~ m|^d.*| ) {
	    if( ($next_dir) = ($dir =~ m|.*\d (.*)|s) ) {
		parse_path("$path$next_dir/");
	    }
	}
	else {
	    
	    if( ($file) = ($dir =~ m|.*\d (.*)|) ) {
                print "$hostname$path$file\n";
            }

	}
    }

}
parse_path("/");
