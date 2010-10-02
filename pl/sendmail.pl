#!/usr/bin/perl


if(@ARGV<2)
{
    print "Usage : $0 <filename> <Subject>\n";
    exit;
}
my $filename = shift;
my $subject = shift;
my $content;
print "Filename is : $filename\n";
print "Subject matter is : $subject\n";
$subject = "Subject: ".$subject;
open FILE, "$filename" or die $!;
while (my $line = <FILE>) 
{
    $content = $content.$line;
}
close FILE;
print "File content retrieved...\n";
print "Now sending e-mail.Please wait...\n";
my $sendmail = "/usr/sbin/sendmail -t";
my $reply_to = "Reply-to: \@gmail.com";
my $send_to  = "To: simula67\@gmail.com";
open(SENDMAIL, "|$sendmail") or die "Cannot open $sendmail: $!";
print SENDMAIL $send_to."\n";
print SENDMAIL $reply_to."\n";
print SENDMAIL $subject."\n";
print SENDMAIL "Content-type: text/plain\n\n";
print SENDMAIL $content;
close(SENDMAIL);
print "E-mail sent succesfully...\n";
