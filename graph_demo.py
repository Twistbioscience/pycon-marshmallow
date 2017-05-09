from fields.mutables import MutableBase, NestedMutableBase
from typing import Iterable, Dict


class Node(NestedMutableBase):
    def __init__(self, id: int, value: str):
        super().__init__()
        self._id = id
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: str):
        self._value = v
        self.changed()


class MiniGraph(MutableBase):
    def __init__(self):
        self._nodes: Dict[int, Node] = {}
        self._edges = set()

    def get_node(self, id: int) -> Node:
        return self._nodes[id]

    def add_node(self, id: int, value: str):
        if id in self._nodes:
            raise ValueError('Node id already in this graph')
        n = Node(id, value)
        self._nodes[id] = n
        n.register(self)
        self.changed()

    def remove_node(self, id: int):
        if id not in self._nodes:
            raise ValueError('Node is not in this graph')
        # unregister and remove node
        n = self._nodes[id]
        n.unregister(self)
        del self._nodes[id]
        # remove all edges pointing to the removed node
        self._edges = {(src_id, dest_id) for src_id, dest_id in self._edges if src_id != id and dest_id != id}
        self.changed()

    def add_edge(self, src_id: int, dest_id: int):
        if src_id not in self._nodes or dest_id not in self._nodes:
            raise ValueError('Both node ids must be in this graph')
        self._edges.add((src_id, dest_id))
        self.changed()

    def remove_edge(self, src_id: int, dest_id: int):
        self._edges.remove((src_id, dest_id))

