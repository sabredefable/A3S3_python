class ListWithPaths():
    def __init__(self):
        self.names = []
        self.paths = []
        self._index = 0

    def add(self, name, path):
        self.names.append(name)
        self.paths.append(path)

    def get(self, position):
        #returns a list with both the name and the path to the position'th element
        return [self.names[position], self.paths[position]]

    def findPath(self, name):
        index = self.names.index(name)
        if index > -1:
            return path[index]
        else:
            return None

    def has(self, name):
        isInNames = False
        for x in self.names:
            if name in x:
                isInNames = True
                break
        return isInNames

    def getSubPackages(self, name, allArguments = False):
        instances = []
        if allArguments:
            for x in self.names:
                if name in x:
                    instances.append([x, self.paths[self.names.index(x)]])
        else:
            for x in self.names:
                if name in x:
                    instances.append(x)

        return instances



    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            result = self.names
            self._index += 1
            return result
        elif self._index == 1:
            result = self.paths
            self._index += 1
            return result
        else:
            # Termine l'itération
            raise StopIteration