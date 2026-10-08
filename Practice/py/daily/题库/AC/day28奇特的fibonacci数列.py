#Eclat对数字3情有独钟，以至于她生活中所有涉及到数字的东西都是3的倍数（比如她出的题目题号都是三的倍数）。
#今天她碰到了一个奇怪的fibonacci数列，定义如下：
#F(n)=F(n−1)+F(n−2)(n≥2)
#F(0)=7；F(1)=11；F(n)=F(n−1)+F(n−2)(n≥2)现在Eclat想要知道她随意给出一个n（n<1,000,000），而F(n)能否被 3 整除。

#输入格式
#多组测试数据，每行一个整数 n
#n，读到文件结束（EOF）为止。
#输出格式
#对每个 n 输出一行：yes 或 no



import sys
for n in map(int,sys.stdin.read().split()):
    print("yes" if n%4==2 else "no")