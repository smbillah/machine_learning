'''
Created on Aug 31, 2012

@author: masumadmin

'''
from arff import UNKNOW_REAL, UNKNOW_CAT, Reader, NominalType
from collections import defaultdict
from sys import maxint 
from math import exp
from operator import mul, sub 
import re
from ctypes.test.test_array_in_pointer import Value




def build_author_index(path):
    regex= [r"^@attribute\s+(\w+)\s+(REAL|real)$", r"^@attribute\s+(\w+)\s+{(.+)}"]    
    desc=dict()
    
    with open(path, 'r') as f:
        line =  f.readline()        
        while not re.match(r'^@(RELATION|relation)\s+\w+', line):
            line =  f.readline()
                    
        line = f.readline()        
        while not line.strip():
            line =  f.readline()
        index=0
        while re.match(r'^@(attribute|ATTRIBUTE).*',line):                                                                                
            for i , reg in enumerate(regex):
                m= re.match(reg, line)
                if m:
                    if i==0: desc[index]= dict()                        
                    elif i==1:
                        cat_dict=dict()
                        cats = re.split(',', m.group(2))
                        for k, cat in enumerate(cats):
                            temp = [0 for _ in range(len(cats))]
                            temp[k]=1
                            cat_dict[cat] = temp
                        desc[index]= cat_dict
                                                                            
                    else:print 'problem'                        
                    break                                                                    
            line = f.readline()
            while not line.strip(): 
                line =  f.readline()                        
            index+=1
    print desc

def read_attributes(path):
    with open(path,'r') as f:
        reader = Reader(f)
        
        for _ in reader:
            pass
        for field in reader.fields:                        
            if isinstance(field,NominalType):
                print field.name, '=',field.enum
            else:
                print field.name, '=',field.type


def read_image_data(path):
    matrix = list()
    
    data_segment = False    
    with open(path, 'r') as f:
        for line in f:            
            if data_segment:
                if not line.strip():
                    continue
                values = line.split(",")
                column = list()
#                if len(values)!=9216:
#                    print 'critical error!'            
                for value in values:
                    column.append(float(value)/255.0)
                matrix.append(column)
                continue
            if line.startswith("@DATA"):
                data_segment=True
    return matrix

def read_action_data(path):
    matrix = list()
    actions ={'a':[1.0,0.0,0.0,0.0],'b':[0.0,1.0,0.0,0.0],'c': [0.0,0.0,1.0,0.0],'d': [0.0,0.0,0.0,1.0]}
    data_segment = False    
    with open(path, 'r') as f:
        for line in f:            
            if data_segment:                
                value = line.strip()
                if not value:
                    continue                
                matrix.append(actions[value][:])
                continue
            if line.startswith("@DATA"):
                data_segment=True
    return matrix


def read_data(path):
    matrix = list()
    categorical_cols= dict()    
    numeric_cols = dict()
    col_descriptor=list()
    
    with open(path,'r') as f:
        reader = Reader(f)
        
        for row in reader:
            if not row: continue
            column = list()
            
            for i in range(len(row)):
                c= row[i]
                column.append(c)
                        
                #handle numeric value
                if type(c) is float or type(c) is int:                                   
                    if i not in numeric_cols:
                        numeric_cols[i] = dict({'min':maxint, 'max':-maxint-1, 'avg':0, 'count':0}) 
                    
                    if c != UNKNOW_REAL:                     
                        numeric_cols[i]['avg'] += c 
                        numeric_cols[i]['count']+= 1 
                        if c < numeric_cols[i]['min']: numeric_cols[i]['min']=c
                        if c > numeric_cols[i]['max']: numeric_cols[i]['max']=c
                    
                #categorical value
                if type(c) is str:                
                    if i not in categorical_cols:
                        categorical_cols[i] = defaultdict(int)                
                    categorical_cols[i][c]+=1                     
    
            matrix.append(column)
        
        #read the meta-data. here is the format:
        # [{'header': {'start': 2, 'type': 1, 'length': 3}, 'enum': {'a': [1,0,0], 'b':[0,1,0], 'c': [0,0,1]}}]
        index=0
        length=0
        for field in reader.fields:                        
            if isinstance(field,NominalType):                
                length = len(field.enum)
                header = {'start': index, 'type': 1, 'length': length, 'name':field.name}
                enum=dict()
                for c in field.enum:                        
                    zero_vect= [0 for _ in range(length)]
                    zero_vect[field.enum.index(c)]=1
                    enum[c.strip()]=zero_vect
                col_descriptor.append({'header':header, 'enum':enum})
            
            else:                
                length=1
                header = {'start': index, 'type': 0, 'length': length, 'name':field.name}
                col_descriptor.append({'header':header})                                                
            index+=length
    
#    for c in col_descriptor: 
#        print c 
    
    #calculate average for nominal columns
    for index in numeric_cols:        
        if numeric_cols[index]['count']:
            numeric_cols[index]['avg'] /= (numeric_cols[index]['count']*1.0)                
#    print numeric_cols
    
    #find out missing value
    most_freq_value = dict()        
    for index in categorical_cols:
        if UNKNOW_CAT in categorical_cols[index]:
            del  categorical_cols[index][UNKNOW_CAT]
        #get the most likely value
        most_freq_value[index] = max(categorical_cols[index], key=categorical_cols[index].get)
#    print  most_freq_value
        
    
    #substitute the missing positions
#    print 'matrix:'                        
    flat_matrix=list()
    for row in matrix:                
        flat_row=list() 
        for i in range(len(row)):            
            if i in numeric_cols:
                if row[i] == UNKNOW_REAL:
                    row[i] = numeric_cols[i]['avg']
                denom= numeric_cols[i]['max']- numeric_cols[i]['min']
                if denom:
                    row[i] = (row[i]-numeric_cols[i]['min'])/(numeric_cols[i]['max']- numeric_cols[i]['min'])
                flat_row.append(row[i])
            
            if i in categorical_cols:
                if row[i] == UNKNOW_CAT:
                    row[i] = most_freq_value[i]                 
                flat_row.extend(col_descriptor[i]['enum'][row[i].strip("'")])
        flat_matrix.append(flat_row)
        #print flat_row
    #end
    
    #clean up
    del matrix
    del numeric_cols
    del categorical_cols
    
#    print col_descriptor[-1][0]['start']
#    print flat_matrix[0][ col_descriptor[-1][0]['start']:]
    
    return flat_matrix, col_descriptor        
    
def scalar_prod(scalar, vector):    
    result = list()
    for c in vector:
        result.append(c*scalar)
    return result


def dot_prod(v1, v2):
    return sum(map(mul, v1, v2))

def vector_addition(v1, v2):
    if len(v1)!=len(v2):
        raise Exception("Dimension mismatch")
    
    result = list()
    for i in range(len(v1)):
        result.append(v1[i]+v2[i])
    return result

def vector_subtraction(v1, v2):
    return map(sub, v1, v2)


def calculate_centroid(matrix):
    no_of_vectors= len(matrix)
    no_of_colomns= len(matrix[0])
    
    #initialize to zero
    mean_vector = list()
    for col in range(no_of_colomns):
        mean_vector.append(0)
    
    #sum up all colomns
    for row in matrix:
        for col in range(no_of_colomns):
            mean_vector[col] += row[col]
    
    #calculate average
    for col in range(no_of_colomns):
        mean_vector[col] /= 1.0*no_of_vectors    
    return mean_vector


def move_to_origin(matrix, centroid):
    no_of_vectors= len(matrix)
    no_of_colomns= len(matrix[0])
    
    #print mean_vector
    for row in range(no_of_vectors):
        for col in range(no_of_colomns):
            matrix[row][col] -= centroid[col]
        
    #print matrix 
    return    

def matrix_vector_prod(matrix, vector):
    no_of_vectors= len(matrix)
    no_of_colomns= len(matrix[0])
    if no_of_colomns != len(vector):
        raise Exception("Matrix and vector have incompatible dimensions")
    
    result= list()   
    for i in range(no_of_vectors):
        result.append(dot_prod(matrix[i], vector))    
    return result    

def num_rows(matrix):
    return len(matrix)

def num_columns(matrix):
    return len(matrix[0])

def num_dims(vector):
    return len(vector)

def transpose(matrix):
    return zip(*matrix)

def hamming_distance(source, target):
    if len(source) != len(target):
        raise Exception("incompatible dimensions")
    
    for i in range(len(source)):
        if source[i]!=target[i]: 
            return 1
    return 0

def logistic_function(x):
        return 1.0/(1.0 + exp(-x))
#unit test
#m= list()
#m.append([1,2,3])
#m.append([2,3,3])
##
##print num_rows(m)
##print num_columns(m)
#print transpose(m)
#print hamming_distance([0,1,0],[0,1,1])