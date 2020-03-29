import pygame

pygame.init()
#--------------------------------------------

#CONSTANCS USED IN MAZE_GEN
screen_size=(WIDTH,HEIGHT)=(800,800)
BGCOLOUR=( 255 , 255 , 255)

screen=pygame.display.set_mode(screen_size)
rekt=(50,50,WIDTH-100,HEIGHT-100)
screen.fill((255,255,255))#white color of the screen
screen.fill((71, 0, 156),rekt)


pygame.display.update()

class cell (object):
	def __init__(self,cell_size,color,pos):
		self.cell_size=cell_size
		self.color=color
		self.pos=pos
		self.rekt=(pos[0],pos[1],self.cell_size,self.cell_size)
		self.is_src=False
		self.is_dest=False
		self.is_wall=False
		
	def change_cell_color(self,color):
		self.color=color
	def draw(self,SCREEN,color=[71,0,156]):
		SCREEN.fill(color,self.rekt)		
		pygame.display.update(self.rekt)
		
		
class Grid (object):
	source_set=False #both are python static variables thet are shared by all the objects of grid class
	dest_set=False
	dest=(0,0)#cell coordinates of source and destination
	src=(0,0)
	erectwall=False
	breakwall=False
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

MAZE=Grid(50,50,14,50,50)

	

#pygame.display.update()
#pygame.display.update(50  ,  50  ,   MAZE.xcount*MAZE.cell_size  , MAZE.ycount*MAZE.cell_size)
pressed=False
wall=[]

operation=0
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
								print(MAZE.src,"\nsrc_set?",MAZE.source_set)
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
								print(MAZE.dest, "\ndest_set?",MAZE.dest_set)
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
					
						
			if event.type==pygame.MOUSEBUTTONDOWN:
				pressed=True
				if event.button==1:
					print("LEFT CLICK")
					MAZE.erectwall=True
					MAZE.breakwall=False
				elif event.button==3:
					print("RIGHT CLICK")
					MAZE.breakwall=True
					MAZE.erectwall=False	
			if event.type==pygame.MOUSEBUTTONUP:
				pressed=False	
		


