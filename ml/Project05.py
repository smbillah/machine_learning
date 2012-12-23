'''
Created on Oct 4, 2012

@author: Masum
'''
from MLP import MLP
from Utility import read_data
from math import sqrt
from random import shuffle


def unit_test():    
    mlp = MLP([2,2,2,2]);
    mlp.layers[1].set_params([[.2,-.1],[.3,-.3]],[.1,-.2])
    mlp.layers[2].set_params([[-.2,-.3],[-.1,.3]],[.1,.2])
    mlp.layers[3].set_params([[-.1,.3],[-.2,-.3]],[.2,.1])
    

    num_labels=2
    data= [.3, .7, .1, 1.0]

   
    predicted =  mlp.predict(data[:-num_labels])
    print 'predicted: ', predicted            
    mlp.output_error_calculation(data[-num_labels:])
    mlp.backpropagation()
    
    print 'errors:'
    for layer in mlp.layers:
        print layer.e
    
    mlp.gradient_descend(.1)
    print 'weights:'
    for layer in mlp.layers:
        print zip( layer.b, layer.weight)
        
def unit_test2():    
    mlp = MLP([1,2,1]);
    mlp.layers[1].set_params([[-.3],[4]],[.15,-2])
    mlp.layers[2].set_params([[0,2]],[-1])
    
    

    num_labels=1
    data= [1.0, 1.0]

   
    predicted =  mlp.predict(data[:-num_labels])
    print 'predicted: ', predicted            
    mlp.output_error_calculation(data[-num_labels:])
    mlp.backpropagation()
    
    print 'errors:'
    for layer in mlp.layers:
        print layer.e
    
    mlp.gradient_descend(.5)
    print 'weights:'
    for layer in mlp.layers:
        print zip( layer.b, layer.weight)

def n_fold_cross_validation(mlp, n, data, num_label):
    indices = [i for i in xrange(len(data))]
    shuffle(indices)
    total_error=0
    
    for i in xrange(n):
        test_set= list()
        begin = i* len(indices)/n
        end = (i+1)* len(indices)/n
        
        for j in xrange(begin, end):
            test_set.append(indices[j])
        
        training_set= list(set(indices) - set(test_set))
        mlp.train(data, training_set, num_label)
        
        for i in test_set:
            row = data[i]
            predicted= mlp.predict(row[:-num_label])
            if predicted.index(max(predicted)) != row[-num_label:].index(max(row[-num_label:])):
                total_error+= 1                
        #end for
    #end for    
    return sqrt( 1.0*total_error/len(data))


def run_test():
    unit_test2()
#    
#    matrix_data, col_desc= read_data('data/iris.arff')
#    num_label= col_desc[-1]['header']['length']
#    num_input = col_desc[-1]['header']['start']
#    
##    mlp = MLP([num_input,num_label]);        
##    error= n_fold_cross_validation(mlp, 10, matrix_data, num_label)
##    print 'iris1: ', error
##        
#    mlp = MLP([num_input,4,num_label]);
##    print mlp.layers, len(mlp.layers)
#            
#    error= n_fold_cross_validation(mlp, 10, matrix_data, num_label)
#    print 'iris2: ', error
#    
#    matrix_data, col_desc= read_data('data/labor.arff')    
#    num_label= col_desc[-1]['header']['length']
#    num_input = col_desc[-1]['header']['start']
#    mlp = MLP([num_input,num_label]);                
#    error= n_fold_cross_validation(mlp, 10, matrix_data, num_label)
#    print 'labor1: ', error

#    
#import profile
#profile.run('run_test()')

if __name__ == '__main__':
#    unit_test()
    #Allocate an n-by-k matrix, X, to hold intrinsic vectors
#    X= list()
#    for _ in xrange(n):                        
#        X.append([0*x for x in xrange(k)])

    run_test()
    
#    print 'Done!'

