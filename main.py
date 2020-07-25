import logging
import pickle
import communication as comm
import health # don't remove

SERVICE_NAME = "health hub"

logging.basicConfig()
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

listener = comm.consumer.start_listenting()
handler = comm.station

for message in listener:
    logger.info("Received communication on topic %s", message.topic)
    try:
        request = pickle.loads(message.value)
    except pickle.UnpicklingError as err:
        logger.error("Failed to unpickle request: %s", err)

    handler.handle_request(request)