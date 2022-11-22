# -*-coding:utf-8-*-
def compare(v1, v2):
    """
    :param v1: 第一个版本号
    :param v2: 第二个版本号 两个版本号中只能包含数字和 "." 存在
    :return: 0表示v1=v2， 1表示v1>v2 , -1表示v1<v2
    """
    lst_1 = v1.split('.')
    lst_2 = v2.split('.')
    c = 0
    while True:
        if c == len(lst_1) and c == len(lst_2):
            return 0
        if len(lst_1) == c:
            lst_1.append(0)
        if len(lst_2) == c:
            lst_2.append(0)
        if int(lst_1[c]) > int(lst_2[c]):
            return 1
        elif int(lst_1[c]) < int(lst_2[c]):
            return -1
        c += 1
        
if __name__ == '__main__':
    a = compare("0.1.2", "0.1")
    print(a)
