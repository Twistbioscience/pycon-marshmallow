from fields.mutables import MutableBase, NestedMutableBase
from typing import Dict
from fields.marshmallow_field import MarshmallowJSON
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from marshmallow import Schema, fields, post_load, pre_dump
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4



class Node(NestedMutableBase):
    def __init__(self, id: int, value: str):
        super().__init__()
        self._id = id
        self._value = value

    @property
    def id(self):
        return self._id

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

    def deserialize(self, payload):
        for n in payload['nodes']:
            self._add_node(n['id'], n['value'])
        for e in payload['edges']:
            self._add_edge(e['src_id'], e['dest_id'])

    def serialize(self):
        nodes = [{'id': node.id, 'value': node.value} for node in self._nodes.values()]
        edges = [{'src_id': src_id, 'dest_id': dest_id} for src_id, dest_id in self._edges]
        return {'nodes': nodes, 'edges': edges}

    def get_node(self, id: int) -> Node:
        return self._nodes[id]

    def _add_node(self, id: int, value: str):
        if id in self._nodes:
            raise ValueError('Node id already in this graph')
        n = Node(id, value)
        self._nodes[id] = n

    def add_node(self, id: int, value: str):
        self._add_node(id, value)
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

    def _add_edge(self, src_id: int, dest_id: int):
        if src_id not in self._nodes or dest_id not in self._nodes:
            raise ValueError('Both node ids must be in this graph')
        self._edges.add((src_id, dest_id))

    def add_edge(self, src_id: int, dest_id: int):
        self._add_edge(src_id, dest_id)
        self.changed()

    def remove_edge(self, src_id: int, dest_id: int):
        self._edges.remove((src_id, dest_id))

    def __repr__(self):
        nodes = ', '.join([f'{n.id}: {n.value}' for n in self._nodes.values()])
        edges = ', '.join([f'{src_id, dest_id}' for src_id, dest_id in self._edges])
        return nodes + ' / ' + edges


class NodeSchema(Schema):
    id = fields.Integer()
    value = fields.String()


class EdgeSchema(Schema):
    src_id = fields.Integer()
    dest_id = fields.Integer()


class GraphSchema(Schema):
    nodes = fields.Nested(NodeSchema, many=True)
    edges = fields.Nested(EdgeSchema, many=True)

    @pre_dump
    def dump_graph(self, obj: MiniGraph):
        return obj.serialize()

    @post_load
    def create_graph(self, data):
        g = MiniGraph()
        g.deserialize(data)
        return g


Base = declarative_base()


class ManufacturingPlan(Base):
    __tablename__ = 'plan'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    order_item_id = Column(String)
    graph = Column(MiniGraph.as_mutable(MarshmallowJSON(GraphSchema)))


def main():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/pycon_marshmallow', echo=True)  # Turn on echo to follow sqlalchemy session
    session_maker = sessionmaker(bind=engine)
    session: Session = session_maker()

    plan = ManufacturingPlan(order_item_id='123')
    plan.id = uuid4()
    plan_id = plan.id
    g = MiniGraph()
    g.add_node(1, 'A')
    g.add_node(2, 'B')
    g.add_node(3, 'C')
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    plan.graph = g

    session.add(plan)
    session.commit()

    plan_copy = session.query(ManufacturingPlan).get(plan_id)
    # prints Plan 123 has graph 1: A, 2: B, 3: C / (1, 2), (2, 3)
    print(f'Plan {plan_copy.order_item_id} has graph {plan_copy.graph}')

    plan_copy.graph.add_edge(1, 3)
    plan_copy.graph.get_node(1).value = 'hello'

    session.commit()

    plan_copy2 = session.query(ManufacturingPlan).get(plan_id)
    # prints Plan 123 has graph 1: hello, 2: B, 3: C / (1, 2), (1, 3), (2, 3)
    print(f'Plan {plan_copy2.order_item_id} has graph {plan_copy2.graph}')


if __name__ == "__main__":
    main()




