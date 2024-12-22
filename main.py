# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from automata.Automata import Automata
from automata.Manager import Manager
from automata.Simulation import Simulation
from automata.Tape import Tape
from automata.Transition import Transition


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def mainAlgorithm():
    #initiate new automata
    automata = Automata()
    k = int(input("enter amount of words: "))
    #set automata states
    automata.alphabet.add('0')
    automata.alphabet.add('1')
    automata.add_state(0, True)
    automata.add_state(1)
    automata.set_start_state(0)
    #set transition
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))
    automata.add_transition(Transition(k, automata.alphabet))

    tapes = []
    for i in range(k):
        tapes.append(Tape(input(f"enter tape {i+1}")))



    #2 words case:
    # automata.add_transition(0, ['0', '#'], 0)
    # automata.add_transition(0, ['#', '0'], 0)
    # automata.add_transition(0, ['1', '#'], 1)
    # automata.add_transition(0, ['#', '1'], 1)
    # automata.add_transition(1, ['0', '#'], 1)
    # automata.add_transition(1, ['#', '0'], 1)
    # automata.add_transition(1, ['1', '#'], 0)
    # automata.add_transition(1, ['#', '1'], 0)

    #3 words case:
    # automata.add_transition(0, ['1', '#', '#'], 1)
    # automata.add_transition(0, ['0', '#', '#'], 0)
    # automata.add_transition(0, ['#', '1', '#'], 1)
    # automata.add_transition(0, ['#', '0', '#'], 0)
    # automata.add_transition(0, ['#', '#', '1'], 1)
    # automata.add_transition(0, ['#', '#', '0'], 0)
    # automata.add_transition(1, ['1', '#', '#'], 0)
    # automata.add_transition(1, ['0', '#', '#'], 1)
    # automata.add_transition(1, ['#', '1', '#'], 0)
    # automata.add_transition(1, ['#', '0', '#'], 1)
    # automata.add_transition(1, ['#', '#', '1'], 0)
    # automata.add_transition(1, ['#', '#', '0'], 1)


    # print(automata.alphabet)
    # t1 = Tape("01")
    # t2 = Tape("10")
    # t3 = Tape("11")
    # tapes = [t1, t2, t3]

    # manager = Manager(automata, tapes)
    # print(manager.mainLoop())
    # sim1 = Simulation(automata,tapes)
    # sim2 = Simulation(automata,tapes,[[0,1,0]],1)
    # sims = {sim1,sim2}
    # print(sim1.history)
    # sim3 = Simulation(automata,tapes,[[0,1,0]],1)
    # sim4 = Simulation(automata,tapes,[[0,1,1]],1)
    # print(sim4 in sims)
    tapes[0].currentPos = 1
    tapes[0].symbol = '1'
    sim3 = Simulation(automata, tapes, [[0, 0, 0],[0,1,0]], 0)

def test():
    automata = Automata()
    k = int(input("enter amount of words: "))
    # set automata states
    automata.alphabet.add('0')
    automata.alphabet.add('1')
    automata.add_state(0, True)
    automata.add_state(1)
    automata.set_start_state(0)
    #set transition
    automata.add_transition(Transition(0, ['0', '#'], 0))
    automata.add_transition(Transition(0, ['#', '0'], 0))
    automata.add_transition(Transition(0, ['1', '#'], 1))
    automata.add_transition(Transition(0, ['#', '1'], 1))
    automata.add_transition(Transition(1, ['0', '#'], 1))
    automata.add_transition(Transition(1, ['#', '0'], 1))
    automata.add_transition(Transition(1, ['1', '#'], 0))
    automata.add_transition(Transition(1, ['#', '1'], 0))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))
    # automata.add_transition(Transition(k, automata.alphabet))

    t1 = Tape("01")
    t2 = Tape("10")
    t3 = "11"
    tapes = [t1, t2]
    tapes[0].currentPos = 1
    tapes[0].symbol = '1'
    history = [[0,0,0],[0,1,0]]
    # sim = Simulation(tapes,history,history[0])
    manager = Manager(automata, tapes)
    print(manager.addTape(t3,history))


def test2():
    automata = Automata()
    k = int(input("enter amount of words: "))
    # set automata states
    automata.alphabet.add('0')
    automata.alphabet.add('1')
    automata.add_state(0, True)
    automata.add_state(1)
    automata.set_start_state(0)
    # set transition
    automata.add_transition(Transition(0, ['0', '#'], 0))
    automata.add_transition(Transition(0, ['#', '0'], 0))
    automata.add_transition(Transition(0, ['1', '#'], 1))
    automata.add_transition(Transition(0, ['#', '1'], 1))
    automata.add_transition(Transition(1, ['0', '#'], 1))
    automata.add_transition(Transition(1, ['#', '0'], 1))
    automata.add_transition(Transition(1, ['1', '#'], 0))
    automata.add_transition(Transition(1, ['#', '1'], 0))

    t1 = Tape("01")
    t2 = Tape("10")
    t3 = "11"
    tapes = [t1, t2]
    tapes[0].currentPos = 1
    tapes[0].symbol = '1'
    history = [[0, 0, 0], [0, 1, 0]]
    # sim = Simulation(tapes,history,history[0])
    manager = Manager(automata, tapes)
    manager.stepBack()
    print(manager)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
