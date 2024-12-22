class PathTracker:
    def __init__(self):
        self.path = []

    def record(self, state, position):
        self.path.append((state, position))

    def getPath(self):
        return self.path

