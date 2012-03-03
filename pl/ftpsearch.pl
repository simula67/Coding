#!/usr/bin/perl
#Prints all the files from an ftp site
use Net::FTP;
    
$hostname = shift;
die "Usage : $0 <hostname> [username] [password]\n" unless (defined($hostname));
$user = shift;
$user = "anonymous" unless (defined($user));
$pass = shift;
$pass = "ftpsearch" unless (defined($pass));

sub parse_path {
    my $conn = Net::FTP->new("$hostname", Debug => 0) or die "Cannot connect to $hostname: $@";
    $conn->login("$user","$pass") or die "Cannot login ", $conn->message;
    my $path = shift;
    my $next_dir;
    my $file;
    $conn->cwd("$path") or die "CWD error : ", $conn->message;
    my @directories = $conn->dir();
    foreach $dir (@directories) {
	if( $dir =~ m|^d.*| ) {
	    if( ($next_dir) = ($dir =~ m|.*\d (.*)|s) ) {
		$conn->quit();
		parse_path("$path$next_dir/");
	    }
	}
	else {
	    
	    if( ($file) = ($dir =~ m|.*\s(.*)|) ) {
                print "$hostname$path$file\n";
            }

	}
    }

}
parse_path("/");
