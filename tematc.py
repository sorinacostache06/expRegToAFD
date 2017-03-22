from graphviz import Digraph
ops_priority = {'*':3, '.':2, '|': 1, '(': 0, ')':0}
ops = ["(", ")", "*", ".", "|"]

class Tree:
    def __init__(self):
        self.root = None
        self.left = None
        self.right = None
        self.value = None
        self.index = None
        self.nullabale = None
        self.fisrtpoz = []
        self.lastpoz = []

global followpos
followpos = [[] for _ in range(25)]
global stari
stari = []
pozLitere = {}
tranzitii = []

def infix_to_postfix(exp):
        elements = []
        last_str = ""
        for x in exp:
                if (x in ops):
                        if len(last_str) > 0:
                                elements.append(last_str)
                        last_str = ""
                        elements.append(x)
                else:
                        last_str += x
        if len(last_str) > 0:
                elements.append(last_str)


        # print (elements)
        stack = []
        output = []
        # elements.reverse()
        for element in elements:
                # print stack
                if (element in ops):
                        if (element == '('):
                                stack.append(element)
                        elif (element == ')'):
                                while (stack[-1] != '('):
                                        output.append(stack[-1])
                                        stack.pop(-1)
                                stack.pop(-1)
                        else:
                                while (len(stack) > 0 and ops_priority[stack[-1]] >=  ops_priority[element]):
                                        output.append(stack[-1])
                                        stack.pop(-1)
                                stack.append(element)
                else:
                        output.append(element)

        while(len(stack) > 0):
                output.append(stack[-1])
                stack.pop(-1)
        # print(output)
        return output


def create_exp_tree(current_node, postfix, index):
        current_node.value = postfix[index]
        current_node.index = index
        index-=1

        if (current_node.value in ops):
                if (current_node.value == '*'):
                        if (index >= 0):
                                current_node.left = Tree()
                                index = create_exp_tree(current_node.left, postfix, index)
                # elif (current_node.value == '|'):
                #         if (index >= 0):
                #                 current_node.right = Tree()
                #                 index = create_exp_tree(current_node.right, postfix, index)
                #         if (index >= 0):
                #                 current_node.left = Tree()
                #                 index = create_exp_tree(current_node.left, postfix, index)
                else:
                        if (index >= 0):
                                current_node.right = Tree()
                                index = create_exp_tree(current_node.right, postfix, index)
                        if (index >= 0):
                                current_node.left = Tree()
                                index = create_exp_tree(current_node.left, postfix, index)
        return index

# def indexare(current_node):
#     global contor
#     if current_node.left is None and current_node.right is None:
#         current_node.index = contor
#         contor += 1   

def print_tree(tree):
        if (tree):
                print ('Valoare : ') 
                print (tree.value)
                print ('Index :') 
                print (tree.index)
                #print('Nullabale: ') 
                #print(tree.nullabale)
                #print('Firstpos: ') 
                #print(tree.fisrtpoz)
                #print('Lastpos: ') 
                #print(tree.lastpoz)
                #print('\n')
                print_tree(tree.left)
                print_tree(tree.right)	

def dfs(node):
    #print(node.value)
    #print(node.index)
    if (node.left is None and node.right is None):
        node.nullabale = False
        node.fisrtpoz.append(node.index)
        node.lastpoz.append(node.index)
        pozLitere[node.index] = node.value
    if (node.left is not None):
        dfs(node.left)
    if (node.right is not None):
        dfs(node.right)
    if (node.value == '.'):
        node.nullabale = nullabaleC(node.left) and nullabaleC(node.right)
        if node.left is not None:
            # print('aici stanga')
          if (node.left.nullabale is True and node.right is not None):
            node.fisrtpoz += node.right.fisrtpoz
          node.fisrtpoz += node.left.fisrtpoz
        else:
          print(node.value, ' aici ', node.right.value)
        
        if node.right is not None:
            # print('aici dreapta')
          if (node.right.nullabale is True and node.left is not None):
            node.lastpoz += node.left.lastpoz
          node.lastpoz += node.right.lastpoz
        else:
          print('nu e bine 2')
        if node.left is not None:
          for i in node.left.lastpoz:
            # print(i)
            #print('i = ' + str(i))
            corectPoz = node.right.fisrtpoz
            #print('Fir ' + str(corectPoz))
            followpos[int(i)] += corectPoz
            #print('followpos ' + str(followpos[int(i)]))
    if (node.value == '|'):
        node.nullabale = nullabaleC(node.left) or nullabaleC(node.right)
        if node.left is not None:
            node.fisrtpoz += node.left.fisrtpoz
            node.lastpoz += node.left.lastpoz
        if node.right is not None:
            node.fisrtpoz += node.right.fisrtpoz
            node.lastpoz += node.right.lastpoz
        #node.lastpoz = list(chain.from_iterable(node.lastpoz))
    if (node.value == '*'):
        node.nullabale = nullabaleC(node)
        if node.left is not None:
            node.fisrtpoz += node.left.fisrtpoz
            node.lastpoz += node.left.lastpoz
        else:
          print('nu e bine 3')
        if node.left is not None:
          # print(vect)
          for i in node.left.lastpoz:
            # print(i)
            #print('i = ' + str(i))
            corectPoz = node.left.fisrtpoz
            #('Firstpos' + str(node.left.fisrtpoz))
            followpos[int(i)] += corectPoz
            #print('followpos ' + str(followpos[int(i)]))



def elD():
  for i in range(len(followpos)):
    followpos[i] = list(set(followpos[i]))
  for i in range(len(followpos)):
    if ' ' in followpos[i]:
      followpos[i].remove(' ')

def nullabaleC(node):
  if node == None:
    return False
  if (node.value == '*'):
    return True
  if (node.value == 'a' or node.value == 'b' or node.value == '#'):
    return False
  else:
    return False
    
def getUnmarkedState(stari):
  for i in stari:
    if i[1] is False:
      return i
  return None
  

def stariNemarcare(stare_cur,stari):
  stari_noi = []
  for x in stari:
    if set(x[0]) != set(stare_cur[0]):
      stari_noi.append(x)
    else:
      stari_noi.append((x[0],True))
  return stari_noi
    
def AFD(my_tree):
  global stari
  q0 = my_tree.fisrtpoz
  stari.append((q0,False))
  while True:
    stare_cur = getUnmarkedState(stari)
    if stare_cur is not None:
      for l in alphabet:
        nextState = []
        changed = False
        for s in stare_cur[0]:
          print(pozLitere[int(s)] , l)
          if pozLitere[int(s)] == l:
            nextState += followpos[int(s)]
            changed = True
        nextState = list(set(nextState))
        print(not[x for x in stari if set(x[0]) == set(nextState)])
        if not [x for x in stari if set(x[0]) == set(nextState)] and nextState:
          stari.append((nextState,False))
        if changed:
          tranzitii.append((stare_cur[0],nextState,l))
      stari = stariNemarcare(stare_cur,stari)
    else:
      break

stari_finale = []
stari_normale = []

def detTipStari(stari):
  for stare in stari:
    flag = False
    for c in stare[0]:
      print(pozLitere[int(c)])
      if pozLitere[int(c)] == "#\n":
        flag = True
        break
    if flag is False:
      stari_normale.append(stare[0])
    else:
      stari_finale.append(stare[0])

def draw_graph(stare_initiala,stari_normale,stari_finale,tranzitii):
  g = Digraph("AFN")
  g.attr('node', shape='diamond')
  stare_initiala.sort()
  g.node(str(stare_initiala), 'q%s' % ",".join([str(x) for x in stare_initiala]))
  for stare in stari_finale:
    g.attr('node', shape='doublecircle')
    stare.sort()
    g.node(str(stare), 'q%s' % ",".join([str(x) for x in stare]))
  g.attr('node', shape='circle')
  for stare in stari_normale:
        stare.sort()
        g.node(str(stare), 'q%s' % ",".join([str(x) for x in stare]))
  for tranzitie in tranzitii:
        tranzitie[0].sort()
        tranzitie[1].sort()
  	g.edge(str(tranzitie[0]), str(tranzitie[1]), label = tranzitie[2])
  g.render('x.gv',view=True)    

file = open("input.txt","r") 
# alphabet = file.readlines()
lines = file.readlines()
alphabet = lines[0]
exp = lines[1]
postfix = infix_to_postfix(exp)

# print(postfix)
#print(len(postfix))
my_tree = Tree()
create_exp_tree(my_tree, postfix, len(postfix)-1)
dfs(my_tree)
AFD(my_tree)
stare_initiala = my_tree.fisrtpoz
detTipStari(stari)
print(stare_initiala)
print('Stari normale')
print(stari_normale)
print('Stari finale')
print(stari_finale)
print_tree(my_tree)
#print(dfs(my_tree, postfix[len(postfix)-1] ))
elD()
draw_graph(stare_initiala,stari_normale,stari_finale,tranzitii)
# print(followpos)
