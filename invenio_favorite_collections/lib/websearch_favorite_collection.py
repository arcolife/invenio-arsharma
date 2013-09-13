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

"""Favorite Collections feature"""

from invenio.dbquery import run_sql as res
from invenio.webuser import \
    getUid, page_not_authorized, \
    isGuestUser, collect_user_info, \
    isUserSubmitter, username_exists_p, \
    isUserAdmin, get_email, \
    get_session, get_user_preferences, get_user_info

from invenio.urlutils import redirect_to_url, make_canonical_urlargd, drop_default_urlargd
#import invenio.websearchadminlib as wa
#from websearch_webcoll import Collections
#from pexpect import spawn

#favorite_collection = res("SELECT * FROM fav_collec")
#user_info = collect_user_info(req)

def _get(req):
    uid = getUid(req)
    
def perform_add_new_favorite_from_collection(uID, collID, req):
    """Add collection to favorite(s).
    
    @param uID: User ID who wants to add the collection
    @param collID: collection ID for adding to favorites
    @param req: returned object from AJAX request
    """
    if isGuestUser(uID):
        return "login first!"
    else:
        try:
            favorites = res("INSERT INTO into fav_collec values(%d,%d)"%(uID,collID));
            return favorites
        except:
            return ''

def perform_delete_favorite_from_collection(uID, collID, req):
    """Delete a collection from favorite(s).
    @param uID: User ID who wants to add the collection
    @param collID: collection ID for adding to favorites
    @param req: returned object from AJAX request
    """
    if isGuestUser(uID):
        return "..login to access this feature!"
    else:
        try:
            favorites = res("DELETE FROM fav_collec WHERE id_user=%d AND id_collection=%d"%(uID, collID))
            return "Successfully deleted the requested collection from list of favorites!"
        except:
            return ''

def perform_calculate_favorites(uID):
    """Talks to DB for extracting favorites for a user
    
    @param uID: User ID of currently logged in user
    """
    if isGuestUser(uID):
        return "..login to access this feature!"
    else:
        try:
            id_favs = res("SELECT id_collection FROM fav_collec WHERE id_user=%d"%(uID))
            favorites = []
            for id_fav in id_favs:
                favorites.append(res("SELECT name FROM collection WHERE id=%d"%(id_fav[0]))[0][0])
            return favorites
        except:
            return ''
