import time
import re

#---defblock---#

def loud(calfunc):
    def wrapper(*args,**kwargs):
        x=calfunc(*args,**kwargs)
        return x
    return wrapper

#---defblock---#

@loud
def add(x,y):return x+y

#---defblock---#

@loud
def minus(x,y):return x-y

#---defblock---#

@loud
def times(x,y):return x*y

#---defblock---#

@loud
def quotient(x,y):return x/y

#---defblock---#

@loud
def power(x,y):return x**y

#---defblock---#

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.put=[]
        self.math=[]
        self.math_list=[]
        self.precision=False
        self.operator_dict={"+":add,"-":minus,"*":times,"/":quotient,"^":power,"=":None}
        self.operator_weight_dict={"+":1,"-":1,"*":2,"/":2,"^":3,"=":0}
        self.error="别乱输喵omo"
        self.answer=None
        self.t=0
        self.calculation=self.timer(self.calculation)

    #---defblock---#

    def main_run(self):
        self.math=[];self.math_list=[]

        if self.value():
            try:
                self.calculation()
            except ZeroDivisionError:
                print("分母不能为0喵omo")
                return False
            except OverflowError:
                print("太大了喵~受不了了喵~算不出来喵~")
                return False
            return True
        else:return False

    #---defblock---#

    def timer(self,func):
        def wrapper(*args,**kwargs):
            t0=time.perf_counter()
            result=func(*args,**kwargs)
            self.t+=time.perf_counter()-t0
            return result
        return wrapper

    #---defblock---#

    def value(self):
        if len(self.put)==0:
            print("这根本没东西可算喵omo")
            return False

        for i,p in enumerate(self.put):
            if p is None:
                continue
            if p=="-":
                if i==0 or self.put[i-1] in self.operator_dict:
                    try:
                        self.math.append(-float(self.put[i+1])) 

                    except (ValueError,IndexError):
                        print(self.error)
                        return False
                    self.put[i+1]=None
                else:
                    self.math.append(p)

            else:
                self.math.append(p)


        for n,m in enumerate(self.math):

            if n%2==0:
                try:
                    self.math_list.append(float(m))
                except ValueError:
                    print(self.error)
                    return False
            elif n%2==1:
                if m not in self.operator_dict:
                    print(self.error)
                    return False
                else:
                    self.math_list.append(m)
        if len(self.math_list)==1:
            print(f"这根本只有一个{self.math}喵,是不是你用括号把整个式子包起来了喵")
            self.answer=self.math_list[0]
            return True
        elif "=" in self.math_list[-2::-1]:
            print(f"{self.error}你的等号跑哪里去了喵omo")
            return False
        elif isinstance(self.math_list[-1],str) and self.math_list[-1]!="=":
            print("你表达式没输完喵")
            return False

        return True                 #纯净可运算math列表，运算函数分双栈

    #---defblock---#

    def calculation(self):
        if self.math_list[-1]!="=":
            self.math_list.append("=")

        num_stack=[]
        operator_stack=[]
        
        for t in self.math_list:
            if isinstance(t,float):
                num_stack.append(t)
            else:
                while operator_stack and self.operator_weight_dict[t]<=self.operator_weight_dict[operator_stack[-1]]:
                    y=num_stack.pop()
                    x=num_stack.pop()

                    num_stack.append(self.operator_dict[operator_stack.pop()](x,y))                    
                operator_stack.append(t)

        self.answer=num_stack[0]

    #---defblock---#

#——————classblock——————#

class Pack():

    #---defblock---#

    def __init__(self):
        self.pack=[]
        self.index=0
        self.large=[];self.middle=[]
        self.packed=[];self.large_packed=[];self.middle_packed=[]
        self.error="括号怎么用的喵omo"

    #---defblock---#

    def main_pack(self):

        while self.index<len(self.pack):
            if self.pack[self.index]=="{":
                if not self.large_pack(pack=self.pack,packed=self.packed,index=self.index):return False
            elif self.pack[self.index]=="[":
                if not self.middle_pack(pack=self.pack,packed=self.packed,index=self.index,under=False):return False
            elif self.pack[self.index]=="(":
                if not self.small_pack(pack=self.pack,packed=self.packed,index=self.index,under=False):return False
            else:
                self.packed.append(self.pack[self.index])
                self.index+=1

        return True

    #---defblock---#

    def large_pack(self,pack,packed,index):
        self.large=[];self.large_packed=[]
        if "}" not in self.pack[index:]:
            print(self.error)
            return False
        else:
            index+=1
            self.index+=1

            while pack[index]!="}":
                self.large.append(pack[index])
                index+=1
                self.index+=1

            if "[" in self.large:
                if not self.middle_pack(pack=self.large,packed=self.large_packed,index=0,under=True):return False
            else:
                print(self.error)
                return False

            main.put=self.large_packed
            if not main.main_run():return False
            large_answer=main.answer

            packed.append(large_answer)
            
            index+=1
            self.index+=1
            return True

    #---defblock---#

    def middle_pack(self,pack,packed,index,under):
        if "]" not in pack[index:]:
            print(self.error)
            return False
        else:
            while index<len(pack):
                if pack[index]=="[":
                    self.middle=[];self.middle_packed=[]
                    index+=1
                    if under:pass
                    else:    
                        self.index+=1

                    while pack[index]!="]":
                        self.middle.append(pack[index])
                        index+=1
                        if under:pass
                        else:    
                            self.index+=1

                    index+=1
                    if under:pass
                    else:
                        self.index+=1

                    if "(" in self.middle:
                        if not self.small_pack(pack=self.middle,packed=self.middle_packed,index=0,under=True):return False
                    else:
                        print(self.error)
                        return False

                    main.put=self.middle_packed
                    if not main.main_run():return False
                    middle_answer=main.answer
                    
                    packed.append(middle_answer)

                else:
                    packed.append(pack[index])

                    index+=1
                    if under:pass
                    else:
                        self.index+=1

        if under:pass
        else:    
            self.index+=1
        return True

    #---defblock---#

    def small_pack(self,pack,packed,index,under):
        small=[]
        if ")" not in pack[index:]:
            print(self.error)
            return False
        else:
            while index<len(pack):
                if pack[index]=="(":
                    small=[]
                    index+=1
                    if under:pass
                    else:
                        self.index+=1

                    while pack[index]!=")":
                        small.append(pack[index])
                        index+=1
                        if under:pass
                        else:    
                            self.index+=1
                    index+=1
                    if under:pass
                    else:
                        self.index+=1

                    main.put=small
                    if not main.main_run():return False
                    small_answer=main.answer

                    packed.append(small_answer)

                else:
                    packed.append(pack[index])

                    index+=1
                    if under:pass
                    else:
                        self.index+=1
        if under:pass
        else:
            self.index+=1
        return True

    #---defblock---#

#——————classblock——————#

token=re.compile(r"\.\d*|\d+\.?\d*|[+\-*/^=\(\)\[\]\{\}]")
main=Main()
pack=Pack()

pack.pack=token.findall(input("我需要算什么喵："))
if pack.main_pack():

    precision=False
    while precision is False:
        try:
            precision=int(input("你需要小数点后几位喵："))
            if precision<0:
                precision=False
                print("别乱输喵omo")
                continue
        except (TypeError,ValueError):
            print("别乱输喵omo")

    main.put=pack.packed
    if main.main_run():

        answer=main.answer
        t=main.t
        if answer is not None:
            print(f"答案是{answer:.{precision}f}喵,思考用时约{t*1000:.4f}ms喵")