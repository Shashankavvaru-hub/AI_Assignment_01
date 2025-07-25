class State:
    def __init__(self,config):
        self.config=config
        self.goal=['R', 'R', 'R', '_', 'L', 'L', 'L']

    def goalTest(self):
        return self.config==self.goal

    def moveGen(self):
        children=[]
        for i in range(len(self.config)):
            if self.config[i]=='L':
                if i + 1 < len(self.config) and self.config[i + 1] == '_':
                    next_state=self.config[:]
                    next_state[i], next_state[i + 1]=next_state[i + 1], next_state[i]
                    children.append(State(next_state))
                if i + 2 < len(self.config) and self.config[i + 1] == 'R' and self.config[i + 2] == '_':
                    next_state=self.config[:]
                    next_state[i], next_state[i + 2] = next_state[i + 2], next_state[i]
                    children.append(State(next_state))
            elif self.config[i]=='R':
                if i-1 >= 0 and self.config[i-1]=='_':
                    next_state=self.config[:]
                    next_state[i], next_state[i-1]=next_state[i-1],next_state[i]
                    children.append(State(next_state))
                if i-2 >= 0 and self.config[i-1] == 'L' and self.config[i-2]=='_':
                    next_state=self.config[:]
                    next_state[i], next_state[i-2]=next_state[i-2],next_state[i]
                    children.append(State(next_state))
        return children

    def __eq__(self, other):
        return isinstance(other, State) and self.config==other.config

    def __hash__(self):
        return hash(tuple(self.config))

    def __repr__(self):
        return ''.join(self.config)

def removeVisited(children, OPEN, CLOSED):
    open_nodes=[]
    for node,_ in OPEN:
        open_nodes.append(node)
    closed_nodes=[]
    for node, _ in CLOSED:
        closed_nodes.append(node)
    new_nodes=[]
    for node in children:
        if node not in open_nodes and node not in closed_nodes:
            new_nodes.append(node)
    return new_nodes

def reconstructPath(node_pair, CLOSED):
    parent_map={}
    for node,parent in CLOSED:
        parent_map[node]=parent
    node, parent=node_pair
    path=[node]
    while parent is not None:
        path.append(parent)
        parent=parent_map[parent]
    path.reverse()
    for i in range(len(path)):
        print(path[i])
        if i!=len(path)-1:
            print(" <- ")
    return path

def bfs(start):
    OPEN=[(start, None)]
    CLOSED=[]
    while OPEN:
        node_pair=OPEN.pop(0)
        node, parent=node_pair
        if node.goalTest():
            print("Goal is found")
            reconstructPath(node_pair, CLOSED)
            return
        CLOSED.append(node_pair)
        children=node.moveGen()
        new_nodes=removeVisited(children, OPEN, CLOSED)
        new_pairs=[]
        for child in new_nodes:
            new_pairs.append((child, node))
        OPEN+=new_pairs

def dfs(start):
    OPEN=[(start, None)]
    CLOSED=[]
    while OPEN:
        node_pair=OPEN.pop(0)
        node,parent=node_pair
        if node.goalTest():
            print("Goal is found")
            reconstructPath(node_pair, CLOSED)
            return
        CLOSED.append(node_pair)
        children=node.moveGen()
        new_nodes=removeVisited(children, OPEN, CLOSED)
        new_pairs=[]
        for child in new_nodes:
            new_pairs.append((child, node))
        OPEN=new_pairs+OPEN

init_state=State(['L', 'L', 'L', '_', 'R', 'R', 'R'])
print("BFS solution:")
bfs(init_state)
print("\nDFS solution:")
dfs(init_state)
