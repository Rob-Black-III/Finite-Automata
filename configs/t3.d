# File:  t3.d
# DFA
# Q_ - the set of states
1 @ 3 2 1-4 
# Sigma_ - the alphabet
a b c 
# q_0_ - the start state
1
# F_ - the set of accept states
1 1-4 
# delta_ - the transition function
1-4  a 2
1-4  c @
3  b @
@  a @
2  a 3
1-4  b @
3  a 1-4
3  c @
1  a 2
2  c @
@  c @
@  b @
1  c @
2  b @
1  b @
