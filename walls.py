import pygame
import sys
from collections import deque #used for queue
pygame.init()
#--------------------------------------------

#CONSTANCS USED IN MAZE_GEN
screen_size=(WIDTH,HEIGHT)=(800,800)
BGCOLOUR=( 255 , 255 , 255)


#SETTING UP THE SCREEN
screen=pygame.display.set_mode(screen_size)
rekt=(50,50,WIDTH-100,HEIGHT-100)
FPS=90#frasmes per second 

screen.fill((255,255,255))#white color of the screen
screen.fill((71, 0, 156),rekt)#voilet cor of the screeen

wall=[]
pygame.display.update()
#_________________________________________________________
class cell (object):
	def __init__(self,cell_size,color,pos):
		self.cell_size=cell_size
		self.color=color
		self.pos=pos
		self.rekt=(pos[0],pos[1],self.cell_size,self.cell_size)
		self.is_src=False #set the flag if the cell obj is  SOURCE
		self.is_dest=False#set the flag if the cell obj is DESTINATION
		self.is_wall=False#sel if the flag is cell obj is WALL
		#________________variables used by path finding algos________________________
		self.parent=(0,0)
		self.visited=False #set if the cell is visited
		self.dist=0#dist from SOURCE cell
		#_______________________________________________________________________
	def change_cell_color(self,color):
		self.color=color
	def draw(self,SCREEN,color=[71,0,156]):
		self.color=color
		SCREEN.fill(color,self.rekt)		
		pygame.display.update(self.rekt)
	def resetcell(self,screen):
		self.is_src=False
		self.is_dest=False
		self.is_wall=False
		self.parent=(0,0)
		self.visited=False
		self.dist=0
		self.draw(screen)
		
		
class Grid (object):
	source_set=False #both are python static variables thet are shared by all the objects of grid class
	dest_set=False
	dest=(0,0)#cell coordinates of source and destination
	src=(0,0)
	erectwall=False #flsg that allows to to build wall
	breakwall=False#flag that allows to break walls
	
	def __init__(self,rows,cols,cell_size,x,y,color=[71,0,156]):
		self.xcount=rows
		self.ycount=cols
		self.cell_size=cell_size
		self.pos=(x,y)
		self.cell_color=color
		self.grid=[]
		for i in range(0, self.xcount):
			self.grid.append([])
			for j in range (0,self.ycount):
				self.grid[i].append(cell(self.cell_size,     self.cell_color ,     (50+i*self.cell_size ,50+j*self.cell_size )))
				self.grid[i][j].draw(screen)	
	def resetsrc(self):
		#print(self.src,"\nsrc_set?",self.source_set)
		self.source_set=False
		self.grid [ self.src[0] ] [ self.src[1] ].draw(screen)
		self.src=(0,0)
	def resetdest(self):
		#print(self.dest,"\nsrc_set?",self.dest_set)
		self.dest_set=False
		self.grid [ self.dest[0] ] [ self.dest[1] ].draw(screen)
		self.dest=(0,0)
	def reset(self,screen):
		self.resetsrc()
		self.resetdest()
		self.erectwall=False
		self.breakwall=False
		for i in range( self.xcount):
			for j in range (self.ycount):
				self.grid[i][j].resetcell(screen)		



def isvalid(cell_coord,maze):
	if(cell_coord [  0 ]  >= 0 and cell_coord [  0 ]  < 50 and cell_coord [ 1 ] >=0 and cell_coord [  1 ]  <50 and not maze.grid[ cell_coord [  0 ]   ][ cell_coord [  1  ]   ].is_wall):
		return True
	return False
def setfps(x):
	global_var= globals()
	global_var["FPS"]=x
	print("fps set to ",x)	
def BFS(maze):
	maze.grid [ maze.src[0] ] [ maze.src[1] ].dist=0
	maze.grid [ maze.src[0] ] [ maze.src[1] ].visited=True #set the SOURCE  CELL  as VISITED
	maze.grid[ maze.src[0] ][ maze.src[1] ].parent=(-1,-1)#set the PARENT of the  SOURE CELL as (-1,-1)
	
	visited_cell_color=[184,255,99]
	
	q=deque() #queue maintains the vertices whose adjacent vertives are yet to be explored
	q.append(maze.src)
	
	adj=[(0,-1),(1,0),(0,1),(-1,0)] 
	while(len(q)!=0):
		current_cell=q.popleft();
		t=pygame.time.Clock()
		t.tick(FPS)
		for i in adj:
			neighbour=(  current_cell [ 0 ] + i[0] , current_cell [ 1 ] + i [ 1 ] )
			if( isvalid( neighbour ,maze) and not  maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].visited ):
				if neighbour != maze.dest:
					maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].draw(screen,visited_cell_color)
				else:
					maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].draw(screen,(255,255,255))
				
				maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].visited=True
				maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].dist  = maze.grid[ current_cell[ 0 ] ][ current_cell[ 1 ] ].dist+1
				maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].parent=current_cell
				q.append(neighbour)
				if current_cell != maze.src :#maze.grid[ neighbour[ 0 ] ][ neighbour[ 1 ] ].parent
					maze.grid[ current_cell[ 0 ] ][current_cell[ 1 ] ].draw(screen, (99, 163, 184 ))	
				
			if ( isvalid( neighbour,maze )  and neighbour==maze.dest ):
				return True	
	return False			
def print_shortest_path(maze):
	if( not BFS(maze) ):
		print("NO PATH EXIST BETWEEN  YOUR CHOSEN SOURCE AND DSETINATION")
		return 
	dest=maze.dest
	print(" PATH EXIST BETWEEN  YOUR CHOSEN SOURCE AND DSETINATION")
	while	maze.grid[ dest[0] ] [ dest[1] ].parent !=  (-1,-1)	:	
		maze.grid [ dest[0] ] [ dest[1] ].draw(screen,[255,255,255])
		dest=maze.grid [ dest[0] ] [ dest[1] ].parent
		t=pygame.time.Clock()
		t.tick(FPS)

#pygame.display.update()
#pygame.display.update(50  ,  50  ,   MAZE.xcount*MAZE.cell_size  , MAZE.ycount*MAZE.cell_size)

def mainloop():
	MAZE=Grid(50,50,14,50,50)
	operation=0
	pressed=False
	while True :
		if pressed:	
				mouse_pos=pygame.mouse.get_pos()
				
				if operation==2:#DRAWS WALLS
						
							wall.append(((mouse_pos[0]-50)//MAZE.cell_size  ,  (mouse_pos[1]-50)//MAZE.cell_size , pressed))		
							for i in wall:
								if(i[2]==True and   i[0]>=0 and i[0]<50 and i[1]>=0 and i[1]<50  and not MAZE.grid[ i[0] ] [ i[1] ].is_src and not MAZE.grid[ i[0] ] [ i[1] ].is_dest ):
									if MAZE.erectwall==True and not MAZE.grid[ i[0] ] [ i[1] ].is_wall:
										MAZE.grid[ i[0] ] [ i[1] ].draw(screen,(255,5,255))
										MAZE.grid[ i[0] ] [ i[1] ].is_wall=True
										MAZE.breakwall=False
									elif MAZE.breakwall ==True and MAZE.grid[ i[0] ] [ i[1] ].is_wall:
										MAZE.grid[ i[0] ] [ i[1] ].draw(screen)
										MAZE.grid[ i[0] ] [ i[1] ].is_wall=False
										MAZE.erectwall=False
									wall.pop()
									
				elif operation==3 and not MAZE.source_set:#DRAWS SOURCE
							wall.append(((mouse_pos[0]-50)//MAZE.cell_size  ,  (mouse_pos[1]-50)//MAZE.cell_size , pressed))		
							for i in wall:
								if(i[2]==True and  i[0]>=0 and i[0]<50 and i[1]>=0 and i[1]<50  and not MAZE.grid[ i[0] ][ i[1] ].is_wall and not MAZE.grid[ i[0] ] [ i[1] ].is_src and not MAZE.grid[ i[0] ] [ i[1] ].is_dest ):
									MAZE.grid[ i[0] ] [ i[1] ].draw(screen,(255,255,255))
									MAZE.grid[ i[0] ] [ i[1] ].is_src=True
									MAZE.source_set=True
									MAZE.src=(i[0],i[1])
									#print(MAZE.src,"\nsrc_set?",MAZE.source_set)
									wall.pop()
									operation=0
									break
				elif operation==4 and not MAZE.dest_set:#DRAWS DESTINATION
							wall.append(((mouse_pos[0]-50)//MAZE.cell_size  ,  (mouse_pos[1]-50)//MAZE.cell_size , pressed))		
							for i in wall:
								if(i[2]==True and  i[0]>=0 and i[0]<50 and i[1]>=0 and i[1]<50  and not MAZE.grid[ i[0] ][ i[1] ].is_wall and not MAZE.grid[ i[0] ] [ i[1] ].is_src and not MAZE.grid[ i[0] ] [ i[1] ].is_dest ):
									MAZE.grid[ i[0] ] [ i[1] ].draw(screen,(0,0,0))
									MAZE.grid[ i[0] ] [ i[1] ].is_dest=True
									MAZE.dest_set=True
									MAZE.dest=(i[0],i[1])
									#print(MAZE.dest, "\ndest_set?",MAZE.dest_set)
									wall.pop()
									operation=0
									break
		if operation ==5 and MAZE.source_set :
					MAZE.resetsrc()
					opeartion=0
		if operation==6 and MAZE.dest_set:
					MAZE.resetdest()	
					operation=0					
									
								
		for event in pygame.event.get():		
				if event.type==pygame.QUIT:
					run=False
					pygame.quit()	
					quit()
				if event.type==pygame.KEYDOWN :
					if event.key==pygame.K_2:
						operation=2
						#print("DRAWING WALLS")
					elif event.key==pygame.K_3:
						operation=3
						#print("set_src")
					elif event.key==pygame.K_4: 	
						operation=4
						#print("set_dest")
					elif event.key==pygame.K_5: 	
						operation=5
						#print("reset_src")
					elif event.key==pygame.K_6: 	
						operation=6
						#print("reset_src")
					elif event.key==pygame.K_1 and MAZE.source_set and MAZE.dest_set:
						operation=0
						print_shortest_path(MAZE)
					elif event.key==pygame.K_9:
						MAZE.reset(screen)	
				if event.type==pygame.MOUSEBUTTONDOWN:
					pressed=True
					if event.button==1:
						#print("LEFT CLICK")
						MAZE.erectwall=True
						MAZE.breakwall=False
					elif event.button==3:
						#print("RIGHT CLICK")
						MAZE.breakwall=True
						MAZE.erectwall=False	
				if event.type==pygame.MOUSEBUTTONUP:
					pressed=False	
		
if __name__ == "__main__":
	    print("Arguments count:", {len(sys.argv)})
	    for  arg in enumerate  (sys.argv):
		print("Argument  ",arg[0],"=",arg[1])
		if( arg[1]=="-fps"):
			#print( sys.argv[ int(arg[0] +1) ])
			setfps(int(sys.argv[ int(arg[0] +1)]))
            mainloop()   

