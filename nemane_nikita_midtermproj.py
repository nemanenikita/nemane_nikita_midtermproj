#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd;
import numpy as np;


# In[20]:


data1=[]
order_of_elements = []
dictionary={}


# In[21]:


def load_data_set():
    print("Please enter which data set you need \n1)Amazon \n2)BestBuy \n3)Nike \n4)Data1")
    while True:
        choice_of_data = input()
        if choice_of_data == "1":
            path_to_data = "Amazon.csv"
            print("User chose Amazon dataset")
            break
        elif (choice_of_data =="2"):
            path_to_data ="Bestbuy.csv"
            print("User chose BestBuy dataset")
            break
        elif (choice_of_data =="3"):
            path_to_data ="Nike.csv"
            print("User chose Nike dataset")
            break
        elif (choice_of_data =="4"):
            path_to_data ="Data1.csv"
            print("User chose Data1 dataset")
            break
        else:
            print("Please enter the right input between 1 to 4")
    return path_to_data


# In[22]:


# This function receives path to data and order of items
def load_data(data_path,order):
#     Loads the data
    Transactions=[] #list to append transactions
    path = pd.read_csv(data_path)
    transaction_data = path.Transactions
#     print("td",transaction_data)
    for t in transaction_data:
        comma_separated = list(t.strip().split(',')) #will get list of items
        unique_data = list(np.unique(comma_separated)) #unique is used to remove repetition
        unique_data.sort(key=lambda x: order.index(x)) #sort according to lexical order
        Transactions.append(unique_data) #Append into the transaction list
#     print("Transactions",Transactions)
    return Transactions


# In[23]:


#load the data and return order of data
def single_element():
    path = pd.read_csv(data_path)
    records = path.Transactions
    for i in records:
        comma_separated = i.split(",")
        for j in comma_separated:
            data1.append(j)
    for k in data1:
        count = 0
        for l in data1:
            if(k==l):
                count+=1
        dictionary.update({k:count})
    for i in dictionary.keys():
        order_of_elements.append(i)
#     print("order of elements",order_of_elements)
    return order_of_elements


# In[24]:


#This function goes over the transactions and count the number of occurences
# Using python sets operation to check if the itemset is subset of the set
# and if it is then incrementing the count
def occurence_count(items, Transactions):
    count =0
    for i in range(len(Transactions)):
        if set(items).issubset(set(Transactions[i])):
            count+=1
    return count


# In[25]:


#This function joins two sets, it first sorts itemsets according to their order
#Checks if they are joinable, means all the items within the sorted itemsets are same except the last one
#and in the last one the one belonging to second itemset must be greater than the last one in the 1st itemset
def combination_two_sets(set1,set2,order):
    set1.sort(key=lambda x: order.index(x))
    set2.sort(key=lambda x: order.index(x))
    for i in range(len(set1)-1):
        if set1[i]!=set2[i]:
            return []
    if order.index(set1[-1])< order.index(set2[-1]):  #last item of each itemset
        return set1+[set2[-1]]
#     print("->",[])
    return [] #if the condition does not satisfies then return empty list


# In[26]:


#This function joins 2 itemsets
#It will look for each of the itemset within set of itemsets
#it will check if combination_of_two_sets returns empty list and then append in the combination set
def combination_sets(sets,order):
    C_S = []
    for i in range(len(sets)):
        for j in range(i+1,len(sets)):
            it_out = combination_two_sets(sets[i],sets[j],order)
            if len(it_out)>0:
                C_S.append(it_out)
#     print("C_S",C_S)
    return C_S


# In[27]:


#This function will return List of frequent itemsets, List of their support counts and List of newly discarded items
#It will check the length of discarded items list if it is greater than 0 then it will check
#whether they contain any subset of itemsets that was previously discarded
#else it will call occurence_count function to count their frequency
#check if it is greater than threshold support
#if greater then append to the List of frequent items.
#else append to the list of discarded items
def get_frequent_items(itemsets, Transactions, support, prev_discarded):
    L=[]
    supp_count=[]
    new_discarded =[]    
    k = len(prev_discarded.keys())
    for s in range(len(itemsets)):
        discarded_before = False
        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break
        if not discarded_before:
            count = occurence_count(itemsets[s],Transactions)
            if count/len(Transactions) >= support:
                L.append(itemsets[s])
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])
    print('List of Frequent Items-',L)
    print("Support Count-",supp_count)
    print("New Discarded Items\b",new_discarded)
    return L, supp_count, new_discarded


# In[28]:


from itertools import combinations, chain
#returns all the subsets
#using itertools library
#combinations returns all the posible combinations of specific size
#chain will put iterables given by combination in just one iterable
#combinations of s on size r from 1 to len(itemset)+1
def powerset(s):
    return list(chain.from_iterable(combinations(s,r) for r in range(1, len(s)+1)))

def write_rules(X,X_S,S,conf,sup,number_of_trans):
    out_rules = ""
    out_rules+= "\nFreq. Itemsets: {} \n".format(X)
    out_rules+= "    Rule: {} -> {} \n".format(list(S),list(X_S))
    out_rules+="   Confidance: {0:2.3f} ".format(conf) #string formatting rounding off the decimal places to 3
    out_rules+="   Support: {0:2.3f} ".format(sup/number_of_trans)
    return out_rules


# In[29]:


data_path = load_data_set()
order = single_element()
Transactions = load_data(data_path,order)
while True:
    try:
        support= float(input("Enter support in percent:(1 to 100)"))
        if support<1 or support>100:
            raise ValueError
        break
    except ValueError:
        print("Invalid support value.The number must be in the range of 1-100")
while True:
    try:
        confidence= float(input("Enter confidence in percent:(1 to 100)"))
        if confidence<1 or confidence>100:
            raise ValueError
        break
    except ValueError:
        print("Invalid support value.The number must be in the range of 1-100")

min_support = support/100
min_conf = confidence/100

number_of_trans = len(Transactions)
Transactions
#Initialization
C={}  #set of candidates as a dictionary where the keys are going to be the iterations
L={}
itemset_size = 1
Discarded = {itemset_size:[]}
C.update({itemset_size : [[f] for f in order]}) #all the candidates of itemset of size 1
C


# In[12]:


#Create L1 dictionary similar to C but containning only frequent items
supp_count_L={}
f,sup, new_discarded= get_frequent_items(C[itemset_size],Transactions, min_support, Discarded)
Discarded.update({itemset_size :new_discarded})#update variables with just generated outputs
L.update({itemset_size:f})
supp_count_L.update({itemset_size: sup})


# In[219]:


#Function to print the table
def print_table(T,supp_count):
    print("Itemset  | Frequency")
    for k in range(len(T)):
        print("{}   :   {}".format(T[k],supp_count[k]))
    print("\n\n")
print_table(L[1], supp_count_L[1]) #to print 1st iteration


# In[220]:


#now we are going to implement the main loop of the algorithm.
#we need to generate candidates on each iteration set of itemset of size k
#after that we need to generate frequent itemsets
#to generate the c[k], we are going to need the join step from L[k-1]
#after that we are able to generate L[k] the frequent itemsets
#if size of L[k]>1 then algo works else the set is empty the algo stops
k=itemset_size+1
convergence = False
while not convergence:
    C.update({ k : combination_sets(L[k-1],order)})
    print(C)
    print("\nTable of Frequent itemsets C{}: \n".format(k))
    print_table(C[k],[occurence_count(it,Transactions) for it in C[k]])
    f,sup,new_discarded = get_frequent_items(C[k],Transactions,min_support,Discarded)
    Discarded.update({k:new_discarded})
    L.update({k:f})
    supp_count_L.update({k:sup})
    if len(L[k])==0:
        convergence=True
    else:
        print("\nTable of selected Frequent itemsets L{} \n".format(k))
        print_table(L[k],supp_count_L[k])
    k+=1


# In[221]:


#generate association rules
#we need to loop over all the frequent itemsets i.e the itemsets in L
#for each itemsets we need to generate all the rules according to the combinations
#frequent itemsets of size 1 cannot producce significant rules so we can start with size 2 i.e K=1 in dictionary 
assoc_rules_str=""
for i in range(1, len(L)):
    for j in range(len(L[i])):
        s = powerset(L[i][j]) #to produce combinations
        s.pop()#get rid of last element which contains subsets of all the items and we dont need that
        for z in s:
            S = set(z)
            X = set(L[i][j])
            X_S=set(X-S)
            sup_x = occurence_count(X,Transactions)
            sup_x_s =occurence_count(X_S,Transactions)
            conf = sup_x/occurence_count(S,Transactions)
            if conf>= min_conf  and sup_x>= min_support:
                assoc_rules_str+= write_rules(X,X_S,S,conf,sup_x,number_of_trans)


# In[222]:


print(assoc_rules_str)


# In[ ]:





# In[ ]:




