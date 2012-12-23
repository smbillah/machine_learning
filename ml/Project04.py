'''
Created on Sep 18, 2012

@author: masumadmin
'''
from Utility import read_data
from NFoldValidation import NFoldValidation
from PCA02 import PCA02
from MYSVGWriter import MYSVGWriter



if __name__ == '__main__':
    matrix, cat_cols, nom_cols = read_data('data/credit-a.arff')
    
    num_folds=3    
    nfold = NFoldValidation(matrix, cat_cols, nom_cols,num_folds)
    print 'total error in linear regression:', nfold.run()
    
    components=5
    pca02= PCA02(matrix, cat_cols, nom_cols, components)
    pca02.train()
        
    
    #plot3.svg
    svg =  MYSVGWriter(500, 500, 0, 0, 100, 100)
    start_position=4
    for i in range(len( pca02.eigenvalues)):        
        svg.rect(start_position, 0, 3, 27*pca02.eigenvalues[i] , 0x008080)
        start_position+= 4                

#    print pca02.eigenvalues
    svg.svgprint("plot3.svg")
    
    #plot4.svg
    svg =  MYSVGWriter(500, 500, -100, -100, 110, 110)
    start_position=10
    for i  in range(len( pca02.matrix)):        
        row = pca02.matrix[i]
        reduced= pca02.reduce(row[:len(row)], 2)
        x= 10**17*reduced[0]#to scale data
        y= 10**17*reduced[1]#to scale data
        
        if pca02.Y[i][0]:
            svg.dot(x ,y,1, 0x008080)
        else:
            svg.dot(x ,y,1, 0x800000)
    
    svg.svgprint("plot4.svg")    
        
        
    print 'done'
        
        
    
    