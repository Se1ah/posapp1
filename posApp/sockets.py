from nfc.clf import ContactlessFrontend
from django.http import HttpResponse
import json
from nfc.clf import RemoteTarget

from channels.generic.websocket import WebsocketConsumer


def runReader(client):
    print(client)
    working = 1
    clf = ContactlessFrontend('usb')  # Use the appropriate transport for your NFC reader
    target = clf.sense(RemoteTarget('106A'))
    if client is not None:
        client.send(json.dumps({'tag': 'started'}))
    while True:
        try:
            if target is not None:
                tag_data = target.sdd_res  # Replace with your desired tag data extraction logic
                if client is not None:
                    client.send(json.dumps({'tag': tag_data}))  # Send the tag information to the WebSocket
            target = clf.sense(RemoteTarget('106A'))
        except:
            print("error")


class NFCConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({'tag': "data"}))
        # clf = ContactlessFrontend('usb')  # Use the appropriate transport for your NFC reader
        # target = clf.sense(RemoteTarget('106A'))
        # print(target)
        # if target is None:
        #     self.send(json.dumps({'tag': "tag_data"}))
        # if target.sdd_res:
        #     tag_data = str(target)#.sdd_res
        #     self.send(json.dumps({'tag': tag_data}))
        print('runReader')
        #runReader(self)

    def receive(self, text_data=None, bytes_data=None):
        print("receive")
        clf = ContactlessFrontend('usb')  # Use the appropriate transport for your NFC reader
        target = clf.sense(RemoteTarget('106A'))
        if target is not None:
            self.send(json.dumps({'tag': str(target)}))
    def disconnect(self, close_code):
        pass
