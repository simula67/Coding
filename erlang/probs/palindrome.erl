-module(palindrome).
-export([pal/1]).
reverse([]) ->    
    [];
reverse([H|T]) ->
    lists:append( reverse(T) , [H] ).
pal(List) ->
    RevList = reverse(List),
    isPal(List,RevList).
isPal([],[]) ->
    true;
isPal([H|T1],[H|T2]) ->
    isPal(T1,T2);
isPal([H1|_],[H2|_]) ->
    false.


