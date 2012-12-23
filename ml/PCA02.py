'''
Created on Sep 20, 2012

@author: masumadmin
'''

from  UnsupervisedLearner import UnsupervisedLearner 
import random
from math import sqrt 
from Utility import * #@UnusedWildImport
import math




class PCA02(UnsupervisedLearner):
    '''
    classdocs
    '''
    
    #local variables
    matrix= list() # pxq feature matrix
    Y = list() # pxr label matrix
    
    cat_cols, nom_cols = None, None
    
    components=1
    centroid = list()
    eigenvalues = list()
    principal_components = list()    
    matrix = list()

    def __init__(self, data_matrix, cat_cols, nom_cols,components):
        '''
        Constructor
        '''        
        self.k= components
        
           
        self.cat_cols = cat_cols
        self.nom_cols = nom_cols        
        
        
        for row in data_matrix:
            new_row = list()
            for i in range(len(row)-1):
                if i in self.nom_cols:
                    new_row.append(row[i])
                if i in self.cat_cols:
                    for v in row[i]:
                        new_row.append(v)
            self.matrix.append(new_row)
            self.Y.append(row[-1])
        
#        print self.matrix[0]

        
    def train(self):
    
        self.centroid= calculate_centroid(self.matrix)
        move_to_origin(self.matrix, self.centroid)
        
        for _ in range(self.k):        
            pc= self.first_principal_component()
            self.principal_components.append(pc)
            eigen_value = self.remove_component(pc)
            self.eigenvalues.append(eigen_value)
        
    
    
    def reduce(self, large_vector, k=2):
        return matrix_vector_prod(self.principal_components, large_vector)[:k]
    
    
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
        
        return math.sqrt( (b-a)/no_of_colomns)
        
   
