'''
a series of ships classes
'''
import pygame
import math
import Graphics
class Ships:
    def __init__ (self,grid,x,y,player,weapon=0,armour=0):
        '''
        initialize Ship class
        '''
        self.grid=grid
        self.player=player
        self.x=x
        self.y=y
        self.range=None
        self.cost=None
        self.weapon_cost=None
        self.move_cost=None
        self.image=None
        self.damage=None
        self.health=None
        self.weapon_type=weapon
        self.armour_type=armour
        self.freeze=False
        self.type=None
        
        # deleted blit: self.image.blit(self.surface,(16*x,16*y))
    def __str__(self):
        '''
        returns a description of the ship object
        '''
        return("{0} at {1},{2}; player is {3}".format(self.type,self.x,self.y,self.player))

    def move(self,x,y):
        '''
        move the ship,return a cost
        '''
        if not self.freeze:
            cost=self.move_cost*(abs(self.x-x)+abs(self.y-y))
            #rect=pygame.draw.rect(self.surface,(255,255,255),self.image.get_rect())
            #rect.blit(self.surface,(16*self.x,16*self.y))
            #self.image.blit(self.surface,(16*self.x,16*self.y))<-- unused coding to blit, now in Graphics.py (class Grid)
            self.x=x
            self.y=y
            self.grid.refresh()
            self.get_center()
            
            return cost
        else:
            print("this {0} is frozen at the moment".format(self))
            #should include more ways to inform the player, unfinished
            return 0

    def attack(self,target):
        '''
        attack the target, containing  animations
        '''
        if self.get_distance(target)<= self.range:
            target.get_damage(self.damage,self.weapon_type)
            clock=pygame.time.Clock()
            self.grid.attack(self,target)
            # unfinished railgun animation <-- now finished
            return self.weapon_cost
        else:
            #unfinished alert
            print("attack of {0} to {1} out of range".format(self,target))
            return 0

    def get_damage(self,damage,weapon_type):
        if(abs(weapon_type-self.armour_type)==0):
            self.health=self.health-int(damage/2)
        else:
            self.health=self.health-damage

    def get_distance(self,ship):
        l=(abs(self.center_x-ship.center_x))*(abs(self.center_x-ship.center_x))+(abs(self.center_y-ship.center_y))*(abs(self.center_y-ship.center_y))
        d=math.sqrt(l)
        return d

    def rotate(self):
        #rotate the image if on the opponent side
        if self.player==1:
            self.image=pygame.transform.rotate(self.image,180)

    def check_click(self,position):
        WIDTH=self.image.get_width()
        HEIGHT=self.image.get_height()
        x_match = position[0] > self.grid.x_to_X(self.x) and position[0] < self.grid.x_to_X(self.x) + WIDTH
        y_match = position[1] > self.grid.y_to_Y(self.y) and position[1] < self.grid.y_to_Y(self.y) + HEIGHT
        if x_match and y_match:
            return True
        else:
            return False


    def chosen(self):
        WIDTH=self.image.get_width()
        HEIGHT=self.image.get_height()
        pygame.draw.rect(self.grid.display,(255,0,0),(self.grid.x_to_X(self.x),self.grid.y_to_Y(self.y),WIDTH,HEIGHT),5)


class Torpedos(Ships):
    '''
    class Torpedos, as an basic example in ships; they have no special power
    small ship at a size of 1x1, or 16x16

    '''
    def __init__(self,grid,x,y,player,weapon=0,armour=0):
        super().__init__(grid,x,y,player)
        self.range=3
        self.cost=100
        self.weapon_cost=10
        self.move_cost=5
        self.image=pygame.image.load('ships/Torpedo.png')
        self.get_center()
        self.damage=10
        self.health=15
        self.type="Torpedo"
        self.rotate()
        grid.new_ship(self)
        self.val=1

    def get_center(self):
        self.center_x=self.x+0.5
        self.center_y=self.y-0.5

class Destroyers(Ships):
    '''
    class Destroyers, a larger ship that cannot fire lasers, no special power
    small ship at 1x2, or 16x32
    '''
    def __init__(self,grid,x,y,player,weapon=0,armour=0):
        super().__init__(grid,x,y,player)
        self.range=6
        self.cost=500
        self.weapon_cost=50
        self.move_cost=20
        self.get_center()
        self.image=pygame.image.load('ships/Destroyer.png')
        self.damage=25
        self.health=40
        self.type="Destroyer"
        self.rotate()
        grid.new_ship(self)
        self.val=2

    def get_center(self):
        self.center_x=self.x+0.5
        self.center_y=self.y-1

class Cruisers(Ships):

    '''
    class Cruisers, a larger ship that can fire lasers and railgun, no special power
    bigger ship at 2x4, or 32x64
    '''
    def __init__(self,grid,x,y,player,weapon,armour):
        super().__init__(grid,x,y,player,weapon,armour)
        self.range=10
        self.cost=1000
        self.weapon_cost=100
        self.move_cost=50
        self.get_center()
        self.image=pygame.image.load('ships/Cruiser.png')
        self.damage=50
        self.health=100
        self.type="Cruiser"
        self.weapon_type=weapon
        self.armour_type=armour
        self.rotate()
        grid.new_ship(self)
        self.val=3

    def get_center(self):
        self.center_x=self.x+1
        self.center_y=self.y-2
class Carriers(Ships):
    '''
    class Carriers, same grade as the cruisers, and have the same weapons like the cruisers, special power is to deploy torpedo ships
    same grade at 2x4 or 32x64
    '''
    def __init__(self,grid,x,y,player,weapon,armour):
        super().__init__(grid,x,y,player,weapon,armour)
        self.range=10
        self.cost=5000
        self.weapon_cost=100
        self.move_cost=100
        self.get_center()
        self.image=pygame.image.load('ships/Carrier.png')
        self.damage=50
        self.health=150
        self.type="Carrier"
        self.ships=True
        self.rotate()
        grid.new_ship(self)
        self.val=4
        self.weapon_type=weapon
        self.armour_type=armour

    def get_center(self):
        self.center_x=self.x+1
        self.center_y=self.y-2

    def launch(self):
        if self.ships:
            ships=[]
            if self.x==1:
                self.x=2
            if self.x==64:
                self.x=63
            x=self.x
            y=self.y
            player=self.player
            ships.append(Torpedos(self.grid,x-1,y,player))
            ships.append(Torpedos(self.grid,x-1,y-1,player))
            ships.append(Torpedos(self.grid,x-1,y-2,player))
            ships.append(Torpedos(self.grid,x-1,y-3,player))
            ships.append(Torpedos(self.grid,x+2,y,player))
            ships.append(Torpedos(self.grid,x+2,y-1,player))
            ships.append(Torpedos(self.grid,x+2,y-2,player))
            ships.append(Torpedos(self.grid,x+2,y-3,player))
            return ships
        else:
            #a way to tell players deployed already
            print('already deployed')

class E_ships(Ships):
    '''
    class E-ships, same grade as Destroyers, can fire lasers and railgun, but can also fire up emp
    ship at 1x2,or 16x32
    '''
    def __init__(self,grid,x,y,player,weapon,armour):
        super().__init__(grid,x,y,player,weapon,armour)
        self.range=10
        self.cost=5000
        self.move_cost=50
        self.weapon_cost=100
        self.image=pygame.image.load('ships/E-ship.png')
        self.damage=50
        self.health=80
        self.type="E-ship"
        self.ships=[]
        self.rotate()
        grid.new_ship(self)
        self.get_center()
        self.val=5
    def EMP(self,ships):
         #have to enter a list of ships, but cannot detect(needs further programming)<--done
         self.ships.clear()
         for item in ships:
             
             item.freeze=True
             self.ships.append(item)
         
    def unfreeze(self):
         #this should be used after one round
         for item in self.ships:
             item.freeze=False
    def get_center(self):
        self.center_x=self.x+0.5
        self.center_y=self.y-1

class Base(Ships):
    '''
    a basic Base class as the home base, cannot move
    Base at 8x4, or 128*64
    '''
    def __init__(self,grid,x,y,player,weapon=0,armour=0):
        super().__init__(grid,x,y,player)
        self.range=15
        self.weapon_cost=150
        self.damage=80
        self.health=500
        self.center_x=self.x+4
        self.center_y=self.y-2
        self.image=pygame.image.load('ships/HomeBase.png')
        self.type="Base"
        self.get_center()
        self.val=6
        if player==0:
            self.x=29
            self.y=6
        if player==1:
            self.x=29
            self.y=62
        self.get_center()

    def move(self,x,y):
        '''
        having shome fun
        '''
        print("why are u trying to move the home base???")
    def get_center(self):
        self.center_x=self.x+4
        self.center_y=self.y-2

        
def summon_ship(g,X,Y,label2,val2,label,p0,p=0):

    ship=None
    if label=="ships/Torpedo.png" or label==1:
        if p0.RP >=100:
            ship=Torpedos(g,X,Y,p,label2,val2)
            p0.ships.append(ship)
            p0.RP=p0.RP-ship.cost
            g.refresh()
        else:
            print("not enough RP")
        
    if label=="ships/Destroyer.png" or label==2:
        if p0.RP >=500:
            ship=Destroyers(g,X,Y,p,label2,val2)
            p0.ships.append(ship)
            p0.RP=p0.RP-ship.cost
            g.refresh()
        else:
            print("not enough RP")
        
    if label=="ships/Cruiser.png"or label==3:
        if p0.RP >=1000:
            ship=Cruisers(g,X,Y,p,label2,val2)
            p0.ships.append(ship)
            p0.RP=p0.RP-ship.cost
            g.refresh()
        else:
            print("not enough RP")
        
    if label=="ships/Carrier.png" or label==4:
        if p0.RP >=5000:
            ship=Carriers(g,X,Y,p,label2,val2)
            p0.ships.append(ship)
            p0.RP=p0.RP-ship.cost
            g.refresh()
        else:
            print("not enough RP")
        
    if label=="ships/E-ship.png"or label==5:
        if p0.RP >=5000:
            ship=E_ships(g,X,Y,p,label2,val2)
            p0.ships.append(ship)
            p0.RP=p0.RP-ship.cost
            g.refresh()
        else:
            print("not enough RP")
    
    return ship