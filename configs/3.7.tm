# Example 3.7 from Sipser
# This machine accepts strings of 0-s with a length that is a power of 2
# Example: 0, 00, 0000, 00000000
# All others are rejected
# States
Q1 Q2 Q3 Q4 Q5 QAccept QReject
# Sigma
0
# Gamma
0 x u
# Start State
Q1
# Accept State
QAccept
# Reject State
QReject

# delta
Q1 u QReject u R
Q1 x QReject x R
Q1 0 Q2      u R
Q2 u QAccept u R
Q2 x Q2      x R
Q2 0 Q3      x R
Q3 x Q3      x R
Q3 0 Q4      0 R
Q3 u Q5      u L
Q4 0 Q3      x R
Q4 x Q4      x R
Q4 u QReject u R
Q5 u Q2      u R
Q5 0 Q5      0 L
Q5 x Q5      x L
###
