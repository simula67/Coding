#!/usr/bin/perl
use HTML::SimpleLinkExtor;
my $file = new HTML::SimpleLinkExtor();
$filename = $ARGV[0];
if($filename eq "" ) {
    print "\nUsages: ./link.pl filename.html\n";
    exit ;
}

$file->parse_file($filename);
my @links= $file->a;
foreach $link (@links){
    chomp;
    print "$url$link\n";
}
