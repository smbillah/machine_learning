'''
Created on Sep 11, 2012

@author: masumadmin
'''
from SupervisedLearning import SupervisedLearning
from random import normalvariate, shuffle
from Utility import num_columns, num_rows, dot_prod, matrix_vector_prod,\
    vector_addition

class LinearRegression(SupervisedLearning):
    '''
    classdocs
    '''
    D= list() # pxq feature matrix
    Y = list() # pxr label matrix
    M = list() # rxq matrix to learn
    b = list() # r-dimensional vector
    

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
    def train(self, data_matrix, label_matrix):
        self.D = data_matrix
        self.Y = label_matrix
        
        num_feature_vectors = num_rows(self.D)
        num_features= num_columns(self.D)
        num_outputs = num_columns(self.Y)
        
        #initialize b
        for _ in range(num_outputs):
            self.b.append(0.0)
        
        #initialize M
        for _ in range(num_outputs):
            row = list()
            for _ in range(num_features):
                row.append(0.1*normalvariate(0,1))
            self.M.append(row)
        
        #maintain an array on indices of f.v which will be shuffled each time
        indices = list()
        for i in range(num_feature_vectors):
            indices.append(i)
        
        num_folds= 0.05
        for i in range(20):
            shuffle(indices)
            for i in range(num_feature_vectors):
                for j in range(num_outputs):
                    e = self.Y[indices[i]][j] - (dot_prod(self.D[indices[i]], self.M[j]) + self.b[j])
                    self.b[j] += num_folds*e
                    for components in range(num_features):
                        self.M[j][components] += num_folds*e*self.D[indices[i]][components]                         
            num_folds *= .85
    
    #end train method
        
    def predict(self, test_vector):
        return vector_addition(matrix_vector_prod(self.M, test_vector), self.b)
        
                