import numpy as np
import random

aa=np.zeros(9,dtype=(np.int16))

def check_winner(arr):
  arr=arr.reshape(3,3)
  if arr[0,0]==1 and arr[0,1]==1 and arr[0,2]==1:return 1
  if arr[1,0]==1 and arr[1,1]==1 and arr[1,2]==1:return 1
  if arr[2,0]==1 and arr[2,1]==1 and arr[2,2]==1:return 1
  if arr[0,0]==1 and arr[1,0]==1 and arr[2,0]==1:return 1
  if arr[0,1]==1 and arr[1,1]==1 and arr[2,1]==1:return 1
  if arr[0,2]==1 and arr[1,2]==1 and arr[2,2]==1:return 1
  if arr[0,0]==1 and arr[1,1]==1 and arr[2,2]==1:return 1
  if arr[0,2]==1 and arr[1,1]==1 and arr[2,0]==1:return 1

  if arr[0,0]==2 and arr[0,1]==2 and arr[0,2]==2:return -1
  if arr[1,0]==2 and arr[1,1]==2 and arr[1,2]==2:return -1
  if arr[2,0]==2 and arr[2,1]==2 and arr[2,2]==2:return -1
  if arr[0,0]==2 and arr[1,0]==2 and arr[2,0]==2:return -1
  if arr[0,1]==2 and arr[1,1]==2 and arr[2,1]==2:return -1
  if arr[0,2]==2 and arr[1,2]==2 and arr[2,2]==2:return -1
  if arr[0,0]==2 and arr[1,1]==2 and arr[2,2]==2:return -1
  if arr[0,2]==2 and arr[1,1]==2 and arr[2,0]==2:return -1
  return 0

class node:
  def __init__(self,arr,active,visits,children,parent) -> None:
    self.arr=arr
    self.children=children
    self.parent=parent
    self.visits=0
    self.ucb1=float('inf')
    self.active=active
    self.value=0

  def __repr__(self) :
    return str(f'{self.arr.reshape(3,3)},value:{self.value:^20},visits:{self.visits:^4},ucb1:{self.ucb1}')

  def selection(self):
    if self.children==[]:return self
    else:
      maxx=-float('inf')
      max_node=None
      for i in self.children:
        if i.ucb1>maxx:
          maxx=i.ucb1
          max_node=i
      return max_node.selection()

  def expansion(self):
    if self.children==[]:
      carr=self.arr.copy()
      kk=list(np.where(carr==0))[0]
      for i in range(len(kk)):
        carr=self.arr.copy()
        carr[kk[i]]=self.active
        if self.active==1:tactive=2
        if self.active==2:tactive=1
        new_node=node(carr,tactive,0,[],self)
        self.children.append(new_node)

  def simulation(self):
    carr=self.arr.copy()
    tactive=self.active
    while np.any(carr==0):
      if check_winner(carr)== 1:return 1           #change scoring parameters
      if check_winner(carr)==-1:return -1          #change scoring parameters
      kk=list(np.where(carr==0))[0]
      ran=random.randint(0,len(kk)-1)
      ran=kk[ran]
      if tactive==1:carr[ran]=1;tactive=2
      elif tactive==2:carr[ran]=2;tactive=1
    return 0                                      #change scoring parameters

  def backpropagation(self):
    exploration_rate=2                         #change exploration factor
    if self.parent==None:self.visits+=1;return
    simulation1=self.simulation()
    for i in self.parent.children:
      if i.visits==0:
        i.ucb1=float('inf')
      else:
        i.ucb1=i.value/i.visits+np.sqrt(exploration_rate*np.log(i.parent.visits+1)/i.visits)
    self.visits+=1
    self.value+=simulation1
    self.ucb1=self.value/self.visits+np.sqrt(exploration_rate*np.log(self.parent.visits+1)/self.visits)
    if self.parent!=None:
      self.parent.backpropagation()

  def show_best_move(nodex):
    for i in range(1000):
      k=nodex.selection()
      k.expansion()
      k.backpropagation()
    for i in  nodex.children:
      i.children=[]
    return(nodex.selection())

def best(arr,active):
  node1=node(arr,active,0,[],None)
  return node1.show_best_move().arr


main_game=np.zeros(9)
main_game[0]=1
print(main_game.reshape(3,3))
print()
while np.any(main_game==0):
  aa=int(input('input>>'))
  print()
  if main_game[aa-1]!=0 :
    print('wrong input')
    print()
  else:
    main_game[aa-1]=2
    if check_winner(main_game)==-1:
      print('YOU win')
      break
    main_game=best(main_game,1)
    print(main_game.reshape(3,3))
    print()
    if check_winner(main_game)==1:
      print('PC wins ')
      break
