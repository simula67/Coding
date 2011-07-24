-module(last_mod).
-export([sim_last/1]).
sim_last([]) ->
    error;
sim_last( [H|[]] ) ->
    H;
sim_last( [_|T] ) ->
    sim_last(T).
