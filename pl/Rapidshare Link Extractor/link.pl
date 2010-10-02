#!/usr/bin/perl

use LWP;
use HTML::Form;
use Term::ANSIColor qw(:constants);
use warnings;
my $url = shift;
print $url."\n";
my $ua = LWP::UserAgent->new;
my $response = $ua->get($url);
return error(" (page 1 error, ",$response->status_line, ")") unless ($response->is_success);
my @forms = HTML::Form->parse($response);
print "\nForms coming up : \n";
print $forms[0]->dump;
my $req = $forms[0]->click();
$response = $ua->request($req);
return error(" (page 2 error, ", $response->status_line, ")") unless ($response->is_success);
my $wait_max = 2;
# Process the resulting page
while(1) 
	{
	my $wait;
	$_ = $response->decoded_content."\n"; 
	if(m/reached the download limit for free-users/) 
		{
		($wait) = m/Or try again in about (\d+) minutes/sm;
		info("reached the download limit for free-users");			
		} 
	elsif(($wait) = m/Currently a lot of users are downloading files\.  Please try again in (\d+) minutes or become/) 
		{
		info("currently a lot of users are downloading files");
		} 
	elsif(($wait) = m/no available slots for free users\. Unfortunately you will have to wait (\d+) minutes/) 
		{
		info("no available slots for free users");
		} 
	elsif(m/already downloading a file/) 
		{
		info("already downloading a file");
		$wait = 60;
		} 
	else 
		{
		last;
		}
	
	if ($wait > $wait_max) 
		{
		debug("should wait $wait minutes, interval-check in $wait_max minutes");
		$wait = $wait_max;
		}
	dwait($wait*60);
	$response = $ua->request($req);
	}
my ($download, $wait) = m/form name="dlf" action="([^"]+)".*var c=(\d+);/sm;
return error("plugin error (could not extract download link)") unless $download;
dwait($wait);
print "\n";
print "Download link is :\n $download";
print "\n";
# Non-fatal error
sub error 
	{
	output(RED, "error", \@_);
	return 0;
	}

sub output 
	{
	print shift, &timestamp, @_==2?uc(shift).": ":"";
	print while ($_ = shift(@{$_[0]}));
	print RESET "\n";
	}
sub dwait
	{
	my ($wait, $rem, $sec, $min);
	$wait = $rem = shift or return;
	$|++; # unbuffered output;
	($sec,$min) = localtime($wait);
	info(sprintf("Waiting %d:%02d",$min,$sec));
	sleep($rem);
	}
# Generate a timestamp
sub timestamp 
	{
	my ($sec,$min,$hour) = localtime;
	sprintf "[%02d:%02d:%02d] ",$hour,$min,$sec;
	}
sub info 
	{
	output(RESET, \@_);
	return 0;
	}
