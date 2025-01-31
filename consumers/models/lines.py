"""Contains functionality related to Lines"""
import json
import logging

from models import Line


logger = logging.getLogger(__name__)


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.red_line = Line("red")
        self.green_line = Line("green")
        self.blue_line = Line("blue")

    def process_message(self, message):
        """Processes a station message"""
        # print(f"============={message.topic()}")
        if "arrival.station" in message.topic():
            value = message.value()
            if message.topic() == "org.chicago.cta.stations.table.v1":
                
                # logger.info("Message topic table")
                value = json.loads(value)
                print(f"============={value}")
            if value["line"] == "green":
                self.green_line.process_message(message)
                # logger.info("Load green line")
            elif value["line"] == "red":
                self.red_line.process_message(message)
                # logger.info("Load red line")
            elif value["line"] == "blue":
                self.blue_line.process_message(message)
                # logger.info("Load blue line")
            else:
                logger.debug("discarding unknown line msg %s", value["line"])
        elif "TURNSTILE_SUMMARY" == message.topic():
            self.green_line.process_message(message)
            self.red_line.process_message(message)
            self.blue_line.process_message(message)
        else:
            logger.info("ignoring non-lines message %s", message.topic())
