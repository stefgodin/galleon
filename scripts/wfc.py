class WF:
    def wave_function(self, map: Map, pos: Pos, cell: Cell) -> set[tuple[Tile, int]]:
        return { (o, 1) for o in cell.valid_options }

    def entropy(self, map: Map, pos: Pos, cell: Cell, wf: set[tuple[Tile, int]]) -> float:
        if (total := sum(w for _, w in wf)) == 0:
            return -1

        return -sum(
            p * log(p) for _, w in wf
            if (p := float(w) / float(total)) > 0
        )

    def take(self, map: Map, pos: Pos, tile: Tile):
        pass

    def after_collapse(self, map: Map, reductions: int):
        pass

    def draw(self, map: Map, entropies: dict[Pos, float], scale: int, screen: pygame.Surface):
        pass

    def draw_on_cell(self, map: Map, pos: Pos, cell: Cell, entropies: dict[Pos, float], screen_pos: Pos, scale: int, screen: pygame.Surface):
        pass


