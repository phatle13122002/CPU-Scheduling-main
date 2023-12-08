from pickle import NONE
import pygame
import string
import copy

alphabet = list(string.ascii_uppercase)	

pygame.init()
pygame.font.init()


cal_size = 30
gantt_size = 20

clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('Hệ điều hành')
textfont = pygame.font.SysFont("monospace", gantt_size)
newfont = pygame.font.SysFont("monospace", cal_size)


startX = 100 
startY = 100

endY = 100
line_width = 3



BLACK = (0,0,0)
space = 40


screen_roll = 0
move_speed = 20

def draw_text(text,x,y,color):
    text =  textfont.render(text,1,color)
    screen.blit(text, (x+screen_roll,y))

def draw_cal(text,x,y,color):
    text =  newfont.render(text,1,color)
    screen.blit(text, (x,y))
    #screen.blit(text, (x+screen_roll,y))


def draw_milestone(position):
    global space
    pygame.draw.line(screen,BLACK,((startX+space*position+screen_roll),startY-5),((startX+space*position+screen_roll),startY+5),line_width)
    

class Process():
    count = 0
    global alphabet
    def __init__(self,burst,arr_time=0):
       Process.count +=1
       self.count = Process.count - 1 
       self.burst = burst
       self.arr_time = arr_time
       self.name = alphabet[self.count]
       self.ori_burst = burst
       self.first = None
       self.finish = None
       self.res = None
       self.wait = None
       self.turnaround = None
      
class CPU_Processes():
    def __init__(self):
        self.processes = []
        self.queue = []
        self.current = []
        self.finish = []
        self.draw_queue = {}
    
    def insertQ(self,quantum):
        self.quantum = quantum
    
    
    def display_queue(self):
        print('display_queue',len(self.draw_queue))
        count = 0
        for key,values in self.draw_queue.items():  
            print('bắt đầu sổ list ')
            print('milestone',key)
            if count == len(self.draw_queue)-1:
                cur_run = None
            else:
                cur_run = list(values)[0]  
            print('Running: ',cur_run)
            for key,value in values.items():
                print("key",key)
                print('value',value.get('burst'))            
            count += 1
            
    def add_draw_queue(self,data,milestone):
        temp = {}
        for each in data:
            temp[each.name] = {"burst":each.burst,'arrive time':each.arr_time}
        self.draw_queue[milestone] = temp
        
    def display_finish(self):
        for each in self.finish:
            print("Tên tiến trình: ",each.name)
            print("Thời gian kết thúc: ", each.finish)
    
    def display_processes(self,milestone):
        print('________________________________')
        print('Mốc thời gian: ',milestone,"\nQueue:")
        for element in self.queue:
             print("{} ({}) |Arrive time {}".format(element.name, element.burst,element.arr_time))
            
        print('________________________________')
    
    
    def CPU_run(self,typ):    
        t = 0
        on_going = 0
        if typ == '1':
            self.queue = self.processes
            self.add_draw_queue(self.queue,t)
            self.display_processes(0)
            while self.queue:
                if self.queue[0].burst > self.quantum:
                    run_pro = self.queue.pop(0)
                    if run_pro.first == None:
                        run_pro.first = on_going
                    run_pro.burst -= self.quantum
                    self.processes.append(run_pro)
                    on_going+=self.quantum
                    self.add_draw_queue(self.queue,on_going)
                    
                else:
                    self.add_draw_queue(self.queue,on_going)
                    run_pro = self.queue.pop(0)
                    on_going += run_pro.burst
                    if run_pro.first == None:
                        run_pro.first = on_going
                    run_pro.finish = on_going
                    self.finish.append(run_pro)
                self.display_processes(on_going)
                self.add_draw_queue(self.queue,on_going)
                
                
        else: 
            while len(self.processes) != 0 or len(self.queue) != 0 or len(self.current)!=0:
                if on_going == t and t != 0 and self.current:
                    if self.current[0] == 0:
                        self.current.pop()
                    else:
                        self.queue.append(self.current.pop())
                        self.add_draw_queue(self.queue, t)
                        
# =============================================================================
#                 for process in self.processes:
#                     print('vong lap for',process.arr_time)
#                     
#                     if process.arr_time <= t:
#                         queue = self.processes.pop(0)
#                         self.queue.append(queue)
#                         self.display_processes(t)
#                         self.add_draw_queue(self.queue, t)
#                     else:
#                         break
#                 
# =============================================================================
                
                pro_index = 0
                while pro_index < len(self.processes):
                    if self.processes[pro_index].arr_time == t:
                        queue =self.processes.pop(0)
                        self.queue.append(queue)
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, t)
                        if len(self.processes) >= 1:
                            pro_index = pro_index - 1
                    pro_index += 1
                    
                    
                if self.queue and on_going <= t :
                    self.display_processes(t)
                    self.add_draw_queue(self.queue, t)
                    run_pro = self.queue.pop(0)
                    if run_pro.first == None:
                        run_pro.first = t
                    if run_pro.burst > self.quantum:
                        run_pro.burst -= self.quantum
                        self.current.append(run_pro)
                        #cap nhat lai on_going
                        on_going = t + self.quantum
                        

                    else:
                        on_going = t + run_pro.burst
                        run_pro.finish = on_going
                        self.finish.append(run_pro)
                        self.current.append(0)
                        
                if len(self.processes) == 0 and len(self.queue) == 0 and len(self.current) == 0:
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, on_going)
                        print('da het tien trinh')
                t += 1
    def CPU_run_srtf(self,typ):    
        t = 0
        on_going = 0
        if typ == '1':
            self.queue = self.processes
            self.sort_burst_time()
            self.add_draw_queue(self.queue,t)
            self.display_processes(0)
            while self.queue:
                if self.queue[0].burst > self.quantum:
                    run_pro = self.queue.pop(0)
                    run_pro.burst -= self.quantum
                    self.processes.append(run_pro)
                    on_going+=self.quantum
                    if run_pro.first == None:
                        run_pro.first = on_going -self.quantum
                    self.add_draw_queue(self.queue,on_going)
                    
                else:
                    self.add_draw_queue(self.queue,on_going)
                    run_pro = self.queue.pop(0)
                    on_going += run_pro.burst
                    if run_pro.first == None:
                        run_pro.first = on_going - run_pro.burst
                    run_pro.finish = on_going
                    self.finish.append(run_pro)
                self.display_processes(on_going)
                self.add_draw_queue(self.queue,on_going)
        else: 
            while len(self.processes) != 0 or len(self.queue) != 0 or len(self.current)!=0:
                if on_going == t and t != 0 and self.current:
                    if self.current[0] == 0:
                        self.current.pop()
                    else:
                        self.queue.append(self.current.pop())
                        self.sort_burst_time()
                        self.add_draw_queue(self.queue, t)
                        
                pro_index = 0
                while pro_index < len(self.processes):
                    if self.processes[pro_index].arr_time == t:
                        queue =self.processes.pop(0)
                        self.queue.append(queue)
                        self.sort_burst_time()
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, t)
                        if len(self.processes) >= 1:
                            pro_index = pro_index - 1
                    pro_index += 1
                    
                    
                if self.queue and on_going <= t :
                    self.sort_burst_time()
                    self.display_processes(t)
                    self.add_draw_queue(self.queue, t)
                    run_pro = self.queue.pop(0)
                    if run_pro.burst > self.quantum:
                        run_pro.burst -= self.quantum
                        self.current.append(run_pro)
                        #cap nhat lai on_going
                        on_going = t + self.quantum

                    else:
                        on_going = t + run_pro.burst
                        run_pro.finish = on_going
                        self.finish.append(run_pro)
                        self.current.append(0)
                    if run_pro.first == None:
                        run_pro.first = t
                        
                if len(self.processes) == 0 and len(self.queue) == 0 and len(self.current) == 0:
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, on_going)
                        print('da het tien trinh')
                t += 1

    def CPU_run_fcfs(self,typ):    
        t = 0
        on_going = 0
        if typ == '1':
            self.queue = self.processes
            self.add_draw_queue(self.queue,t)
            self.display_processes(0)
            while self.queue:
                self.add_draw_queue(self.queue,on_going)
                run_pro = self.queue.pop(0)
                if run_pro.first == None:
                        run_pro.first = on_going
                on_going += run_pro.burst
                run_pro.finish = on_going
                self.finish.append(run_pro)
                self.display_processes(on_going)
                self.add_draw_queue(self.queue,on_going)
        else: 
            while len(self.processes) != 0 or len(self.queue) != 0 or len(self.current)!=0:
                if on_going == t and t != 0 and self.current:
                    if self.current[0] == 0:
                        self.current.pop()
                    else:
                        self.queue.append(self.current.pop())
                        self.add_draw_queue(self.queue, t)
                        
                pro_index = 0
                while pro_index < len(self.processes):
                    if self.processes[pro_index].arr_time == t:
                        queue =self.processes.pop(0)
                        self.queue.append(queue)
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, t)
                        if len(self.processes) >= 1:
                            pro_index = pro_index - 1
                    pro_index += 1
                    
                    
                if self.queue and on_going <= t :
                    self.display_processes(t)
                    self.add_draw_queue(self.queue, t)
                    run_pro = self.queue.pop(0)
                    if run_pro.first == None:
                        run_pro.first = t
                    on_going = t + run_pro.burst
                    run_pro.finish = on_going
                    self.finish.append(run_pro)
                    self.current.append(0)
                        
                if len(self.processes) == 0 and len(self.queue) == 0 and len(self.current) == 0:
                        self.display_processes(t)
                        self.add_draw_queue(self.queue, on_going)
                        print('da het tien trinh')
                t += 1
                
                
            
            
               
            
    def sort_arrive_time(self):
        count = len(self.processes)
        for x in range(0,count):
            lowest_value = x
            for each in range(x+1,count):
                if self.processes[each].arr_time < self.processes[lowest_value].arr_time:
                    lowest_value = each
            self.processes[x],self.processes[lowest_value] = self.processes[lowest_value],  self.processes[x]
    
    
    def sort_burst_time(self):
        count = len(self.queue)
        for x in range(0,count):
            lowest_value = x
            for each in range(x+1,count):
                if self.queue[each].burst < self.queue[lowest_value].burst:
                    lowest_value = each
            self.queue[x],self.queue[lowest_value] = self.queue[lowest_value],  self.queue[x]
        
    
    def show_process_detail(self):
        for element in self.finish:
            print('Tên tiến trình: ',element.name)
            print('Lần đầu chạy: ',element.first)
            print('Thời gian đến: ',element.arr_time)
            print('Thời gian burst: ',element.ori_burst)
            print('Thời gian phản hồi: ',element.res)
            print('Thời gian turnaround: ',element.turnaround)
            print('Thời gian đợi: ',element.wait)
        
    def cal_detail(self):
        for element in self.finish:
            element.res = element.first - element.arr_time
            element.wait = element.finish - element.ori_burst - element.arr_time
            element.turnaround = element.finish - element.arr_time
                    
       
run = True


print('Thời gian vào bằng 0?\n1. Đúng 2.Không')
typ = input('Nhập lựa chọn: ')
while True:
    try:
        quantum =input('Nhap thoi gian Q: ')
        if len(quantum) == 0 or quantum == 0:
            quantum = None
        else:
            quantum = int(quantum)
        break
    except:pass
list_pro = CPU_Processes()
list_pro.insertQ(quantum)

rrb = CPU_Processes()
rrb.insertQ(quantum)

srjf = CPU_Processes()
srjf.insertQ(quantum)

procount = 0
while run:
    if len(list_pro.processes) == 4:
        run = False
    print('Tiến trình ',alphabet[procount])
    procount+=1
    if typ != '1':
        burst = input('Nhập burst time: ')
        if len(burst) == 0: 
            run = False    
        else:
            try:
                burst = int(burst)
                arr_time = input('Nhập arrive time: ') 
                arr_time = int(arr_time)
                process = Process(burst,arr_time)
                list_pro.processes.append(copy.deepcopy(process))
                rrb.processes.append(copy.deepcopy(process))
                srjf.processes.append(copy.deepcopy(process))

            except:
                print('Burst time, arrive time phải là số.')
    else:
        burst = input('Nhập burst time: ')
        if len(burst) == 0: 
            run = False    
        else:
            try:
                burst = int(burst)
                process = Process(burst)
                list_pro.processes.append(copy.deepcopy(process))
                rrb.processes.append(copy.deepcopy(process))
                srjf.processes.append(copy.deepcopy(process))
            except:
                print('Burst time, arrive time phải là số.')
if typ != '1':
    list_pro.sort_arrive_time()
    rrb.sort_arrive_time()
    srjf.sort_arrive_time()

list_pro.CPU_run_fcfs(typ)
list_pro.cal_detail()
list_pro.show_process_detail()
if quantum != None:
    rrb.CPU_run(typ)
    rrb.cal_detail()

    srjf.CPU_run_srtf(typ)
    srjf.cal_detail()
        
amount_milestone = int(list(list_pro.draw_queue)[-1])



left = False
right = False

run = True
page = 1
while run:
    if right:
        screen_roll += move_speed
    
    elif left:
        screen_roll -= move_speed
    if page == 1:
        screen.fill((255,255,255))
        draw_cal("FIRST COME FIRST SERVE", 200, 5,(255,135,43))
        draw_text("Gantt:", 50,50,BLACK)
        draw_text("T",70,80,BLACK)
        draw_text("Queue", 20,115,BLACK)
        draw_text("Page: " + str(page),350,450,BLACK )
    
        #Draw milestone and milestone describe
        draw_milestone(amount_milestone)
        draw_text('0',startX-7,startY-30,BLACK)
    
        #Draw horizontal line
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-5),(startX+screen_roll,startY+5),line_width)
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-2),(startX+screen_roll+space*amount_milestone,endY),line_width)
    
        #Draw milestone ...
        for key,values in list_pro.draw_queue.items():
            draw_milestone(key)
            draw_text(str(key),(startX+space*key)-7,startY-30,BLACK)
           
            row = 0
            for s_key,value in values.items():
                burst_time = "(" + str(value.get("burst"))+")"
                draw_text(str(s_key),(startX+space*key)-10,startY + 10  +row *space/2,BLACK)
                draw_text(burst_time,(startX+space*key),startY+10 + row *space/2,BLACK)
                row += 1
    
        #Process detail
        countRow = 0
        for element in list_pro.finish:
            draw_text('Tên tiến trình: ' + element.name,startX -50  + 320*countRow,240,BLACK)
            draw_text('Thời gian phản hồi: ' + str(element.res),startX -50 + 320*countRow,280,BLACK)
            draw_text('Thời gian chờ: ' + str(element.wait),startX -50 + 320*countRow,320,BLACK)
            draw_text('Thời gian turnaround: ' + str(element.turnaround),startX - 50 + 320*countRow,360,BLACK)
            countRow += 1

    elif page == 2:
        screen.fill((255,255,255))
        draw_cal("ROUND ROBIN", 200, 5,(255,135,43))
        draw_text("Gantt:", 50,50,BLACK)
        draw_text("T",70,80,BLACK)
        draw_text("Queue", 20,115,BLACK)
        draw_text("Page: " + str(page),350,450,BLACK )
    
        #Draw milestone and milestone describe
        draw_milestone(amount_milestone)
        draw_text('0',startX-7,startY-30,BLACK)
    
        #Draw horizontal line
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-5),(startX+screen_roll,startY+5),line_width)
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-2),(startX+screen_roll+space*amount_milestone,endY),line_width)

    
        #Draw milestone ...
        for key,values in rrb.draw_queue.items():
            draw_milestone(key)
            draw_text(str(key),(startX+space*key)-7,startY-30,BLACK)
           
            row = 0
            for s_key,value in values.items():
                burst_time = "(" + str(value.get("burst"))+")"
                draw_text(str(s_key),(startX+space*key)-10,startY + 10  +row *space/2,BLACK)
                draw_text(burst_time,(startX+space*key),startY+10 + row *space/2,BLACK)
                row += 1
    
        #Process detail
        countRow = 0
        for element in rrb.finish:
            draw_text('Tên tiến trình: ' + element.name,startX -50 + 320*countRow,240,BLACK)
            draw_text('Thời gian phản hồi: ' + str(element.res),startX  -50 + 320*countRow,280,BLACK)
            draw_text('Thời gian chờ: ' + str(element.wait),startX -50 + 320*countRow,320,BLACK)
            draw_text('Thời gian turnaround: ' + str(element.turnaround),startX -50+ 320*countRow,360,BLACK)
            countRow += 1

    elif page == 3:
        screen.fill((255,255,255))
        draw_cal("SHORTEST REMAINING JOB FIRST", 150, 5,(255,135,43))
        draw_text("Gantt:", 50,50,BLACK)
        draw_text("T",70,80,BLACK)
        draw_text("Queue", 20,115,BLACK)
        draw_text("Page: " + str(page),350,450,BLACK )
    
        #Draw milestone and milestone describe
        draw_milestone(amount_milestone)
        draw_text('0',startX-7,startY-30,BLACK)
    
        #Draw horizontal line
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-5),(startX+screen_roll,startY+5),line_width)
        pygame.draw.line(screen,BLACK,(startX+screen_roll,startY-2),(startX+screen_roll+space*amount_milestone,endY),line_width)
   
    
        #Draw milestone ...
        for key,values in srjf.draw_queue.items():
            draw_milestone(key)
            draw_text(str(key),(startX+space*key)-7,startY-30,BLACK)
           
            row = 0
            for s_key,value in values.items():
                burst_time = "(" + str(value.get("burst"))+")"
                draw_text(str(s_key),(startX+space*key)-10,startY + 10  +row *space/2,BLACK)
                draw_text(burst_time,(startX+space*key),startY+10 + row *space/2,BLACK)
                row += 1
    
        #Process detail
        countRow = 0
        for element in srjf.finish:
            draw_text('Tên tiến trình: ' + element.name,startX-50 + 320*countRow,240,BLACK)
            draw_text('Thời gian phản hồi: ' + str(element.res),startX-50 + 320*countRow,280,BLACK)
            draw_text('Thời gian chờ: ' + str(element.wait),startX-50 + 320*countRow,320,BLACK)
            draw_text('Thời gian turnaround: ' + str(element.turnaround),startX-50 + 320*countRow,360,BLACK)
            countRow += 1

        

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                #screen_roll += move_speed
                left = True
            elif event.key == pygame.K_LEFT:
                #screen_roll -= move_speed
                right = True
            
            elif event.key == pygame.K_UP:
                if quantum != None:
                    if page == 3: page =0 
                    page +=1
                    screen_roll = 0
            elif event.key == pygame.K_DOWN:
                 if quantum != None: 
                    if page == 1: page = 4
                    page -=1
                    screen_roll = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                left = False
            elif event.key == pygame.K_LEFT:
                right = False
                
                
    
    
    pygame.display.update()
    clock.tick(20)
pygame.quit()
    