#给定只由 6 种括号字符组成的字符串：(, ), [, ], {, }。
#判断每个字符串是否为“合法括号序列”，合法则输出 YES，否则输出 NO。合法括号序列的定义：
#空串合法； 若 A 合法，则 (A), [A], {A} 均合法； 若 A 与 B 均合法，则 AB 合法



import sys
data=sys.stdin.read().splitlines()
T=int(data[0])
df={")":"(","]":"[","}":"{"}
for put in data[1:T+1]:
    answer=[]
    key=True
    for f in put:
        if f==" ":pass
        elif f in "([{":
            answer.append(f)
        else:
            if not answer:key=False;break
            else:
                if answer[-1]!=df[f]:key=False;break
                else:answer.pop()
    if key and not answer:print("YES")
    else:print("NO")