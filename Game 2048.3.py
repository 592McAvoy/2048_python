from graphics import *
from mybutton import *
from random import *
import copy
import time

        
class Make_sure:# make sure about player's choices
    def __init__(self,Title,topic):
        self.win = GraphWin(Title,200,140)
        self.win.setCoords(0.0,0.0,10.0,7.0)
        Text(Point(5.0,5.0),"Do you really want to\n %s the game?"%topic).draw(self.win)
        self.noButton = Button(self.win, Point(2.3,2.0),4.0,1.5,"return")
        self.yesButton = Button(self.win, Point(8.0,2.0),4.0,1.5,"Yes")
        self.noButton.activate()
        self.yesButton.activate()
    def check(self):
        k = self.win.getMouse()
            
        while not (self.noButton.clicked(k) or\
                   self.yesButton.clicked(k)):
            k = self.win.getMouse() 
        if self.noButton.clicked(k):
            self.win.close()
            return False

        if self.yesButton.clicked(k):
            self.win.close()
            return True

class Fail(Make_sure):
    def __init__(self):
        self.win = GraphWin("fail",100,250)
        self.win.setCoords(0.0,0.0,2.0,5.0)
        Text(Point(1.0,4.0),"Sorry\nyou failed..").draw(self.win)
        self.yesButton = Button(self.win, Point(1.0,2.5),3.5,1.0,"restart")
        self.noButton = Button(self.win, Point(1.0,1.0),1.0,0.5,"Quit")
        self.noButton.activate()
        self.yesButton.activate()  
    
class Number:
    def __init__(self,value,xVal,yVal,wVal,size=0): # design numbers       
        self.value = value
        self.x = xVal
        self.y = yVal
        self.w = wVal
        color_dic = {"2":[color_rgb(250,250,250),color_rgb(59,203,245)],\
                     "4":[color_rgb(245,182,216),color_rgb(250,250,250)],\
                     "8":[color_rgb(255,161,179),color_rgb(238,241,204)],\
                     "16":[color_rgb(179,221,113),color_rgb(249,247,65)],\
                     "32":[color_rgb(251,241,124),color_rgb(249,143,65)],\
                     "64":[color_rgb(143,216,237),color_rgb(251,249,94)],\
                     "128":[color_rgb(245,203,249),color_rgb(252,251,175)],\
                     "256":[color_rgb(252,251,198),color_rgb(139,202,242)],\
                     "512":[color_rgb(126,196,50),color_rgb(199,230,166)],\
                     "1024":[color_rgb(65,156,249),color_rgb(252,246,90)],\
                     "2048":[color_rgb(247,43,124),color_rgb(250,250,250)],\
                     "4096":[color_rgb(228,166,230),color_rgb(253,238,110)]}#different number has different color to distinguish them
                     
        self.t= Text(Point(self.x,self.y),"%d"%self.value)#number
        self.square = Rectangle(Point(self.x-0.5,self.y+0.5),Point(self.x+0.5,self.y-0.5))#number's background
        #set suitable size for numbers differentiaing in lenth
        if size != 0:
            self.t.setSize(size)                   
        elif 2 <= self.value < 99:
            self.t.setSize(30)
        elif 100 <= self.value < 999:
            self.t.setSize(27)
        elif 1000 <= self.value < 9999:
            self.t.setSize(23)
            
        self.square.setFill(color_dic["%d"%self.value][0])
        self.square.draw(self.w)
        
        self.t.setTextColor(color_dic["%d"%self.value][1])
        self.t.draw(self.w)
    
class Game:
    def __init__(self):# set background and some basic datas
        self.win = GraphWin("Game 2048",350,490)
        self.score = 0
        self.winscore = 2048
        self.win.setBackground(color_rgb(208,241,251))
        
        self.win.setCoords(0.0,0.0,5.0,7.0)
        Line(Point(0.5,2),Point(0.5,6)).draw(self.win)
        Line(Point(1.5,2),Point(1.5,6)).draw(self.win)
        Line(Point(2.5,2),Point(2.5,6)).draw(self.win)
        Line(Point(3.5,2),Point(3.5,6)).draw(self.win)
        Line(Point(4.5,2),Point(4.5,6)).draw(self.win)
        Line(Point(5.5,2),Point(5.5,6)).draw(self.win)
        Line(Point(0.5,2),Point(4.5,2)).draw(self.win)
        Line(Point(0.5,3),Point(4.5,3)).draw(self.win)
        Line(Point(0.5,4),Point(4.5,4)).draw(self.win)
        Line(Point(0.5,5),Point(4.5,5)).draw(self.win)
        Line(Point(0.5,6),Point(4.5,6)).draw(self.win)
        
        self.sButton = Button(self.win, Point(1.1,1.3),1.2,0.4,"Restart")
        self.qButton = Button(self.win, Point(1.1,0.7),1.2,0.4, "Quit")        
        self.leftButton = Button(self.win, Point(2.8,0.7),0.6,0.5,"<<")
        self.rightButton = Button(self.win, Point(4.2,0.7),0.6,0.5, ">>")
        self.downButton = Button(self.win, Point(3.5,0.7),0.6,0.5,"\/")
        self.upButton = Button(self.win, Point(3.5,1.3),0.6,0.5,"/\\")

        Text(Point(1.1,6.7),"Your Scores:").draw(self.win)
        self.t_scores = Text(Point(3,6.7),"%d"%self.score)
        self.t_scores.draw(self.win)

        Text(Point(1.1,6.3),"Best Scores:").draw(self.win)
        
        self.record = [[0,0,0,0],\
                      [0,0,0,0],\
                      [0,0,0,0],\
                      [0,0,0,0]] #this list is uesd to record each number, so as to make further judgement
        self.random_number = [2,4]
        self.random_coordinate = [[1.0,2.5],[2.0,2.5],[3.0,2.5],[4.0,2.5],\
                                 [1.0,3.5],[2.0,3.5],[3.0,3.5],[4.0,3.5],\
                                 [1.0,4.5],[2.0,4.5],[3.0,4.5],[4.0,4.5],\
                                 [1.0,5.5],[2.0,5.5],[3.0,5.5],[4.0,5.5]]#this list includes all the coordinates so them can be choosed as a number's coordinate
        self.box = [] #the box is used to draw numbers
        self.store = []

    def best_scores(self):
        ff = open("grade.txt",'r')
        bb = ff.readline()
        self.max_ = eval(bb)        
        self.f_scores = Text(Point(3,6.3),"%d"%self.max_)
        self.f_scores.draw(self.win)

    def change_best_scores(self):
        if self.score > self.max_:
            ff = open("grade.txt",'w')
            ff.write("%d"%self.score)
            ff.close()
        else:
            pass

    def Button_activate(self):
        self.qButton.activate()
        self.sButton.activate()
        self.leftButton.activate()
        self.rightButton.activate()
        self.downButton.activate()
        self.upButton.activate()

    def transepose(self):# this function is to transepose "self,record",so that "right" and "left" direction can be dealed with just as "up" and "down" direction
        aa = []
        for i in range(len(self.record)):
            aa.append([])
        for i in range(len(self.record)):
            for j in range(len(self.record[i])):
                aa[j].append(self.record[i][j])
        self.record = aa

    def move_down(self,lis):# to deal with numbers downward or leftward
        def Bdown(A):#to put the numbers together
            for i in range(len(A)-1):
                if A[i] == 0:
                    A[i+1],A[i] = A[i],A[i+1]
           
            for i in range(len(A)-1):
                if A[i] == 0 and A[i+1] != 0:
                    return Bdown(A)
            return A

        def Cdown(A):#to add up the same numbers
            if A[0] == A[1]:
                A[0] *=2
                A[1],A[2],A[3] = A[2],A[3],0
                return A
            elif A[1] == A[2]:
                A[1] *= 2
                A[2],A[3] = A[3],0
                return A
            elif A[2] == A[3]:
                A[2] *= 2
                A[3] = 0
                return A
            else:
                return A
        for i in lis:#deal with each number by turn
            Bdown(i)
            Cdown(i)

    def move_up(self,lis):# to deal with numbers upward or rightward
        def Bup(A):#to put the numbers together
            for i in range(1,len(A)):
                if A[i] == 0:
                    A[i-1],A[i] = A[i],A[i-1]
           
            for i in range(len(A)-1):
                if A[i] != 0 and A[i+1] == 0:
                    return Bup(A)
            return A

        def Cup(A):#to add up the same numbers
            if A[-1] == A[-2]:
                A[-1] *=2
                A[0],A[1],A[2] = 0,A[0],A[1]
                return A
            elif A[-2] == A[-3]:
                A[-2] *= 2
                A[0],A[1]= 0,A[0]
                return A
            elif A[0] == A[1]:
                A[1] *= 2
                A[0] = 0
                return A
            else:
                return A
            
        for i in lis:#deal with each number by turn
            Bup(i)
            Cup(i)

    def update(self):# record the new situation after player's operation, so the program can do corresponding changes   
        self.random_coordinate = []
        self.store = []
        for i in range(len(self.record)):
            for j in range(len(self.record[i])):
                if self.record[i][j] != 0:
                    self.store.append([self.record[i][j],i+1.0,j+2.5]) # record all numbers
                else:
                    self.random_coordinate.append([i+1.0,j+2.5]) # record all blanks

    def undraw_old_numbers(self):# undraw all numbers
        if self.box == []:
            pass
        else:
            for item in self.box:
                item.t.undraw()
                item.square.undraw()

    def draw_new_numbers(self):# draw numbers according to player's operation
        for item in self.store:
            self.box.append(Number(item[0],item[1],item[2],self.win))#draw the new numbers

    def change_scores(self):# show scores that player has won and change it in time     
        self.t_scores.undraw()
        self.score = 0
        for item in self.record:
            for v in item:
                self.score += v
        self.t_scores = Text(Point(3,6.7),"%d"%self.score)
        self.t_scores.draw(self.win)   

    def check_numbers(self):# check whether a direction is clickable, if not, deactivate the corresponding Button
        self.transepose()
        c_record = copy.deepcopy(self.record)
        self.move_down(c_record)
        if c_record == self.record:
            self.leftButton.deactivate()
        c_record = copy.deepcopy(self.record)
        self.move_up(c_record)
        if c_record == self.record:
            self.rightButton.deactivate()
            
        self.transepose()
        c_record = copy.deepcopy(self.record)
        self.move_down(c_record)
        if c_record == self.record:
            self.downButton.deactivate()
        c_record = copy.deepcopy(self.record)
        self.move_up(c_record)
        if c_record == self.record:
            self.upButton.deactivate()

    def check_win(self):# check if player has add numbers up to 2048        
        for item in self.record:
            for v in item:
                if v == self.winscore:
                    congwin = GraphWin("win",100,100)
                    congwin.setCoords(0.0,0.0,10.0,10.0)
                    Text(Point(5.0,7.5)," Hooray!\n You win!").draw(congwin)
                    ctButton = Button(congwin, Point(5.0,2.6),7.0,3.5,"Continue")
                    ctButton.activate()
                    c = congwin.getMouse()
                    while not ctButton.clicked(c):
                        c = congwin.getMouse()
                    congwin.close()
                    self.winscore = 99999

    def random_num(self):#randomly produce a number 
        a = choice(self.random_number)#to raise a number randomly
        b = choice(self.random_coordinate)#find a position to put the number randomly
        self.record[int(b[0]-1)][int(b[1]-2)] = a # record the number  
        self.num = Number(a,b[0],b[1],self.win)#draw the number

    def all_undraw(self):# undraw a number and its background
        self.num.t.undraw()
        self.num.square.undraw()

    def run(self):# start the game
        self.best_scores()
        while True:
            self.Button_activate()
            self.random_num()# firstly produce a number(2 or 4) randomly
                   
            self.check_numbers()# check whether some direction is available
            
            if self.leftButton.active == 0 and \
               self.rightButton.active == 0 and \
               self.upButton.active == 0 and\
               self.downButton.active == 0: # player failed the game
                ff = Fail()
                fresult = ff.check()
                if fresult == False:# player choose to quit
                    break
                if fresult == True:# player choose to restart
                    self.change_best_scores()
                    self.f_scores.undraw()
                    self.best_scores()
                    self.record = [[0,0,0,0],\
                                  [0,0,0,0],\
                                  [0,0,0,0],\
                                  [0,0,0,0]]
                    self.random_coordinate = [[1.0,2.5],[2.0,2.5],[3.0,2.5],[4.0,2.5],\
                                 [1.0,3.5],[2.0,3.5],[3.0,3.5],[4.0,3.5],\
                                 [1.0,4.5],[2.0,4.5],[3.0,4.5],[4.0,4.5],\
                                 [1.0,5.5],[2.0,5.5],[3.0,5.5],[4.0,5.5]]
                    self.all_undraw()
                    self.undraw_old_numbers()
                    self.Button_activate()
                    self.random_num()                            

            q = self.win.getMouse()#player clicks

            while not (self.qButton.clicked(q) or\
                       self.sButton.clicked(q) or\
                       self.leftButton.clicked(q) or\
                       self.rightButton.clicked(q) or\
                       self.upButton.clicked(q) or\
                       self.downButton.clicked(q)):#avoid nonsense click leading to error
                q = self.win.getMouse()#player has to click until it is meaningful

            if self.qButton.clicked(q):#player clicks "Quit"
                qq = Make_sure("Quit","quit")# aviod player's careless operation
                qresult = qq.check()
                if qresult == True:
                    break
                if qresult == False:
                    q = self.win.getMouse()
                    while not (self.leftButton.clicked(q) or\
                               self.rightButton.clicked(q) or\
                               self.upButton.clicked(q) or\
                               self.downButton.clicked(q)):#avoid nonsense click leading to error
                        q = self.win.getMouse()
                    pass

            if self.sButton.clicked(q):#player clicks "Restart"
                ss = Make_sure("Redo","restart")# aviod player's careless operation
                sresult = ss.check()
                if sresult == False:
                    q = self.win.getMouse()
                    while not (self.leftButton.clicked(q) or\
                               self.rightButton.clicked(q) or\
                               self.upButton.clicked(q) or\
                               self.downButton.clicked(q)):#avoid nonsense click leading to error
                        q = self.win.getMouse()
                    pass
                if sresult == True:
                    self.record = [[0,0,0,0],\
                                  [0,0,0,0],\
                                  [0,0,0,0],\
                                  [0,0,0,0]]
                    self.all_undraw()
                    self.undraw_old_numbers()

            if self.leftButton.clicked(q):#player clicks "<<"
                self.transepose()
                self.all_undraw()
                self.move_down(self.record)
                self.transepose()
                self.update()
                self.undraw_old_numbers()
                self.draw_new_numbers()

            if self.rightButton.clicked(q):#player clicks ">>"
                self.transepose()
                self.all_undraw()
                self.move_up(self.record)
                self.transepose()
                self.update()
                self.undraw_old_numbers()
                self.draw_new_numbers()

            if self.upButton.clicked(q):#player clicks "/\"
                self.all_undraw()
                self.move_up(self.record)                
                self.update()
                self.undraw_old_numbers()
                self.draw_new_numbers()

            if self.downButton.clicked(q):#player clicks "\/"
                self.all_undraw()
                self.move_down(self.record)                
                self.update()
                self.undraw_old_numbers()
                self.draw_new_numbers()
                
            
            self.change_scores()
            self.check_win()

        self.win.close()
        self.change_best_scores()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
    




 
