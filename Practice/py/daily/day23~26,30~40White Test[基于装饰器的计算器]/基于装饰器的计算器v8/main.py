import time,re,json,os,functools,math

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.token=re.compile(
                              r"""\d+\.?\d*|e|pi|π|i|°#数字和角度
                              |//|[+\-*/^=%\(\)\[\]\{\}]|<|>#基础算符
                              |!!|!#模块算符
                              |sin|cos|tan|cot|sec|csc#模块算符(三角函数)
                              |arcsin|asin|arccos|acos|arctan|atan""",re.VERBOSE#模块算符(反三角函数)
                              )
        self.e=constant("e");self.pi=constant("pi")
        self.basic_operator_set={"+","-","*","/","//","%","&","^"}
        self.trigono_set={
                          "sin","cos","tan","cot","sec","csc",
                          "arcsin","asin","arccos","acos","arctan","atan"
                          }
        self.modular_operator_set={"!","!!",*self.trigono_set}
        self.operator_weight_dict={
                                   "+":1,"-":1,"*":2,"/":2,"//":2,"%":2,"&":3,"^":4,
                                   "(":0,"[":0,"{":0,"<":0
                                   }
        self.brackets_dict={")":"(","]":"[","}":"{",">":"<"}
        self.implicit_times_set={"e","pi","π",*self.brackets_dict.values(),*self.trigono_set}
        self.error="别乱输喵omo"
        self.put=[]
        self.precision=False
        self.answer=None
        self.t=0
        self.calculation=self.timer(self.calculation)
        self.data=loader()

    #---defblock---#

    def main_run(self):
        #主运行流程方法
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

                if isinstance(self.answer,complex):
                    if abs(float(f"{self.answer.imag:.{self.precision}f}"))!=1:
                        answer=(f"{self.answer.real:.{self.precision}f}{self.answer.imag:+.{self.precision}f}i"
                                if abs(self.answer.real)>1e-12 else f"{self.answer.imag:.{self.precision}f}i")
                    else:
                        answer=((f"{self.answer.real:.{self.precision}f}+i"if abs(self.answer.real)>1e-12 else "i")
                                if self.answer.imag>0 else 
                                (f"{self.answer.real:.{self.precision}f}-i"if abs(self.answer.real)>1e-12 else "-i"))

                else:answer=f"{self.answer:.{self.precision}f}"

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
        #计时器
        def wrapper(*args,**kwargs):
            t0=time.perf_counter()
            result=func(*args,**kwargs)
            self.t+=time.perf_counter()-t0
            return result
        return wrapper

    #---defblock---#

    def stackpoper(self,operator_stack,num_stack):
        #出栈处理器
            y=num_stack.pop();x=num_stack.pop();o=operator_stack.pop()
            if o in self.basic_operator_set:return basic_math(x,y,o)

    #---defblock---#

    def pop_judge(self,operator,top):
        #栈权判断器
        if operator=="^":return self.operator_weight_dict[operator]<self.operator_weight_dict[top]
        return self.operator_weight_dict[operator]<=self.operator_weight_dict[top]

    #---defblock---#

    def calculation(self):
        #计算流程方法
        i=0;num_stack=[];operator_stack=[]
        try:
            if len(self.put)==0:print("这根本没东西可算喵omo");return False
            elif self.put[-1]=="=":self.put.pop()
            #初始化判断
            for i in range(len(self.put)): 
            #计算栈循环
                if self.put[i] is None:continue
                #空值判断
                elif self.put[i] in self.basic_operator_set:
                #基础算符入栈判断
                    if self.put[i] in ("+","-"):
                    #一阶算符的入栈判断与合并
                        if i==0 or self.put[i-1] in self.basic_operator_set or self.put[i-1] in self.brackets_dict.values():
                        #多算符与顶算符合并
                            j=1
                            while self.put[i+j] in ("+","-"):
                                if self.put[i+j]=="+":self.put[i+j]=None
                                else:self.put[i]=("+" if self.put[i]=="-" else "-");self.put[i+j]=None
                                j+=1

                            num_stack.append(1 if self.put[i]=="+" else -1);operator_stack.append("&")

                        else:
                        #单算符入栈
                            while operator_stack and self.pop_judge(operator=self.put[i],top=operator_stack[-1]):
                                num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                            operator_stack.append(self.put[i])

                    else:
                    #高阶算符入栈判断
                        while operator_stack and self.pop_judge(operator=self.put[i],top=operator_stack[-1]):
                            num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                        operator_stack.append(self.put[i])

                elif self.put[i] in self.modular_operator_set:
                #模块算符入栈
                    if self.put[i] in ("!","!!"):
                    #(双)阶乘运算
                        num_stack.append(factorial(num_stack.pop()) if self.put[i]=="!" else defactor(num_stack.pop()))
                        if self.put is not None and i<len(self.put)-1 and self.put[i+1] in self.implicit_times_set:
                        #隐乘法判断
                            while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                                num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                            operator_stack.append("*")

                    elif self.put[i] in self.trigono_set:operator_stack.append(self.put[i])
                    #三角函数入栈(由于其栈位在数字之前,故在数字入栈/括号收官类计算)

                elif self.put[i] in self.brackets_dict.values():operator_stack.append(self.put[i])
                #括号及绝对值入栈判断
                elif self.put[i] in self.brackets_dict:
                #反括号及绝对值入栈,括号及绝对值收官
                    while operator_stack[-1]!=self.brackets_dict[self.put[i]]:
                        num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                    operator_stack.pop()
                    if self.put[i]==">":num_stack.append(absolute(num_stack.pop()))
                    #绝对值判断
                    if operator_stack and operator_stack[-1] in self.trigono_set:
                    #三角函数计算
                        if i<len(self.put)-1 and self.put[i+1]=="°":pass
                        else:
                            num_stack.append(
                                                trigono(num_stack.pop(),operator_stack.pop()) 
                                                if operator_stack[-1] in ("sin","cos","tan","cot","sec","csc") 
                                                else antrigono(num_stack.pop(),operator_stack.pop()) 
                                                )
                                
                    if self.put is not None and i<len(self.put)-1 and self.put[i+1] in self.implicit_times_set:
                    #隐乘法判断
                        while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                            num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                        operator_stack.append("*")

                else:
                #角度及数字入栈
                    if self.put[i]=="°":
                    #角度转弧度入栈
                        if self.put[i-1] in self.brackets_dict or float(self.put[i-1]) or float(self.put[i-1])==0:
                            num_stack.append(basic_math(basic_math(num_stack.pop(),180,"/"),self.pi,"*"))
                            if operator_stack and operator_stack[-1] in self.trigono_set:
                            #三角函数计算
                                num_stack.append(
                                                 trigono(num_stack.pop(),operator_stack.pop()) 
                                                 if operator_stack[-1] in ("sin","cos","tan","cot","sec","csc") 
                                                 else antrigono(num_stack.pop(),operator_stack.pop()) 
                                                 )

                            if i<len(self.put)-1 and self.put[i+1] in self.implicit_times_set:
                            #隐乘法判断
                                while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                                    num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                                operator_stack.append("*")

                        else:raise ModularError

                    else:
                    #数字入栈
                            if self.put[i] in ("e","pi","π","i"):
                            #常用无理数e,π及虚数单位i入栈
                                if self.put[i]=="e":num_stack.append(self.e)
                                elif self.put[i] in ("pi","π"):num_stack.append(self.pi)
                                else:num_stack.append(1j)

                            else:num_stack.append(float(self.put[i]))
                            #有理数入栈
                            if operator_stack and operator_stack[-1] in self.trigono_set:
                            #三角函数计算
                                if i<len(self.put)-1 and self.put[i+1]=="°":pass
                                else:
                                    num_stack.append(
                                                        trigono(num_stack.pop(),operator_stack.pop()) 
                                                        if operator_stack[-1] in ("sin","cos","tan","cot","sec","csc") 
                                                        else antrigono(num_stack.pop(),operator_stack.pop()) 
                                                        )

                            if i<len(self.put)-1 and self.put[i+1] in self.implicit_times_set:
                            #隐乘法判断
                                while operator_stack and self.pop_judge(operator="*",top=operator_stack[-1]):
                                    num_stack.append(self.stackpoper(operator_stack=operator_stack,num_stack=num_stack))

                                operator_stack.append("*")

        except (IndexError,ValueError,TypeError,ModularError):print(self.error);return False

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

class ModularError(Exception):pass

#——————classblock———————#

#---defblock---#

def constant(C):
    #e,π常数初始化
    n=1;R=1;e=1
    pi=basic_math(
                  basic_math(antrigono(0.2,"atan"),16,"*"),
                  basic_math(antrigono(basic_math(1,239,"/"),"atan"),4,"*"),
                  "-"
                  )#马青公式:pi=16arctan(1/5)-4arctan(1/239)
    while absolute(R)>1e-17:
        R=basic_math(1,factorial(n),"/")
        e+=R;n+=1

    return (e if C=="e" else pi)

#---defblock---#

def basic_math(x,y,o):
    #基础计算
    basic_dict={
                "+":lambda:x+y,"-":lambda:x-y,
                "*":lambda:x*y,"/":lambda:x/y,"//":lambda:x//y,"%":lambda:x%y,
                "&":lambda:x*y,
                "^":lambda:x**y
                }
    return basic_dict[o]()

#---defblock---#

def absolute(x):
    #绝对值计算
    if isinstance(x,complex):return(basic_math(basic_math(basic_math(x.real,2,"^"),basic_math(x.imag,2,"^"),"+"),0.5,"^"))
    else:return(x if x>=0 else -x)

#---defblock---#

def modular_math(func):
    #模块化装饰器
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        modular_name=func.__name__;args=list(args)
        if modular_name in ("factorial","defactor"):
        #阶乘初始化
            if args[0]<0 or args[0]%1!=0 or args[0]>10**5:raise ModularError
            elif args[0]==0:return 1
        elif modular_name in ("trigono","antrigono"):
        #三角函数初始化
            if modular_name=="trigono":
            #正三角函数初始化
                while absolute(args[0])>main.pi:
                    args[0]=(args[0]-basic_math(2,main.pi,"*") if args[0]>0 else args[0]+basic_math(2,main.pi,"*"))

            else:
            #反三角函数初始化
                if args[1] in ("asin","arcsin","acos","arccos"):
                #反正余弦初始化
                    if absolute(args[0])>1:raise ModularError
                    elif absolute(args[0])==1:
                        if args[1] in ("asin","arcsin"):return(main.pi/2 if args[0]==1 else -main.pi/2)
                        else:return(0 if args[0]==1 else main.pi)

                    else:
                    #反正余弦转化为反正切问题,变参x>>x/(1-x^2)^0.5
                        args[0]=basic_math(
                                        args[0],
                                        basic_math(basic_math(1,basic_math(args[0],2,"^"),"-"),0.5,"^"),
                                        "/"
                                        )#x=x/(1-x^2)^0.5
                k=0
                while absolute(args[0])>0.2:
                #反正切参数缩放:atanx=2antan(x/(1+(1+x^2)^0.5),变参x>>x/1+(1+x^2)^0.5
                    args[0]=basic_math(
                                       args[0],basic_math(1,basic_math(
                                                                       basic_math(1,basic_math(args[0],2,"^"),"+"),0.5,"^"
                                                                       ),"+"),"/"
                                       )#x=x/1+(1+x^2)^0.5
                    k+=1

                args.append(k)

        module=func(*args,**kwargs)
        return module
    return wrapper

#---defblock---#

@modular_math
def factorial(*args):
    #阶乘计算
    x=args[0];y=1
    for n in range(int(x),1,-1):y*=n
    return y

#---defblock---#

@modular_math
def defactor(*args):
    #双阶乘计算
    x=args[0];y=1
    for n in range(int(x),1,-2):y*=n
    return y

#---defblock---#

@modular_math
def trigono(*args):
    #三角函数计算
    x=args[0];t=args[1]
    sinx=x;cosx=1
    R=1;n=1
    while absolute(R)>1e-17:
    #正弦计算
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(basic_math(2,n,"*"),1,"+"),"^"),
                                factorial(basic_math(basic_math(2,n,"*"),1,"+")),"/"
                                ),"*"
                     )#R=(-1)^n*x^(2n+1)/(2n+1)!
        sinx+=R;n+=1

    R=1;n=1
    while absolute(R)>1e-17:
    #余弦计算
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(2,n,"*"),"^"),
                                factorial(basic_math(2,n,"*")),"/"
                                ),"*"
                     )#R=(-1)^n*x^(2n)/(2n)!
        cosx+=R;n+=1

    trigono_dict={
                  "sin":lambda:sinx,"cos":lambda:cosx,"tan":lambda:sinx/cosx,
                  "cot":lambda:cosx/sinx,"sec":lambda:1/cosx,"csc":lambda:1/sinx
                  }#三角推导式
    try:
        if trigono_dict[t]()>1e16:raise ZeroDivisionError
        return trigono_dict[t]()
    except ZeroDivisionError:print("这个三角函数不存在喵，趋于无穷了喵");raise OverflowError

#---defblock---#

@modular_math
def antrigono(*args):
    #反三角函数计算
    x=args[0];a=args[1];k=args[2]
    antri=x;R=1;n=1
    while absolute(R)>1e-17:
    #反正切计算(反正余弦转化为正切:asinx=atan(x/(1-x^2)^0.5))
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(basic_math(2,n,"*"),1,"+"),"^"),
                                basic_math(basic_math(2,n,"*"),1,"+"),"/"
                                )
                     ,"*"
                     )#R=(-1)^n*x^(2n+1)/(2n+1)
        antri+=R;n+=1
    
    antri*=basic_math(2,k,"^")
    antrigono_dict={
                    "arctan":lambda:antri,"atan":lambda:antri,"arcsin":lambda:antri,"asin":lambda:antri,
                    "arccos":lambda:basic_math(main.pi/2,antri,"-"),"acos":lambda:basic_math(main.pi/2,antri,"-")
                    }
    return antrigono_dict[a]()

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
                print(f"你在第{record['序号']}轮\n问了：{record['问题']}喵\n答案是：{record['答案']}喵~\n")
            return True
        except (TypeError,KeyError):
            print("这次的记录被搞坏了喵，我给你清空了喵");return False
        
#---defblock---#

main=Main()
main.main_run()