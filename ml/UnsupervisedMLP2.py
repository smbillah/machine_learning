'''
Created on Oct 17, 2012

@author: Masum
'''

from SupervisedLearning import SupervisedLearning
from Layer import Layer
from random import randrange, choice
from operator import mul
from math import exp


class UnsupervisedMLP2(SupervisedLearning):

    def __init__(self, descriptor, path, block_size):
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
        
        
        self.f_data = open(path,'r')
        self.block_size = block_size
    
    
    def get_y(self, index):
        self.f_data.seek(index * self.block_size , 0)
        r = self.f_data.read(self.block_size).strip().split(' ')
        y = [int(r[0]), int(r[1]), float(r[2]), float(r[3])]
        return y
    
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
        
            
    def output_error_calculation(self, target_vector, out_neuron_index, c):        
        #target: [a0 a1 #1 #2]
        j=2        
        predicted_vector = self.layers[-1].f
                      
#        for i in xrange(self.layers[-1].num_nurons):
        for i in range(out_neuron_index, out_neuron_index + c):                        
            e = (target_vector[j]-predicted_vector[i])*(predicted_vector[i])*(1-predicted_vector[i])
#            print 'e:', e
#            print 'prev e:',self.layers[-1].e[i]
            self.layers[-1].e[i] = e
            j +=1            
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
        for i in xrange(layer0.num_nurons):
            for j in xrange(layer1.num_nurons):
                layer0.f[i] += layer1.weight[j][i]*step_size*layer1.e[j]                
                    
    def backpropagation(self, out_neuron_index, c):
        prev= self.layers[-1]
        layer= self.layers[-2]
                                                
        for i in xrange(layer.num_nurons):
            e_i=0.0
            for j in range(out_neuron_index, out_neuron_index+c):                                             
                e_i += prev.weight[j][i] * prev.e[j] * layer.f[i] * (1-layer.f[i])
            layer.e[i] = e_i
        
        if len(self.layers)>2:
            prev= self.layers[-2]
            for layer in reversed(self.layers[1:-2]):                    
                for i in xrange(layer.num_nurons):
                    e_i=0.0
                    for j in xrange(prev.num_nurons):
                        e_i += prev.weight[j][i] * prev.e[j] * layer.f[i] * (1-layer.f[i])
                    #e_i is available
                    layer.e[i] = e_i            
                prev = layer
                
                
    def train(self, X, Y, k, learning_rate=0.8):                                 
        c = 2 #two output: # co-author, # citation
        feature = list()
        for _ in xrange(10): #10
            for _ in xrange(100000):# 10000000  10,000,000
                y = choice(Y)                
                feature[:]= X[y[0]][:]
                label = y
                out_neuron_index = 2*y[1]
                self.predict(feature);
                self.output_error_calculation(label, out_neuron_index, c)
                self.backpropagation(out_neuron_index, c)                                    
                self.gradient_descend(learning_rate)                                
                self.gradient_descend_input(learning_rate)
                X[y[0]][:] = self.layers[0].f[:]
            
            learning_rate *= 0.75;
           
                
                
    