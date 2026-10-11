import time

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.math=input("我需要算什么喵，数字和符号隔一个空格喵：").split()
        self.math_list=[]
        self.num_list=[]
        self.operator_list=[]
        self.precision=False
        self.operator_dict={"+":add,"-":minus,"*":times,"/":quotient,"^":power,"=":None,".":None}
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
                print(self.error,"分母不能为0喵omo")

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
        elif "=" in self.math_list[-2::-1] or self.math_list[-1]!="=":
            print(f"{self.error}你的等号跑哪里去了喵omo")
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

        self.num_list=self.math_list[0::2]
        self.operator_list=self.math_list[1::2]

        return True

    #---defblock---#

    def calculation(self):            
        x=self.num_list[0]
        for y,symbol in zip(self.num_list[1:],self.operator_list):
            x=self.operator_dict[symbol](x,y)

        self.answer=x

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