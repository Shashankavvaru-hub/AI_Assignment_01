class State:
    def __init__(self, left, right, umbrella_side, time_elapsed):
        self.left=left
        self.right=right
        self.umbrella=umbrella_side
        self.time=time_elapsed

    def goalTest(self):
        return len(self.left)==0 and self.umbrella=='R'

    def moveGen(self):
        children=[]
        people=self.left if self.umbrella=='L' else self.right
        for i in range(len(people)):
            for j in range(i,len(people)):
                crossing=[people[i]] if i==j else [people[i], people[j]]
                next_left=self.left[:]
                next_right=self.right[:]
                next_side='R' if self.umbrella=='L' else 'L'
                if self.umbrella=='L':
                    for p in crossing:
                        next_left.remove(p)
                        next_right.append(p)
                else:
                    for p in crossing:
                        next_right.remove(p)
                        next_left.append(p)
                crossing_time=max(crossing)
                new_time=self.time+crossing_time
                if new_time<=60:
                    children.append(State(next_left,next_right,next_side,new_time))
        return children

    def __eq__(self,other):
        return (sorted(self.left)==sorted(other.left) and
                sorted(self.right)==sorted(other.right) and
                self.umbrella==other.umbrella)
    def __hash__(self):
        return hash((tuple(sorted(self.left)),tuple(sorted(self.right)),self.umbrella))
    def __repr__(self):
        return f"Left:{self.left},Right:{self.right},Time:{self.time}"
        
def removeVisited(children, OPEN, CLOSED):
    open_nodes=[]
    for node, _ in OPEN:
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
    for node, parent in CLOSED:
        parent_map[node]=parent
    node,parent=node_pair
    path=[node]
    while parent is not None:
        path.append(parent)
        parent=parent_map[parent]
    path.reverse()
    print("\nSolution Path:")
    for step in path:
        print(step)
    print(f"\nTotal Time: {path[-1].time} minutes")
    return path

def bfs(start):
    OPEN=[(start, None)]
    CLOSED=[]
    while OPEN:
        node_pair=OPEN.pop(0)
        node, parent=node_pair
        if node.goalTest():
            print("Goal Found!")
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
        node, parent=node_pair
        if node.goalTest():
            print("Goal Found!")
            reconstructPath(node_pair, CLOSED)
            return
        CLOSED.append(node_pair)
        children=node.moveGen()
        new_nodes=removeVisited(children, OPEN, CLOSED)
        new_pairs=[]
        for child in new_nodes:
            new_pairs.append((child, node))
        OPEN=new_pairs+OPEN

Amogh=5
Ameya=10
Grandmother=20
Grandfather=25
init_state=State([Amogh,Ameya,Grandmother,Grandfather],[],'L',0)
print("BFS solution:")
bfs(init_state)
print("\nDFS solution:")
dfs(init_state)
