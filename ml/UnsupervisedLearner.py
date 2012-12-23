'''
Created on Aug 31, 2012

@author: masumadmin
'''

from abc import ABCMeta, abstractmethod


class UnsupervisedLearner(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @abstractmethod
    def train(self, matrix):
        pass
    
    @abstractmethod
    def reduce(self, large_vector):
        pass
    
    @abstractmethod
    def expand(self, small_vector):
        pass
        