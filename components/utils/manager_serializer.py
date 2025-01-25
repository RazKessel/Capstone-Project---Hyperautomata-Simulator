from backend.manager import Manager
from backend.tape import Tape
from backend.simulation import Simulation

def serialize_manager(manager):
    if not manager:
        return None
    tapes_data = []
    for t in manager.tapes:
        tapes_data.append(t.symbols)
    sim_current_state = manager.sim.currentState
    sim_history = manager.sim.history
    return {
        'tapes': tapes_data,
        'sim_currentState': sim_current_state,
        'sim_history': sim_history
    }
    
def deserialize_manager(data, automata):
    if not data:
        return None

    tapes_list = []
    for tape_symbols in data.get('tapes', []):
        tapes_list.append(Tape(tape_symbols))
    mgr = Manager(automata, tapes_list)
    sim_curr_state = data.get('sim_currentState', 0)
    sim_history = data.get('sim_history', [])
    sim = Simulation(tapes_list, sim_history, sim_curr_state)
    mgr.sim = sim
    mgr.visited = {sim}
    mgr.queue = [sim]
    return mgr