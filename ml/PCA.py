'''
Created on Aug 31, 2012

@author: masumadmin
'''
from  UnsupervisedLearner import UnsupervisedLearner 
import random
from math import sqrt 
from Utility import * #@UnusedWildImport



class PCA(UnsupervisedLearner):
    '''
    classdocs
    '''
    
    #local variables
    components=1
    centroid = list()
    eigenvalues = list()
    principal_components = list()    
    matrix = list()

    def __init__(self, components):
        '''
        Constructor
        '''        
        self.k= components

        
    def train(self, matrix):
        self.matrix = matrix
        self.centroid= calculate_centroid(self.matrix)
        move_to_origin(self.matrix, self.centroid)
        
        for _ in range(self.k):        
            pc= self.first_principal_component()
            self.principal_components.append(pc)
            eigen_value = self.remove_component(pc)
            self.eigenvalues.append(eigen_value)
        
    
    def reduce(self, large_vector):
        return matrix_vector_prod(self.principal_components, large_vector)
    
    
    def expand(self, small_vector):
        return matrix_vector_prod(transpose(self.principal_components), small_vector)
            
    def set_k(self, components):
        self.k=components        

    def first_principal_component(self):    
        no_of_colomns= len(self.matrix[0])
        
        p, zero_vect = list(), list()
        for _ in range(no_of_colomns):
            p.append(random.random())
            zero_vect.append(0.0)
        
        #normalize p
        p = scalar_prod(1/sqrt(dot_prod(p, p)), p)                
        m=0.0    
        for i in range(199):
            t=zero_vect;
            for row in self.matrix:
                t = vector_addition(t, scalar_prod(dot_prod(row, p), row))
            d= sqrt(dot_prod(t, t))
            p = scalar_prod(1/d, t)
            
            if i < 6 or (d-m) > 0.0001: m = d
            else: break         
        return p
       
    def remove_component(self, pc):
        no_of_colomns= len(self.matrix[0])
        b=0
        for row in self.matrix:
            b += dot_prod(row, row)
        
        for i in  range(len(self.matrix)):
            d= dot_prod(pc, self.matrix[i])
            self.matrix[i] = vector_addition(self.matrix[i], scalar_prod(-1*d, pc))
        
        a=0
        for row in self.matrix:
            a += dot_prod(row, row)
        
        return (b-a)/no_of_colomns
        
   
