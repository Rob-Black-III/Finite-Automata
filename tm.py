"""
Author: Rob Black rdb5063@rit.edu
Turing Machine Project - Creates a Turing Machine based on a file specified as input.
The user can input strings and can see if the string is accepted or denied
by the machine.
"""

class TuringMachine:

    """
    Turing Machine constructor, consisting of a 7-tuple based on Sipser's definiton.
    """
    def __init__(self,states,inputAlphabet,tapeAlphabet,transitionFunction,startState,acceptState,rejectState):
        self.states = states
        self.inputAlphabet = inputAlphabet
        self.tapeAlphabet = tapeAlphabet
        self.transitionFunction = transitionFunction
        self.startState = startState
        self.acceptState = acceptState
        self.rejectState = rejectState

    """
    Main TM Loop. Asks for input until no characters are entered.
    """
    def run(self):
        while(True):
            testString = input("--> ")
            #Checks for exit case, else runs the machine
            if(not testString):
                print("Goodbye")
                break;
            else:
                self.parseString(testString)

    """
    Runs a string through the machine. Prints each stage of the tape
    as the string is parsed.
    """
    def parseString(self, string):
        tape = list(string)
        tapeHead = 0
        print(str(self.startState) + ''.join(tape))
        currentState = self.startState

        #Loop until accept or reject. Checked later.
        while(True):

            #Check for halt condition
            if(currentState == self.acceptState or currentState == self.rejectState):
                break;

            #Check for a transition
            for key in self.transitionFunction:
                splitKey = key.split(',')
                if(splitKey[0] == currentState and splitKey[1] == tape[tapeHead]):

                    """
                    print()
                    print("Current State: " + currentState)
                    print("Current TapeHead Position: " + str(tapeHead))
                    print("Current TapeChar: " + tape[tapeHead])
                    """

                    splitValue = self.transitionFunction[key].split(',')

                    """
                    print("Writing " + splitValue[1] + " to tape[" + str(tapeHead) + "]")
                    """
                    #Write value to tape.
                    tape[tapeHead] = splitValue[1]

                    #Move Tape Head
                    if(splitValue[2] == 'L'):
                        #Check if at left of tape, else decrease.
                        if(tapeHead == 0):
                            pass
                        else:
                            tapeHead = tapeHead - 1
                    elif(splitValue[2] == 'R'):
                        if(tapeHead >= len(tape)-1):
                            #Extend Tape if needed by adding a 'u' for blank.
                            tape.append('u')
                        tapeHead = tapeHead + 1

                    #Change State
                    currentState = splitValue[0]

                    #Print the tape
                    tapeToPrint = tape.copy()
                    tapeToPrint.insert(tapeHead,currentState)
                    print(''.join(tapeToPrint))
                    break;
            
            #Block executes if no key found (i.e. no transition)
            else:
                #Print the tape
                tapeToPrint = tape.copy()
                tapeToPrint.insert(tapeHead,'QReject')
                print(''.join(tapeToPrint))
                break;


"""
Preprocessing function. 
"""
def createTMFromFilename(filename):
    with open(filename, 'r') as file:
        #lines = file.readlines()
        specification = list()
        #Preprocessing of lines
        for line in file:
            #Handles comments
            if(line[0] == "#" or not line.strip()):
                pass
            else:
                specification.append(line)
    
    #Strips newline characters
    specification = [x.strip() for x in specification]
    print("Turing Machine Specification Filename: " + filename)

    return createTM(specification)


"""
Parses a plaintext representation of a Turing Machine and returns
a Turing Machine object.
"""
def createTM(lines):
    states = set()
    inputAlphabet = set()
    tapeAlphabet = set()
    transitionFunction = dict()
    startState = None
    acceptState = None
    rejectState = None

    #Add all TM states to "states" set.
    allNodes = lines[0].split(" ")
    for node in allNodes:
        states.add(node)

    #Add input alphabet to "inputAlphabet" set.
    iAlphabet = lines[1].split(" ")
    for character in iAlphabet:
        inputAlphabet.add(character)

    #Add tape alphabet to "tapeAlphabet" set.
    tAlphabet = lines[2].split(" ")
    for character in tAlphabet:
        tapeAlphabet.add(character)

    #Read start, accept, and reject states and assign to variables.
    startState = lines[3]
    acceptState = lines[4]
    rejectState = lines[5]

    #Read transition function and assign each transition to a dictionary (key,value) pair.
    for i in range(6,len(lines)):

        #Normalize the input so all values are separated by a single space.
        transition = " ".join(lines[i].split())
        transition = transition.split(" ")

        if(transition[0] in states and transition[1] in tapeAlphabet):
            transKey = (transition[0] + ',' + transition[1])
        else:
            print("Unrecognized symbol in transition key.")
            continue;

        if(transition[2] in states and transition[3] in tapeAlphabet):
            transValue = (transition[2] + ',' + transition[3] + ',' + transition[4])
            transitionFunction[transKey] = transValue
        else:
            print("Unrecognized symbol in transition value.")
            continue;

    """
    print("TRANSITION FUNCTION")
    for key in transitionFunction.keys():
        print(key + ": " + transitionFunction[key])
    """

    #Return a new Turing Machine
    return TuringMachine(states,inputAlphabet,tapeAlphabet,transitionFunction,startState,acceptState,rejectState)

"""
Main function. Contains basic preprocessing, input checking, and formatting
so the other helper functions may perform as expected.
"""
def main():
    filename = input("Enter a filename containing a Turing Machine: ")
    myTuringMachine = createTMFromFilename(filename)
    myTuringMachine.run()

if __name__ == '__main__':
    main()
