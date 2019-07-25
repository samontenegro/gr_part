import sys
from pathlib import Path
from ete3 import Tree, TreeNode, TreeStyle, TextFace, NodeStyle

ts = TreeStyle()
ts.show_leaf_name           = False
ts.scale                    = 50
ts.branch_vertical_margin   = 25
ts.rotation                 = 90
ts.show_scale               = False

def getArg():
    N = int(sys.argv[1])

    if N > 0:
        return N
    else:
        raise Exception("Argument must be positive!")

def styleFace(val):
    x = TextFace(val)
    x.margin_bottom = 5
    x.margin_right  = 10
    x.rotation      = 270
    x.fsize         = 6
    return x

def styleShow(T):
    T.show(tree_style=ts)

def treeSetPrint(T):
    for t in T:
        print(t, "\n")

def renderSet(G):
    trees = len(G)
    partitionSet = G[0].value
    fileType = ".png"

    Path.mkdir(Path("partition_trees_"+str(partitionSet)),exist_ok=True)
    for i in range(trees):
        fileName = Path("partition_trees_"+str(partitionSet)+"/G_"+str(partitionSet)+"_"+str(i+1)+fileType).__str__()
        G[i].render(fileName, w = 500, units = "mm", dpi = 72, tree_style=ts)

def lam(N):
    if N % 2 == 0:
        return int(N/2)
    elif N % 2 == 1:
        return int((N-1)/2)

def partitionTreeSet(N):
    if N == 1:
        x = Tree(";",format=100)
        x.add_features(value=N, name=str(N))
        
        xFace = styleFace(x.name)
        x.add_face(xFace,column=0,position="branch-top")

        return (x,)
    else:
        y = ()
        base = Tree(";",format=100)
        base.dist = 1

        for k in range(lam(N)):
            left    = partitionTreeSet(N-(k+1))
            right   = partitionTreeSet(k+1)

            for l in left:
                for r in right:
                    l.dist = 1
                    r.dist = 1

                    z = base.copy()
                    z.dist = 1
                    
                    z.add_features(value=N, name=str(N))
                    z.add_child(l.copy())
                    z.add_child(r.copy())

                    zFace = styleFace(z.name)
                    z.add_face(zFace,column=0,position="branch-top")

                    y = y + (z,)
        
        return y

N = getArg()

print("//===================================")
print("//     Generating Tree Set")
print("//===================================")

G = partitionTreeSet(N)
trees = len(G)

print("//     Rendering Tree Set")
print("//===================================")

renderSet(G)

print("//     Done! "+str(trees)+" trees printed")
print("//===================================")
