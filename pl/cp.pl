#!/usr/bin/perl
#      cp command in perl
#      Coded by simula67

if(@ARGV < 2){
    print "Usage $0 <source file names> <destination path>\n";
    exit 1;
}
my ($dest_file,$ind,$match);
for($ind=0;$ind<(@ARGV-1);$ind= $ind+1){
    if( ($match) = ($ARGV[$ind] =~ /.*\/(\S*)/) ){
	$dest_file = $ARGV[$#ARGV]."/".$match;
    }
    else{
	$dest_file=$ARGV[$#ARGV]."/".$ARGV[$ind];
    }
    open INP, "<$ARGV[$ind]" or die "Failed to open input file";
    open OUTPUT, ">$dest_file" or die "Failed to open output file";
    select OUTPUT;
    while(<INP>){
	print;
    }
}
