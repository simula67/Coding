-module(last).
-export([last/1]).
last([_|[T]]) ->
    last([T]);
last([H]) ->
    H;
last([]) ->
    error.

