#!/usr/bin/perl 
use LWP::Simple;
my $url = shift;
die "Failed to fetch file\n" unless(head($url));
($content_type,$document_len,$modified_time,$expire_time,$server) = head($url);
print "Content Type : $content_type\n";
$kb_size = $document_len/1024;
print "Document Length : $kb_size KB\n";
print "Modified time : $modified_time\n";
print "Expire time : $modified_time\n";
print "Expires in : $expire_time\n";
print "Server : $server\n";
