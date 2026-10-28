#prgm1 
# w=float(input("Enter weight"))
# h=float(input("Enter height"))
# BMI=w/(h**2)
# print("BMI",BMI)
# if BMI<18.5:
#     print("underweight")
# elif BMI>=18.5 & BMI<25:
#     print("Normal")
# elif BMI>=25 & BMI<30:
#     print("overweight")
# else:
    #print("Obese")




#prgm2
# u=int(input("Enter no of units: "))
# if u<=100:
#     bill=u*1
# elif u<=200:
#     bill=100*1+(u-100)*2
# else:
#     bill=100*1+100*2+(u-200)*5
# print("bill : ",bill)




#prgm3
# a=int(input("Enter first angle:"))
# b=int(input("Enter second angle: "))
# c=int(input("enter third angle: "))
# if a==b & b==c & c==a:
#     print("Equilateral")
# elif a==b or b==c or c==a:
#     print("Isoceles")
# else:
#     print("Scalene")



#prgm 4-nested if else
age=int(input("Enter age: "))
if age>=18:
    print("allowed for match")
    if age>=18 and age<30:
        print("$2 for ticket")
    elif age>=30 and age<60:
        print("$1 for ticket")
    else:
        print("0$ for ticket")
else:
    print("Not allowed for match")