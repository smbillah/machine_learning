'''
Created on Oct 4, 2012

@author: Masum
'''
from SupervisedLearning import SupervisedLearning
from Layer import Layer
from random import shuffle


class MLP_Fast(SupervisedLearning):
    '''
    classdocs
    '''
    
    def __init__(self, descriptor):
        #[4 2 3 2]
        self.layers= list()
        self.descriptor = descriptor;
        for num_neurons in self.descriptor[1:]:
            index = 0 ; 
            if not index:
                layer= Layer(index, num_neurons, None, self.descriptor[0])
            else:
                layer= Layer(index, num_neurons, self.layers[-1])
            index+=1
            self.layers.append(layer)
            
            
    def predict(self, input_vector):
        output_vector = input_vector[:]
        for layer in self.layers:
            output_vector = layer.predict(output_vector)            
        return output_vector
    
    def output_error_calculation(self, predicted_vector, target_vector):        
        if len(predicted_vector)!=len(target_vector):
            raise Exception("dimension mismatch")
        
        for i in range(len(predicted_vector)):
            e = (target_vector[i]-predicted_vector[i])*(predicted_vector[i])*(1-predicted_vector[i])
            self.layers[-1].e[i]=e            
        return self.layers[-1].e
    
    
    def gradient_descend(self, step_size, input_vector):
        feed = input_vector[:]
        
        for i in range(len(self.layers)):
            layer = self.layers[i]                        
            for j in range(layer.num_nurons):
                for k in range(len(layer.weight[j])):
                    layer.weight[j][k] = layer.weight[j][k] + step_size*layer.e[j]*feed[k]                
                layer.b[j] = layer.b[j] + step_size*layer.e[j]
            feed= layer.f
            
    
    def backpropagation(self):
        prev= self.layers[-1]
                
        for layer in reversed(self.layers[:-1]):                    
            for i in range(layer.num_nurons):
                e_i=0.0
                for j in range(prev.num_nurons):
                    e_i += prev.weight[j][i] * prev.e[j] * layer.f[i] * (1-layer.f[i])
                #e_i is available
                layer.e[i] = e_i            
            prev = layer
                
                
    def train(self, data_matrix, index,num_labels, learning_rate=0.1):                
        indices = index[:]
        for _ in range(500):            
            for i in indices:
                data = data_matrix[i]            
                predicted_vector =  self.predict(data[:-num_labels])                        
                self.output_error_calculation(predicted_vector, data[-num_labels:])
                self.backpropagation()                                    
                self.gradient_descend(learning_rate, data[:-num_labels])            
            learning_rate*= 0.997
                
                
                
                
        
        
            
    
    
    
        