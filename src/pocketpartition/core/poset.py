from functools import lru_cache

class Poset:
    _instances:dict = dict()  # Class-level dictionary to hold instances

    def __new__(cls, elements, relations):
        key = (frozenset(elements), frozenset(tuple(rel) for rel in relations))
        if key not in cls._instances:
            instance = super(Poset, cls).__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, elements=None, relations=None):
        self._elements = frozenset(elements) if elements else frozenset()
        self._relations = frozenset(relations) if relations else frozenset()
        self._validate_poset()

    @property
    def elements(self):
        return self._elements
    
    @property
    def relations(self):
        return self._relations
    
    def __repr__(self):
        return f"Poset with {len(self._elements)} elements and {len(self._relations)} relations"

    def __str__(self):
        return self.__repr__()

    def _validate_poset(self):
        self._check_reflexivity()
        self._check_antisymmetry()
        self._check_transitivity()

    def add_element(self, element):
        new_elements = self._elements.union({element})
        new_relations = self._relations.union({(element, element)})  # Reflexivity
        return Poset(new_elements, new_relations)

    def add_relation(self, a, b):
        if a in self._elements and b in self._elements:
            new_relations = self._relations.union({(a, b)})
            new_poset = Poset(self._elements, new_relations)
            return new_poset
        else:
            raise ValueError("Both elements must be in the poset.")

    def _check_reflexivity(self):
        for element in self._elements:
            if (element, element) not in self._relations:
                raise ValueError(f"Reflexivity violated for element: {element}")

    def _check_antisymmetry(self):
        for (a, b) in self._relations:
            if (b, a) in self._relations and a != b:
                raise ValueError(f"Antisymmetry violated for pair: ({a}, {b})")

    def _check_transitivity(self):
        for (a, b) in self._relations:
            for (c, d) in self._relations:
                if b == c and (a, d) not in self._relations:
                    raise ValueError(f"Transitivity violated for pairs: ({a}, {b}), ({c}, {d})")
    
    @lru_cache(maxsize=None)
    def cover_relations(self):
        covers = set()
        for (x, y) in self._relations:
            if x != y:  # x < y
                is_cover = True
                for b in self._elements:
                    if b == x or b == y:
                        continue
                    if (x, b) in self._relations and (b, y) in self._relations:
                        is_cover = False
                        break
                if is_cover:
                    covers.add((x, y))
        return covers

    def display(self):
        print("Elements:", self._elements)
        print("Relations:", self._relations)
