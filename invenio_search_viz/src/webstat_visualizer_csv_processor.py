import pandas as pd
from urlparse import parse_qs
import gzip, cPickle, json, operator
#import re
import numpy as np

try:
    f = gzip.open('../data/query_dict.data','rb')
    print "\n....loading query data. Hold on.."
    print "\n time before loading: %s"%(pd.datetime.today().time().isoformat())
    pd_dict = pd.Series(cPickle.load(f))
    f.close()
    print "\n time after loading: %s\n\n"%(pd.datetime.today().time().isoformat())
except:
    quit("\nError: invalid path specified for data file!\nQuitting..")

weeks = [ 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] 
# right now declare no. of weeks manually because of sample data, 
# later on, store in some buffer or a file.

def perform_breakdown_query_units(q_parsed, f):
    """ Searches for combinations within parsed query
    For eg: after loading dictionary pd_dict, look up 
    1. parse_qs(pd_dict[3214343]) 
    2. parse_qs(pd_dict[10]) 
    3. parse_qs(pd_dict[6])
   
    Some of them might contain key 'f', some might contain keyword in key 'p'
    others might not contain anything, just plain 'p'
    
    @params q_parsed: parsed url arguments
    @params f: = 'keyword' -> field name to be passed to create_basic_search_units()
    """
    parsed_keys = q_parsed.keys()    
    p_tmp=[]; c_tmp=[]; f_tmp=[]; a_tmp=[]
    p_chk = False; f_chk= False #; flag = False
    # check for presence of url arguments 'p', 'c' and 'f'
    if 'p' in parsed_keys:
        p_tmp = q_parsed['p'] # query string
        p_chk = True
    if 'c' in parsed_keys:
        c_tmp = q_parsed['c'] # list of all collections present in url arguments
    if 'f' in parsed_keys:
        f_tmp = q_parsed['f'] # list of field names (if any)
        f_chk = True

    if p_chk:
        # check if a keyword is embedded in search query
        if len(p_tmp[0].split(':'))>1:
            # if ':' present, means a field is implicitly mentioned.
            p_breakdown = create_basic_search_units(None, p=p_tmp[0], f=f)

            for broken_args in p_breakdown:
                if broken_args[2] == 'author':
                    #flag = True # checked: author name implicitly included in query
                    if '*' in broken_args[1]:
                        # find position of arguments before/after astrix '*' 
                        # (sometimes included in author name)
                        pos_tmp = np.where(np.array(broken_args[1].split('*'))!='')[0]
                        #append the first argument in resultant array
                        a_tmp.append(broken_args[1].split('*')[pos_tmp[0]]) 
                    else:
                        # if in proper name format already, append already!
                        a_tmp.append(broken_args[1])
                else:
                    pass
        else:
            pass
    else:
        pass
    
    # next, check f_tmp for field names, if present, then check for 'author'
    if f_chk: 
        for i in f_tmp:
            if i=='author':
                a_tmp.append(p_tmp[0])
    # finally return everything, in 3 categorized lists
    return p_tmp, a_tmp, c_tmp

f = 'keyword' # declare argument for method: create_basic_search_units()

for week in weeks:
    collec_tmp = {}
    # read the respective csv files
    # Format: q_id, u_id, timestamp
    data = pd.read_csv('../data/csv/w_'+ str(week)+'.csv') #
    print "\n 1st 2 rows of data from csv of current week %d\n %s"%(week,data[:2]),"\n"
    print "Time: %s \n"%(pd.datetime.today().time().isoformat())
    #q_ids = data['q_id'].values

    #for q_id in q_ids:
    for elem in xrange(len(data)):
        q_id = data.get_value(elem, 'q_id')
        try:
            query_parsed =  parse_qs(pd_dict[q_id]) # dictionary with field as keys
            
            # categorize parameters, and return as lists
            p_tmp, a_tmp, c_tmp = perform_breakdown_query_units(query_parsed, f)
            
            # make list of tuples with (field, parameters)
            fields = [('c',c_tmp),('a',a_tmp),('p',p_tmp)]
            for field in fields:
                try:
                    # check if current field exists (as a dictionary)
                    collec_tmp[field[0]].keys()
                except:
                    # else make one
                    collec_tmp[field[0]]={}
                for element in field[1]:
                    if element in collec_tmp[field[0]].keys():
                        # parameter already present? ..increase count
                        collec_tmp[field[0]][element]+=1
                    else:
                        # else initialize count
                        collec_tmp[field[0]][element]=1
        except:
            pass
    for i in ['c','a','p']:
        print "\n..length of %s: %d\n"%(i,len(collec_tmp[i].keys()))
    try:
        f1 = open('../data/json/count_'+str(week)+'.json','w')
        f1.write(json.dumps(collec_tmp))
        f1.close()
    except:
        print "..couldnt dump json for week %d !!"%(week)
        print "..probably UTF-8 encoding error"
        pass

#print json.dumps(collec_tmp),"\n"
#dumpIt = unicode(str(collec_tmp), errors='ignore')
'''
# code to load dump 
f = open('count.json','r')
freq_data = json.loads(f)
f.close()
print freq_data.keys()

# and sort values
raw_input('press enter to print most searched author')
print sorted(freq_data['a'].iteritems(), key=operator.itemgetter(1)) 
'''

#next
# save in json with embedded keys (dict of dic) and 1st key as timestamp
