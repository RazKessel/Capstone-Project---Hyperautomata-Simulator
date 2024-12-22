
class Simulation:
    def __init__(self, tapes, history = None, currentState = 0):
        self.currentState = currentState
        self.tapes = tapes
        self.history = history if history is not None else [[0] * (len(tapes) + 1)]
        self.id = self.__hash__()

    def __hash__(self):
        return hash(tuple(self.history[-1]))

    def __eq__(self, other):
        return self.id == other.id

    # def stepForward(self):
    #     #יוצרים מערך של כל הסמלים במיקומם הנוכחי של הטייפים
    #     #יוצרים רשימה של כל הטרנזקציות אותם אנחנו לוקחים מהסט טרנזקציות עם מפתח  מצב נוכחי
    #     #רצים בלולאה על כל הטרנזקציות ובודקים עם יש התאמה
    #     # אם יש התאמה מעדכנים היסטוריה
    #     #משימות להמשך
    #     #צריך ליצור סימולציה חדשה
    #     #צריך להכניס את החדשה לתור
    #     #זה קורה במנגר
    #     #בסוף הלולאה על הטרנזקציות הסימולציה הנוכחית, כלומר שמסיימים לבדוק את כל האופציוץת האפשריות => להוציא את הסימוצליה הנוכחית מהתור
    #
    #
    #     tapesPositions = [tape.symbol for tape in self.tapes]
    #     transitions = self.automata.transitions.get(self.current_state, []) #Current State is a key for transitions list
    #
    #     for transition in transitions:
    #         if transition.symbolsVector.matches(tapesPositions): #test in main
    #             self.current_state = transition.target_state
    #             historySnapShot = []
    #             historySnapShot.append(self.current_state)
    #             for pos in tapesPositions:
    #                 historySnapShot.append(pos)
    #             self.history.append(historySnapShot)
    #
    #     return

    # def stepBack(self):
    #     #מחזירים את ההיסטוריה צעד אחד אחורה
    #     #מעדכנים את המיקומים בטייפים בהתאם להיסטוריה האחרונה
    #     self.history.pop()
    #     snapShot = self.history[-1]
    #     self.currentState = snapShot[0]
    #     i = 1
    #     for tape in self.tapes:
    #         tape.currentPos = snapShot[i]
    #         i+=1
    #





