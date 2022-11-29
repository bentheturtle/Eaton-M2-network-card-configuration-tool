#!/usr/bin/env python

import http.client
import json
import os
import urllib

#import MySQLdb
try:
    import ssl
    havessl = True
except ImportError:
    print ("error: no ssl support")
    havessl = False


class BiosClient:
    def host(self,uri):
        start = uri.find("://")
        if start == -1 : start = 0
        else : start = start + 3
        end = uri.find("/",start)
        if end == -1 : end = len(uri)
        return uri[start:end]

    def location(self,uri):
        start = uri.find("://")
        if start == -1 : start = 0
        else : start = start + 3
        end = uri.find("/",start)
        if end == -1 : end = len(uri)
        return uri[end:]

    def connect(self,uri):
        if uri[:5].lower() == "https":
            if havessl and hasattr(ssl, '_create_unverified_context'):
                return http.client.HTTPSConnection( host=self.host(uri), context=ssl._create_unverified_context() )
            return http.client.HTTPSConnection( host=self.host(uri) )
        return http.client.HTTPConnection( self.host(uri) )

    def http_request(self, request, uri, params, headers):
        try:
            if params == None : params = ""
            print("http_request " + request + " " + uri)
            C = self.connect(uri)
            C.request(request, self.location(uri), params, headers )
            response = C.getresponse()
            data = response.read()
            return ( "%i %s" % (response.status, response.reason), data )
        except BaseException as e:
            return ( "999 Communication problem '%s'" % (e.args[0]), "")

    def put(self, uri, params = None):
        return self.http_request( "PUT", uri, params, { } )

    def changePassword(self, username="", password="", newPassword=""):
        print("changePassword " + username + " " + password + " => " + newPassword)
        params = json.dumps({ 'user' :{'username' : username, 'current_pwd' : password, 'new_pwd': newPassword  }},  sort_keys=False,indent=0, separators=(',', ': '))
        result = self.put( os.environ["BIOS_URL"] + "/card/users/password", params )
        return result


