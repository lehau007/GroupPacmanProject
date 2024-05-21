from collections import deque
import queue
from board import boards
import numpy as np
WIDTH = 900
HEIGHT = 950 
arr = boards
def bfs(player_x : int,player_y : int):
   q = deque()
   num1 = (HEIGHT - 50) // 32
   num2 = WIDTH // 30
   check = [[0 for col in range(30)] for row in range(33)]
   start = (player_y // num1 ,player_x // num2,-1)
   q.append(start)
   while((len(q))):
      cur = q.popleft()
      if((arr[cur[0]][cur[1]] == 1 or arr[cur[0]][cur[1]] == 2) and cur != start):
         return cur[2]
      
      if cur[0] == 32 or cur[0] == 0 : 
          continue
      
      if(arr[cur[0] + 1][cur[1]] < 3 and check[cur[0] + 1][cur[1]] == 0):
         q.append((cur[0] + 1,cur[1],2))
         check[cur[0] + 1][cur[1]] = 1

      if(arr[cur[0] - 1][cur[1]] < 3 and check[cur[0] - 1][cur[1]] == 0):
         q.append((cur[0] - 1,cur[1],3))
         check[cur[0] - 1][cur[1]] = 1

      if cur[1] == 29:
         if(arr[cur[0]][0] < 3 and check[cur[0]][0] == 0):
            q.append((cur[0],0,0))
            check[cur[0]][0] = 1
      if(arr[cur[0]][cur[1] + 1] < 3 and check[cur[0]][cur[1] + 1] == 0):
         q.append((cur[0],cur[1] + 1,0))
         check[cur[0]][cur[1] + 1] = 1
      if cur[1] == 0:
         if(arr[cur[0]][29] < 3 and check[cur[0]][29] == 0):
            q.append((cur[0],29,1))
            check[cur[0]][29] = 1
      if(arr[cur[0]][cur[1] - 1] < 3 and check[cur[0]][cur[1] - 1] == 0):
         q.append((cur[0],cur[1] - 1,1))
         check[cur[0]][cur[1] - 1] = 1

