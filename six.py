#start stop
# #n=10
# for i in range(0,n+1):
#     print(i)   1 to 10




# n=10
# for i in range(0,n-1):
#     print(i)  1 to 8



# n=10
# for i in range(0,n):
#     print(i) 1 to 9


# n=10
# for i in range(1,n):
#     print(i) 1 to 9


# n=10
# for i in range(1,n+1):
#     print(i) 1 to 10


# n=10 
# for i in range(1,n-1):
#     print(i)  1 to 8





#start stop step
# n=10
# for i in range(1,n,2):
#     print(i)  1,3,5,7,9




# n=10
# for i in range(100,0,-1):
#     print(i) 100 to 1




#factors
# n=12
# for i in range(1,n+1):
#     if n%i==0:
#         print(i)





# n=int(input())
# for i in range(1,n+1):
#     if n%i==0:
#         print(i)




# n=12
# f=1
# for i in range(1,n+1):
#     f=f*i
# print(f)




#prime number
# n=5
# if n>1:
#     for i in range(2,n):
#         if n%i==0:
#             print("not a prime number")
#     else:
#         print("prime number")


#seven table
# n=7
# for i in range(1,n+4):
#     print(n,"*",i,"=",(n*i))



#binary number
n=1010
sum=0
power=0
for i in range(n):
    digit=n%10
    sum=sum+digit*2**power
    n=n//2
    power=power+1
print(sum)