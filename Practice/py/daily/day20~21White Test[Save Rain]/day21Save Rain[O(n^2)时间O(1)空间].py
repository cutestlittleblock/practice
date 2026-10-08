pillar=[]
rain=0
given_pillar=input("请给定柱子,数字间用“,”隔开:")

n_str=given_pillar.split(",")
for n in n_str:
    pillar.append(int(n))

left_max=pillar[0]

for x,i in enumerate(pillar):
    left_max=max(left_max,pillar[x])
    right_max=max(pillar[x:])

    if left_max<right_max:
        v=max(0,left_max-i)
        rain+=v
    else:
        v=max(0,right_max-i)
        rain+=v

print(rain)