import pygame
import Ships
import Input
import Enemy
import Graphics
import Player
import Enemy
import random
    #resolution is 1024x1024
    #64x64
    #x and y means 64x64
    #need to x16
    #weapon type 0 means kinetic energy weapon, 1 means lazer
    #resolution means (blit) x=x*16 y=(64-y)*16

BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)

#Enemy.init()
k,index=Enemy.get_index()
"""
#demo
pygame.init()
p0=Player.Player(0)
p1=Player.Player(1)
g=Graphics.Grid()
m=Graphics.Menu(g)
p0=Player.Player(0)
p1=Player.Player(1)
m.start_menu()
m.in_game_multi_player(p0,p1,0)

g.draw_grid()
b0,b1=g.draw_and_create_base()
print("{0}{1}".format(b0,b1))
s1=Ships.Carriers(g,20,30,0,1,1)
s2=Ships.Cruisers(g,10,30,1,1,1)
s1.move(20,40)
s2.move(20,48)
s2.attack(s1)
g.refresh()

s3=Ships.Cruisers(g,30,30,0,0,0)
s4=Ships.Destroyers(g,40,30,1,0,0)
s4.attack(s3)
g.refresh()

m.in_game_multi_player(p0,p1,1,s3)
pygame.display.update()
input()
"""


pygame.init()
while True:
    g=Graphics.Grid()
    m=Graphics.Menu(g)


    if m.start_menu()=="S":
        #single player
        '''
        X_train, X_test, y_train, y_test = Enemy.load_data()
        LRmodel=Enemy.AI(X_train, X_test, y_train, y_test)
        print("-" * 10)
        '''
        
        p0=Player.Player(0)
        p1=Player.Player(1)
        b0,b1=g.draw_and_create_base()
        p0.ships.append(b0)
        p1.ships.append(b1)
        round=0
        sround=0
        is_player0=True
        activated_eship=None
        activated_sround=None
        while p0.ships[0].health>0 and p1.ships[0].health>0:
            sround=sround+1
            if is_player0:
                this_round=0
                round=round+1
                if round != 1:
                        p0.RP=p0.RP+2000
                        p1.RP=p1.RP+2000
                is_player0=not is_player0
            else:
                this_round=1
                is_player0=not is_player0
            m.in_game_single_player(p0,p1,this_round)
            next_round=False
            ship_to_display=None
            ship_to_deploy=None
            
            if activated_eship and activated_sround==sround-2:
                activated_eship.unfreeze()
                activated_eship=None
                activated_sround=None

            if this_round==0:
                player_RP_before=p0.RP
            elif this_round==1:
                player_RP_before=p1.RP
            round_count=0
            # single round
            while not next_round and round_count<=4 and this_round == 1:
                '''
                lists=[]
                for item in g.make_list():
                    lists.append(item)
                x_list=Enemy.make_x_list(round,sround,1,p1.RP,p1.RP-random.randint(500,5000))
                y_list=LRmodel.predict(x_list)
                print(y_list)
                '''

                Input.undo_deploy(m)
                Input.undo_menu(m)
                Input.unclickable_deploy(m)
                g.refresh()
                m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)


                flag=False
                round_count=round_count+1
                for item in p1.ships:
                    for ship in g.all_ships:
                        if item.get_distance(ship)<=item.range and ship.player==0 and item.player==1:
                            if p1.RP>item.weapon_cost:
                                        item.attack(ship)
                                        p1.RP=p1.RP-item.weapon_cost
                            print("{0} attacked {1}".format(item,ship))
                            flag=True
                            if ship.health<=0:
                                    g.del_ship(ship,p0)
                                    g.refresh()
                            break
                    if flag==True:
                        break


                function = random.randint(1,4)
                print(function)
                if function == 1:
                    if len(p1.ships)==1:
                        round_count=round_count-1
                        continue
                    ship_to_move=random.choice(p1.ships)
                    if ship_to_move.val!=6:
                        while True:
                            x=random.randint(ship_to_move.x-5,ship_to_move.x+5)
                            y=random.randint(ship_to_move.y-15,ship_to_move.y+2)
                            if y<5  or y> 50:
                                continue
                            X=g.x_to_X(x)
                            Y=g.y_to_Y(y)
                            for item in g.all_ships:
                                collide=item.check_click((X,Y))
                                if collide:
                                    break
                            if collide:
                                continue
                            backup=p1.RP
                            x_backup=ship_to_move.x
                            y_backup=ship_to_move.y
                            p1.RP=p1.RP-ship_to_move.move(x,y)
                            if p1.RP<0:
                                p1.RP=backup
                                ship_to_move.move(x_backup,y_backup)
                                break
                            else:
                                break
                elif function==2:
                    i=0
                    while i<5:
                        if len(p1.ships)>6:
                            round_count=round_count-1
                            break
                        val=random.randint(1,5)
                        armour_val=random.randint(0,1)
                        weapon_val=random.randint(0,1)
                        x=random.randint(5,58)
                        y=random.randint(54,61)
                        X=g.x_to_X(x)
                        Y=g.y_to_Y(y)
                        print("should summon val:{0},armour:{1},weapon:{2}".format(val,weapon_val,armour_val))
                        for item in g.all_ships:
                            collide=item.check_click((X,Y))
                            if collide:
                                break
                        if collide:
                            continue
                        ship=Ships.summon_ship(g,x,y,weapon_val,armour_val,val,p1,1)
                        
                        if ship:
                            break
                        else:
                            i=i+1
                elif function==3:
                    flag=False
                    for item in p1.ships:
                        for ship in g.all_ships:
                            if item.get_distance(ship)<=20 and ship.player!=this_round and item.val!=6 and item!=ship:
                                while True:
                                    x=random.randint(ship.x-5,ship.x+5)
                                    y=random.randint(ship.y-5,ship.y+5)
                                    X=g.x_to_X(x)
                                    Y=g.y_to_Y(y)
                                    for item in g.all_ships:
                                        collide=item.check_click((X,Y))
                                        if collide:
                                            break
                                    if collide:
                                        continue

                                    if p1.RP>item.weapon_cost:
                                        item.attack(ship)
                                        p1.RP=p1.RP-item.weapon_cost
                                    print("{0} attacked {1} while moving".format(item,ship))
                                    flag=True
                                    if ship.health<=0:
                                            g.del_ship(ship,p0)
                                            g.refresh()
                                            break
                                    break
                        if flag==True:
                            break
                elif function==4:
                    flag=False
                    for item in p1.ships:
                        for ship in g.all_ships:
                            if item.get_distance(ship)<=10 and ship.player!=this_round and (item.val==4 or item.val==5) and item!=ship:
                                while True:
                                    x=random.randint(ship.x-5,ship.x+5)
                                    y=random.randint(ship.y-5,ship.y+5)
                                    X=g.x_to_X(x)
                                    Y=g.y_to_Y(y)
                                    for item in g.all_ships:
                                        collide=item.check_click((X,Y))
                                        if collide:
                                            break
                                    if collide:
                                        continue
                                    
                                    if item.val==4:
                                        launch=False
                        
                                        if p1.RP>=500:
                                            p1.RP=p1.RP-500
                                            launch=True
                                           
                                        m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                                        if launch:
                                            for item in val1.launch():
                                                g.new_ship(item)
                                                if this_round==0:
                                                    p0.ships.append(item)
                                                elif this_round==1:
                                                    p1.ships.append(item)
                                                g.refresh()

                                    if item.val==5:
                                        launch=False
                                        
                                        if this_round==1 and p1.RP>=1000:
                                            p1.RP=p1.RP-1000
                                            launch=True
                                        m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                                        if launch:
                                            EMP=[]
                                            for item in g.all_ships:
                                                if item.get_distance(val1)<=10 and item!=val1:
                                                    EMP.append(item)
                                            val1.EMP(EMP)
                                            activated_eship=val1
                                            activated_sround=sround
                                            g.EMP(activated_eship)


                                    print("{0} attacked {1} while moving".format(item,ship))
                                    flag=True

                                    break

                        if flag==True:
                            break
                    if flag==False:
                        round_count=round_count-1
                        continue





            while not next_round and round_count<=4 and this_round == 0:
                round_count=round_count+1
                lists=[]
                '''
                lists=[]
                for item in g.make_list():
                    lists.append(item)
                '''

                Input.undo_deploy(m)
                Input.undo_menu(m)
                Input.unclickable_deploy(m)
                g.refresh()
                m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                label1,val1=Input.listen1(g,m)
                if label1=="ship":
                    print(val1)
                    ship_to_display=val1
                    val1.chosen()
                    m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                elif label1=="button":
                    print(val1)
                    
                    Input.unclickable_menu(m)
                    Input.undo_deploy(m)
                    m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)

                    if val1.label[6:]=="Torpedo.png":
                        m.torpedo_color=RED
                    elif val1.label[6:]=="Destroyer.png":
                        m.destroyer_color=RED
                    elif val1.label[6:]=="Cruiser.png":
                        m.cruiser_color=RED
                    elif val1.label[6:]=="Carrier.png":
                        m.carrier_color=RED
                    elif val1.label[6:]=="E-ship.png":
                        m.eship_color=RED
                    
                    m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                    ship_to_deploy=val1
                elif label1=="finish":
                    print("finish")
                    next_round=True
                    continue
                label2,val2=Input.listen2(g,m,p0,p1,this_round,ship_to_display,label1,round_count)
                if label2=="undo":
                    round_count=round_count-1
                    continue
                if label2=="move":
                    while True:
                        m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                        x,y,n=Input.listen3()
                        X=g.X_to_x(x)
                        Y=g.Y_to_y(y)
                        X_backup=val1.x
                        Y_backup=val1.y
                        for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide:
                                    break
                        if not collide and x<1024 and y<1024:
                            if this_round==0 and val1.player==0:
                                backup=p0.RP
                                p0.RP=p0.RP-val1.move(X,Y)
                                if p0.RP<0:
                                    p0.RP=backup
                                    val1.move(X_backup,Y_backup)
                                    print("insufficient RP")
                                else:
                                    Enemy.writerow(index,round_count,sround,this_round,backup,p0.RP,val1.val,X_backup,Y_backup,0,X,Y,0,0,0,lists)
                                    break
                            elif this_round==1 and val1.player==1:
                                backup=p1.RP
                                p1.RP=p1.RP-val1.move(X,Y)
                                if p1.RP<0:
                                    p1.RP=backup
                                    val1.move(X_backup,Y_backup)
                                    print("insufficient RP")
                                else:
                                    Enemy.writerow(index,round_count,sround,this_round,backup,p1.RP,val1.val,X_backup,Y_backup,0,X,Y,0,0,0,lists)
                                    break
                            
                        if m.undo.check_click((x,y)):
                            round_count=round_count-1
                            break

                if label2=="attack":
                    m.attack_color=RED
                    m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                    while True:
                        X_backup=val1.x
                        Y_backup=val1.y
                        x,y,n=Input.listen3()
                        X=g.X_to_x(x)
                        Y=g.Y_to_y(y)
                        target=None
                        for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide and item!=val1:
                                    target=item
                                    break
                        backup0=p0.RP
                        backup1=p1.RP
                        if target:
                             if val1.get_distance(target)>=val1.range:
                                 print("attack out of range")

                        if collide and n==0 and target:
                            if this_round==0 and val1.player==0 and target.player==1 and val1.get_distance(target)<=val1.range:
                                if p0.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p0.RP=p0.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                if target.health<=0:
                                    g.del_ship(target,p1)
                                    g.refresh()
                                break
                           

                        if collide and n==1 and target:
                            if round_count>5:
                                break
                            if this_round==0 and val1.player==0 and target.player==1 and val1.get_distance(target)<=val1.range:
                                if p0.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p0.RP=p0.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                round_count=round_count+1
                                if target.health<=0:
                                    g.del_ship(target,p1)
                                    g.refresh()
                                    
                                
                                   
                        if m.undo.check_click((x,y)):
                            round_count=round_count-1
                            break
                        if not collide and n==0:
                            round_count=round_count-1
                            break
                                
                if label2=="change":
                    #yeah,nothing here :p
                    round_count=round_count-1
                    continue
                if label2=="special":
                    backup0=p0.RP
                    backup1=p1.RP
                    if val1.type=="Carrier":
                        launch=False
                        
                        if this_round==0 and p0.RP>=500:
                            p0.RP=p0.RP-500
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        elif this_round==1 and p1.RP>=500:
                            p1.RP=p1.RP-500
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                        if launch:
                            for item in val1.launch():
                                g.new_ship(item)
                                if this_round==0:
                                    p0.ships.append(item)
                                elif this_round==1:
                                    p1.ships.append(item)
                                g.refresh()

                    if val1.type=="E-ship":
                        launch=False
                        if this_round==0 and p0.RP>=1000:
                            p0.RP=p0.RP-1000
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        elif this_round==1 and p1.RP>=1000:
                            p1.RP=p1.RP-1000
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        m.in_game_single_player(p0,p1,this_round,ship_to_display,round_count)
                        if launch:
                            EMP=[]
                            for item in g.all_ships:
                                if item.get_distance(val1)<=10 and item!=val1:
                                    EMP.append(item)
                            val1.EMP(EMP)
                            activated_eship=val1
                            activated_sround=sround
                            g.EMP(activated_eship)

                if label2==1 or label2==0:
                        backup0=p0.RP
                        backup1=p1.RP
                        while True:
                            x,y,n=Input.listen3()
                            X=g.X_to_x(x)
                            Y=g.Y_to_y(y)
                            for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide:
                                    break
                            if m.undo.check_click((x,y)):
                                round_count=round_count-1
                                break
                            if x<1024 and y<1024:
                                if Y<14 and not collide and this_round==0:
                                    print(X,Y,val1.label)
                                    ship=Ships.summon_ship(g,X,Y,label2,val2,val1.label,p0,0)
                                    if ship:
                                        Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,ship.val,0,0,2,X,Y,0,label2+1,val2+1,lists)
                                    break
                                if Y>54 and not collide and this_round==1:
                                    print(X,Y,val1.label)
                                    ship=Ships.summon_ship(g,X,Y,label2,val2,val1.label,p1,1)
                                    if ship:
                                        Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,ship.val,0,0,2,X,Y,0,label2+1,val2+1,lists)
                                    break

                

    elif m.start_menu()=="M":
        #multi player
        print("multiplayer")
        p0=Player.Player(0)
        p1=Player.Player(1)
        b0,b1=g.draw_and_create_base()
        p0.ships.append(b0)
        p1.ships.append(b1)
        round=0
        sround=0
        is_player0=True
        activated_eship=None
        activated_sround=None
        while p0.ships[0].health>0 and p1.ships[0].health>0:
            sround=sround+1
            if is_player0:
                this_round=0
                round=round+1
                if round != 1:
                        p0.RP=p0.RP+2000
                        p1.RP=p1.RP+2000
                is_player0=not is_player0
            else:
                this_round=1
                is_player0=not is_player0
            m.in_game_multi_player(p0,p1,this_round)
            next_round=False
            ship_to_display=None
            ship_to_deploy=None
            
            if activated_eship and activated_sround==sround-2:
                activated_eship.unfreeze()
                activated_eship=None
                activated_sround=None

            if this_round==0:
                player_RP_before=p0.RP
            elif this_round==1:
                player_RP_before=p1.RP
            round_count=0
            # single round
            while not next_round and round_count<=4:
                round_count=round_count+1
                lists=[]
                '''
                for item in g.make_list():
                    lists.append(item)
                '''

                Input.undo_deploy(m)
                Input.undo_menu(m)
                Input.unclickable_deploy(m)
                g.refresh()
                m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                label1,val1=Input.listen1(g,m)
                if label1=="ship":
                    print(val1)
                    ship_to_display=val1
                    val1.chosen()
                    m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                elif label1=="button":
                    print(val1)
                    
                    Input.unclickable_menu(m)
                    Input.undo_deploy(m)
                    m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)

                    if val1.label[6:]=="Torpedo.png":
                        m.torpedo_color=RED
                    elif val1.label[6:]=="Destroyer.png":
                        m.destroyer_color=RED
                    elif val1.label[6:]=="Cruiser.png":
                        m.cruiser_color=RED
                    elif val1.label[6:]=="Carrier.png":
                        m.carrier_color=RED
                    elif val1.label[6:]=="E-ship.png":
                        m.eship_color=RED
                    
                    m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                    ship_to_deploy=val1
                elif label1=="finish":
                    print("finish")
                    next_round=True
                    continue
                label2,val2=Input.listen2(g,m,p0,p1,this_round,ship_to_display,label1,round_count)
                if label2=="undo":
                    round_count=round_count-1
                    continue
                if label2=="move":
                    while True:
                        m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                        x,y,n=Input.listen3()
                        X=g.X_to_x(x)
                        Y=g.Y_to_y(y)
                        X_backup=val1.x
                        Y_backup=val1.y
                        for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide:
                                    break
                        if not collide and x<1024 and y<1024:
                            if this_round==0 and val1.player==0:
                                backup=p0.RP
                                p0.RP=p0.RP-val1.move(X,Y)
                                if p0.RP<0:
                                    p0.RP=backup
                                    val1.move(X_backup,Y_backup)
                                    print("insufficient RP")
                                else:
                                    Enemy.writerow(index,round_count,sround,this_round,backup,p0.RP,val1.val,X_backup,Y_backup,0,X,Y,0,0,0,lists)
                                    break
                            elif this_round==1 and val1.player==1:
                                backup=p1.RP
                                p1.RP=p1.RP-val1.move(X,Y)
                                if p1.RP<0:
                                    p1.RP=backup
                                    val1.move(X_backup,Y_backup)
                                    print("insufficient RP")
                                else:
                                    Enemy.writerow(index,round_count,sround,this_round,backup,p1.RP,val1.val,X_backup,Y_backup,0,X,Y,0,0,0,lists)
                                    break
                            
                        if m.undo.check_click((x,y)):
                            round_count=round_count-1
                            break

                if label2=="attack":
                    m.attack_color=RED
                    m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                    while True:
                        X_backup=val1.x
                        Y_backup=val1.y
                        x,y,n=Input.listen3()
                        X=g.X_to_x(x)
                        Y=g.Y_to_y(y)
                        target=None
                        for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide and item!=val1:
                                    target=item
                                    break
                        backup0=p0.RP
                        backup1=p1.RP
                        if collide and n==0 and target:
                            if this_round==0 and val1.player==0 and target.player==1 and val1.get_distance(target)<=val1.range:
                                if p0.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p0.RP=p0.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                if target.health<=0:
                                    g.del_ship(target,p1)
                                    g.refresh()
                                break
                            if this_round==1 and val1.player==1 and target.player==0 and val1.get_distance(target)<=val1.range:
                                if p1.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p1.RP=p1.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                if target.health<=0:
                                    g.del_ship(target,p0)
                                    g.refresh()
                                break

                        if collide and n==1 and target:
                            if round_count>5:
                                break
                            if this_round==0 and val1.player==0 and target.player==1 and val1.get_distance(target)<=val1.range:
                                if p0.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p0.RP=p0.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                round_count=round_count+1
                                if target.health<=0:
                                    g.del_ship(target,p1)
                                    g.refresh()
                                    
                            if this_round==1 and val1.player==1 and target.player==0 and val1.get_distance(target)<=val1.range:
                                if p1.RP-val1.weapon_cost<0:
                                    print("insufficient money")
                                    break
                                p1.RP=p1.RP-val1.attack(target)
                                Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,1,target.x,target.y,0,0,0,lists)
                                round_count=round_count+1
                                if target.health<=0:
                                    g.del_ship(target,p0)
                                    g.refresh()
                                   
                        if m.undo.check_click((x,y)):
                            round_count=round_count-1
                            break
                        if not collide and n==0:
                            round_count=round_count-1
                            break
                                
                if label2=="change":
                    #yeah,nothing here :p
                    round_count=round_count-1
                    continue
                if label2=="special":
                    backup0=p0.RP
                    backup1=p1.RP
                    if val1.type=="Carrier":
                        launch=False
                        
                        if this_round==0 and p0.RP>=500:
                            p0.RP=p0.RP-500
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        elif this_round==1 and p1.RP>=500:
                            p1.RP=p1.RP-500
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                        if launch:
                            for item in val1.launch():
                                g.new_ship(item)
                                if this_round==0:
                                    p0.ships.append(item)
                                elif this_round==1:
                                    p1.ships.append(item)
                                g.refresh()

                    if val1.type=="E-ship":
                        launch=False
                        if this_round==0 and p0.RP>=1000:
                            p0.RP=p0.RP-1000
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        elif this_round==1 and p1.RP>=1000:
                            p1.RP=p1.RP-1000
                            launch=True
                            Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,val1.val,val1.x,val1.y,0,val1.x,val1.y,1,0,0,lists)
                        m.in_game_multi_player(p0,p1,this_round,ship_to_display,round_count)
                        if launch:
                            EMP=[]
                            for item in g.all_ships:
                                if item.get_distance(val1)<=10 and item!=val1:
                                    EMP.append(item)
                            val1.EMP(EMP)
                            activated_eship=val1
                            activated_sround=sround
                            g.EMP(activated_eship)

                if label2==1 or label2==0:
                        backup0=p0.RP
                        backup1=p1.RP
                        while True:
                            x,y,n=Input.listen3()
                            X=g.X_to_x(x)
                            Y=g.Y_to_y(y)
                            for item in g.all_ships:
                                collide=item.check_click((x,y))
                                if collide:
                                    break
                            if m.undo.check_click((x,y)):
                                round_count=round_count-1
                                break
                            if x<1024 and y<1024:
                                if Y<14 and not collide and this_round==0:
                                    print(X,Y,val1.label)
                                    ship=Ships.summon_ship(g,X,Y,label2,val2,val1.label,p0,0)
                                    if ship:
                                        Enemy.writerow(index,round_count,sround,this_round,backup0,p0.RP,ship.val,0,0,2,X,Y,0,label2+1,val2+1,lists)
                                    break
                                if Y>54 and not collide and this_round==1:
                                    print(X,Y,val1.label)
                                    ship=Ships.summon_ship(g,X,Y,label2,val2,val1.label,p1,1)
                                    if ship:
                                        Enemy.writerow(index,round_count,sround,this_round,backup1,p1.RP,ship.val,0,0,2,X,Y,0,label2+1,val2+1,lists)
                                    break

    if p0.ships[0].health<0:
        m.game_ends(0,rounds)
        input()
        break
    elif p1.ships[0].health<0:
        m.game_ends(1,rounds)
        input()
        break

