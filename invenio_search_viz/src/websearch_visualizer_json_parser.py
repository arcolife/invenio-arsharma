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

""" test cmd script to show frequency of fields from a particular week's json file"""

import json, operator, pprint

weeks = range(22,36)
print "Weeks for which data is available:\n",weeks,"\n"
week = int(raw_input('Enter the week #, for loading json: '))

try:
    f = open('../data/json/count_'+str(week)+'.json','r')
    freq_data = json.load(f)
    print freq_data.keys()
    f.close()
except:
    if week not in weeks:
        quit("Wrong week specified!\nQuitting..")
    else:
        quit("No JSON object could be decoded.\nMaybe due to a previous UTF-8 dump error through json.dumps().\nQuitting..")

# and sort values
raw_input('\npress enter to proceed... ')

fields = ['c','a','p']
choice = raw_input("\n----\n'a' - author\n\'c' - collection\n'p' - global searched terms\n-----\nEnter your choice(letter): ")
print type(choice)
try:
    sorted_data = sorted(freq_data[choice].iteritems(), key=operator.itemgetter(1))
    pprint.pprint(sorted_data)
except:
    print '\nwrong choice!\n'
    quit()
