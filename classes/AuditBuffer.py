from classes.ListWithPaths import ListWithPaths


class AuditBuffer:
    def __init__(self):
        self._items = []
        self._features = []

    def add(self, item, features):
        self._items.append(item)
        self._features.append(features)

    def get_features(self, item):
        index = self.find(item)
        if index is not None:
            return self._features[self.find(item)]
        else:
            return None

    def find(self, target):
        for i in range(len(self._items)):
            if self._items[i] == target:
                return i
        return None

    def get_items(self):
        return self._items