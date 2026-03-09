from wfc import WF
from typing import TypeVar, override


T = TypeVar('T', bound=WF)

class Extend(WF):
    inner: T

    @override
    def __init__(self):
        super().__init__()
        self.inner = inner

    def wave_function(self, map: Map, pos: Pos, cell: Cell) -> set[tuple[Tile, int]]:
        return { (o, 1) for o in cell.valid_options }
    
    