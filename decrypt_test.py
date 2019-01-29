# 单日
# key = 'K%Z6DnmLwd9BQek+61%4,-30925.87'
# data = "Z99Z"
# 多日
# 简单映射,映射表前一半字符对应后一半字符，把 data 的数据
key = "I4+2SzpFxAOLPnU.3-2497+%,86051"
data = 'U22UAU2p2AU4PU'
# n = {}
# s = []
# for i in range(len(key) // 2):
#     n[key[i]] = key[len(key) // 2 + i]
# for j in range(len(data)):
#     s.append(n[data[j]])
# print(s)
# print(list(map(int,''.join(s).split(','))))
m = list(key)
# print(m)
d = dict(zip(m[:len(m)//2],m[len(m)//2::]))
print(m[:len(m)//2])
print(m[len(m)//2::])
# print(d)
# print(list(map(lambda x:d[x],data)))
print(''.join(map(lambda x:d[x],data)).split(','))
str_list =  ''.join(map(lambda x: d[x], data)).split(',')
data_list = []
for s in str_list:
    data_list.append(int(s))
print(data_list)