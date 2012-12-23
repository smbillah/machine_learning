'''
Created on Oct 4, 2012

@author: Masum
'''
from random import normalvariate
from operator import mul
from math import exp

class Layer(object):       

    def __init__(self, index, num_nurons, prev_layer, num_inputs=0):
        self.weight = list()
        self.b= list()
        self.f= list()
        self.e= list()
        
        self.index= index
        self.num_nurons= num_nurons
        self.prev_layer = prev_layer
                            
        
        for _ in xrange(self.num_nurons):
            self.b.append(0.0)
            self.f.append(0.0)
            self.e.append(0.0)
                        
            if index:#for hidden layers                                
                #initialize hidden layer's weight with random values
                w= list()
                for _ in xrange(self.prev_layer.num_nurons):
                    w.append(0.1*normalvariate(0,1))                
                self.weight.append(w)
    
    def train(self):
        pass
      
    def predict(self, input_vector):        
#        print input_vector, self.weight
        for i in xrange(self.num_nurons):
            self.f[i]= sum(map(mul,input_vector, self.weight[i])) + self.b[i]
            self.f[i] = 1.0/(1.0 + exp(-self.f[i]))
        return self.f
    
    def set_params(self, weight, bias):
        self.weight = weight
        self.b = bias
            
        