-module(thirdlast).
-export([third_last/1]).
third_last(List) ->
    sim_last([] , [] , [] ,List).
sim_last( Curr_head, Last_head, _,[H|T] ) ->
    sim_last( H,Curr_head,Last_head,T );
sim_last(_,_,Third_last,[]) ->
    Third_last.
