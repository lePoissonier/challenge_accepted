from pathlib import Path
from json import dumps
from arena import Arena
from elements import Item, Knight


class Serialize:
    @staticmethod
    def read_moves():
        """
        Read moves from file and output instructions.
        """
        _contents = Path('./moves.txt').read_text()
        moves = _contents.strip().split('\n')
        if moves[0] == 'GAME-START':
            moves.pop(0)
        if moves[-1] == 'GAME-END':
            moves.pop()
        return tuple(tuple(m.split(':')) for m in moves)

    @staticmethod
    def serialize_gamestate(knights: list, items: list):
        result = {}

        for k in knights:
            k_result = (k.pos.to_json() if k.pos else None, k.status)
            if k.equipped:
                k_result += (
                    k.equipped.name,
                    k.base_attack + k.equipped.attack,
                    k.base_defence + k.equipped.defence,
                )
            else:
                k_result += (None, k.base_attack, k.base_defence)
            result[k.colour] = k_result

        for i in items:
            i_result = (i.pos.to_json(), i.pos.knight is not None)
            result[i.name] = i_result

        return result

    @staticmethod
    def commit_to_fs(state):
        return Path('./final_state.json').write_text(dumps(state))



class RunGame:
    def setup_board(self):
        """
        Setup initial board with: knights, items, and positions.
        """
        self.arena = Arena()
        ab = self.arena.board

        self.R = Knight('R', 'red', ab[0][0])
        self.Y = Knight('Y', 'yellow', ab[0][7])
        self.B = Knight('B', 'blue', ab[7][0])
        self.G = Knight('G', 'green', ab[7][7])

        ab[0][0].knight = self.R
        ab[0][7].knight = self.Y
        ab[7][0].knight = self.B
        ab[7][7].knight = self.G

        self.item_axe = Item('Axe', 4, ab[2][2], 2, 0)
        self.item_dagger = Item('Dagger', 2, ab[2][5], 1, 0)
        self.item_magicstaff = Item('MagicStaff', 3, ab[5][2], 1, 1)
        self.item_helmet = Item('Helmet', 1, ab[5][5], 0, 1)

        ab[2][2].items.append(self.item_axe)
        ab[2][5].items.append(self.item_dagger)
        ab[5][2].items.append(self.item_magicstaff)
        ab[5][5].items.append(self.item_helmet)

        return (
            self.arena,
            self.R,
            self.Y,
            self.B,
            self.G,
            self.item_axe,
            self.item_dagger,
            self.item_magicstaff,
            self.item_helmet,
        )

    def run_instructions(self):
        instructions = Serialize.read_moves()

        for (knight_id, direction) in instructions:
            knight = getattr(self, knight_id)
            self.arena.move_knight(knight, direction)


if __name__ == '__main__':
    game = RunGame()

    (
        arena,
        kR,
        kY,
        kB,
        kG,
        item_axe,
        item_dagger,
        item_magicstaff,
        item_helmet,
    ) = game.setup_board()

    game.arena.render()

    game.run_instructions()

    game.arena.render()

    state = Serialize.serialize_gamestate((kR, kY, kB, kG), (item_axe, item_dagger, item_magicstaff, item_helmet))
    Serialize.commit_to_fs(state)

