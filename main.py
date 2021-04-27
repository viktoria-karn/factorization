from random import randint
import math
import random
import sympy
import os

#f(a)=a^2+1
def func(a):
	return a**2 + 1

def erathosphene(n):
	return [
	    x for x in range(2, n + 1) if x not in [
	        i for sub in
	        [list(range(2 * j, n + 1, j)) for j in range(2, n // 2)]
	        for i in sub
	    ]
	]


def my_gcd(a, b):
  count_gcd_cycle=0
  while a!=0 and b!=0:
    if a >= b:
      a = a % b
    else:
      b = b % a
    count_gcd_cycle+=1
  return [a+b,count_gcd_cycle]


def Pollard(N):
    count_first_cycle=0
    count_second_cycle=0
    #создаем список для хранения двух значений-вычисленного делителя и кол-ва итераций
    gcd_func=[]
    d = N
    while d==N:
        a = random.randint(0, N - 1)
        x = func(a) % N
        y = func(func(a)) % N
        gcd_func = my_gcd(abs(y-x),N)
        d=gcd_func[0]
        count_first_cycle+=gcd_func[1]
        while d==1:
            x = func(x) % N
            y = func(func(y))% N
            gcd_func = my_gcd(abs(y-x),N)
            d=gcd_func[0]
            count_second_cycle+=gcd_func[1]
    #если получили d во внешнем цикле
    if(count_second_cycle==0):
      iteration=count_first_cycle
    else:
      iteration=count_first_cycle*count_second_cycle
    return [d,iteration]

#очистка консоли
os.system("clear")

with open ("sourse.txt","r") as sourse_file:
  #номер строки,содержащей составное число из файла sourse.txt-имя файла,содержащего разложение этого составного числа
  file_name=1
  for N in sourse_file:
    N_copy=int(N)
    decompose_pollard = []
    decompose_end=[]
    N=int(N)
    
    L=[]
    l_index=[]
    prime_number = erathosphene(1000)
    for i in prime_number:
      if (N % i) == 0:
        L.append([i, 1])
        l_index.append(i)
        N //= i
        while (N % i) == 0:
            pos = l_index.index(i)
            L[pos][1] += 1
            N //= i
    
    while N!=1:
      k=Pollard(N)[0]
      if not sympy.isprime(k):
        continue
      N//=k
      if k not in l_index:
        L.append([k,1])
        l_index.append(k)
      else:
        pos=l_index.index(k)
        L[pos][1]+=1
      if(sympy.isprime(N)):
        if N not in l_index:
          L.append([N,1])
          l_index.append(N)
        else:
          pos=l_index.index(N)
          L[pos][1]+=1
        break
    
    L.sort()

    #записываем в файл  
    with open(str(file_name)+".txt","w") as write_file:
      for row in L:
        write_file.write("{} {}\n".format(str(row[0]),str(row[1])))
    file_name+=1

    #проверка(перемножаем множители и сверяем с исходням числом из файла)
    check_number=1
    count=0
    for row in L:
      check_number*=pow(row[0],row[1])
    print(check_number)
    with open("sourse.txt","r") as read_file:
      for line in read_file:
        count+=1
        if(count==file_name-1):    
          if (check_number==int(line)):
            print("All right")
          else:
            print("Everything is bad")
          break
