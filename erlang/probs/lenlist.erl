-module(lenlist).
-export([len_list/1, len_acc/1]).
len_list([_]) ->
    1;
len_list([_|T]) ->
    1+len_list(T).
len_acc(List) ->
    len_acc(List,0).
len_acc( [ H|T ] ,Acc ) ->
    len_acc(T,Acc + 1);
len_acc([],Acc) ->
    Acc.
