import threading
import logging
import json
from chatbot.utils import handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.daemon = True
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)

    def work(self, item):
        if isinstance(item['data'], bytes):
            try:
                msg = item['data'].decode('utf-8')
                decode_msg = json.loads(msg)
                print(decode_msg)
                func_name = decode_msg['type']
                if func_name in handler:
                    handler[func_name](decode_msg)
                # if decode_msg['type'] in actions:
                #     print(decode_msg)
                #     actions[decode_msg['type']](decode_msg)
            except ValueError as e:
                raise ValueError("Error decoding msg to microservice: %s", str(e))

    def run(self):
        for item in self.pubsub.listen():
            try:
                self.work(item)
            except Exception as e:
                print(e)
                continue
