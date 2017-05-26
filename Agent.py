from socket import *
from collections import deque
import sys, getopt
# python pycharmprojects\Treasurehunter\Agent.py -p 12345
class Node():
    def __init__(self):
        self.value = None
        self.father = None
        self.raft = False
        self.dynamite = 0
        self.row = None
        self.column = None

    def inherit(self, node):  # create new node inherit from father
        self.father = node
        self.raft = node.raft
        self.dynamite = node.dynamite
        self.row = node.row
        self.column = node.column


class Agent:
    def __init__(self):
        self.axe = False
        self.key = False
        self.gold = False
        self.dynamite = 0
        self.raft = False
        self.on_raft = False
        self.column = 40
        self.row = 40
        self.start_row = self.row
        self.start_col = self.column
        self.actions = {'left': 'L', 'right': 'R', 'forward': 'F', 'chop': 'C', 'blast': 'B', 'unlock': 'U'}
        self.drct = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        self.tile_type = {'tree': 'T', 'door': '-', 'wall': '*', 'water': '~', 'land': ' ', 'key': 'k', 'axe': 'a',
                          'dynamite': 'd', 'treasure': '$'}
        self.dirn = self.drct['S']
        self.tile_type = {'tree': 'T', 'door': '-', 'wall': '*', 'water': '~', 'land': ' ', 'key': 'k', 'axe': 'a',
                          'dynamite': 'd', 'treasure': '$'}  # type of terrain tile
        self.passable = [self.tile_type['land'], self.tile_type['key'], self.tile_type['axe'],
                         self.tile_type['dynamite'], self.tile_type['treasure']]
        self.world = [[None] * 80 for _ in range(80)]
        self.border = {'W': 38, 'N': 38, 'S': 42, 'E': 42}
        self.have_been = {(self.row, self.column)}
        self.host = "localhost"
        self.port = 12345
        self.addr = (self.host, self.port)
        self.sock = socket()
        self.view = [[None] * 5 for _ in range(5)]
        self.goal_list = deque()

    def get_action(self, view):
        action = ''
        return action

    def goal_dealer(self):
        for i in range(self.border['N'],self.border['S']+1):
            for j in range(self.border['W'],self.border['E']+1):
                if self.world[i][j] == '$':
                    self.goal_list.append((i,j))
                elif self.world[i][j] == 'k':
                    self.goal_list.append((i,j))
                elif self.world[i][j] == 'd':
                    self.goal_list.append((i,j))
                elif self.world[i][j] == 'a':
                    self.goal_list.append((i, j))

    def get_view(self, data):
        view = [[' '] * 5 for _ in range(5)]
        n = 0
        for i in range(5):
            for j in range(5):
                if not (i == 2 and j == 2):
                    try:
                        view[i][j] = data[n]
                        n += 1
                    except IndexError:
                        pass
        return view

    def print_view(self, view):
        print('\n+-----+')
        for i in range(5):
            print('|', end='')
            for j in range(5):
                if i == 2 and j == 2:
                    print('^', end='')
                else:
                    print(view[i][j], end='')
            print('|')
        print('+-----+')

    def save_to_world(self, view):
        c, r = None, None
        if self.dirn == self.drct['N']:  # NORTH  = 1
            c = -2
            self.row -= 1
        elif self.dirn == self.drct['S']:  # SOUTH  = 3
            c = 2
            self.row += 1
        elif self.dirn == self.drct['W']:  # WEST   = 2
            r = -2
            self.column -= 1
        elif self.dirn == self.drct['E']:  # EAST   = 0
            r = 2
            self.column += 1
        for i in range(-2, 3):
            if c == -2:
                self.world[self.row + c][self.column + i] = view[0][2 + i]
            elif c == 2:
                self.world[self.row + c][self.column - i] = view[0][2 + i]
            elif r == -2:
                self.world[self.row - i][self.column + r] = view[0][2 + i]
            elif r == 2:
                self.world[self.row + i][self.column + r] = view[0][2 + i]
        if self.row - 2 < self.border['N']:
            self.border['N'] = self.row - 2
        if self.row + 2 > self.border['S']:
            self.border['S'] = self.row + 2
        if self.column - 2 < self.border['W']:
            self.border['W'] = self.column - 2
        if self.column + 2 > self.border['E']:
            self.border['E'] = self.column + 2
        if (self.row, self.column) not in self.have_been:
            self.have_been.add((self.row, self.column))
#        for i in range(-2, 3):
#            for j in range(-2, 3):
#                if self.dirn == self.drct['S']:
#                    self.world[self.row - i][self.column - j] = view[2 + i][2 + j]
#                elif self.dirn == self.drct['N']:
#                    self.world[self.row + i][self.column + j] = view[2 + i][2 + j]
#                elif self.dirn == self.drct['E']:
#                    self.world[self.row + j][self.column - i] = view[2 + j][2 + i]
#                elif self.dirn == self.drct['W']:
#                    self.world[self.row - j][self.column + i] = view[2 + j][2 + i]
        #-----------------------------------------------------
#        if self.row - 2 < self.border['N']:
#            self.border['N'] = self.row - 2
#        if self.row + 2 > self.border['S']:
#            self.border['S'] = self.row + 2
#        if self.column - 2 < self.border['W']:
#            self.border['W'] = self.column - 2
#        if self.column + 2 > self.border['E']:
#            self.border['E'] = self.column + 2
#        if (self.row, self.column) not in self.have_been:
#            self.have_been.add((self.row, self.column))

    def right(self):
        self.sock.send('R'.encode("UTF-8"))
        if self.dirn == 3:
            self.dirn = 0
        else:
            self.dirn += 1
        view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
        self.print_view(view)
        return view

    def left(self):
        self.sock.send('L'.encode("UTF-8"))
        if self.dirn == 0:
            self.dirn = 3
        else:
            self.dirn -= 1
        view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
        self.print_view(view)
        return view

    def forward(self):
        if self.view[1][2] == 'k':
            self.key = True
        if self.view[1][2] == 'd':
            self.dynamite += 1
        if self.view[1][2] == 'a':
            self.axe = True
        if self.view[1][2] == '$':
            self.gold = True
            self.sock.send('F'.encode("UTF-8"))
            self.view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
            self.save_to_world(self.view)
            self.move_to(self.find_path(self.start_row, self.start_col, self.raft))
            exit()

        if self.view[1][2] == '~':
            self.raft = False

        if self.view[1][2] == 'T':
            self.sock.send('C'.encode("UTF-8"))
            self.view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
        if self.view[1][2] == '-':
            self.sock.send('U'.encode("UTF-8"))
            self.view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
        if self.view[1][2] == '*' and self.dynamite:
            self.sock.send('B'.encode("UTF-8"))
            self.dynamite -= 1
        self.sock.send('F'.encode("UTF-8"))
        self.view = self.get_view(self.sock.recv(24, MSG_WAITALL).decode("UTF-8"))
        self.print_view(self.view)
        self.save_to_world(self.view)

    def explore(self):  # go to the border which have not been
        from copy import deepcopy
        item = ['$', 'd', 'k', 'a']
        prior = deepcopy(self.border)
        for i in range(self.border['N'], self.border['S']):
            for j in range(self.border['W'], self.border['E']):
                if self.world[i][j] in item:
                    print(self.world[i][j],i,j)
                    temp = self.find_path(i, j, False)
                    if temp:
                        self.move_to(temp)
                elif (i, j) not in self.have_been and self.world[i][j] in self.passable:
                    #print('i j',i,j)
                    temp = self.find_path(i, j, False)
                    print(temp)
                    if temp:
                        print('here1')
                        self.move_to(temp)

        if prior == self.border:  # no more area to discover
            return
        else:
            self.explore()

    def find_path(self, target_row, target_column, use_raft):  # use breadth first search to find the right position
        start = Node()
        start.column = self.column
        start.row = self.row
        start.raft = use_raft
        start.dynamite = self.dynamite
        open_list = deque()
        open_list.append(start)
        been = [(self.row, self.column)]
        #weighted_sequence = []
        results = []
        result = []
        while len(open_list):
            passable = {' ', 'd', 'k', 'a', '$'}
            node = open_list.popleft()
            if node.raft:
                passable.add('~')
            if node.dynamite:
                passable.add('*')
                passable.add('T')
                passable.add('-')
            if self.axe:
                passable.add('T')
            if self.key:
                passable.add('-')
            for i in [-1, 1]:
                if self.world[node.row + i][node.column] in passable and (node.row + i, node.column) not in been:
                    new_node = Node()
                    new_node.inherit(node)
                    new_node.row = node.row + i
                    if self.world[node.row + i][node.column] != '~' and self.world[node.row][node.column] == '~':
                        new_node.raft = False
                    if self.world[node.row + i][node.column] == '*' or (
                    self.world[node.row + i][node.column] == 'T' and not self.axe) or (
                    self.world[node.row + i][node.column] == '-' and not self.key):
                        new_node.dynamite -= 1
                    open_list.append(new_node)

                    if new_node.row == target_row and new_node.column == target_column:
                        while new_node is not None:
                            result.append((new_node.row, new_node.column))
                            new_node = new_node.father
                        result.reverse()
                        results.append(result)
                        result = []
                    else:
                        been.append((new_node.row, new_node.column))
                        #return result
                if self.world[node.row][node.column + i] in passable and (node.row, node.column + i) not in been:
                    new_node = Node()
                    new_node.inherit(node)
                    new_node.column = node.column + i
                    if self.world[node.row][node.column + i] != '~' and self.world[node.row][node.column] == '~':
                        new_node.raft = False
                    if self.world[node.row][node.column + i] == '*' or (
                    self.world[node.row][node.column + i] == 'T' and not self.axe) or (
                    self.world[node.row][node.column + i] == '-' and not self.key):
                        new_node.dynamite -= 1
                    open_list.append(new_node)
                    been.append((new_node.row, new_node.column))
                    if new_node.row == target_row and new_node.column == target_column:
                        while new_node is not None:
                            result.append((new_node.row, new_node.column))
                            new_node = new_node.father
                        result.reverse()
                        results.append(result)
                        result = []
                    else:
                        been.append((new_node.row, new_node.column))
                        #return result
        for i in range(len(results)):
            tool_used = False
            for j in range(len(results[i])):
                if self.world[results[i][j][0]][results[i][j][1]] in {'*', 'T', '-', '~'}:
                    tool_used = True
            if tool_used == False:
                return results[i]
        if len(results):
            return results[0]
        return False
        '''
        for node in essential_path:
            passable = {' ', 'd', 'k', 'a', '$'}
            if node.row == target_row and node.row == target_row:
                break
            if node.raft:
                passable.add('~')
            if self.axe:
                passable.add('T')
            if self.key:
                passable.add('-')
            if node.dynamite:
                passable.add('*')
                passable.add('T')
                passable.add('-')
            for i in [-1, 1]:  # breadth frist search check out every place where can go to
                if self.world[node.row + i][node.column] in passable:
                    new_node = Node()
                    new_node.inherit(node)
                    new_node.row = node.row + i
                    if self.world[node.row + i][node.column] == '~':
                        new_node.raft = False
                    if self.world[node.row + i][node.column] == '*' or (self.world[node.row + i][node.column] == 'T' and
                                                                             self.axe == False):
                        new_node.dynamite -= 1
                    if (new_node.row, new_node.column) not in been:
                        been.append((new_node.row, new_node.column))
                        essential_path.append(new_node)

                if self.world[node.row][node.column + i] in passable:
                    new_node = Node()
                    new_node.inherit(node)
                    new_node.column = node.column + i
                    if self.world[node.row][node.column + i] == '~':
                        new_node.raft = False
                    if self.world[node.row][node.column + i] == '*' or (self.world[node.row][node.column + i] == 'T' and
                    self.axe == False) or (self.world[node.row][node.column + i] == '-' and
                    self.key == False):
                        new_node.dynamite -= 1
                    if (new_node.row, new_node.column) not in been:
                        been.append((new_node.row, new_node.column))
                        essential_path.append(new_node)
        if essential_path[-1].row != target_row or essential_path[-1].column != target_column:  # goal is not reachable
            return False
        result = []

        while node.father is not None:
            result.append([node.row, node.column])
            if not (node.row, node.column) in self.have_been:
                self.have_been.add((node.row, node.column))
            node = node.father
        result.reverse()
        #print(result)
        return result
        '''

    def move_to(self, result):  # follow the search path go to destination
        print(result)
        for point in result:
            print('tile:', self.world[point[0]][point[1]])
            a = self.row - point[0]
            b = self.column - point[1]
            if a == -1:
                while self.dirn != self.drct['S']:
                    self.right()
                self.forward()

            elif a == 1:
                while self.dirn != self.drct['N']:
                    self.right()
                self.forward()
            elif b == 1:
                while self.dirn != self.drct['W']:
                    self.right()
                self.forward()
            elif b == -1:
                while self.dirn != self.drct['E']:
                    self.right()
                self.forward()
        return

    def pick_item(self):
        item = ['$', 'd', 'k', 'a']
        goal = []
        for i in range(self.border['N'] - 5, self.border['S'] + 5):
            for j in range(self.border['W'] - 5, self.border['E'] + 5):
                if self.world[i][j] in item:
                    temp = self.find_path(i, j, self.raft)
                    if temp:
                        goal.append(temp)
        if len(goal) == 0:
            return
        for p in goal:
            self.move_to(p)

    def main(self, argv = None):
        if argv is None:
            argv = sys.argv
        ops, args = getopt.getopt(sys.argv[1:], "p:h:")
        for op, value in ops:
            if op == "-p":
                self.port = int(value)
            if op == "-h":
                self.host = value
        self.addr = (self.host, self.port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.addr)
        self.start_row = int(self.sock.recv(2).decode("UTF-8"))
        self.start_col = int(self.sock.recv(2).decode("UTF-8"))
        self.dirn = int(self.sock.recv(1).decode("UTF-8"))
        print(self.start_row, self.start_col, self.dirn)
        self.row = self.start_row
        self.column = self.start_col
        self.border['N'] = self.start_row - 2
        self.border['S'] = self.start_row + 2
        self.border['W'] = self.start_col - 2
        self.border['E'] = self.start_col + 2
        b = self.sock.recv(24, MSG_WAITALL).decode("UTF-8")
        print('b=',b, end='|')
        self.view = self.get_view(b)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.dirn == self.drct['S']:
                    self.world[self.row - i][self.column - j] = self.view[2 + i][2 + j]
                elif self.dirn == self.drct['N']:
                    self.world[self.row - i][self.column - j] = self.view[2 - i][2 - j]
                elif self.dirn == self.drct['E']:
                    self.world[self.row - i][self.column - j] = self.view[2 + j][2 - i]
                elif self.dirn == self.drct['W']:
                    self.world[self.row - i][self.column - j] = self.view[2 - j][2 + i]
        #self.save_to_world(self.view)
        #aa = 100
        while True:
            #self.print_view(self.view)
            self.explore()
            self.pick_item()
            #aa -=1

if __name__ =='__main__':
    agent = Agent()
    agent.main()
