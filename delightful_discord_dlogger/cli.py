"""
File Name: cli.py

Authors: Kyle Seidenthal

Date: 16-06-2021

Description: CLI for logging.

"""

from delightful_discord_dlogger import logger
import fire
import json

from delightful_discord_dlogger.logger import Logger

def log_message(title, description, json_config=None, content=None, fields=None,
                color=None, thumbnail_url=None, image_url=None, footer=None,
                new_embed=False):
    """Log a message to the webhook in embedded format.

        Args:
            title (str): The title of the message.
            description (str): The description of the message.

        Kwargs:
            json_config (str): Path to a webhook config file.  Uses default
                               config if not specified.
            content (str): Non-formatted text message.
            fields (str): Path to fields json with format:
                            {"fields":
                            [
                            {"name": "field_name",
                             "value": "value",
                             "inline": "true"}
                             ]
                             }
            color (int): Decimal representation of embed color or one of "red",
                         "orange", "yellow", "green", "cyan", "blue", "purple",
                         "pink".
            thumbnail_url (str): Url for thumbnail image.
            image_url (str): Url for message image.
            footer (Footer): A footer object for the message.
            new_embed (bool): If False the config will be edited with the new
                              info.  If True, a new embed will be appended for
                              this message. Non-specified values will be taken
                              from the last embed in the config.
        Returns: None

        """

    l = Logger(json_path=json_config)

    if fields is not None:
        with open(fields, 'r') as jsonfile:
            fs = json.load(jsonfile)

        fs = fs["fields"]

        fields = []
        for f in fs:
            new_f =  l.create_field(f["name"], f["value"], f["inline"])
            fields.append(new_f)
    else:
        fields = []

    if color == "red":
        color = logger.COLOR_RED
    elif color == "orange":
        color = logger.COLOR_ORANGE
    elif color == "yellow":
        color = logger.COLOR_YELLOW
    elif color == "green":
        color = logger.COLOR_GREEN
    elif color == "cyan":
        color = logger.COLOR_CYAN
    elif color == "blue":
        color = logger.COLOR_BLUE
    elif color == "purple":
        color = logger.COLOR_PURPLE
    elif color == "pink":
        color = logger.COLOR_PINK

    l.log_message(title, description, content=content, fields=fields,
                  color=color, thumbnail_url=thumbnail_url,
                  image_url=image_url, footer=footer, new_embed=new_embed)

def main():
    fire.Fire(log_message)

if __name__ == "__main__":

    main()


