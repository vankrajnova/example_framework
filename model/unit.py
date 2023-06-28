from enum import Enum


class NodeType(Enum):
    Orgunit = "Подразделение"
    Position = "Должность"


class Node:
    def __init__(self, type, name, oid, hr_id=None):
        self.type = type
        self.name = name
        self.oid = oid
        self.hr_id = hr_id
        self._parent = None
        self._children = []
        self._base_roles = []

    def has_parent(self):
        return self._parent is not None

    def get_parent(self):
        return self._parent

    def has_children(self):
        return len(self._children) > 0

    def get_children(self):
        return self._children

    def add_child(self, unit):
        unit._parent = self
        self._children.append(unit)

    def has_base_roles(self):
        return len(self._base_roles) > 0

    def get_base_roles(self):
        return self._base_roles

    def get_parent_chain_as_lines(self):
        parent_chain = self.get_parent_chain()
        lines = []
        if parent_chain is not None:
            for unit in parent_chain:
                lines.append(unit.name)
        return lines

    def get_parent_chain(self):
        parent_chain = []
        if self.has_parent():
            if self._parent.has_parent():
                parent_chain = self._parent.get_parent_chain()
            parent_chain.append(self._parent)
        return parent_chain

    def calculate_all_base_roles(self):
        all_base_roles = []
        if self.has_base_roles():
            all_base_roles = all_base_roles + self.get_base_roles()
        if self.has_parent():
            all_base_roles = all_base_roles + self._parent.calculate_all_base_roles()
        return all_base_roles



class Position(Node):
    def __init__(self, name, oid=None, hr_id=None):
        Node.__init__(self, NodeType.Position, name, oid, hr_id=hr_id)

    def __eq__(self, other):
        if self.hr_id is not None and other.hr_id is not None:
            return (self.name == other.name) and (self.hr_id == other.hr_id)
        else:
            return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f"Position: name={self.name}, oid={self.oid}, hr_id={self.hr_id}"


class Orgunit(Node):

    def __init__(self, name, full_name=None, oid=None, hr_id=None):
        Node.__init__(self, NodeType.Orgunit, name, oid, hr_id=hr_id)
        if full_name is None:
            self.full_name = name
        else:
            self.full_name = full_name

    def __eq__(self, other):
        if self.hr_id is None:
            return self.name == other.name and self.full_name == other.full_name and self.oid == other.oid
        else:
            return self.name == other.name and self.full_name == other.full_name \
                and self.oid == other.oid and self.hr_id == other.hr

    def __repr__(self):
        return f"Orgunit: name={self.name}, full_name={self.full_name}, oid={self.oid}, hr_id={self.hr_id}"
