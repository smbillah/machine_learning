'''
Created on Oct 4, 2012

@author: Masum
'''
from SupervisedLearning import SupervisedLearning
from Layer import Layer
from random import shuffle
from operator import mul
from math import exp


class MLP(SupervisedLearning):
    '''
    classdocs
    '''
    
    def __init__(self, descriptor):
        #[4 2 3 2]
        self.layers= list()
        
        self.descriptor = descriptor;
        index = 0 
        for num_neurons in self.descriptor:
            if not index:
                layer= Layer(index, num_neurons, None, self.descriptor[index])
            else:
                layer= Layer(index, num_neurons, layer)
            index+=1
            self.layers.append(layer)
    
    def predict(self, input_vector):
        self.layers[0].f[:] = input_vector[:]
        
        for layer in self.layers[1:]:
            for i in xrange(layer.num_nurons):
                #self.f[i]= logistic_function(dot_prod(input_vector, self.weight[i]) + self.b[i])            
#                print layer.prev_layer.f, layer.weight[i],  layer.b[i]
                layer.f[i]= sum(map(mul,layer.prev_layer.f, layer.weight[i])) + layer.b[i]
                layer.f[i] = 1.0/(1.0 + exp(-layer.f[i]))
#        print self.layers[-1].f
        return self.layers[-1].f
        
            
    def output_error_calculation(self, target_vector):        
        predicted_vector = self.layers[-1].f

#        if len(predicted_vector)!=len(target_vector):
#            raise Exception("dimension mismatch")        
        for i in xrange(self.layers[-1].num_nurons):
            e = (target_vector[i]-predicted_vector[i])*(predicted_vector[i])*(1-predicted_vector[i])
            self.layers[-1].e[i]=e            
        return self.layers[-1].e
    
    
    def gradient_descend(self, step_size):               
        for layer in self.layers[1:]:                               
            for j in xrange(layer.num_nurons):
                for k in xrange(layer.prev_layer.num_nurons):
                    layer.weight[j][k] = layer.weight[j][k] + step_size*layer.e[j]*layer.prev_layer.f[k]                
                layer.b[j] = layer.b[j] + step_size*layer.e[j]
                        
    
    def backpropagation(self):
        prev= self.layers[-1]
                
        for layer in reversed(self.layers[1:-1]):                    
            for i in xrange(layer.num_nurons):
                e_i=0.0
                for j in xrange(prev.num_nurons):
                    e_i += prev.weight[j][i] * prev.e[j]
                #e_i is available
                e_i *=layer.f[i] * (1-layer.f[i])
                layer.e[i] = e_i            
            prev = layer
                
                
    def train(self, data_matrix, index,num_labels, learning_rate=0.1):                        
        for _ in xrange(500):
            for i in index:
#                data = data_matrix[i]            
                self.predict(data_matrix[i][:-num_labels])                        
                self.output_error_calculation(data_matrix[i][-num_labels:])
                self.backpropagation()                                    
                self.gradient_descend(learning_rate)            
            learning_rate*= 0.997
                
                
    def train1(self, data_matrix, num_labels, learning_rate=0.1):                        
        index = range(len(data_matrix))
        for _ in xrange(100):
            shuffle(index)
            for i in index:            
                self.predict(data_matrix[i][:-num_labels])                                 
                self.output_error_calculation(data_matrix[i][-num_labels:])
                self.backpropagation()                                    
                self.gradient_descend(learning_rate)            
            learning_rate*= 0.997
                
                
                
        
        
            
    
    
    
        