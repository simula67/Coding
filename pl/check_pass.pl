#!/usr/bin/perl
#    This script tries to check for a given hash (or any string) in a /etc/shadow file and returns the corresponding Login Name
#    of the user whose /etc/shadow contained in the given hash from /etc/passwd. Useful to check if a user is using a weak hash.
#    Author : simula67
#    This script requires root permissin to run as /etc/shadow is readable only by root in most systems.
#    Author claims no resposiblity in how others use this.
my $hash = shift;
die "No hash specified " unless $hash;
open PASSWD, "/etc/passwd" or die 'Failed to open /etc/passwd';
open SHDW, "/etc/shadow" or die 'Failed to open /etc/shadow';
my $ln_shdw;
my $ln_passwd;
my $user;
while(chomp($ln_shdw = <SHDW>))
{
    chomp($ln_passwd = <PASSWD>);
    if($ln_shdw =~ /$hash/)
    {
	($user) = ($ln_passwd =~ m/(\w*?):/);
	print "User \"$user\" contains the given hash\n";
    }
}
