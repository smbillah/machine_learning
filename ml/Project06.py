'''
Created on Oct 4, 2012

@author: Masum
'''
from UnsupervisedMLP import UnsupervisedMLP
from MLP import MLP
from Utility import read_image_data, read_action_data
from MYSVGWriter import MYSVGWriter

min_0, max_0, min_1, max_1 = 0.0,0.0,0.0,0.0   


def rgbToUint(r, g, b):
    return ((int(b) & 0xff) | ((int(g) & 0xff) << 8) | ((int(r) & 0xff) << 16))


def plot_intrinsic(X, w, h):    
    svg =  MYSVGWriter(640, 480, -100, -100, 100, 100)    
    x_prev, y_prev = None, None
    for row in X:                
        x= 10**1*row[0] #to scale data
        y= 10**1*row[1] #to scale data        
        svg.dot(x ,y,1, 0x008080)
        if x_prev and y_prev:
            svg.line(x_prev, y_prev, x, y, .05, 0xc0c0c0)        
        x_prev=x
        y_prev=y        
    svg.svgprint("intrinsic.svg")    

def image_generation(us_mlp, s, w, h, file_name):    
    in_vect= [0.0, 0.0, 0.0, 0.0]
    out_vect=[0.0,0.0,0.0] 
    
    in_vect[2]= s[0]*(max_0-min_0)+min_0
    in_vect[3]= s[1]*(max_1-min_1)+min_1
    
    svg =  MYSVGWriter(640, 480, 0, 0, w, h)    
    for y in range(h):
        in_vect[1] = 1.0* y/h
        for x in range(w):
            in_vect[0] = 1.0*x/w
            out_vect = us_mlp.predict(in_vect)                    
            svg.rect(x, h - 1 - y, 1, 1, rgbToUint(out_vect[0] * 255, out_vect[1] * 255, out_vect[2] * 255));
    
    svg.svgprint(file_name+'.svg')    


 
def normalize(X):
    min_0= min([x[0] for x in X])
    max_0= max([x[0] for x in X])
        
    min_1= min([x[1] for x in X])
    max_1= max([x[1] for x in X])
    
    for x in X:
        x[0]= (x[0]-min_0)/(max_0-min_0)
        x[1]= (x[1]-min_1)/(max_1-min_1)    
        

def run_test():
    print 'starting ....'
    Y = read_image_data('data/observations.arff')    
    print 'image reading is finished...'
    print len(Y)

    #Allocate an n-by-k matrix, X, to hold intrinsic vectors
    X , K = list(), 2
    for _ in xrange(len(Y)):                        
        X.append([0.0*x for x in xrange(K)])
    
    w,h= 64,48
    us_mlp = UnsupervisedMLP([4, 12, 12, 3])
    us_mlp.set_image_dim(w, h)    
    us_mlp.train(Y, X, K)
    
    print 'USMLP training is finished'
    plot_intrinsic(X, w, h)
    
    print 'intrinsic plotting is done'
    #2nd MLP
    normalize(X)
    print 'reading action file'    
    A = read_action_data('data/actions.arff')
    
    print len(A), len(X)
    for i in xrange(len(A)-1):
        row = A[i]
        row.extend(X[i])
        row.extend(X[i+1])
    del A[-1]
    print 'training mlp with action '
    mlp = MLP([6,6,2])
    mlp.train1(A, K)
    print 'training done'

    #operate the crane now!
    #'a':[1.0,0.0,0.0,0.0],'c': [0.0,0.0,1.0,0.0]
    s = [1.0,0.0,0.0,0.0]             
    s.extend(X[0])    
    for i in range(5):
        predict=mlp.predict(s)
        s[4] = predict[0]
        s[5] = predict[1]                
#        image_generation(us_mlp, s, w, h, 'frame'+str(i))
    
    #up
    s[0]=0 ; s[2]=1.0        
    for i in range(5,10):
        predict=mlp.predict(s)
        s[4] = predict[0]
        s[5] = predict[1]                
    image_generation(us_mlp, s, w, h, 'frame'+str(i+1))    
    
#    
#import profile
#profile.run('run_test()')

if __name__ == '__main__':
    run_test()    
    print 'Done!'

