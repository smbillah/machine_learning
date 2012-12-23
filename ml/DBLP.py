'''
Created on Dec 5, 2012

@author: masumadmin
'''

from itertools import combinations, product
from collections import defaultdict
from random import randrange, choice
#    regex= [r"^@attribute\s+(\w+)\s+(REAL|real)$", r"^@attribute\s+(\w+)\s+{(.+)}"]    


def build_author_index(path):
    authors=defaultdict(int)
    
    total_count = 0
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            if not line: continue
            if line.startswith('#@'):
                raw_str = line[2:].strip()
                if not raw_str: continue
                raw_authors = raw_str.split(",")
                for a in raw_authors:                    
                    authors[a] +=1
                    total_count+=1            
    
    print '# of authors:', total_count
    return authors, total_count

#------------------------------------------------------
def save_author_index(path0, path_citation):
    authors, total_count = build_author_index(path0)
    
    with open(path_citation, 'w+') as f:
        f.write(str(total_count)+"\n")
        f.write(str(len(authors.keys()))+"\n")
        total_count=0
        for k in authors.keys():                        
            f.write(k +"\t"+ str(authors[k])+"\t"+str(total_count)+"\n")
            total_count+=1
    return


#------------------------------------------------------
def build_coauthor(path, authors):      
    coauthors=defaultdict(int)
    
    total_count = 0
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            if not line: continue
            if line.startswith('#@'):
                raw_str = line[2:].strip()
                if not raw_str: continue
                raw_authors = raw_str.split(",")
                if len(raw_authors)>1:                                                 
                    for c in combinations(raw_authors,2):                    
                        coauthors[(authors[c[0]],authors[c[1]])] +=1
                        total_count += 1
                   
    print '# of co-authors:', total_count
#    print coauthors         
    return coauthors, total_count
    


def save_coauthor_index(path, coauthors, total_count):
    with open(path, 'w+') as f:
        f.write(str(total_count)+"\n")                
        for k in coauthors.keys():            
            f.write(str(k[0]) +"\t"+ str(k[1]) +"\t"+ str(coauthors[k])+"\n")            
    return
                         
    
def coauthor_network():
    path = 'data/DBLP-citation.txt'
    path2 = 'data/DBLP-coauthor.txt'           
    authors, total_count = build_author_index(path)
    print 'index is done'
    save_author_index('data/author-id.txt', authors, total_count)
    coauthors, total_count = build_coauthor(path, authors)
    save_coauthor_index(path2, coauthors, total_count)

def build_citation_network(path, authors):
    paper_authors= dict()
    paper_papers= dict()
    citation_papers = list()
    is_valid, new_run =False, False
    curr_paper=0
    
#    i = 0
    with open(path, 'r') as f:
        for line in f:                        
            if not line.strip():
                if citation_papers and new_run and is_valid:
#                    i +=1
                    paper_papers[curr_paper] = citation_papers                                        

                    #reset everything
                    citation_papers=[]
                    new_run=False
                    is_valid=False
                    
#                    if i>10: 
#                        print paper_authors
#                        print '--------------'
#                        print paper_papers 
#                        break
#            
            elif line.startswith('#*'):
                new_run=True
            
            elif line.startswith('#@'):
                raw_str = line[2:].strip()
                if raw_str: 
                    raw_authors = raw_str.split(",")
                    is_valid=True                
                                    
            elif line.startswith('#year'):
                pass
            elif line.startswith('#conf'):
                pass
            elif line.startswith('#citation'):
                pass
            elif line.startswith('#index'):
                if is_valid and new_run:
                    curr_paper = int(line[6:])
                    writers = list()
                    for author in raw_authors:
                        writers.append(authors[author])
                    paper_authors[curr_paper]=writers
                
            elif line.startswith('#arnetid'):
                pass
            elif line.startswith('#%'):
                if new_run and is_valid:
                    citation_papers.append(int(line[2:]))
            elif line.startswith('#!'):
                pass            
            else:
                print 'how come!', line
    
    return paper_authors, paper_papers

def write_citation_network(path, authors, paper_authors, paper_papers):
    citations=defaultdict(int)
    for paper in paper_papers.keys():
        writers= paper_authors[paper]
        citing_papers = paper_papers[paper]        
        
        for citing_paper in citing_papers:
#            print 'paper', paper,'writers:', writers
#            print 'citing writers:', citing_paper, paper_authors[citing_paper]         
            if citing_paper in paper_authors:
                for prod in product(writers, paper_authors[citing_paper]):
                    citations[prod]+=1
                
    with open(path, 'w+') as f:        
        f.write(str(len(citations.keys()))+"\n")        
        for k in citations.keys():
            f.write(str(k[0]) +"\t"+ str(k[1]) +"\t"+ str(citations[k])+"\n")
    #clean-up
    citations=[]
    return                        
        
                
def read_author_name_index(path):
    total_count,i = 0, -1
    authors=dict()
    
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue
            if i==1: 
                total_count= int(line)
                continue
            tokens = line.strip().split('\t')
            authors[tokens[0]]= int(tokens[2])            
#            if i>10:break
#    print authors
    return authors, total_count

def read_author_id_index(path):
    total_count,i = 0, -1
    authors=dict()
    
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue
            if i==1: 
                total_count= int(line)
                continue
            tokens = line.strip().split('\t')
            authors[int(tokens[2])]= int(tokens[1])            
#            if i>10:break
#    print authors
    return authors, total_count

def profiling(path):
    total_count,i = 0, -1
    authors=defaultdict(int)
    
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue
            if i==1: 
                total_count= int(line)
                continue
            tokens = line.strip().split('\t')
            authors[int(tokens[1])] +=1             
#            if i>10:break
    for k in authors:
        print str(k), ' ', str(authors[k])

def profile_coauth(path_coauthor):
    i=-1
    c=defaultdict(int)
    with open(path_coauthor, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue            
            toks = line.strip().split('\t')
            t = int(toks[2])
            c[t]+=1
    
    
    for k in c:
        print str(k), ' ', str(c[k])
    

def profile_merge(path_merge):
    i=0
    num = 33367
    c=defaultdict(int)
    w=[]
    with open(path_merge, 'r') as f:
        for line in f.xreadlines():                                    
            toks = line.strip().split('\t')
            t = int(toks[0])
            t1 = int(toks[1])
            c[t]+=1
            c[t1]+=1
            if t not in w:
                w.append(t)
            if t1 not in w:
                w.append(t1)
            
            if i>300:
                break
            i+=1
    
    s=c.keys()
#    for k in c:
#        print str(k), ' ', str(c[k])
    i=0
    x=[]
    with open('data/choice.txt', 'w+') as f:
        for b in w:
#        for i in range(100):        
#            b = choice(s)
#            while b in x:
#                b = choice(s)
#            x.append(b)            
            f.write(str(b)+'\n')            
        

    print len(w)

def profile_merge_random(path_merge, path_merge2):
    i=0    
    a=dict()
    with open(path_merge, 'r') as f:
        for line in f.xreadlines():
            toks = line.strip().split('\t')
            if toks[0] not in a:
                a[toks[0]] = i
                i+=1
            
            if toks[1] not in a:
                a[toks[1]]=i
                i+=1
                               
    with open(path_merge2, 'w+') as f:
        for k in a:
            f.write(k+'\t'+str(a[k])+"\n")

    print 'pairs:', str(i)


def merge(path_coauthor, path_citation, path_merge, authors):
    citation=dict()
    
    total_count,i = 0, -1
    with open(path_citation, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue            
            toks = line.split('\t')
            citation[(int(toks[0]), int(toks[1]))]= int(toks[2])            
            
    f_all = open(path_merge,'w+')
    
    i=-1
    with open(path_coauthor, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue            
            toks = line.strip().split('\t')
            t = (int(toks[0]), int(toks[1]))
            t1 = (int(toks[1]), int(toks[0]))
            if t in citation:
                total_count+=1
                f_all.write(toks[0]+'\t'+toks[1]+'\t'+str( int(toks[2])*1.0/authors[t[0]])+'\t'+str(citation[t])+'\n')
                del citation[t]
            
            elif t1 in citation:
                total_count+=1
                f_all.write(toks[1]+'\t'+toks[0]+'\t'+str( int(toks[2])*1.0/authors[t1[0]])+'\t'+str(citation[t1])+'\n')
                del citation[t1]
            else:
                f_all.write(toks[0]+'\t'+toks[1]+'\t'+str( int(toks[2])*1.0/authors[int(toks[0])])+'\t'+'0'+'\n')
    
    for t in citation:
        f_all.write(str(t[0])+'\t'+str(t[1])+'\t'+'0'+'\t'+ str(citation[t])+'\n')
    
    f_all.close()
#            citation[(int(toks[0]), int(toks[1]))]= int(toks[2])
#            if i>10:break
    print total_count
#    return citation, total_count


def merge2(path_coauthor, path_citation, path_merge, authors):
    citation=dict()
    
    total_count,i = 0, -1
    with open(path_citation, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue            
            toks = line.split('\t')
            citation[(int(toks[0]), int(toks[1]))]= int(toks[2])            
            
    f_all = open(path_merge,'w+')
    
    i=-1
    with open(path_coauthor, 'r') as f:
        for line in f.xreadlines():            
            i += 1            
            if i==0: continue            
            toks = line.strip().split('\t')
            t = (int(toks[0]), int(toks[1]))
            t1 = (int(toks[1]), int(toks[0]))
            if t in citation:
                if int(toks[2])>3 and citation[t]>3:
                    total_count+=1
#                    f_all.write(toks[0]+'\t'+toks[1]+'\t'+str( int(toks[2])*1.0/authors[t[0]])+'\t'+str(citation[t])+'\n')
                    f_all.write(toks[0]+'\t'+toks[1]+'\t'+toks[2]+'\t'+str(citation[t])+'\n')
#                del citation[t]
            
            elif t1 in citation:
                if int(toks[2])>3 and citation[t1]>3:
                    total_count+=1
#                    f_all.write(toks[1]+'\t'+toks[0]+'\t'+str( int(toks[2])*1.0/authors[t1[0]])+'\t'+str(citation[t1])+'\n')
                    f_all.write(toks[1]+'\t'+toks[0]+'\t'+toks[2]+'\t'+str(citation[t1])+'\n')
#                del citation[t1]
            else:
                pass
#                f_all.write(toks[0]+'\t'+toks[1]+'\t'+str( int(toks[2])*1.0/authors[int(toks[0])])+'\t'+'0'+'\n')
    
#    for t in citation:
#        f_all.write(str(t[0])+'\t'+str(t[1])+'\t'+'0'+'\t'+ str(citation[t])+'\n')
    
    f_all.close()
#            citation[(int(toks[0]), int(toks[1]))]= int(toks[2])
#            if i>10:break
    print total_count
#    return citation, total_count


def merge3(path_data, path_merge, authors):
            
    f_all = open(path_merge,'w+')
    
    with open(path_data, 'r') as f:
        for line in f.xreadlines():                                    
            toks = line.strip().split('\t')
            t = (int(toks[0]), int(toks[1]))            
            f_all.write(toks[0]+'\t'+toks[1]+'\t'+str( int(toks[2])*1.0/authors[t[0]])+'\t'+toks[3]+'\n')            
    
    f_all.close()
#            citation[(int(toks[0]), int(toks[1]))]= int(toks[2])
#            if i>10:break
    
#    return citation, total_count


def read_processed_data(path):
    i=0
    Y=list()
    min= 1000000
    max= -1
        
    
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            i += 1                                    
            toks = line.strip().split('\t')
            t = [int(toks[0]), int(toks[1]), float(toks[2]), int(toks[3])]            
            if t[3]< min: min= t[3]
            if t[3]> max: max= t[3]    
#            Y.append(t)
    
    f_all= open('data/train300.txt', 'wb+')        
    
    i=0
    with open(path, 'r') as f:
        for line in f.xreadlines():            
            i += 1                                    
            toks = line.strip().split('\t')
            t = [int(toks[0]), int(toks[1]), float(toks[2]), int(toks[3])]            
            t[3]= 1.0*(t[3]-min)/(max-min)
            f_all.write('{0:0>8d} {1:0>8d} {2:.5f} {3:.5f}\n'.format(t[0], t[1],t[2],t[3]))                
    
    f_all.close()
    print 'total reading', i
    return i

#action list
#coauthor_network()
path0 = 'data/DBLP-citation.txt'
path= 'data/author-id2.txt'
path_coauthor= 'data/coauthors.txt'
path_citation= 'data/citations.txt'
path_data= 'data/merge42.txt'
path_merge2= 'data/merge-author.txt'
path_merge= 'data/merge422.txt'
path_choice= 'data/choice.txt'

#profiling(path)
#profile_coauth(path_coauthor)
#save_author_index(path0, path_coauthor)
#authors, total_count= read_author_name_index(path)
#paper_authors, paper_papers= build_citation_network(path0, authors)
#write_citation_network(path_citation, authors, paper_authors, paper_papers)
#authors, total_count= read_author_id_index(path)#useful
#merge2(path_coauthor, path_citation, path_merge, authors)
#profile_merge(path_merge)
#profile_merge_random(path_merge, path_merge2)
#merge3(path_data, path_merge, authors)
#read_processed_data(path_merge)
#print '@done'