# print the name with the highest no of charactor
l = list()
num = int(input("enter the number of items: "))
for i in range(0,num):
    a = input("enter the string: ")
    l.append(len(a))

print(l)
