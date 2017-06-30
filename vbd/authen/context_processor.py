'''
Created on Jun 30, 2017

@author: xieyanyang
'''

def fillup_username_to_session(request):
    return {'username': request.session.get('username', None)}