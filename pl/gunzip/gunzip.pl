#!/usr/bin/perl -wT


use IO::Uncompress::Gunzip qw(gunzip $GunzipError);

my $input = "changelog.gz";
my $output = "changelog";
gunzip $input => $output or die "gunzip failed: $GunzipError\n";
