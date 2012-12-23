#!/usr/bin/env python
'''
Created on Aug 31, 2012

@author: masumadmin
'''
from PCA import PCA
from Utility import read_data

if __name__ == '__main__':    
    pca= PCA(3)    
    pca.train(read_data('data/iris_sans_class.arff'))   
    
    print "ev1: ",pca.eigenvalues[0]
    print "ev2: ",pca.eigenvalues[1]
    print "ev3: ",pca.eigenvalues[2] 
    print pca.principal_components
    print pca.reduce([0.36158967923198376, -0.08226888783524387, 0.8565721047950943, 0.35884392603772075])
    print pca.expand([1.0, -7.091680853665849e-10, -1.7341683644644945e-13])
    print "OK"