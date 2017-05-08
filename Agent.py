import socket
import sys, getopt

PORT = 31234 # By default
opts, args = getopt.getopt(sys.argv[1:], "p:")
for opt, port_value in opts:
    if opt == "-p":
        PORT = int(port_value)
        break
actions = {'left': 'L', 'right': 'R', 'forward': 'F', 'chop': 'C', 'blast': 'B', 'unlock': 'U'}
direction = {'N': 0, 'E': 1, 'S': 2, 'W': 3}

class Agent:
    def get_action(self, view):
        action = ''
        return action

    def get_view(self, data):
        view = [[' ']*5 for _ in range(5)]
        k = 0
        for i in range(5):
            for j in range(5):
                if not i == 2 and j == 2:
                    try:
                        view[i][j] = data[k]
                        k += 1
                    except IndexError:
                        pass
        return view

    def print_view(self, view):
        print('\n+-----+')
        for i in range(5):
            print('|',end='')
            for j in range(5):
                if i == 2 and j == 2:
                    print('^',end='')
                else:
                    print(view[i][j],end='')
            print('|')
        print('+-----+')

    def main(self):
        pass


class Engine:
    def __init__(self):
        self.map = [] # Map of the world
        self.view = [] # View of agent
        self.axe = False
        self.key = False
        self.dynamite = 0 # Dynamite holding number
        self.treasure = False
        self.raft = False
        self.on_raft = False # Whether the agent is on the raft
        self.offMap = False
        self.won = False
        self.lost = False
        self.actions = {'left': 'L', 'right': 'R', 'forward': 'F', 'chop': 'C', 'blast': 'B', 'unlock': 'U'}
        self.drct = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        self.tile_type = {'tree': 'T', 'door': '-', 'wall': '*', 'water': '~', 'land': ' ', 'key': 'k', 'axe': 'a', 'dynamite': 'd', 'treasure': '$'} #type of terrain tile
        self.passable = [self.tile_type['land'], self.tile_type['key'], self.tile_type['axe'], self.tile_type['dynamite'], self.tile_type['treasure']]
        self.dirn = self.drct['S'] # Default direction
        self.column = 80 # Maximum column number of the world
        self.row = 80 # Maximum row number of the world
        self.icol = 0 # Initial colomn of agent
        self.irow = 0 # Initial row of agent
        self.cur_row = 0 # Current row of agent
        self.cur_col = 0 # Current column of agent
        self.nrow = 0

    def prompt(self, message):
        print(message)
        sys.exit()

    def read_world(self, mapName):
        try:
            with open(mapName, 'r') as mapFile:
                self.nrow = 0
                for line in mapFile.readlines():
                    line = line.strip('\n')
                    line = list(line)
                    if len(line):
                        if len(line)>self.column:
                            raise IOError
                        self.nrow+=1
                        if self.nrow > self.row:
                            raise IOError
                        self.map.append([line[c] for c in range(len(line))])
                        if '^' in line:
                            self.dirn = self.drct['N']
                            self.cur_col = line.index('^')
                            self.cur_row = self.nrow-1
                            self.icol = self.cur_col
                            self.irow = self.cur_row
                        elif '>' in line:
                            self.dirn = self.drct['E']
                            self.cur_col = line.index('>')
                            self.cur_row = self.nrow-1
                            self.icol = self.cur_col
                            self.irow = self.cur_row
                        elif 'v' in line:
                            self.dirn = self.drct['S']
                            self.cur_col = line.index('v')
                            self.cur_row = self.nrow-1
                            self.icol = self.cur_col
                            self.irow = self.cur_row
                        elif '<' in line:
                            self.dirn = self.drct['W']
                            self.cur_col = line.index('<')
                            self.cur_row = self.nrow-1
                            self.icol = self.cur_col
                            self.irow = self.cur_row
        except FileNotFoundError:
            self.prompt('File not found.')
        except IOError:
            self.prompt('IO error.')

    def pick_up(self, item, row, col):
        if item == self.tile_type['axe']:
            self.axe = True
        elif item == self.tile_type['key']:
            self.key = True
        elif item == self.tile_type['dynamite']:
            self.dynamite += 1
        elif item == self.tile_type['treasure']:
            self.treasure = True
        if not self.offMap:
            self.map[row][col] = self.tile_type['land']

    def turn_left(self):
        self.dirn = (self.dirn + 3) % 4
        return True

    def turn_right(self):
        self.dirn = (self.dirn + 1) % 4
        return True

    def forward(self, new_row, new_col):
        if (new_row < 0 or new_row > self.nrow) or (new_col < 0 or new_col >= len(self.map[self.nrow])):
            if not self.offMap:
                self.map[self.cur_row][self.cur_col] = self.tile_type['water']
                self.offMap = True
            self.cur_row = new_row
            self.cur_col = new_col
            self.lost = True
            return True
        ch = self.map[new_row][new_col]
        if ch == self.tile_type['tree'] or ch == self.tile_type['wall'] or ch == self.tile_type['door']:
            return False
        if not self.offMap:
            self.map[self.cur_row][self.cur_col] = self.tile_type['land']
        if ch == self.tile_type['water']:
            if self.on_raft:
                if not self.offMap:
                    self.map[self.cur_row][self.cur_col] = self.tile_type['water']
            elif self.raft:
                self.on_raft = True
                if not self.offMap:
                    self.map[self.cur_row][self.cur_col] = self.tile_type['land']
            else:
                self.lost = True
        elif ch in self.passable:
            if self.on_raft and not self.offMap:
                self.map[self.cur_row][self.cur_col] = self.tile_type['water']
                self.on_raft = False
                self.raft = False
        self.cur_row = new_row
        self.cur_col = new_col
        self.pick_up(ch, new_row, new_col)
        self.offMap = False
        return True


    def apply(self, action):
        action.upper()
        d_col, d_row = 0, 0
        if self.dirn == self.drct['N']:
            d_row = -1
        elif self.dirn == self.drct['S']:
            d_row = 1
        elif self.dirn == self.drct['W']:
            d_col = -1
        elif self.dirn == self.drct['E']:
            d_col = 1
        new_row = self.cur_row + d_row
        new_col = self.cur_col + d_col
        ch = self.map[new_row][new_col]
        if action == self.actions['left']:
            if self.turn_left():
                return True
        elif action == self.actions['right']:
            if self.turn_right():
                return True
        elif action == self.actions['forward']:
            if self.forward(new_row, new_col):
                if self.treasure and self.cur_row == self.irow and self.cur_col == self.icol:
                    self.won = True
                return True
            return False
        elif action == self.actions['chop']:
            if self.axe and ch == self.tile_type['tree']:
                self.map[new_row][new_col] = self.tile_type['land']
                self.raft = True
                return True
            return False
        elif action == self.actions['unlock']:
            if self.key and ch == self.tile_type['door']:
                self.map[new_row][new_col] = self.tile_type['land']
                return True
            return False
        elif action == self.actions['blast']:
            if self.dynamite and (self.map[new_row][new_col] == self.tile_type['tree'] ):
                self.map[new_row][new_col] = self.tile_type['land']
                self.raft = True
                return True
            return False
        return False

    def print_world(self):
        ch = ' '
        print()
        for i in range(self.nrow+1):
            for j in range(len(self.map[i])):
                if i == self.cur_row and j == self.cur_col:
                    if self.dirn == self.drct['N']:
                        ch = '^'
                    elif self.dirn == self.drct['E']:
                        ch = '>'
                    elif self.dirn == self.drct['S']:
                        ch = 'v'
                    elif self.dirn == self.drct['W']:
                        ch = '<'
                else:
                    ch = self.map[i][j]
                print(ch, end='')
            print()
        print()

    def visualize(self):
        r, c = 0, 0
        for i in range(-2,3):
            for j in range(-2,3):
                if self.dirn == self.drct['N']:
                    r = self.cur_row + i
                    c = self.cur_col + j
                elif self.dirn == self.drct['S']:
                    r = self.cur_row - i
                    c = self.cur_col - j
                elif self.dirn == self.drct['E']:
                    r = self.cur_row + i
                    c = self.cur_col - j
                elif self.dirn == self.drct['W']:
                    r = self.cur_row - i
                    c = self.cur_col + j
                if r in range(0, self.nrow+1) and c in range(0, len(self.map[r])):
                    self.view[2+i][2+j] = map[r][c]
                else:
                    self.view[2+i][2+j] = '.'

    def print_usage(self):
        self.prompt('Usage: python Raft [-p <port>] -i map [-m <maxmoves>] [-s]')

    def main(self, args):
        engine = Engine()
        silent = False
        mapName = ''
        action = 'F'
        maxmoves = 10000
        port = 0
        engine.read_world(mapName)
        engine.print_world()
        if port:
            pass
        else:
            agent = Agent()
            for i in range(maxmoves):
                engine.visualize()
                action = agent.get_action(engine.view)
                engine.apply(action)
                if not silent:
                    engine.print_world()
                if engine.won:
                    engine.prompt(f'Game won in {i} moves.')
                elif engine.lost:
                    engine.prompt('Game lost.')
            engine.prompt(f'Exceeded maximum of {maxmoves} moves.')



