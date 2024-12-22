from automata.Simulation import Simulation
import copy

from automata.Tape import Tape
from automata.Transition import Transition



class Manager:
    def __init__(self, automata,tapes):
        self.automata = automata           # Instance of Automata
        self.tapes = tapes

        self.accepting_states = automata.accept_states
        self.sim = Simulation(self.tapes)
        self.visited = {self.sim}  #set of visited simulatios
        self.queue = [self.sim] # List of active Simulation objects


    def stepTo(self,targetState):
        #נראה לי שהפונקציה הזו צריכה להיות בSIMULATION
        #צריך לשנות את המבנה של האוטומט - המעברים צריכים להיות בסט, ולהוסיף equal לtransition
        sim = self.sim
        possible_transitions = self.automata.transitions.get(targetState)
        '''
        check for all the possible_transitions if there is a transition with targetState == targetState:
            if there is:
                if transition.symbolsVector.matches(tapesCopy):
                update current state
                update history
                create a new simulation
        '''
        return True



    def mainLoop(self):
        '''להוסיף ארגומנט סימולציה כדי להריץ מאמצע אחרי שמוסיפים מילה
        צריך להוסיף מתודה להוספת מילה (שקוראת למתודה אדיט בסימבול ווקטור - מוסיף אות לווקטור)

        '''
        flag = True
        while any(tape.symbol != '#' for tape in self.tapes) \
                and (len(self.queue))>0:
            if flag:
                sim = self.queue.pop(0)
                self.tapes = sim.tapes
                flag = False



            for transition in self.automata.transitions.get(sim.currentState):
                history = sim.history.copy()
                tapesCopy = copy.deepcopy(self.tapes)
                if transition.symbolsVector.matches(tapesCopy):

                    current_state = transition.targetState
                    historySnapShot = []
                    historySnapShot.append(current_state)

                    for tape in tapesCopy:
                        historySnapShot.append(tape.currentPos)

                    history.append(historySnapShot)
                    newSim = Simulation(tapesCopy, history, current_state)
                    if newSim in self.visited:
                        continue
                    else:
                        self.visited.add(newSim)
                        self.queue.append(newSim)

            sim = self.queue.pop(0)
            self.tapes = sim.tapes
            if (sim.currentState in self.accepting_states) and (all(tape.symbol == '#' for tape in self.tapes)):

                print("here is an accapting run...")
                return sim.history


        print("there is no accepting run...")
        return sim.history


    def addTape(self, tape, history):
        automata = self.automata
        for char in tape:
            if char not in automata.alphabet:
                print("The tape is not valid: at least one of its char is not in the alphabet")
                return
        self.setTapes(history[-1])
        self.tapes.append(Tape(tape))

        automata.transitions = {}
        k = len(self.tapes)
        print()
        print("set transitions:")
        automata.add_transition(Transition(0, ['1', '#', '#'], 1))
        automata.add_transition(Transition(0, ['0', '#', '#'], 0))
        automata.add_transition(Transition(0, ['#', '1', '#'], 1))
        automata.add_transition(Transition(0, ['#', '0', '#'], 0))
        automata.add_transition(Transition(0, ['#', '#', '1'], 1))
        automata.add_transition(Transition(0, ['#', '#', '0'], 0))
        automata.add_transition(Transition(1, ['1', '#', '#'], 0))
        automata.add_transition(Transition(1, ['0', '#', '#'], 1))
        automata.add_transition(Transition(1, ['#', '1', '#'], 0))
        automata.add_transition(Transition(1, ['#', '0', '#'], 1))
        automata.add_transition(Transition(1, ['#', '#', '1'], 0))
        automata.add_transition(Transition(1, ['#', '#', '0'], 1))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        # automata.add_transition(Transition(k, automata.alphabet))
        '''edit automata screen
            eventListener -> addTransitions        
        '''
        sim = Simulation(self.tapes,history,history[-1][0])
        self.visited = {sim}  # empty visited
        self.queue = [sim]  # empty queue
        self.sim = sim
        h = self.mainLoop()
        return h

    def setTapes(self, snapShot):
        snapShot = snapShot[1:]
        for i in range(len(snapShot)):
            self.tapes[i].currentPos = snapShot[i]
            if(snapShot[i] >= len(self.tapes[i].symbols)):
                self.tapes[i].symbol = '#'
            else:
                self.tapes[i].symbol = self.tapes[i].symbols[snapShot[i]]
        return

    def stepBack(self,history):
        #מחזירים את ההיסטוריה צעד אחד אחורה
        #מעדכנים את המיקומים בטייפים בהתאם להיסטוריה האחרונה
        history.pop()
        snapShot = history[-1]
        currentState = snapShot[0]
        tapes = self.setTapes(snapShot)
        sim = Simulation(tapes, history, currentState)
        #להסגר על פונקציונליות רצויה ולשכתב את הפוקנציה. לאחר מכן לבדוק.




