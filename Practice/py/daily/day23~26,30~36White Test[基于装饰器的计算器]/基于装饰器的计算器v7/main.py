import time,re,json,os

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.token=re.compile(r"\.\d*|\d+\.?\d*|[+\-*/^=\(\)\[\]\{\}]")                    #最小token为"一串有长度数字+小数点+任意长度数字"(表示整小数)或"任意运算符"(加减乘除乘方括号)
        self.put=[]
        self.precision=False
        self.operator_dict={"+":add,"-":minus,"*":times,"/":quotient,"^":power,"&":times}
        self.operator_weight_dict={"+":1,"-":1,"*":2,"/":2,"&":3,"^":4,"(":0,"[":0,"{":0}
        self.brackets_dict={")":"(","]":"[","}":"{"}
        self.error="别乱输喵omo"
        self.answer=None
        self.t=0
        self.calculation=self.timer(self.calculation)
        self.data=loader()

    #---defblock---#

    def main_run(self):
        switch=True;serial=1
        self.data.append([])
        while switch:
            answer=None;self.t=0;self.precision=False
            question=input("我需要算什么喵：")
            self.put=self.token.findall(question)
            try:
                if not self.calculation():continue
                while self.precision is False:
                    try:
                        self.precision=int(input("你需要小数点后几位喵："))
                        if self.precision<0:
                            self.precision=False
                            print(self.error)
                            continue
                    except (TypeError,ValueError):
                        print(self.error)
                answer=f"{self.answer:.{self.precision}f}"

                print(f"答案是{answer}喵,计算用时约{self.t*1000:.4f}ms喵")
            except ZeroDivisionError:
                print("分母不能为0喵omo");answer=None
            except OverflowError:
                print("太大了喵~受不了了喵~算不出来喵~");answer="太大了喵，你就当是∞"

            self.data[-1].append({"问题":question,"答案":answer,"序号":serial});serial+=1
            saver(self.data)

            switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")
            while switch.upper()=="H":
                while True:
                    try:
                        s=int(input("你想看上几次使用记录喵（给自然数喵，看这次就输0喵）："))+1
                        if s<1 or s>len(self.data):
                            print("根本没有这种使用记录喵omo给我重输喵omo")
                            continue
                        break
                    except (TypeError,ValueError):
                        print("我服了你听不懂喵话喵omo给我重输喵omo")
                if not history(self.data[-s]):self.data[-s]=[];saver(self.data)

                switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")
        print("感谢使用喵~下班下班~")


    #---defblock---#

    def timer(self,func):
        def wrapper(*args,**kwargs):
            t0=time.perf_counter()
            result=func(*args,**kwargs)
            self.t+=time.perf_counter()-t0
            return result
        return wrapper

    #---defblock---#

    def stackpoper(self,operator_stack,num_stack):
            y=num_stack.pop();x=num_stack.pop()
            return self.operator_dict[operator_stack.pop()](x,y)

    #---defblock---#

    def pop_judge(self,operator,top):
        if operator=="^":return self.operator_weight_dict[operator]<self.operator_weight_dict[top]
        return self.operator_weight_dict[operator]<=self.operator_weight_dict[top]

    #---defblock---#

    def calculation(self):    
        i=0;num_stack=[];operator_stack=[]
        try:
            if len(self.put)==0:print("这根本没东西可算喵omo");return False
            if self.put[-1]!="=" and self.put[-1] not in self.brackets_dict:
                float(self.put[-1])
            elif self.put[-1]=="=":self.put.pop()
            #初始化判断
            while i<len(self.put):  
            #计算栈循环
                if self.put[i] in ("+","-"):
                #一阶算符的入栈判断与合并
                    while self.put[i+1] in ("+","-"):
                    #一阶算符的合并
                        if self.put[i]=="+":
                            if self.put[i+1]=="+":del self.put[i+1]
                            else:self.put[i]="-";del self.put[i+1]
                        else:
                            if self.put[i+1]=="+":del self.put[i+1]
                            else:self.put[i]="+";del self.put[i+1]
                    if i==0 or self.put[i-1] in self.operator_weight_dict:
                        if self.put[i]=="+":num_stack.append(1);operator_stack.append("&")
                        else:num_stack.append(-1);operator_stack.append("&")
                    else:
                        while operator_stack and self.pop_judge(operator=self.put[i],top=operator_stack[-1]):
                            num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
                        operator_stack.append(self.put[i])
                    i+=1

                elif self.put[i] in ("*","/","^"):
                #高阶算符入栈判断
                    while operator_stack and self.pop_judge(operator=self.put[i],top=operator_stack[-1]):
                        num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
                    operator_stack.append(self.put[i])
                    i+=1

                elif self.put[i] in self.brackets_dict.values():operator_stack.append(self.put[i]);i+=1
                #括号入栈判断
                elif self.put[i] in self.brackets_dict:
                #反括号入栈,括号收官
                    while operator_stack[-1]!=self.brackets_dict[self.put[i]]:
                        num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
                    operator_stack.pop()
                    if i<len(self.put)-1 and self.put[i+1] in self.brackets_dict.values():
                        while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                            num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
                        operator_stack.append("*")
                    i+=1

                else:
                #数字入栈兼非法输入检测
                    num_stack.append(float(self.put[i]))
                    if i<len(self.put)-1 and self.put[i+1] in self.brackets_dict.values():
                        while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                            num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
                        operator_stack.append("*")
                    i+=1

        except (IndexError,ValueError):print(self.error);return False

        try:
        #答案收官
            while operator_stack:
                if operator_stack[-1] in self.brackets_dict.values():print(self.error);return False
                num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))
        except IndexError:print(self.error);return False
        if len(num_stack)!=1:print(self.error);return False
        self.answer=num_stack[0]

        return True

#——————classblock——————#

#---defblock---#

def add(x,y):return x+y

#---defblock---#

def minus(x,y):return x-y

#---defblock---#

def times(x,y):return x*y

#---defblock---#

def quotient(x,y):return x/y

#---defblock---#

def power(x,y):return x**y

#---defblock---#

def saver(data):
    os.makedirs(os.path.join(os.path.dirname(__file__),"saves"),exist_ok=True)
    p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#---defblock---#

def loader():
    p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)            
    except FileNotFoundError:return []        
    except json.JSONDecodeError:print("历史记录坏掉了喵~下班修喵~");return []
    if not isinstance(data,list):print("历史记录坏掉了喵~下班修喵~");return []
    return data

#---defblock---#

def history(data):
    print("历史记录如下喵~")
    if not data:print("这次的历史记录为空喵，应该是坏了喵");return True
    else:
        try:
            for record in data:
                print(f"你在第{record['序号']}轮\n问了{record['问题']}喵\n答案是{record['答案']}喵~\n")
            return True
        except (TypeError,KeyError):
            print("这次的记录被搞坏了喵，我给你清空了喵");return False
        
#---defblock---#

main=Main()
main.main_run()