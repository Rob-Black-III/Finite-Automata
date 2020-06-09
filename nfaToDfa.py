"""
nfaToDfa.py
@author: Rob Black rdb5063@rit.edu
"""

"""
DFA represents an DFA, encompassing all requirements for a formal definition
"""
class DFA:
    def __init__(self, allStates, alphabet, transitionFunction, startState, acceptStates):
        self.allStates = allStates
        self.alphabet = alphabet
        self.transitionFunction = transitionFunction
        self.startState = startState
        self.acceptStates = acceptStates

"""
NFA represents an NFA, encompassing all requirements for a formal definition
"""
class NFA:
    def __init__(self, allStates, alphabet, transitionFunction, startState, acceptStates):
        self.allStates = allStates
        self.alphabet = alphabet
        self.transitionFunction = transitionFunction
        self.startState = startState
        self.acceptStates = acceptStates

"""
Queue is a helper data structure.
Used in processing transitions
"""
class Queue:
    def __init__(self):
        self.items = []

    def getElements(self):
        return self.items

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

"""
getLinesForNFAFromFilename parses the file
into a list, skipping comments and removing
newline characters.
@param filename: name of NFA file to parse.
@return lines: list of NFA definition
"""
def getLinesForNFAFromFilename(filename):
    with open(filename, 'r') as file:
        lines = list()
        #Preprocessing of lines
        for line in file:
            #Handles comments
            if(line[0] == "#"):
                pass
            else:
                lines.append(line)
    #Strips newline characters
    lines = [x.strip() for x in lines]
    return lines

"""
createNFA creates an NFA from a list of lines
@param lines: lines outlining the formal definiion of
an nfa
@return myNfa: NFA stucture
"""
def createNFA(lines):
    q = set()
    sigma = set()
    trans = dict()
    s = ""
    f = set()

    #Q - The set of States
    allNodes = lines[0].split(" ")
    for node in allNodes:
        q.add(node)

    #Sigma - the alphabet
    if(lines[1].split(" ")[0] == "@"):
        sigma.add('@')
        pass
    else:
        alphabet = lines[1].split(" ")
        
    for character in alphabet:
        sigma.add(character)

    #The start state
    s = lines[2]

    #F - the set of accept states
    acceptStates = lines[3].split(" ")
    for state in acceptStates:
        f.add(state)

    #The transition function
    for i in range(4,len(lines)):
        transLine = lines[i].split(" ")
        curNode = transLine[0]
        finalNodes = transLine[2:]
        key = curNode + "," + transLine[1]
        if key in trans:
            pass
        else:
            trans[key] = set()
        
        for node in finalNodes:
            (trans[key]).add(node)

        if '.' in transLine:
            sigma.add('.')

    myNfa = NFA(q,sigma,trans,s,f)
    return myNfa

"""
createDFAFromNFA converts and NFA structure to a DFA structure
via the helper functions below
@return DFA: A DFA structure
"""
def createDFAFromNFA(myNFA):
    dfaAllStatesAsList = getPowersetAsList(myNFA.allStates)
    dfaAllStates = convertPowerset(dfaAllStatesAsList) #GOOD
    dfaAlphabet = convertAlphabet(myNFA.alphabet) #GOOD
    dfaStartState = reachability(myNFA.startState,myNFA.transitionFunction) #GOOD
    dfaAcceptStates = createDFAAcceptStates(dfaAllStates,myNFA.acceptStates) #GOOD
    dfaTransitionFunction = createDFATransitionFunction(dfaStartState,myNFA.transitionFunction,dfaAlphabet)

    return DFA(dfaAllStates,dfaAlphabet,dfaTransitionFunction,dfaStartState,dfaAcceptStates)

"""
createDFATransitionFunction creates the transition function for the DFA
@param startStateDFA: the start state of the DFA
@param transitionFunctionNFA: the transitionFunction for the NFA
@param alphabetDFA: the alphabet of the DFA
@return transitionFunction DFA: the transitionFunction for the DFA
"""
def createDFATransitionFunction(startStateDFA, transitionFunctionNFA,alphabetDFA):
    transitionFunctionDFA = dict()
    processedStates = set()
    statesToProcess = list()
    statesToProcess.append(startStateDFA)

    while(len(statesToProcess) != 0):
        state = statesToProcess.pop(0)
        processedStates.add(state)

        for alphabetChar in alphabetDFA:
            newState = getNewState(state,alphabetChar, transitionFunctionNFA)

            #put the empty symbol
            if(state == set()):
                state = '@'
            if(newState == ''):
                newState = '@'
                
            key = state + ',' + alphabetChar
            
            transitionFunctionDFA[str(key)] = str(newState)
            #print("trans (" + str(key) + ") --> " + str(transitionFunctionDFA[key]))
            
            if(newState not in processedStates and newState not in statesToProcess):
                statesToProcess.append(newState)

    print(transitionFunctionDFA)
    return transitionFunctionDFA

"""
getNewState gets a new state for the transition function
@param state: the current state
@param alphabetChar: the character with the transition
@param transitionFunctionNFA: the transiton function
@return setItem: a new state in string form
"""
def getNewState(state, alphabetChar, transitionFunctionNFA):
    r = set(state.split('-'))
    result = set()
    for state in r:
        key = state + ',' + alphabetChar
        if(key in transitionFunctionNFA.keys()):
            listOfStates = transitionFunctionNFA[key]
            for s in listOfStates:
                epsilonClosure = reachability(s, transitionFunctionNFA)
                result.add(epsilonClosure)

    newState = set(sorted(list(result)))

    finalSet = set()
    for item in result:
        item = item.split('-')
        for o in item:
            finalSet.add(o)

    finalSet = set(sorted(list(finalSet)))

    counter = 1
    setItem = ''
    for item in finalSet:
        if(counter == 1):
            setItem += str(item)
        else:
            setItem += '-' + str(item)
        counter+=1

    #return string form
    return setItem

"""
createDFAAcceptStates creates the set of accept states for the DFA
@param allStatesDFA: all the states of the DFA
@param acceptStatesNFA: all the accept states of the NFA
@return acceptStatesDFA: all the accept states of the DFA
"""
def createDFAAcceptStates(allStatesDFA,acceptStatesNFA):
    acceptStatesDFA = set()
    allIndividualStates = list()
    for dfaState in allStatesDFA:
        dfaStateStripped = (list)(dfaState.strip('-'))
        for a in acceptStatesNFA:
            if(a in dfaStateStripped):
                acceptStatesDFA.add(dfaState)
    if acceptStatesDFA == set():
        return acceptStatesNFA
    return acceptStatesDFA

"""
reachability is the epsilon closure function implementation
@param stateNFA: the current state of the NFA
@param transitionFunctionNFA: the transiton function
@return setItem: a new state in string form
"""
def reachability(stateNFA, transitionFunctionNFA):
    validStates = set()
    nodesToProcess = Queue()
    nodesToProcess.enqueue(stateNFA)
    while(1):
        if(nodesToProcess.size() <= 0):
            break;
        node = nodesToProcess.dequeue()
        validStates.add(node)
        transition = str(node) + ',.'
        #if epsilon, check, else, return stateNFA
        if(transition in transitionFunctionNFA.keys()):
            nodesToGoTo = transitionFunctionNFA[transition]
            for curNode in nodesToGoTo:
                if(curNode not in nodesToProcess.getElements() and (curNode not in validStates)):
                    nodesToProcess.enqueue(curNode)

    setItem = ''
    counter = 1
    for item in validStates:
        if(counter == 1):
            setItem += item
        else:
            setItem += '-' + item
        counter+=1
    return setItem

"""
getPowersetAsList gets the powerset of a set
@param s: a set
@return r: powerset of s in a list
"""
def getPowersetAsList(s):
    r = [[]]
    for e in s:
        r += [x+[e] for x in r]
    return r

"""
convertAlphabet creates an alphabet for the DFA from the NFA
@param alphabetNFA: the alphabet of the NFA
@return alphabetCopy: the alphabet of the soon-to-be DFA.
"""
def convertAlphabet(alphabetNFA):
    alphabetCopy = alphabetNFA.copy()
    try:
        alphabetCopy.remove('.')
    except KeyError:
        pass
    return alphabetCopy

"""
convertPowerset converts a powerset of states
to a form in which the DFA can read it.
@param powerSetAsList: converted base set 's' through powerSetAsList(s)
@return dfaAllStatesAsSet: all states of the new DFA
"""
def convertPowerset(powersetAsList):
    dfaAllStatesAsSet = set()
    for element in powersetAsList:
        if(not element):
            dfaAllStatesAsSet.add('@')
        else:
            setItem = ''
            counter = 1
            for item in element:
                if(counter == 1):
                    setItem += item
                else:
                    setItem += '-' + item
                counter+=1
            dfaAllStatesAsSet.add(setItem)
    #print(dfaAllStatesAsSet)
    return dfaAllStatesAsSet

"""
printNFA encapsulates all aspect of the NFA to print to STDOUT
@param myNFA: NFA Structure
@return void
"""
def printNFA(myNFA):
    print("NFA: ")
    print("Q = " + str(set(sorted(myNFA.allStates))))
    print("Sigma_e = " + str(set(sorted(myNFA.alphabet))))
    print("delta = " + str(myNFA.transitionFunction))
    print("s = " + str(myNFA.startState))
    print("F = " + str(set(sorted(myNFA.acceptStates))))

"""
printDFA encapsulates all aspect of the DFA to print to STDOUT
@param myDFA: DFA Structure
@return void
"""
def printDFA(myDFA):
    print("DFA: ")
    print("Q_ = " + str(set(sorted(myDFA.allStates))))
    print("Sigma_ = " + str(set(sorted(myDFA.alphabet))))
    print("delta_ = " + str(myDFA.transitionFunction))
    print("s_ = " + str(myDFA.startState))
    print("F_ = " + str(set(sorted(myDFA.acceptStates))))

"""
writeDFAToFile writes the DFA to a file in specified format,
so that other DFA machines can read it.
@param myDFA: DFA Structure
@param filename: filename of output file as string.
@return void
"""
def writeDFAToFile(myDFA,filename):
    print("Writing to file: " + filename)
    f = open(filename, "w")
    f.write("# File: " + filename + ": \n")
    f.write("# DFA\n")
    
    f.write("#" + ": Q_ - the set of states\n")
    for state in myDFA.allStates:
        f.write(str(state) + " ")
    f.write("\n")
    
    #f.write("Q_ = " + str(sorted(myDFA.allStates)) + "\n")
    f.write("#" + ": Sigma_ - the alphabet\n")
    for state in myDFA.alphabet:
        f.write(str(state) + " ")
    f.write("\n")

    f.write("#" + ": q_0_ - the start state\n")
    f.write(str(myDFA.startState) + "\n")

    f.write("#" + ": F_ - the set of accept states\n")
    for state in myDFA.acceptStates:
        f.write(str(state) + " ")
    f.write("\n")
    #f.write("F_ = " + str(sorted(myDFA.acceptStates)) + "\n")

    f.write("#" + ": delta_ - the transition function\n")
    for key,value in myDFA.transitionFunction.items():
        key = key.split(',')
        for item in key:
            f.write(item + " ")
        f.write(value + "\n")
    
    f.close()

"""
main is used as a concise structure of the program.
Its' purpose is to call helper functions to create the NFA
and DFA, ask for input, etc.
"""
def main():
    filename = input("Enter a filename containing an NFA: ")
    lines = getLinesForNFAFromFilename(filename)
    myNFA = createNFA(lines)
    newDFA = createDFAFromNFA(myNFA)

    printNFA(myNFA)
    printDFA(newDFA)

    filename = input("Enter a filename output the DFA: ")
    writeDFAToFile(newDFA,filename)
    
    print("------------------")


if __name__ == "__main__":
    main()
