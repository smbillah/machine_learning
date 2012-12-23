'''
Created on Sep 20, 2012

@author: masumadmin
'''
from SupervisedLearning import SupervisedLearning
from random import normalvariate, shuffle, choice
from Utility import num_columns, num_rows, dot_prod, matrix_vector_prod,\
    vector_addition, scalar_prod, hamming_distance


class NFoldValidation(SupervisedLearning):
    '''
    classdocs
    '''
    D= list() # pxq feature matrix
    Y = list() # pxr label matrix
    M = list() # rxq matrix to learn
    b = list() # r-dimensional vector
    num_folds=2
    cat_cols, nom_cols = None, None
    

    def __init__(self, data_matrix, cat_cols, nom_cols, num_folds):
        '''
        Constructor
        '''
        self.D = data_matrix        
        self.cat_cols = cat_cols
        self.nom_cols = nom_cols        
        self.n= num_folds
        
        self.indices = list()
        for i in range(len(self.D)):
            self.indices.append(i)
        shuffle(self.indices)
        
    
    def run(self):
        total_error=0
        for i in range(self.n):
            test= list()
            begin = i* len(self.indices)/self.n
            end = (i+1)* len(self.indices)/self.n
            
            for j in range(begin, end):
                test.append(self.indices[j])
            
            training=list(set(self.indices) - set(test))
            shuffle(training)
            self.train( training)
            total_error+= self.predict(test)
        return total_error
    
        
    
    def train(self, indices):        
        num_outputs = len(self.D[0][-1])        
        num_features= num_columns(self.D)-1
        
        #initialize b
        self.b=[]
        for i in range(num_outputs):
            self.b.append(0.0)

        #initialize M
        self.M=[]
        for _ in range(num_outputs):
            row = list()
            for i in range(num_features):
                if i in self.nom_cols:
                    row.append(0.1*normalvariate(0,1))
                if i in self.cat_cols:
                    row.append( self.cat_cols[i][choice(self.cat_cols[i].keys())])                
            self.M.append(row)        
        #print 'before:', self.M
            
        #maintain an array on indices of f.v which will be shuffled each time
        
        
        num_folds= 0.05
        for i in range(10):            
            for i in indices:
                for j in range(num_outputs):
                    
                    predicted = 0
                    for components in range(num_features):                            
                        if components in self.nom_cols:
                            predicted += self.D[i][components]*self.M[j][components]
                        if components in self.cat_cols:
                            predicted += dot_prod(self.D[i][components], self.M[j][components])
                    predicted += self.b[j]
                    e = self.D[i][-1][j] - predicted
                    self.b[j] += num_folds*e
                    
                    for components in range(num_features):                            
                        if components in self.nom_cols:
                            self.M[j][components] += num_folds*e*self.D[i][components]                            
                        if components in self.cat_cols:
                            self.M[j][components] =  vector_addition(self.M[j][components], scalar_prod(num_folds*e, self.D[i][components]))                                             
            num_folds *= .85        
#        print 'after:', self.M
    
    #end train method
        
    def predict(self, test_data):        
        result= list()
        quantized =[0,0]
        sse=0 
        for index in test_data:
            test_vector= self.D[index]
            for i in range(len(self.M)):            
                predicted = 0
                for components in range(len(self.M[i])):                            
                    if components in self.nom_cols:
                        predicted += self.M[i][components]*test_vector[components]
                    if components in self.cat_cols:
                        predicted += dot_prod(self.M[i][components], test_vector[components])
                predicted += self.b[i]
                result.append(predicted)            
            quantized[result.index(max(result))]=1
            sse+= hamming_distance(quantized, test_vector[-1])**2
            result = []
            quantized =[0,0]
        return sse
        
                