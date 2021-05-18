#2nd greedy of random map size
#Greedy AI: Terrain Occupier
import os
import random
from copy import deepcopy

class blackwhite(object):

    global n0
    n0=8
    def __init__(self):#initials
        global n0
        self.matrix = [[0]*n0 for i in range(n0)]
        self.matrix[round(n0/2)-1][round(n0/2)-1], self.matrix[round(n0/2)][round(n0/2)] = 1,1
        self.matrix[round(n0/2)-1][round(n0/2)], self.matrix[round(n0/2)][round(n0/2)-1] = 2,2
        self.black, self.white = 2,2
        self.goblack = True
        self.ok = True
        self.nogo = 0
        self.win = None
        
    def pr(self):#print the chessboard
        #o = os.system('cls')
        self.showmatrix = [[0]*n0 for i in range(n0)]
        for i in range(n0):
            for j in range(n0):
                if self.matrix[i][j] == 1:
                    self.showmatrix[i][j] = 'X'
                elif self.matrix[i][j] == 2:
                    self.showmatrix[i][j] = 'O'
                else:
                    self.showmatrix[i][j] = ' '
        print('-' * 13, 'Reversi', '-' * 13)
        print('    Black "X": %d vs White "O": %d    ' % (self.black,self.white))
        print(' ',end='')
        for i in range(n0):
            print('   %d' %(i%10),end='')
        print('\n')
        print('  +' + '---+' * n0)
        for i in range(n0):
          
            
            print(str(i%10)+' | ' + ' | '.join(self.showmatrix[i]), '| ')
            print('  +' + '---+' * n0)
        if self.goblack:
            print('Turn: Black')
        else:
            print('Turn: White')

    def available(self,x,y,vmx,vgb):#Check whether it is ok to place
        if vmx[x][y] != 0 or not (0<=x<n0 and 0<=y<n0): return []
        d = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        bav, wav = [], []
        for v in d:
            if 0<=x+v[0]<n0 and 0<=y+v[1]<n0:
                if vmx[x+v[0]][y+v[1]] == 2 and vgb:
                    bav.append(v)
                if vmx[x+v[0]][y+v[1]] == 1 and not vgb:
                    wav.append(v)
        if vgb and len(bav) == 0: return []
        if not vgb and len(wav) == 0: return []
        if vgb:
            mark = []
            for e in bav:
                temp= []
                px,py = x+e[0],y+e[1]
                while vmx[px][py] == 2:
                    temp.append((px,py))
                    if 0<=px+e[0]<n0 and 0<=py+e[1]<n0:
                        px,py = px+e[0],py+e[1]
                    else:
                        break
                else:
                    if vmx[px][py] == 1: mark += temp
        if not vgb:
            mark = []
            for e in wav:
                temp= []
                px,py = x+e[0],y+e[1]
                while vmx[px][py] == 1:
                    temp.append((px,py))
                    if 0<=px+e[0]<n0 and 0<=py+e[1]<n0:
                        px,py = px+e[0],py+e[1]
                    else:
                        break
                else:
                    if vmx[px][py] == 2: mark += temp
        return mark
                                            
    def putxy(self,x,y,mark,vmx,vgb):
        if vgb:
            vmx[x][y] = 1
            for each in mark:
                vmx[each[0]][each[1]] = 1
        else:
            vmx[x][y] = 2
            for each in mark:
                vmx[each[0]][each[1]] = 2
        return vmx
        
    def check(self):#Conditions to end the game
        if self.nogo > 2:
            self.ok = False
            diff = []
            for i in range(n0):
                for j in range(n0):
                    diff.append(self.matrix[i][j])
            bk = diff.count(1)
            wt = diff.count(2)
            self.black = diff.count(1)
            self.white = diff.count(2)
            if bk > wt: 
                self.win = 'Black Win!!'
            elif bk < wt:
                self.win = 'White Win!!'
            else:
                self.win = 'Draw Game!'
            return
        diff = []
        for i in range(n0):
            for j in range(n0):
                diff.append(self.matrix[i][j])
        if len(set(diff)) == 2:
            self.ok = False
            bk = diff.count(1)
            wt = diff.count(2)
            self.black = diff.count(1)
            self.white = diff.count(2)
            if bk > wt: 
                self.win = 'Black win!!'
            elif bk < wt:
                self.win = 'White win!!'
            else:
                self.win = 'Draw Game!'
        else:
            self.black = diff.count(1)
            self.white = diff.count(2)
        if self.ok:
            bcango, wcango = False, False
            for i in range(n0):
                for j in range(n0):
                    if self.matrix[i][j] == 0:
                        if self.goblack:
                            if self.available(i,j,self.matrix,self.goblack): 
                                bcango = True
                                self.nogo = 0
                        else:
                            if self.available(i,j,self.matrix,self.goblack): 
                                wcango = True
                                self.nogo = 0
            if self.goblack and (bcango == False):
                self.goblack = not self.goblack
                self.nogo += 1
                self.check()
            elif not self.goblack and (wcango == False):
                self.goblack = not self.goblack
                self.nogo += 1
                self.check()

    def AI_evaluate_list(self,queue):
        prio=10
        if len(queue) == 0: return None
        bestmove = queue[0][2][0]
        bestmatrix = queue[0][0]
        for each in queue:
            ematrix = each[0]
            egb = each[1]
            estep = each[2][0]
            if estep in [(0,0),(0,n0-1),(n0-1,0),(n0-1,n0-1)]:#4 corner points are the best
                bestmove = estep
                prio=1
                break
            #elif estep in [(0,2),(0,3),(0,4),(0,5),(7,2),(7,3),(7,4),(7,5),(2,0),(3,0),(4,0),(5,0),(2,7),(3,7),(4,7),(5,7)]:
            elif (estep[0]==0 and estep[1]>1 and estep[1]<n0-2) or (estep[0]==n0-1 and estep[1]>1 and estep[1]<n0-2) or (estep[0]>1 and estep[0]<n0-2 and estep[1]==0) or (estep[0]>1 and estep[0]<n0-2 and estep[1]==n0-1):
            #rest sides are the next best(except for position just next to those corner points)
                
                if prio>2: 
                    bestmove = estep
                    prio=2
                continue    
                
            #elif estep in[(2,2),(2,3),(2,4),(2,5),(3,5),(4,5),(5,5),(5,4),(5,3),(5,2),(4,2),(3,2)]:
            elif (estep[0]>1 and estep[0]<n0-2 and estep[1]>1 and estep[1]<n0-2):
             #points surrounding the initial pieces(at least 2 units away from the sides) are the 3rd best
                if prio>3:
                    bestmove = estep
                    prio=3
                #continue    
            #elif estep in[(1,2),(1,3),(1,4),(1,5),(6,2),(6,3),(6,4),(6,5),(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6)]: 
            elif ((estep[0]==1 or estep[0]==n0-2) and estep[1]>1 and estep[1]<n0-2) or ((estep[1]==1 or estep[1]==n0-2) and estep[0]>1 and estep[0]<n0-2):
                if prio>4:
                    bestmove = estep
                    prio=4
                #continue
            elif ((estep[0]==0 or estep[0]==n0-1) and estep[1]==1) or ((estep[0]==0 or estep[0]==n0-1) and estep[1]==n0-2) or ((estep[1]==0 or estep[1]==n0-1) and estep[0]==n0-2) or ((estep[1]==0 or estep[1]==n0-1) and estep[0]==1) :
                if prio>5:
                    bestmove = estep
                    prio=5            
            
             
            cmovement, pmovement, maxadvantage = 0, 0, -99999
            for i in range(n0):
                for j in range(n0):
                    if self.available(i,j,ematrix,False): cmovement += 1
                    if self.available(i,j,ematrix,True): pmovement += 1
            if maxadvantage < cmovement - pmovement:
                maxadvantage = cmovement - pmovement
                #bestmove = estep
                bestmatrix = deepcopy(ematrix)
            elif maxadvantage == cmovement - pmovement:
                choice = random.choice([True, False])
                if choice: 
                    #bestmove = estep
                    bestmatrix = deepcopy(ematrix)
        return bestmove, bestmatrix, egb
                

    def AI_judge(self,vmx,vgb):
        queue1 = self.DFS(vmx,vgb)
        bmv1 = self.AI_evaluate_list(queue1)[0]
        bmx1 = deepcopy(self.AI_evaluate_list(queue1)[1])
        gb1 = not self.AI_evaluate_list(queue1)[2]
        queue2 = self.DFS(bmx1,gb1,[bmv1])
        return queue2
    
    def DFS(self,mx,gb,prev=[]):
        queue = []
        for i in range(n0):
            for j in range(n0):
                mx1 = deepcopy(mx)
                gb1 = gb
                if self.available(i,j,mx1,gb1):
                    lst = deepcopy(prev)
                    lst.append((i,j))
                    mx2 = self.putxy(i,j,self.available(i,j,mx1,gb1),mx1,gb1)
                    gb2 = not gb1
                    queue.append([mx2,gb2,lst])
        return queue
                    
game = blackwhite()
game.pr()
print('Enter the coordinate you want to go: eg. 0,0')
pos = input().split(',')
x, y = int(pos[0]), int(pos[1])
while game.ok:
    if game.available(x,y,game.matrix,game.goblack):
        mark = game.available(x,y,game.matrix,game.goblack)
        game.matrix = game.putxy(x,y,mark,game.matrix,game.goblack)
        game.goblack = not game.goblack
        game.check()
        game.pr()
        if not game.ok: break
        if game.goblack:
            print('Enter the coordinate you want to go: eg. 0,0')
            pos = input().split(',')
            x, y = int(pos[0]), int(pos[1])
        else:
            print('AI is thinking...')
            queue = game.DFS(game.matrix,game.goblack)
            if game.AI_evaluate_list(queue):
                x, y = game.AI_evaluate_list(queue)[0][0], game.AI_evaluate_list(queue)[0][1]
                if not game.available(x,y,game.matrix,game.goblack):
                    for i in range(n0):
                        for j in range(n0):
                            if game.available(i,j,game.matrix,game.goblack): x,y = i,j
    else:
        print('Invalid Input, please try again! eg. 0,0')
        pos = input().split(',')
        x, y = int(pos[0]), int(pos[1])
print('%s' % game.win)
print('Game Over!!')
input()