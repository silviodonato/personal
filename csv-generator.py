import numpy as np

train = ""
evalu = ""

train_f = open("test-training.csv", "w")
evalu_f = open("test-evaluation.csv", "w")
#f.write(raw)

evalu_n = 0
train_n = 0

for i in range(100000):
    x = np.random.uniform(0,10)
    y = np.random.uniform(0,10)
    z = np.random.uniform(0,10)
    t = np.random.uniform(0,10)
    r = (x**2+y**2+z**2)
    res = int(r**0.5)
    if res>10:
        res=0
#    res = 0
#    if r>25 and r<100:
#        res =1
    if i%2==0:
        evalu +="%d,%d,%d,%d,%d\n"%(x,y,z,t,res)
        evalu_n += 1
    else:
        train +="%d,%d,%d,%d,%d\n"%(x,y,z,t,res)
        train_n += 1

train_f.write("%d,%d\n"%(train_n,4))
train_f.write(train)

evalu_f.write("%d,%d\n"%(evalu_n,4))
evalu_f.write(evalu)


#x_train = []
#y_train = []
#x_eval  = []
#y_eval  = []


#x_train_arr = np.array(x_train)
#y_train_arr = np.array(y_train)
#x_eval_arr = np.array(x_eval)
#y_eval_arr = np.array(y_eval)

