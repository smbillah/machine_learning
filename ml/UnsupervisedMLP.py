'''
Created on Oct 17, 2012

@author: Masum
'''

from SupervisedLearning import SupervisedLearning
from Layer import Layer
from random import choice
from operator import mul
from math import exp


class UnsupervisedMLP(SupervisedLearning):

    def __init__(self, descriptor):
        #[4 2 3 2]
        self.layers= list()
        self.num_layers = len(descriptor) - 1
        self.descriptor = descriptor;
        index = 0 
        for num_neurons in self.descriptor:
            if not index:
                layer= Layer(index, num_neurons, None, self.descriptor[index])
            else:
                layer= Layer(index, num_neurons, layer)
            index+=1
            self.layers.append(layer)
        
    def set_image_dim(self, w, h):
        self.w, self.h = w, h
        self.m_w = range(w)
        self.m_h = range(h)
        
    
    def predict(self, input_vector):
        self.layers[0].f[:] = input_vector[:]
        
        for layer in self.layers[1:]:
            for i in xrange(layer.num_nurons):                            
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
            for i in xrange(layer.num_nurons):
                for j in xrange(layer.prev_layer.num_nurons):
                    layer.weight[i][j] = layer.weight[i][j] + step_size*layer.e[i]*layer.prev_layer.f[j]                
                layer.b[i] = layer.b[i] + step_size*layer.e[i]
                        
    def gradient_descend_input(self, step_size):               
        layer0 = self.layers[0]
        layer1 = self.layers[1]                               
        for i in xrange(2, layer0.num_nurons):
            for j in xrange(layer1.num_nurons):
                layer0.f[i] += layer1.weight[j][i]*step_size*layer1.e[j]                
            
    
    
    def backpropagation(self):
        prev= self.layers[-1]
                
        for layer in reversed(self.layers[1:-1]):                    
            for i in xrange(layer.num_nurons):
                e_i=0.0
                for j in xrange(prev.num_nurons):
                    e_i += prev.weight[j][i] * prev.e[j] * layer.f[i] * (1-layer.f[i])
                #e_i is available
                layer.e[i] = e_i            
            prev = layer
                
                
    def train(self, Y, X, k, learning_rate=0.1):                                 
        c = len(Y[0]) / (self.w * self.h);
        n = len(Y)
        indices = range(n)
                
        for _ in xrange(10): #10
            for _ in xrange(10000000):#10,000,000
                r = choice(indices)
                u = choice(self.m_w)
                v = choice(self.m_h)
                
                features = [1.0*u/self.w, 1.0*v/self.h]
                features.extend(X[r])
                
                s = c * (self.w * v + u);                
                label = Y[r][s:s+c]
                
                self.predict(features);
                self.output_error_calculation(label)
                self.backpropagation()                                    
                self.gradient_descend(learning_rate)                                
                self.gradient_descend_input(learning_rate)
                X[r][:] = self.layers[0].f[2:]
            
            learning_rate *= 0.75;
        
        
                
                
    