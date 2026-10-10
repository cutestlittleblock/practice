import time
import re
import functools
import json

#---defblock---#

def load():
    try:
        with open('save.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data

#---defblock---#

def save(data):
    with open('save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#---defblock---#

def history(data):
    print("历史记录如下喵~")
    for record in data:
        print(f"你在第{record['序号']}轮\n问了{record['问题']}喵\n答案是{record['答案']}喵~\n")
        
#---defblock---#

def loud(calfunc):
    @functools.wraps(calfunc)
    def wrapper(*args,**kwargs):
        x=calfunc(*args,**kwargs)
        return x
    return wrapper

#---defblock---#

@loud
def plus(x,y):return x+y

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
        self.operator_dict={"+":plus,"-":minus,"*":times,"/":quotient,"^":power,"=":None}
        self.operator_weight_dict={"+":1,"-":1,"*":2,"/":2,"^":3,"=":0}
        self.error="别乱输喵omo"
        self.answer=None
        self.t=0
        self.calculation=self.timer(self.calculation);self.value=self.timer(self.value)
        self.top=False

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
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            t0=time.perf_counter()
            result=func(*args,**kwargs)
            self.t+=time.perf_counter()-t0
            return result
        return wrapper

    #---defblock---#

    def value(self):
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
            if self.top:print(f"这根本只有一个{self.math[0]}喵,是不是你用括号把整个式子还是一个数字包起来了喵")
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

class Wrapper():

    #---defblock---#

    def __init__(self):
        self.wrap=[];self.unwrap=[]
        self.index=0        
        self.error="括号怎么用的喵omo"

    #---defblock---#

    def main_wrapper(self):
        self.index=0;self.unwrap=[]

        while self.index<len(self.wrap):
            if self.wrap[self.index]=="{":
                if not self.brace_wrapper(wrap=self.wrap,unwrap=self.unwrap,index=self.index):return False
            elif self.wrap[self.index]=="[":
                if not self.square_wrapper(wrap=self.wrap,unwrap=self.unwrap,index=self.index,nested=False):return False
            elif self.wrap[self.index]=="(":
                if not self.paren_wrapper(wrap=self.wrap,unwrap=self.unwrap,index=self.index,nested=False):return False
            else:
                self.unwrap.append(self.wrap[self.index])
                self.index+=1

        return True

    #---defblock---#

    def index_commit(self,nested,index):
        if nested:pass
        else:
            self.index=index

    #---defblock---#

    def brace_wrapper(self,wrap,unwrap,index):
        brace=[];brace_unwrap=[]

        if "}" not in wrap[index:]:
            print(self.error)
            return False
        else:
            index+=1
            self.index+=1

            while wrap[index]!="}":
                brace.append(wrap[index])
                index+=1
                self.index+=1

            if "[" in brace:
                if not self.square_wrapper(wrap=brace,unwrap=brace_unwrap,index=0,nested=True):return False
            else:
                print(self.error)
                return False

            main.put=brace_unwrap
            if not main.main_run():return False
            brace_answer=main.answer

            unwrap.append(brace_answer)
            
            index+=1
            self.index+=1
            return True

    #---defblock---#

    def square_wrapper(self,wrap,unwrap,index,nested):
        square=[];square_unwrap=[]

        while index<len(wrap) and wrap[index]!="]":
            if wrap[index]=="[":
                square=[];square_unwrap=[]
                index+=1;self.index_commit(nested=nested,index=index)
                try:
                    while wrap[index]!="]":
                        square.append(wrap[index])
                        index+=1;self.index_commit(nested=nested,index=index)
                except IndexError:
                    print(self.error)
                    return False

                index+=1;self.index_commit(nested=nested,index=index)

                if "(" in square:
                    if not self.paren_wrapper(wrap=square,unwrap=square_unwrap,index=0,nested=True):return False
                else:
                    print(self.error)
                    return False

                main.put=square_unwrap
                if not main.main_run():return False
                square_answer=main.answer
                
                unwrap.append(square_answer)
                if not nested:return True

            else:
                unwrap.append(wrap[index])

                index+=1;self.index_commit(nested=nested,index=index)

        if nested:return True

    #---defblock---#

    def paren_wrapper(self,wrap,unwrap,index,nested):
        depth=0;d=0;paren=[]
        
        while index<len(wrap) and wrap[index]!=")":
            if wrap[index]=="(":
                paren=[]
                index+=1;self.index_commit(nested=nested,index=index)
                try:
                    while wrap[index]!=")":
                        if wrap[index]=="(":
                            d+=1;depth=index+1
                            while d:
                                if wrap[depth]=="(":d+=1
                                elif wrap[depth]==")":d-=1
                                else:pass
                                depth+=1
                            if not self.paren_wrapper(wrap=wrap[index:depth],unwrap=paren,index=0,nested=True):return False
                            index=depth;self.index_commit(nested=nested,index=index)
                        else:
                            paren.append(wrap[index])
                            index+=1;self.index_commit(nested=nested,index=index)
                except IndexError:
                    print(self.error)
                    return False
                index+=1;self.index_commit(nested=nested,index=index)

                main.put=paren
                if not main.main_run():return False
                paren_answer=main.answer

                unwrap.append(paren_answer)
                if not nested:return True

            else:
                unwrap.append(wrap[index])

                index+=1;self.index_commit(nested=nested,index=index)

        return True

    #---defblock---#

#——————classblock——————#

token=re.compile(r"\.\d*|\d+\.?\d*|[+\-*/^=\(\)\[\]\{\}]")
main=Main()
wrapper=Wrapper()
switch=True
data=load()
data.append([])
serial=1
if not data:save(data)

try:
    while switch:
        main.t=0;main.top=False
        question=input("我需要算什么喵：");answer=None
        wrapper.wrap=token.findall(question)
        if not wrapper.wrap:print("这根本没东西可算喵omo");continue
        if wrapper.main_wrapper():

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

            main.put=wrapper.unwrap
            main.top=True
            if main.main_run():

                answer=main.answer
                t=main.t
                if answer is not None:
                    print(f"答案是{answer:.{precision}f}喵,思考用时约{t*1000:.4f}ms喵")

        data[-1].append({"问题":question,"答案":f"{answer:.{precision}f}","序号":serial});serial+=1
        save(data)

        switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")
        while switch.upper()=="H":
            if not data:print("没有历史记录喵,要么就是你夏季吧乱改文件了喵")
            else:
                while True:
                    try:
                        s=int(input("你想看上几次使用记录喵（给自然数喵，看这次就输0喵）："))+1
                        if s<0 or s>len(data):
                            print("根本没有这种使用记录喵omo给我重输喵omo")
                            continue
                        break
                    except (TypeError,ValueError):
                        print("我服了你听不懂喵话喵omo给我重输喵omo")
                history(data[-s])                                              

            switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")

except (EOFError,KeyboardInterrupt):print("不用别扒拉喵")

print("下班了喵~感谢使用人家喵~下次再见喵~")