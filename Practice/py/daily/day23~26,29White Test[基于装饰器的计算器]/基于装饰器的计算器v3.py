import time
import re

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.token=re.compile(r"\.\d*|\d+\.?\d*|[+\-*/^=]")                    #最小token为"一串有长度数字+小数点+任意长度数字"(表示整小数)或"任意运算符"(加减乘除乘方)
        self.put=self.token.findall(input("我需要算什么喵："))
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
        if self.value():
            try:
                self.calculation()
                print(f"答案是{self.answer:.{self.precision}f}喵,计算用时约{self.t*1000:.4f}ms喵")
            except ZeroDivisionError:
                print("分母不能为0喵omo")
            except OverflowError:
                print("太大了喵~受不了了喵~算不出来喵~")

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
            print(f"这根本只有一个{self.math}喵")
            return False
        elif "=" in self.math_list[-2::-1]:
            print(f"{self.error}你的等号跑哪里去了喵omo")
            return False
        elif isinstance(self.math_list[-1],str) and self.math_list[-1]!="=":
            print("你表达式没输完喵")
            return False

        while self.precision is False:
            try:
                self.precision=int(input("你需要小数点后几位喵："))
                if self.precision<0:
                    self.precision=False
                    print(self.error)
                    continue
            except (TypeError,ValueError):
                print(self.error)

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

#——————classblock——————#

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

main=Main()
main.main_run()