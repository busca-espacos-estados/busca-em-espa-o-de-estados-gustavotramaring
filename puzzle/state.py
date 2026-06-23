from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutavel de 9 inteiros (0 = espaco vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado invalido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos validos a partir deste estado."""
        row, col = divmod(self.blank_index, 3)
        moves = [
            ("up", -1, 0),
            ("down", 1, 0),
            ("left", 0, -1),
            ("right", 0, 1),
        ]
        children = []

        for action, row_delta, col_delta in moves:
            new_row = row + row_delta
            new_col = col + col_delta

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_index = new_row * 3 + new_col
                new_tiles = list(self.tiles)
                new_tiles[self.blank_index], new_tiles[new_blank_index] = (
                    new_tiles[new_blank_index],
                    new_tiles[self.blank_index],
                )
                children.append(
                    State(
                        tuple(new_tiles),
                        parent=self,
                        action=action,
                        cost=self.cost + 1,
                    )
                )

        return children

    def path(self) -> List["State"]:
        """Retorna a sequencia de estados do estado inicial ate este."""
        states = []
        current: Optional["State"] = self

        while current is not None:
            states.append(current)
            current = current.parent

        return list(reversed(states))

    def actions(self) -> List[str]:
        """Retorna a sequencia de acoes do estado inicial ate este."""
        return [state.action for state in self.path()[1:] if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
