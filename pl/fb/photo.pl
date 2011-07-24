#!/usr/bin/perl
use WWW::Facebook::API;
use Data::Dumper;
$photoDL_sleep_time = 15;
$photoDL_browser = "/usr/bin/google-chrome";
my $photoDL_client = WWW::Facebook::API->new(
    desktop => 1,
    secret => '3a79eb30d270e56b4443be7b49a7e047',
    api_key => '22fc31e248c8f7a017972ce8092b23eb',
    parse => 1,
    );
#$token = $client->auth->login(browser => "$browser",sleep => $sleep_time);
$photoDL_token = $photoDL_client->auth->create_token;
$photoDL_client->auth->get_session($photoDL_token);
print "Token obtained : $photoDL_token";
#my $friends_perl = $client->friends->get_lists();
#print Dumper $friends_perl;
