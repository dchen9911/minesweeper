from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

YELLOW = (1.0, 1.0,0.0, 0.9)

class boardPlot:
    def __init__(self, width, height, board, fig, ax):
        self.width = width
        self.height = height
        self.board = board
        self.finished = False

        self.fig = fig
        self.ax = ax
        self.ax.axis([0, width, 0, height])

        self.ax.set_yticklabels([]) # remove the tick labels
        self.ax.set_xticklabels([])
        self.ax.set_xticks([]) # remove the ticks too
        self.ax.set_yticks([]) 

        for x in range(width):
            for y in range(height):
                new_patch = Rectangle([x,y], 1, 1, facecolor='blue',
                edgecolor='black', alpha=0.9, zorder=1)
                self.board.tiles[x][y].set_patch(new_patch)
                self.ax.add_patch(new_patch)
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
    
    def onclick(self, event):
        if self.board.completed or self.finished:
            return
        if event.inaxes != self.ax:
            return
        x = int(event.xdata)
        y = int(event.ydata)
        if x < 0 or x >= self.width or y < 0 or y > self.height:
            return
        # print('you pressed', event.button, event.xdata, event.ydata)
        if str(event.button) == 'MouseButton.LEFT':
            tile = self.board.tiles[x][y]

            if not tile.opened:
                if tile.patch.get_facecolor() == YELLOW:
                    if tile.opened:
                        tile.patch.set_facecolor('0.9')
                    else:
                        tile.patch.set_facecolor('blue')
                else:
                    tile.patch.set_facecolor('yellow')
            else:
                tiles_to_open = tile.neighbours
                n_yellow = 0
                for n_tile in tiles_to_open:
                    if n_tile.patch.get_facecolor() == YELLOW:
                        n_yellow += 1
                # print(n_yellow)
                if n_yellow != tile.n_neighbour_mines:
                    pass
                else:
                    for n_tile in tiles_to_open:
                        if n_tile.patch.get_facecolor() == YELLOW:
                            continue
                        self.open_tile(n_tile.x, n_tile.y)

        elif str(event.button) == 'MouseButton.RIGHT':
            self.open_tile(x,y)
        plt.draw()

    def open_tile(self, x, y):
        if self.finished:
            return
        n_opened = self.board.open_tile(x,y)
        tiles = self.board.recently_opened
        for tile in tiles:
            patch = tile.patch
            if tile.is_mine:
                patch.set_facecolor('red')
                
            elif tile.n_neighbour_mines == 0:
                patch.set_facecolor('0.9')            
            else:
                patch.set_facecolor('0.9')
                self.ax.text(tile.x + 0.5,tile.y + 0.5, 
                            str(tile.n_neighbour_mines),
                            horizontalalignment='center',
                            verticalalignment='center',
                            zorder=10)
        if n_opened == -1:
            self.ax.text(self.width/2, self.height/2, ':(', size='large',
                            c='white',
                            bbox=dict(facecolor='red', alpha=1, lw=0),
                            horizontalalignment='center',
                            verticalalignment='center',
                            zorder=10)
            self.finished = True
            return
        elif self.board.completed:
            amt_time = '{:.2f}'.format(n_opened)
            self.ax.text(self.width/2, self.height/2, ':) - '+amt_time + ' s', 
                            size='large', c='white',
                            bbox=dict(facecolor='green', alpha=1, lw=0),
                            horizontalalignment='center',
                            verticalalignment='center',
                            zorder=10)
            self.finished = True
            return
        return tiles

    def auto_solve(self):
        raise NotImplementedError('ill do it later *cough*')
        init_prob = n_mines/(self.x*self.y)
        tiles_probs = {}
        min_prob = init_prob
        for row_tiles in self.board.tiles:
            for tile in row_tiles:
                tiles_probs[tile] = init_prob
        x = int(self.width/2)
        y = int(self.height/2) # select first one in the centre
        while True:
            tiles_opened = self.open_tile(x, y)
            if tiles_opened[0].is_mine:
                break
            tiles_to_update = []
            for tile in tiles_opened:
                tiles_probs.pop(tile)
                for n_tile in tile.neighbours:
                    if not n_tile.opened:
                        tiles_to_update.append(n_tile)

            if self.board.completed:
                break


class bogusEvent:
    def __init__(self, x, y, ax):
        self.xdata = x
        self.ydata = y
        self.ax = ax

if __name__ == "__main__":
    from board import board
    width = 9
    height = 10
    n_mines = 8
    new_board = board(width, height, n_mines)    
    new_board.print_basic_layout()

    fig = plt.figure(figsize = (width/3, height/3))
    ax = plt.gca()
    obj = boardPlot(width, height, new_board, fig, ax)
    plt.show()
    # event = bogusEvent(1.1, 0.5, ax)
    # obj.onclick(event)

    # fig.savefig("test.png")