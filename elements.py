import json
from dataclasses import dataclass, field

# a module including the knights, items and the positions


@dataclass
class Pos:
    #This represents a 'square' on the board.

    y: int
    x: int
    knight: dict = None
    items: list = field(default_factory=list)

    def __repr__(self):
        return '[{}, {}]'.format(self.y, self.x)

    def to_json(self):
        return [self.y, self.x]


@dataclass
class Item:
    name: str
    priority: int  # A,M,D,H -> 4,3,2,1
    pos: Pos
    attack: int
    defence: int


STATUS_OPTS = ('LIVE', 'DEAD', 'DROWNED')


@dataclass
class Knight:
    id: str  # One of: R,G,B,Y
    colour: str
    pos: Pos
    status: str = STATUS_OPTS[0]
    equipped: Item = None
    base_attack: int = 1
    base_defence: int = 1

    def update_status(self, idx):
        self.status = STATUS_OPTS[idx]
