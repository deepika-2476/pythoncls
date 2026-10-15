#prgm1
# c_h=int(input("enter no of cpu hours: "))
# s=int(input("enter storage in gb: "))
# d_t=int(input("enter data transfer in b: "))
# c_h_c=c_h*5
# s_c=s*2
# d_t_c=d_t*1
# total_cost=c_h_c+s_c+d_t_c
# if c_h>100:
#     print(total_cost+500)
# else:
#     print(total_cost)



#prgm2-if-elif-else
uptime=float(input("Enter uptime: "))
bill=int(input("enter a bill: "))
if uptime>=99.9:
    refund=0;
elif uptime>=98:
    refund=bill*10/100
else:
    refund=bill*25/100
print("Refund Amount: ",refund)