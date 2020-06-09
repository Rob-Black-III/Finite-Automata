#File: 3.9.tm
#Example 3.9 from Sipser
#Accepts strings of the form w#w where w in {0,1}*
Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 QAccept QReject
0 1 #
0 1 # x u
Q1
QAccept
QReject
Q1 0 Q2      x R
Q1 1 Q3      x R
Q1 # Q8      # R
Q2 0 Q2      0 R
Q2 1 Q2      1 R
Q2 # Q4      # R
Q3 0 Q3      0 R
Q3 1 Q3      1 R
Q3 # Q5      # R
Q4 x Q4      x R
Q4 0 Q6      x L
Q5 x Q5      x R
Q5 1 Q6      x L
Q6 0 Q6      0 L
Q6 1 Q6      1 L
Q6 x Q6      x L
Q6 # Q7      # L
Q7 0 Q7      0 L
Q7 1 Q7      1 L
Q7 x Q1      x R
Q8 x Q8      x R
Q8 u QAccept u R
