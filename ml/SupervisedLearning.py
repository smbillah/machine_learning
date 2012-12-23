'''
Created on Sep 11, 2012

@author: masumadmin
'''
from abc import ABCMeta, abstractmethod

class SupervisedLearning(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
#    @abstractmethod
#    def train(self, data_matrix, label_matrix):
#        pass
    
    @abstractmethod
    def train(self, data_matrix,indices, num_labels, learning_rate=0.1):
        pass
    
    @abstractmethod
    def predict(self, test_vector):
        pass

        