-module(kth).
-export([kth_elem/2]).

kth_elem([H|_],1) ->
    H;
kth_elem([],_) ->
    false;
kth_elem([_|T],Num) ->
    kth_elem(T, Num-1 ).

