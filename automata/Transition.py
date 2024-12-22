from automata.SymbolVector import SymbolVector


class Transition:
    def __init__(self, fromState, vector, targetState):
        self.symbolsVector = SymbolVector(vector)
        self.targetState = targetState
        self.fromState = fromState

    # def __init__(self,k,alphabeta):
    #     self.fromState = int(input("please enter from state: "))
    #     self.targetState = int(input("please enter target state:"))
    #     self.symbolsVector = SymbolVector(k, alphabeta)




