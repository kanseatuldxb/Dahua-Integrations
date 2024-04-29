#!/usr/bin/env python

import sys
import hashlib

import requests
from enum import Enum

if (sys.version_info > (3, 0)):
    unicode = str


class DahuaRpc(object):

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.s = requests.Session()
        self.session_id = None
        self.id = 0

    def request(self, method, params=None, object_id=None, extra=None, url=None):
        """Make a RPC request."""
        self.id += 1
        data = {'method': method, 'id': self.id}
        if params is not None:
            data['params'] = params
        if object_id:
            data['object'] = object_id
        if extra is not None:
            data.update(extra)
        if self.session_id:
            data['session'] = self.session_id
        if not url:
            url = "http://{}/RPC2".format(self.host)
        r = self.s.post(url, json=data)
        return r.json()

    def login(self):


        # login1: get session, realm & random for real login
        url = 'http://{}/RPC2_Login'.format(self.host)
        method = "global.login"
        params = {'userName': self.username,
                  'password': "",
                  'clientType': "Web3.0"}
        r = self.request(method=method, params=params, url=url)

        self.session_id = r['session']
        realm = r['params']['realm']
        random = r['params']['random']

        # Password encryption algorithm
        # Reversed from rpcCore.getAuthByType
        pwd_phrase = self.username + ":" + realm + ":" + self.password
        if isinstance(pwd_phrase, unicode):
            pwd_phrase = pwd_phrase.encode('utf-8')
        pwd_hash = hashlib.md5(pwd_phrase).hexdigest().upper()
        pass_phrase = self.username + ':' + random + ':' + pwd_hash
        if isinstance(pass_phrase, unicode):
            pass_phrase = pass_phrase.encode('utf-8')
        pass_hash = hashlib.md5(pass_phrase).hexdigest().upper()

        # login2: the real login
        params = {'userName': self.username,
                  'password': pass_hash,
                  'clientType': "Web3.0",
                  'authorityType': "Default",
                  'passwordType': "Default"}
        r = self.request(method=method, params=params, url=url)

        if r['result'] is False:
            raise LoginError(str(r))

    def get_product_def(self):
        method = "magicBox.getProductDefinition"

        params = {
            "name" : "Traffic"
        }
        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

    def keep_alive(self):
        params = {
            'timeout': 300,
            'active': False
        }

        method = "global.keepAlive"
        r = self.request(method=method, params=params)

        if r['result'] is True:
            return True
        else:
            raise RequestError(str(r))


    def do_find(self,object_id):
        method = "RecordFinder.doFind"
        object_id = object_id
        params = {
            "count" : 50000
        }
        r = self.request(object_id=object_id,method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))
        else:
            return r

    def reboot(self):
        """Reboot the device."""

        # Get object id
        method = "magicBox.factory.instance"
        params = ""
        r = self.request(method=method, params=params)
        object_id = r['result']

        # Reboot
        method = "magicBox.reboot"
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))
            
    def ListVehicle(self):
        """Reboot the device."""

        # Get object id
        method = "RecordFinder.factory.create"
        params = {"name": "TrafficList"}
        r = self.request(method=method, params=params)
        object_id = r['result']
        print(object_id)
        # Reboot
        method = "RecordFinder.startFind"
        params = {"condition": {"PlateType": "all", "PlateNumber": "**"}}
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordFinder.startFind",r)
        if r['result'] is False:
            raise RequestError(str(r))
            
        method = "RecordFinder.getQuerySize"
        params = ""
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordFinder.getQuerySize",r)
        if r['result'] is False:
            raise RequestError(str(r))
        
        method = "RecordFinder.doSeekFind"
        params = {"offset": 0, "count": 100}
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordFinder.doSeekFind",r)
        if r['result'] is False:
            raise RequestError(str(r))
            
    def AddVehicle(self):
        """Reboot the device."""

        # Get object id
        method = "RecordUpdater.factory.instance"
        params = {"name": "TrafficList"}
        r = self.request(method=method, params=params)
        object_id = r['result']
        print(object_id)
        # Reboot
        method = "RecordUpdater.insert"
        params = {"record":{"PlateNumber":"O-97196","PlateType":"white","MasterOfCar":"Roshan","BeginTime":"2024-04-29 00:00:00","CancelTime":"2024-04-29 23:59:59"}}
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordUpdater.insert",r)
        if r['result'] is False:
            raise RequestError(str(r))
            
    def RemoveVehicle(self):
        """Reboot the device."""

        # Get object id
        method = "RecordUpdater.factory.instance"
        params = {"name": "TrafficList"}
        r = self.request(method=method, params=params)
        object_id = r['result']
        print(object_id)
        # Reboot
        method = "RecordUpdater.remove"
        params ={"recno": 56, "object": object_id}
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordUpdater.remove",r)
        if r['result'] is False:
            raise RequestError(str(r))
            
    def UpdateVehicle(self):
        """Reboot the device."""

        # Get object id
        method = "RecordUpdater.factory.instance"
        params = {"name": "TrafficList"}
        r = self.request(method=method, params=params)
        object_id = r['result']
        print(object_id)
        # Reboot
        method = "RecordUpdater.update"
        params ={"recno": 55, "object": object_id,"record":{"PlateNumber":"A-11111","PlateType":"white","MasterOfCar":"Test 2","BeginTime":"2024-04-27 00:00:00","CancelTime":"2024-04-27 23:59:59"}}
        r = self.request(method=method, params=params, object_id=object_id)
        print("RecordUpdater.Update",r)
        if r['result'] is False:
            raise RequestError(str(r))

    def current_time(self):
        """Get the current time on the device."""

        method = "global.getCurrentTime"
        r = self.request(method=method)
        if r['result'] is False:
            raise RequestError(str(r))

        return r['params']['time']

    def ntp_sync(self, address, port, time_zone):
        """Synchronize time with NTP."""

        # Get object id
        method = "netApp.factory.instance"
        params = ""
        r = self.request(method=method, params=params)
        object_id = r['result']

        # NTP sync
        method = "netApp.adjustTimeWithNTP"
        params = {'Address': address, 'Port': port, 'TimeZone': time_zone}
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))


    def attach_event(self, event = []):
        method = "eventManager.attach"
        if(event is None):
            return
        params = {
            'codes' : [*event]
        }

        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

        return r['params']


    def listen_events(self, _callback= None):
        """ Listen for envents. Attach an event before using this function """
        url = "http://{host}/SubscribeNotify.cgi?sessionId={session}".format(host=self.host,session=self.session_id)
        response = self.s.get(url, stream= True)

        buffer = ""
        for chunk in response.iter_content(chunk_size=1):
            buffer += chunk.decode("utf-8")
            if (buffer.endswith('</script>') is True):
                if _callback:
                    _callback(buffer)
                buffer = ""



class LoginError(Exception):
    pass


class RequestError(Exception):
    pass

dahua = DahuaRpc(host="<Your IP>", username="admin", password="<Your Password>")
dahua.login()
print(dahua.current_time())
dahua.keep_alive()
dahua.AddVehicle()
dahua.UpdateVehicle()
dahua.RemoveVehicle()
dahua.ListVehicle()
