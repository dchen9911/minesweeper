import numpy as np

class boardTile:
    def __init__(self, x, y):
        self.neighbours = []
        self.is_mine = False
        self.n_neighbour_mines = 0
        self.x = x
        self.y = y
        self.opened = False
    
class board:
    def __init__(self, size_x, size_y, n_mines):
        self.tiles = []
        self.x = size_x
        self.y = size_y
        for x in range(0, size_x):
            row_tiles = []
            for y in range(0, size_y):
                new_tile = boardTile(x, y)
                row_tiles.append(new_tile)
            self.tiles.append(row_tiles)
        self.set_mines(n_mines)
        # set all the neighbours and number of neighbour mines
        for row_tiles in self.tiles:
            for tile in row_tiles:
                x_pos = tile.x
                y_pos = tile.y
                # get all the neighbouring tiles
                for x in range(x_pos - 1, x_pos + 2):
                    for y in range(y_pos - 1, y_pos + 2):
                        if x == x_pos and y == y_pos:
                            continue
                        elif x >= self.x or x < 0 or y >= self.y or y < 0:
                            continue
                        tile.neighbours.append(self.tiles[x][y])        
    
                if tile.is_mine:
                    for neighbour_tile in tile.neighbours:
                        neighbour_tile.n_neighbour_mines += 1

    # n is the number of mines
    def set_mines(self, n):
        # random generate numbers 
        mine_coords = []
        while (1):
            n_gen = n - len(mine_coords)
            x_coords = np.random.randint(0, self.x, n_gen)
            y_coords = np.random.randint(0, self.y, n_gen)
            coords = list(zip(x_coords, y_coords))
            mine_coords += coords
            mine_coords = list(set(mine_coords))
            if len(mine_coords) == n:
                break
        for x,y in mine_coords:
            self.tiles[x][y].is_mine = True
        self.mine_coords = mine_coords
    
    # returns the number of tiles opened, -1 if tile was mine
    def open_tile(self, x, y):
        base_tile = self.tiles[x][y]
        if base_tile.is_mine:
            print("Mined out")
            return -1
        elif base_tile.n_neighbour_mines != 0:
            self.base_tile
            pass
        

    def print_basic_layout(self):
        mine_cnt = 0
        print('  ', end = '')
        for x in range(0, self.x):
            print(str(x) + '|', end='')
        print()
        for y in range(0, self.y):
            print(str(y) + '|', end='')
            for x in range(0, self.x):
                tile = self.tiles[x][y]
                if tile.is_mine:
                    print('x', end=' ')
                    mine_cnt += 1
                else:
                    print(tile.n_neighbour_mines, end=' ')
            print()
        print("Mine count: " + str(mine_cnt))


if __name__ == "__main__":
    new_board = board(9,10,10)    
    new_board.print_basic_layout()



        

                


