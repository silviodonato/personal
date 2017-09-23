import numpy as np

train = ""
evalu = ""

train_f = open("test-training.csv", "w")
evalu_f = open("test-evaluation.csv", "w")
#f.write(raw)

evalu_n = 0
train_n = 0

for i in range(10):
    x = np.random.uniform(0,3)
    y = np.exp(np.sin(x))**0.3 +1
    if i%2==0:
        evalu +="%f,%f,%f,%f,%f\n"%(x,x,x,x,y)
        evalu_n += 1
    else:
        train +="%f,%f,%f,%f,%f\n"%(x,x,x,x,y)
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

