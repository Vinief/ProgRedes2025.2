x = '1'
cond_1 = True
while cond_1:
    
    num = str(int(x) * 2)
    
    cont = 0
    
    cond = True
    if len(num) == len(x):
        
        while cond: 
            if x[cont] in num and num[cont] in x and x[cont] != num[cont] and x.count(x[cont]) == num.count(x[cont]):
                cont += 1 
                if cont == len(x):
                    cond,cond_1 = False,False
            else:
                cond = False

    else:
        x = 10**len(str(x))

    x = str(int(x) + 1)    
print(x , num)
