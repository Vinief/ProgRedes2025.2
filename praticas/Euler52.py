x = '1'
cond_1 = True
while cond_1:
    
    num_2 = str(int(x) * 2)
    num_3 = str(int(x) * 3)
    num_4 = str(int(x) * 4)
    num_5 = str(int(x) * 5)
    num_6 = str(int(x) * 6)
    
    cont = 0
    
    cond = True
    if len(num_6) == len(x):
        
        while cond: 
            if x[cont] in num_2 and num_2[cont] in x and x[cont] != num_2[cont] and x.count(x[cont]) == num_2.count(x[cont]) and x[cont] in num_3 and num_3[cont] in x and x[cont] != num_3[cont] and x.count(x[cont]) == num_3.count(x[cont]) and x[cont] in num_4 and num_4[cont] in x and x[cont] != num_4[cont] and x.count(x[cont]) == num_4.count(x[cont]) and x[cont] in num_5 and num_5[cont] in x and x[cont] != num_5[cont] and x.count(x[cont]) == num_5.count(x[cont]) and x[cont] in num_6 and num_6[cont] in x and x[cont] != num_6[cont] and x.count(x[cont]) == num_6.count(x[cont]):

                cont += 1 
                if cont == len(x):
                    cond,cond_1 = False,False
            else:
                cond = False

    else:
        x = 10**len(str(x))
    if cond_1:
        x = str(int(x) + 1)    
print(x , num_2,num_3,num_4,num_5,num_6)
