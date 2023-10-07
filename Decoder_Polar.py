#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Successive cancellation Decoder
def SCD(W,n,p,F):
    if n == 2:
        u_ = [0,0]
        if W[1] == 0:
            pr1 = bplus(p[0],p[1])
            L_1 = (pr1/(1-pr1))
        else:
            pr1 = 1-bplus(p[0],p[1])
            L_1 = (pr1/(1-pr1))
        if F[0]:
            u_[0]=0
        else:
            if L_1 > 1:
                u_[0] = W[0]^1
            else:
                u_[0] = W[0]
        if W[0]== 0 and W[1]==0:
                pr2 = bminus(p[0],p[1],u_[0])
        elif W[0]== 0 and W[1]==1:
                pr2 = bminus(p[0],p[1],u_[0]^1)
        elif W[0]== 1 and W[1]==0:
                pr2 = bminus(p[0],p[1],u_[0]^1)
        elif W[0]== 1 and W[1]==1:
                pr2 = bminus(p[0],p[1],u_[0])
        L_2 = (pr2/(1-pr2))
        if F[1]:
            u_[1] = 0
        else:
            if L_2>1:
                u_[1] = W[1]^1
            else:
                u_[1] = W[1]
        return [u_,[u_[0]^u_[1],u_[1]],[pr1,pr2]]
    else:
            W1 = W.copy()[:int(n/2)]
            W2 = W.copy()[int(n/2):]
            F1 = F.copy()[:int(n/2)]
            F2 = F.copy()[int(n/2):]
            q = [0,]*int(n/2)
            for i in range(int(n/2)):
                if W[int(n/2) + i] == 0:
                    q[i] = bplus(p[i],p[int(n/2) + i])
                else:
                    q[i] = 1 - bplus(p[i],p[int(n/2) + i])
            [X_ch,W1_ch,p1_] = SCD(W1,int(n/2),q,F1)
            r = [0,]*int(n/2)
            for i in range(int(n/2)):
                if W[i]== 0 and W[int(n/2) + i]==0:
                    r[i] = bminus(p[i],p[int(n/2) + i],W1_ch[i])
                elif W[i]== 0 and W[int(n/2) + i]==1:
                    r[i] = bminus(p[i],p[int(n/2) + i],W1_ch[i]^1)
                elif W[i]== 1 and W[int(n/2) + i]==0:
                    r[i] = bminus(p[i],p[int(n/2) + i],W1_ch[i]^1)
                elif W[i]== 1 and W[int(n/2) + i]==1:
                    r[i] = bminus(p[i],p[int(n/2) + i],W1_ch[i])
            [Y_ch,W2_ch,p2_] = SCD(W2,int(n/2),r,F2)
            Z_ch = X_ch + Y_ch
            W_ch = suma(W1_ch,W2_ch) + W2_ch
            p_ = p1_ + p2_
            return [Z_ch,W_ch,p_]

def suma(v,w):
    n = len(v)
    s = [0,]*n
    for i in range(n):
        if v[i] == 0 or v[i]==1:
            if w[i] ==0 or w[i] == 1:
                if v[i] == 0 and w[i] ==0:
                    s[i] = 0
                else:
                    if v[i]==1 and w[i] == 1:
                        s[i] = 0
                    else:
                        s[i] = 1
    return s

#Calculation the new W
def bplus(p,q):
    return p*(1-q) + (1-p)*q

#Calculation the new W|0,1
def bminus(p,q,x):
    if x == 0:
        return p*q/(p*q + (1-p)*(1-q))
    else:
        if x== 1:
            return (1-p)*q/((1-p)*q+p*(1-q))


# In[6]:


table = ["network","channel coding", "the", "we","shannon", "polar coding","learn","introduced","information theory","strong","a powerful tool","is","interesting","typicality","great","know"]
I = [False,False,False,True,False,True,True,True]
F = [True,True,True,False,True,False,False,False]
#Function for read the messages
def read(L):
    message = ""
    for i in range(len(L)):
        n = 8
        p = [0.08,]*n
        Z,_,_ = SCD(L[i],n,p,F)
        U = [Z[i] for i in range(len(Z)) if I[i]]
        V = binary_rep(U)
        message = message + table[V]
        message = message + " "
    return message
def binary_rep(L):
    s = 0
    for i in range(len(L)):
        s = s + L[len(L)-1 - i]*(2**i)
    return s


# In[7]:


cero = [[1,0,1,1,0,0,1,1],[1,0,1,0,0,1,0,0],[1,0,0,0,0,1,1,0]]
one =  [[0,0,0,0,1,1,0,1],[0,0,1,0,1,0,0,1],[1,0,1,0,1,1,1,0]]
two =  [[0,0,0,0,1,0,0,0],[1,0,0,0,1,0,1,0],[1,0,0,0,0,1,0,1],[0,1,1,0,0,0,1,0]]
three =[[1,1,0,1,0,1,0,1],[1,0,0,1,1,1,0,1],[1,1,1,0,0,1,0,1],[0,1,0,0,1,0,1,0]]
four = [[1,1,0,1,1,1,0,0],[1,1,0,0,1,0,1,1],[1,1,1,1,1,0,0,0],[1,0,1,1,1,0,1,0]]


# In[8]:


#Transformation to the natural order
T = [0,4,2,6,1,5,3,7]
def transformation(L):
    L_ = L.copy()
    for i in range(len(L)):
        L_[i] = [L[i][T[j]] for j in range(8)]
    return L_
cero_ = transformation(cero)
one_ = transformation(one)
two_ = transformation(two)
three_ = transformation(three)
four_ = transformation(four)


# In[9]:


#The messages
print(read(cero_))
print(read(one_))
print(read(two_))
print(read(three_))
print(read(four_))


# In[ ]:




