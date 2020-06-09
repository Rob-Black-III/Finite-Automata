"""
Author: Rob Black rdb5063@rit.edu
DFA Project - Creates a machine based on a file specified as input.
The user can input strings and can see if the string is accepted or denied
by the machine.
"""

"""
fileParse parses a raw file and creates the appropriate data structures
for a five tuple DFA to use.

@param lines: The lines of the file, pre-processed to remove comments and whitespaces
@return (q, sigma, trans, s, f): A five tuple consisting of all required parameters
of a DFA.
"""
def fileParse(lines):
    q = set()
    sigma = set()
    trans = dict()
    s = ""
    f = set()
    allNodes = lines[0].split(" ")
    for node in allNodes:
        q.add(node)
    print("Q = " + str(q))
    
    alphabet = lines[1].split(" ")
    for character in alphabet:
        sigma.add(character)
    print("Sigma = " + str(sigma))

    s = lines[2]
    print("s = " + s)

    #''.join(string_with_whitespace.split()) 

    acceptStates = lines[3].split(" ")
    for state in acceptStates:
        f.add(state)
    print("F = " + str(f))

    for i in range(4,len(lines)):
        transLine = lines[i].split(" ")
        key = transLine[0] + "," + transLine[1]
        trans[key] = transLine[2]
        print("transition: (" + key + ") -> " + trans[key])
        
    return (q, sigma, trans, s, f)

"""
runMachine processes a string through a given machine, and tells the user if the string
was accepted or denied by the process.

@param testString: A string to be tested through the string. Assumed to contain only
characters in the alphabet for the machine. No error checking for the other case.
@param machine: A five-tuple specifying the specific machine to use.
"""
def runMachine(testString,machine):
    currentNode = machine[3]
    #Checks for empty string
    if(testString == ""):
        pass
    #Checks for trace mode
    elif(testString[0] == "!"):
        for i in range(1,len(testString)):
            oldCurrentNode = currentNode;
            currentNode = machine[2][str(currentNode) + "," + str(testString[i])]
            print(str(oldCurrentNode) + "," + str(testString[i]) + " -> " + str(currentNode))
    #Else, uses default mode
    else:
        for i in range(0,len(testString)):
            currentNode = machine[2][str(currentNode) + "," + str(testString[i])]
    #Checks if the final/current node is in the set of accept states.
    if(currentNode in machine[4]):
        return "accept"
    else:
        return "reject"

"""
Main function. Contains basic preprocessing, input checking, and formatting
so the other helper functions may perform as expected.
"""
def main():
    filename = input("Enter a filename containing a DFA: ")
    with open(filename, 'r') as file:
        #lines = file.readlines()
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
    print("DFA Specification File: " + filename)
    print()

    #Calls function that converts raw lines to a five tuple.
    machineTuple = fileParse(lines)
    print("------------------")

    while(True):
        testString = input("--> ")
        #Checks for exit case, else runs the machine
        if(testString == "."):
            print("goodbye")
            break;
        else:
            print(runMachine(testString, machineTuple))
            

if __name__ == '__main__':
    main()
