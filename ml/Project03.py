'''
Created on Sep 11, 2012

@author: masumadmin
'''

from Utility import read_data
from LinearRegression import LinearRegression

if __name__ == '__main__':    
    lr= LinearRegression()    
    lr.train(read_data('data/linear_in.arff'), read_data('data/linear_out.arff'))   
    y = lr.predict([1,1,1])
    print "y1: ", y[0]
    print "y2: ", y[1]
    
    