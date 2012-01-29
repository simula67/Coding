-module(times).
-export([times/1,subN/1]).

times(X) ->
    fun(Y) ->
	 X * Y end
	.

subN(N) ->
    fun(Inp) ->
	    Inp - N end
	.
   
