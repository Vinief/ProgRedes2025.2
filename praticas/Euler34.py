
x = '10'
contador = 0
somas = []
somafat = 0
while x != '150' :
    if somafat != x:
        somafat = 0
    else:
        somas += somafat
    contador = 0
    cond = True
    while contador != len(x) and cond: 
        alg = int(x[contador])
        fat = 1
        for a in range(1,int(alg)+1):
            fat *= a
            somafat += fat
            if x == '145':
                print(fat, somafat)

            if fat > int(x):
                cond = False
                break
        contador += 1
    x = str(int(x) + 1)
print(x,somas)
