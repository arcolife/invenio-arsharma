## This file is part of Invenio.
## Copyright (C) 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

""" Search Query URL arguments processor """

#import dependencies
import pandas as pd
#from urlparse import parse_qs
import gzip, cPickle, re, json
#import numpy as np

try:
    from invenio.search_engine import create_basic_search_units
except:
    print '..Invenio not installed (properly). I quit!'
    quit()

f = gzip.open('../data/user_query_tuple.data','rb')
pd_tuple_list = pd.DataFrame.from_records(list(cPickle.load(f)))
f.close()

'''
f = gzip.open('../data/query_dict.data','rb')
pd_dict = pd.Series(cPickle.load(f))
f.close()
'''

#x = pd.DatetimeIndex(pd_tuple_list[2])
'''
x -> 
<class 'pandas.tseries.index.DatetimeIndex'>
[2012-06-01 00:00:01, ..., 2012-08-31 23:59:50]
Length: 1535896, Freq: None, Timezone: None

x.week -> 
array([22, 22, 22, ..., 35, 35, 35], dtype=int32)
'''

weeks = sorted(set(x.week))
print weeks
#[22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

index = 0
max_index = len(pd_tuple_list)
for week in weeks:
    f = open('../data/csv/w_'+ str(week)+'.csv', 'w')
    f.write('q_id,u_id,timestamp'+'\n')
    try:
        while(pd_tuple_list[2][index].week == week and index < max_index):
            f.write(str(pd_tuple_list[0][index]) + ',' 
                    + str(pd_tuple_list[1][index]) + ',' 
                    + pd_tuple_list[2][index].isoformat() + '\n')
            index+=1
        f.close()
        print week, index
    except:
        pass
'''
    for i in pd_tuple_list[2]:
    if i.week == week:
    tmp.append(i)
        else:
    break
'''
