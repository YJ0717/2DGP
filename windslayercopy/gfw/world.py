##월드 관련

from pico2d import *
import gfw

class World:
    def __init__(self, layer_count=1):
        if isinstance(layer_count, list):
            layer_names = layer_count
            layer_count = len(layer_count)
            index = 0
            self.layer = lambda: None
            for name in layer_names:
                self.layer.__dict__[name] = index
                index += 1

        self.objects = [[] for i in range(layer_count)]

    def append(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].append(go)

    def remove(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].remove(go)

    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[] for i in range(layer_count)]

    def update(self):
        for go in self.all_objects():
            go.update()

    def draw(self):
        for go in self.all_objects():
            go.draw()

    def all_objects(self):
        for objs in self.objects:
            for i in range(len(objs) - 1, -1, -1):
                yield objs[i]

    def objects_at(self, layer_index):
        objs = self.objects[layer_index]
        for i in range(len(objs) - 1, -1, -1):
            yield objs[i]

    def count_at(self, layer_index):
        return len(self.objects[layer_index])

    def count(self):
        return sum(len(a) for a in self.objects)
