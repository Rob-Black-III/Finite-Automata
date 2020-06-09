# File:  t2.d
# DFA
# Q_ - the set of states
q1 q1-q2-q3-q4 q1-q4 q1-q3-q4 q1-q3 q1-q2-q3 
# Sigma_ - the alphabet
0 1 
# q_0_ - the start state
q1
# F_ - the set of accept states
q1-q4 q1-q3-q4 q1-q2-q3-q4 
# delta_ - the transition function
q1-q3  0 q1
q1  1 q1-q2-q3
q1-q2-q3  1 q1-q2-q3-q4
q1-q2-q3-q4  0 q1-q3-q4
q1-q3  1 q1-q2-q3-q4
q1-q4  0 q1-q4
q1  0 q1
q1-q3-q4  0 q1-q4
q1-q4  1 q1-q2-q3-q4
q1-q2-q3  0 q1-q3
q1-q3-q4  1 q1-q2-q3-q4
q1-q2-q3-q4  1 q1-q2-q3-q4
