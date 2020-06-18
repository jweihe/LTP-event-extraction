import re
import random
str1='吃饭'
str2='饿'
str3='不爱'
str4='没错'
str5='感冒'
str6='没生气'
list1=['我没有不爱你','我没有说不爱你','你要是这么想我也没办法']
list2=['随便','你要是这么想我也没办法','你别无理取闹了','你就不能安静点吗','我错了行了吧']
pattern1=re.compile(str1)
print("你好小姐姐，欢迎和直男何对话！")

print("咋了？")
while 1==1:
    str=input()
    if str.find(str1)!=-1 or str.find("吃")!=-1:
        print("随便呗 我吃啥都行")
    elif str.find(str2)!=-1:
        print('那你吃点东西呗')
    elif str.find(str3)!=-1:
        print(random.choice(list1))
    elif str.find(str4)!=-1:
        print("我错了 你别闹了")
    elif (-1 != str.find(str5)) or (str.find('舒服') != -1) or (str.find('难受')!=-1):
        print("多喝热水")
    elif(str.find(str6)!=-1):
        print("那就好")
    else:
        print(random.choice(list2))
