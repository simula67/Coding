-module(total).
-export([total/1]).
total([{What,Num}|T]) ->
    cost:cost(What) * Num + total(T);
total([]) ->
    0.
