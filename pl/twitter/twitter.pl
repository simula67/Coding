#!/usr/bin/perl
# This script lets you post tweets without using a browser and without the need to log in...
# Coded by : simula67
use App::Tweet;
if( @ARGV < 1 ){
    print "Usage : $0 <String to tweet> [<username> <password>]\n";
    exit 1;
}
my $tweet = shift;
my $username = shift;
my $pass = shift;
if( !defined($username) || !defined($pass) ){
    print "No username or password entered at command line\n";
    App::Tweet->reconfigure;
    App::Tweet->run(message => "$tweet");
}
else{
    print "Trying to sent the tweet using username : $username and password : $pass\n";
    App::Tweet->run( message => "$tweet",  username => "$username", password => "$pass"  );
}
print "\nMessage (un)successfully passed\n";
