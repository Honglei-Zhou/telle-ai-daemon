import logging
from server.listener import Listener
from server.redis_instance import r
from database.config import thread_number
from chatbot.utils import handler
from chatbot.worker import ThreadPool
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    # client = Listener(r, ['telle_ai_chat', 'telle_ai_service'])
    # client.start()
    #
    # client.join()

    pool = ThreadPool(thread_number)

    while True:
        try:
            packed = r.blpop(['telle:queue:daemon'], 30)

            if not packed:
                continue

            message = json.loads(packed[1])

            print(message)

            func_name = message['type']
            if func_name in handler:
                pool.map(handler[func_name], [message])

        except Exception as e:
            logger.info(e)
            continue




