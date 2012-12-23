'''
Created on Oct 4, 2012

@author: Masum
'''
from UnsupervisedMLP2 import UnsupervisedMLP2
from MLP import MLP
from DBLP import read_processed_data
from MYSVGWriter import MYSVGWriter
from random import normalvariate

min_0, max_0, min_1, max_1 = 0.0,0.0,0.0,0.0   


def rgbToUint(r, g, b):
    return ((int(b) & 0xff) | ((int(g) & 0xff) << 8) | ((int(r) & 0xff) << 16))


def plot_intrinsic(X, w, h):    
    svg =  MYSVGWriter(640, 480, -100, -100, 100, 100)    
    x_prev, y_prev = None, None
    for row in X:                
        x= 10**2*row[0] #to scale data
        y= 10**2*row[1] #to scale data        
        svg.dot(x ,y,1, 0x008080)
        if x_prev and y_prev:
            svg.line(x_prev, y_prev, x, y, .05, 0xc0c0c0)        
        x_prev=x
        y_prev=y        
    svg.svgprint("intrinsic_aa.svg")    

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


 
def normalize(Y):
    min= 1000000
    max= -1
    
                  
    for y in Y:
        if y[3]< min: min=y[3]
        if y[3]>max: max= y[3]
    
    for y in Y:    
        y[3]= 1.0*(y[3]-min)/(max-min)
            
        

def run_test():
    print 'starting ....'
    path_params = 'data/params2.txt'
#    path_merge= 'data/test-c.txt'
    
#    path= 'data/test-a.txt'
    path_train = 'data/train300.txt'
    num_author = -1
    num_data=-1
    block_size=-1
#    with open(path_params,'r') as f:
#        block_size = int(f.readline().strip())
#        num_author = int(f.readline().strip())
#        num_data = int(f.readline().strip())
#    print 'num_author:',num_author, 'num_data:', num_data, 'block_size:', block_size
#    
    authors=dict()
    with open('data/merge-author.txt', 'r') as f:
        for line in f.xreadlines():                                                   
            toks = line.strip().split('\t')
            authors[int(toks[0])]=int(toks[1])
#    print authors
    
    Y=[]
    with open(path_train, 'r') as f:
        for line in f.xreadlines():                                                   
            r = line.strip().split(' ')
            y = [authors[int(r[0])], authors[int(r[1])], float(r[2]), float(r[3])]
            Y.append(y)             
#    print Y
    
    num_author= len(authors)
    print num_author
    
    
    
    
    #Allocate an n-by-k matrix, X, to hold intrinsic vectors
    X , K = list(), 5
    for _ in xrange(num_author):                        
        X.append([.1*normalvariate(0,1) for _ in xrange(K)])
#        X.append([0.0 for _ in xrange(K)])
    
    print 'intrinsic data X:'
    print X
#    return
    
    w,h= 64,48
    topology= [K, 5, 1,2*num_author]
    us_mlp = UnsupervisedMLP2(topology, path_train, block_size)    
    print 'network created'    
    us_mlp.train(X,Y, K)
    
    print 'writing X values:'
    with open('data/X.txt', 'w+') as f:
        for x in X:
            f.write('\t'.join(map(str, x)))
            f.write('\n')
            
    print 'writing W values:'
    with open('data/W.txt', 'w+') as f:
        f.write(' '.join(map(str, topology)))
        f.write('\n')
        
        for layer in us_mlp.layers[1:]:
            for i in xrange(layer.num_nurons):
                f.write(str(layer.b[i])+'\t')                
                f.write(' '.join(map(str, layer.weight[i])))
                f.write('\n')
    
    print 'generating svg'
#    plot_intrinsic(X, w, h)
    
    print 'intrinsic plotting is done'
    return
    
        
#    
#import profile
#profile.run('run_test()')

if __name__ == '__main__':
    run_test()    
    print 'Done!'

