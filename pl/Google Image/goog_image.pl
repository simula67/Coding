#!/usr/bin/perl
# Downloads images from a Google Image

use strict;    
use WWW::Google::Images;

# Take the query from the command line.
my $query = join(' ',@ARGV) or die "Usage: $0 <query>\\n";

# Create a new WWW::Google::Images instance.
my $agent = WWW::Google::Images->new(
    server => 'images.google.com');

# Query Google Images.
my $result = $agent->search($query , 
                            limit => 100,
                            iregex => 'jpg'
    );

# Save each image in the result locally, with
# the format [query][count].[extension].
my $count;
while (my $image = $result->next(  )) {
    $count++;
    print $image->content_url(  ) . "\\n";
    print $image->save_content(base => $query . $count) . "\\n\\n";
}
