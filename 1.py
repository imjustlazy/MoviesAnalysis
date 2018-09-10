# import pdb
s = input()
l = [int(i) for i in s if i.isdigit()]
leng = len(l)
ans = [x-x for x in l]
flag = [x-x for x in l]
# print(ans)
for i, a in enumerate(l):
    # pdb.set_trace()
    if i != 0:
        ans[i] = ans[i-1]
        if a > l[i-1]:
            if flag[i-1] == 1:
                ans[i] = ans[i-1] + a - l[i-1]
                flag[i] = 1
            elif a - l[i-1] > ans[i]:
                ans[i] = a - l[i-1]
                flag[i] = 1
            if i > 3:
                ans[i] = max(ans[i-3] + a - l[i-1], ans[i])
print(ans[len(l)-1])
# print(flag)