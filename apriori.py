"""PYTHON IMPLEMENTATION OF THE APRIORI ALGORITHM TO DETERMINE FREQUENT ITEM SETS ALONG WITH THE ASSOCIATION RULES"""

import csv,itertools
def get_1_item_count(D):
    ele_count = {}
    for transaction in D:
        for item in transaction:
            if item in ele_count:
                ele_count[item] += 1
            else:
                ele_count[item] = 1
    return ele_count 

def find_frequent(C, min_sup):
    frequent_item_set=[]
    for ele in C:
        if C[ele] >= min_sup:
            frequent_item_set.append(ele)  
    return frequent_item_set

def apriori_gen(L,k):
    C_k={}
    j=len(L)
    for item_x in range(0,j):
        for item_y in range(item_x+1,j):
            i=1
            a=list(L[item_x])
            b=list(L[item_y])
            for i in range(0,k-1):
                if a[i]!=b[i]:
                    break
            c_temp=()
            if i == (k-2) and a[k-2] < b[k-2]:
                c_temp=tuple(sorted(set(a)|set(b)))
                if has_no_infrequent_subset(c_temp,L,k-1):
                    C_k[c_temp]=0   
    return C_k

def count_candidate_frequency(C, db):
    for key in C:
        for t in db:
            if set(key).issubset(set(t)):
                C[key] += 1
    return C 

def has_no_infrequent_subset(c,L,k):
    c=list(itertools.combinations(c,k))
    for i in c:
        if (k==1 and not i[0] in L) or (k>1 and not i in L):
            return False
    return True

with open("apriori (1).csv") as transactions:
    trans_db=list(csv.reader(transactions,delimiter=','))
db=[];count={}
for row in range(1,len(trans_db)):
    L=[]
    for item in range(0,len(trans_db[row])):
        if trans_db[row][item]=='1':
            L.append(trans_db[0][item])
    db.append(L)
print("The transaction database is : "+str(db))
minsup = float(raw_input("Enter minimum support : "))
minconf=float(raw_input("Enter minimum confidence : "))
L=[]
C=get_1_item_count(db)
for i in C:
    count[i]=C[i]
print('\nC 1 = '+str(sorted(C.items())))
Lk=sorted(find_frequent(C,minsup))
print('L 1 = '+str(Lk))
L.append(Lk)
k=1
while Lk:
    C=apriori_gen(L[k-1],k+1)
    C=count_candidate_frequency(C,db)
    if C : 
        for i in C:
            count[i]=C[i]
        print('C '+str(k+1)+' = '+str(sorted(C.items())))
    Lk=sorted(list(map(sorted,find_frequent(C,minsup))))
    Lk=list(map(tuple,Lk))
    if Lk : 
        print('L '+str(k+1)+' = '+str(Lk))
        L.append(Lk)
        k+=1    
print("\nFrequent Sets : \n"+str(L)+"\n\nMaximal Frequent Set(s) : \n"+str(L[-1])+"\n")
del(L[0])
print "\nASSOCIATION RULES\n"
for i in L:
    for j in i:
        for k in j:
            y=tuple(set(j)-set(k))
            conf=float(count[j])/float(count[k])
            if conf>minconf:
                print k+"--->"+str(y)+' with confidence of '+str(conf)
        print ''
    print '\n'
