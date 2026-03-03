import pygame

class UIElement:
    pass

class UIState:
    ui_elements: list[UIElement]

def align_in_grid(render_elements: list[list[pygame.Surface|None]], row_padding = 0, col_padding = 0, margin = 0):
    col_count = render_elements[0].__len__() if render_elements.__len__() else 0
    row_count = render_elements.__len__()
    columns_w = [0] * col_count
    row_h = 0
    for row in render_elements:
        i = 0
        for cell in row:
            [cell_w, cell_h] = cell.get_size() if isinstance(cell, pygame.Surface) else (0, 0)
            columns_w[i] = columns_w[i] if columns_w[i] >= cell_w else cell_w
            row_h = row_h if row_h >= cell_h else cell_h
            i += 1
    
    table = pygame.Surface((
        margin * 2 + col_padding * (col_count - 1) + sum(columns_w),
        margin * 2 + (row_padding + row_h) * row_count - row_padding,
    ), pygame.SRCALPHA, 32)
    table = table.convert_alpha()

    cell_y = margin
    for i in range(0, row_count):
        cell_x = margin
        for j in range(0, col_count):
            col_w = columns_w[j]

            cell = render_elements[i][j]
            if isinstance(cell, pygame.Surface):
                [cell_w, cell_h] = cell.get_size()
                table.blit(cell, (cell_x + (col_w - cell_w)/2, cell_y + (row_h - cell_h)/2))

            cell_x += (col_w + col_padding)

        cell_y += (row_h + row_padding)
    
    return table