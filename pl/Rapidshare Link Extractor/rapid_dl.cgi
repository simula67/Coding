#!/usr/bin/perl

# hello.pl -- my first perl script!

print "Content-type: text/plain\n\n";


=head1 NAME

lwp-download - Fetch large files from the web

=head1 SYNOPSIS

B<lwp-download> [B<-a>] <I<url>> [<I<local path>>]

=head1 DESCRIPTION

The B<lwp-download> program will save the file at I<url> to a local
file.

If I<local path> is not specified, then the current directory is
assumed.

If I<local path> is a directory, then the basename of the file to save
is picked up from the Content-Disposition header or the URL of the
response.  If the file already exists, then B<lwp-download> will
prompt before it overwrites and will fail if its standard input is not
a terminal.  This form of invocation will also fail is no acceptable
filename can be derived from the sources mentioned above.

If I<local path> is not a directory, then it is simply used as the
path to save into.

The I<lwp-download> program is implemented using the I<libwww-perl>
library.  It is better suited to down load big files than the
I<lwp-request> program because it does not store the file in memory.
Another benefit is that it will keep you updated about its progress
and that you don't have much options to worry about.

Use the C<-a> option to save the file in text (ascii) mode.  Might
make a difference on dosish systems.

=head1 EXAMPLE

Fetch the newest and greatest perl version:

 $ lwp-download http://www.perl.com/CPAN/src/latest.tar.gz
 Saving to 'latest.tar.gz'...
 11.4 MB received in 8 seconds (1.43 MB/sec)

=head1 AUTHOR

Gisle Aas <gisle@aas.no>

=cut

#' get emacs out of quote mode


use strict;

use LWP::UserAgent ();
use LWP::MediaTypes qw(guess_media_type media_suffix);
use URI ();
use HTTP::Date ();
use CGI;
use LWP;
use HTML::Form;
use Term::ANSIColor qw(:constants);
use warnings;
my $cgi = new CGI;
my $url2 = $cgi->param('url');
die "No Rapidhshare URL entered at script URL" unless defined($url2);
print "Entered URL is : ";
print $url2."\n>";
my $ua2 = LWP::UserAgent->new;
my $response = $ua2->get($url2);
return error(" (page 1 error, ",$response->status_line, ")") unless ($response->is_success);
my @forms = HTML::Form->parse($response);
my $req = $forms[0]->click();
$response = $ua2->request($req);
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
	$response = $ua2->request($req);
	}
my ($download, $wait) = m/form name="dlf" action="([^"]+)".*var c=(\d+);/sm;
return error(" Could not extract download link ") unless $download;
dwait($wait);
print "\nDownload link is : ";
print $download;
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
sub debug 
	{
	output(GREEN, "debug", \@_);
	return 0;
	}
my $progname = $0;
$progname =~ s,.*/,,;    # only basename left in progname
$progname =~ s,.*\\,, if $^O eq "MSWin32";
$progname =~ s/\.\w*$//; # strip extension if any

#parse option
use Getopt::Std;
my %opt;
unless (getopts('a', \%opt)) {
    usage();
}
my $url = URI->new($download || usage());
my $argfile = shift;
usage() if defined($argfile) && !length($argfile);
my $VERSION = "5.813";

my $ua = LWP::UserAgent->new(
   agent => "lwp-download/$VERSION ",
   keep_alive => 1,
   env_proxy => 1,
);

my $file;      # name of file we download into
my $length;    # total number of bytes to download
my $flength;   # formatted length
my $size = 0;  # number of bytes received
my $start_t;   # start time of download
my $last_dur;  # time of last callback

my $shown = 0; # have we called the show() function yet

$SIG{INT} = sub { die "Interrupted\n"; };

$| = 1;  # autoflush

my $res = $ua->request(HTTP::Request->new(GET => $url),
  sub {
      unless(defined $file) {
	  my $res = $_[1];

	  my $directory;
	  if (defined $argfile && -d $argfile) {
	      ($directory, $argfile) = ($argfile, undef);
	  }

	  unless (defined $argfile) {
	      # find a suitable name to use
	      $file = $res->filename;

	      # if this fails we try to make something from the URL
	      unless ($file) {
		  my $req = $res->request;  # not always there
		  my $rurl = $req ? $req->url : $url;

		  $file = ($rurl->path_segments)[-1];
		  if (!defined($file) || !length($file)) {
		      $file = "index";
		      my $suffix = media_suffix($res->content_type);
		      $file .= ".$suffix" if $suffix;
		  }
		  elsif ($rurl->scheme eq 'ftp' ||
			   $file =~ /\.t[bg]z$/   ||
			   $file =~ /\.tar(\.(Z|gz|bz2?))?$/
			  ) {
		      # leave the filename as it was
		  }
		  else {
		      my $ct = guess_media_type($file);
		      unless ($ct eq $res->content_type) {
			  # need a better suffix for this type
			  my $suffix = media_suffix($res->content_type);
			  $file .= ".$suffix" if $suffix;
		      }
		  }
	      }

	      # validate that we don't have a harmful filename now.  The server
	      # might try to trick us into doing something bad.
	      if (!length($file) ||
                  $file =~ s/([^a-zA-Z0-9_\.\-\+\~])/sprintf "\\x%02x", ord($1)/ge)
              {
		  die "Will not save <$url> as \"$file\".\nPlease override file name on the command line.\n";
	      }

	      if (defined $directory) {
	          require File::Spec;
	          $file = File::Spec->catfile($directory, $file);
	      }

	      # Check if the file is already present
	      if (-l $file) {
		  die "Will not save <$url> to link \"$file\".\nPlease override file name on the command line.\n";
	      }
	      elsif (-f _) {
		  die "Will not save <$url> as \"$file\" without verification.\nEither run from terminal or override file name on the command line.\n"
		      unless -t;
		  $shown = 1;
		  print "Overwrite $file? [y] ";
		  my $ans = <STDIN>;
		  unless (defined($ans) && $ans =~ /^y?\n/) {
		      if (defined $ans) {
			  print "Ok, aborting.\n";
		      }
		      else {
			  print "\nAborting.\n";
		      }
		      exit 1;
		  }
		  $shown = 0;
	      }
	      elsif (-e _) {
		  die "Will not save <$url> as \"$file\".  Path exists.\n";
	      }
	      else {
		  print "Saving to '$file'...\n";
	      }
	  }
	  else {
	      $file = $argfile;
	  }
	  open(FILE, ">$file") || die "Can't open $file: $!\n";
          binmode FILE unless $opt{a};
	  $length = $res->content_length;
	  $flength = fbytes($length) if defined $length;
	  $start_t = time;
	  $last_dur = 0;
      }

      print FILE $_[0] or die "Can't write to $file: $!\n";
      $size += length($_[0]);

      if (defined $length) {
	  my $dur  = time - $start_t;
	  if ($dur != $last_dur) {  # don't update too often
	      $last_dur = $dur;
	      my $perc = $size / $length;
	      my $speed;
	      $speed = fbytes($size/$dur) . "/sec" if $dur > 3;
	      my $secs_left = fduration($dur/$perc - $dur);
	      $perc = int($perc*100);
	      my $show = "$perc% of $flength";
	      $show .= " (at $speed, $secs_left remaining)" if $speed;
	      show($show, 1);
	  }
      }
      else {
	  show( fbytes($size) . " received");
      }
  }
);

if (fileno(FILE)) {
    close(FILE) || die "Can't write to $file: $!\n";

    show("");  # clear text
    print "\r";
    print fbytes($size);
    print " of ", fbytes($length) if defined($length) && $length != $size;
    print " received";
    my $dur = time - $start_t;
    if ($dur) {
	my $speed = fbytes($size/$dur) . "/sec";
	print " in ", fduration($dur), " ($speed)";
    }
    print "\n";

    if (my $mtime = $res->last_modified) {
	utime time, $mtime, $file;
    }

    if ($res->header("X-Died") || !$res->is_success) {
	if (my $died = $res->header("X-Died")) {
	    print "$died\n";
	}
	if (-t) {
	    print "Transfer aborted.  Delete $file? [n] ";
	    my $ans = <STDIN>;
	    if (defined($ans) && $ans =~ /^y\n/) {
		unlink($file) && print "Deleted.\n";
	    }
	    elsif ($length > $size) {
		print "Truncated file kept: ", fbytes($length - $size), " missing\n";
	    }
	    else {
		print "File kept.\n";
	    }
            exit 1;
	}
	else {
	    print "Transfer aborted, $file kept\n";
	}
    }
    exit 0;
}

# Did not manage to create any file
print "\n" if $shown;
if (my $xdied = $res->header("X-Died")) {
    print "$progname: Aborted\n$xdied\n";
}
else {
    print "$progname: ", $res->status_line, "\n";
}
exit 1;


sub fbytes
{
    my $n = int(shift);
    if ($n >= 1024 * 1024) {
	return sprintf "%.3g MB", $n / (1024.0 * 1024);
    }
    elsif ($n >= 1024) {
	return sprintf "%.3g KB", $n / 1024.0;
    }
    else {
	return "$n bytes";
    }
}

sub fduration
{
    use integer;
    my $secs = int(shift);
    my $hours = $secs / (60*60);
    $secs -= $hours * 60*60;
    my $mins = $secs / 60;
    $secs %= 60;
    if ($hours) {
	return "$hours hours $mins minutes";
    }
    elsif ($mins >= 2) {
	return "$mins minutes";
    }
    else {
	$secs += $mins * 60;
	return "$secs seconds";
    }
}


BEGIN {
    my @ani = qw(- \ | /);
    my $ani = 0;

    sub show
    {
        my($mess, $show_ani) = @_;
        print "\r$mess" . (" " x (75 - length $mess));
	print $show_ani ? "$ani[$ani++]\b" : " ";
        $ani %= @ani;
        $shown++;
    }
}

sub usage
{
    die "Usage: $progname [-a] <url> [<lpath>]\n";
}
