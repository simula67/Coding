#!/usr/bin/perl
while(<>) {
	if(m/(http:\/\/\S*.deb)/) {
	print "$1\n";
	}
}
