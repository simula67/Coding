#!/usr/bin/perl

use WWW::Mechanize;
use Term::ANSIColor qw(:constants);

# Write nicely
use warnings;

my $verbosity = 3;
sub debug {
	output(GREEN, "debug", \@_) if ($verbosity >= 4);
	return 0;
}

print "Enter the URL : ";
my $inp = <stdin>;
print "The entered URL is : ";
print $inp;
print download($inp) . "\n";

sub download {
	my $file = shift;
	my $mech = WWW::Mechanize->new();
	# Get the primary page
	my $res = $mech->get($file);
	return error("plugin failure (page 1 error, ", $res->status_line, ")") unless ($res->is_success);
	
	# Click the "Free" button
	$mech->form_number(1);
	$res = $mech->submit_form();
	return error("plugin failure (page 2 error, ", $res->status_line, ")") unless ($res->is_success);
	my $wait_max = 2;
	# Process the resulting page
	while(1) {
		my $wait;
		$_ = $res->decoded_content."\n"; 

		if(m/reached the download limit for free-users/) {
			($wait) = m/Or try again in about (\d+) minutes/sm;
			info("reached the download limit for free-users");			
		} elsif(($wait) = m/Currently a lot of users are downloading files\.  Please try again in (\d+) minutes or become/) {
			info("currently a lot of users are downloading files");
		} elsif(($wait) = m/no available slots for free users\. Unfortunately you will have to wait (\d+) minutes/) {
			info("no available slots for free users");

		} elsif(m/already downloading a file/) {
			info("already downloading a file");
			$wait = 60;
		} else {
			last;
		}
		
		if ($wait > $wait_max) {
			debug("should wait $wait minutes, interval-check in $wait_max minutes");
			$wait = $wait_max;
		}
		dwait($wait*60);
		$res = $mech->reload();
	}

	# Extract the download URL
	my ($download, $wait) = m/form name="dlf" action="([^"]+)".*var c=(\d+);/sm;
	return error("plugin error (could not extract download link)") unless $download;
	dwait($wait);

	return $download;
}

sub dwait{
	my ($wait, $rem, $sec, $min);
	$wait = $rem = shift or return;
	$|++; # unbuffered output;
	($sec,$min) = localtime($wait);
	info(sprintf("Waiting %d:%02d",$min,$sec));
	sleep($rem);
}


sub info {
	output(RESET, \@_) if ($verbosity >= 3);
	return 0;
}

# Generate a timestamp
sub timestamp {
	my ($sec,$min,$hour) = localtime;
	sprintf "[%02d:%02d:%02d] ",$hour,$min,$sec;
}

# Warning
sub warning {
	output(YELLOW, "warning", \@_) if ($verbosity >= 2);
	return 0;
}

# Non-fatal error
sub error {
	output(RED, "error", \@_) if ($verbosity >= 1);
	return 0;
}

sub output {
	print shift, &timestamp, @_==2?uc(shift).": ":"";
	print while ($_ = shift(@{$_[0]}));
	print RESET "\n";
}



