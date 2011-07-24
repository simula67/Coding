-module(rev).
-export([rev_list/1, reverse/1]).

rev_list([H|[T|[]]]) ->    
    [T|[H]];
rev_list( [H|T] ) ->
    Rev = rev_list(T),
    [X|Y] = Rev,
    io:format("~n Return ~p ~n",[Rev]),
    [Rev|[H]].

reverse([]) ->
    [];
reverse([H|T]) ->
    lists:append( reverse(T) , [H] ).
