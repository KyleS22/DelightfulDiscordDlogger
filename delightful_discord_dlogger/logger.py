"""
File Name: logger.py

Authors: Kyle Seidenthal

Date: 16-06-2021

Description: Logging using discord webhooks.

"""
import requests
import json
import os

DEFAULT_PATH = os.path.expanduser("~/delightful_discord_logger/config.json")

COLOR_RED = int("0xff0000", 16)
COLOR_ORANGE = int("0xff8400", 16)
COLOR_YELLOW = int("0xffd500", 16)
COLOR_GREEN = int("0x00ff00", 16)
COLOR_CYAN = int("0x00fff2", 16)
COLOR_BLUE = int("0x0000ff", 16)
COLOR_PURPLE = int("0x7300ff", 16)
COLOR_PINK = int("0xff00fb", 16)

class Logger(object):

    """A logging object containing the details for the webhook."""

    def __init__(self, json_path=None):
        """Create a logger.

        Kwargs:
            json_path (string): The path to the json file configuring the
                                webhook.  If left empty, the DEFAULT_PATH
                                will be used.

        Returns: A logger object.

        """

        if json_path is not None:
            self.json_path = json_path
        else:
            self.json_path = DEFAULT_PATH

        with open(self.json_path, 'r') as jsonfile:
            config = json.load(jsonfile)

        self.webhook_url =_get_config_val(config, "webhook_url")

        self.username = _get_config_val(config, "username")
        self.avatar_url = _get_config_val(config, "avatar_url")
        self.content = _get_config_val(config, "content")

        embeds = _get_config_val(config, "embeds")
        self.embeds = []

        for e in embeds:
            self.embeds.append(Embed(embed=e))

    def create_field(self, name, value, inline):
        """Create a new field for a message.

        Args:
            name (str): The name of the field.
            value (str): The text for the field.
            inline (bool): Whether the field should be inline.

        Returns: A new field object.

        """

        f = {"name": name,
             "value": value,
             "inline": inline}

        return Field(field=f)

    def create_footer(self, text, icon_url=None):
        """Create a new footer.

        Args:
            text (str): The text for the footer.

        Kwargs:
            icon_url (str): The url for an icon.

        Returns: A new footer.

        """
        f = {"text": text}

        if icon_url is not None:
            f["icon_url"] = icon_url

        return Footer(footer=f)

    def log_message(self, title, description, content=None, fields=[],
                    color=None, thumbnail_url=None, image_url=None,
                    footer=None, new_embed=False):
        """Log a message to the webhook in embedded format.

        Args:
            title (str): The title of the message.
            description (str): The description of the message.

        Kwargs:
            content (str): Non-formatted text message.
            fields (Field): Fields to add to the message.
            color (int): Decimal representation of embed color.
            thumbnail_url (str): Url for thumbnail image.
            image_url (str): Url for message image.
            footer (Footer): A footer object for the message.
            new_embed (bool): If False the config will be edited with the new
                              info.  If True, a new embed will be appended for
                              this message. Non-specified values will be taken
                              from the last embed in the config.
        Returns: None

        """

        e = self.embeds[-1]

        e.title = title
        e.description = description

        if new_embed:
            e.fields = fields
            e.thumbnail_url = thumbnail_url
            e.image_url = image_url
            e.footer = footer
            e.color = color
            self.embeds.append(e)
        else:

            e.fields += fields

            if thumbnail_url is not None:
                e.thumbnail_url = thumbnail_url

            if image_url is not None:
                e.image_url = image_url

            if footer is not None:
                e.footer = footer

            if color is not None:
                e.color = color

            self.embeds.pop()
            self.embeds.append(e)

        webhook_json = self._create_webhook_json()

        webhook_json["content"] = content

        if self.webhook_url is None:
            print("The config needs a webhook url!")
        else:
            r = requests.post(self.webhook_url, json=webhook_json)

    def _create_webhook_json(self):
        """Create the json for sending to webhook.
        Returns: Dict

        """

        data = {}

        if self.username is not None:
            data["username"] = self.username

        if self.avatar_url is not None:
            data["avatar_url"] = self.avatar_url

        if self.content is not None:
            data["content"] = self.content

        if self.embeds is not None:
            embeds = []
            for e in self.embeds:
                embeds.append(e.to_json())

            data["embeds"] = embeds

        return data


class Embed(object):

    """ Embed for discord webhook."""

    def __init__(self, embed=None):
        """Create an embed.

        Args:
            embeds (dict): A dict representing the embed. If None, embed is empty.

        Returns: An embed object.

        """
        self.author = Author(_get_config_val(embed, "author"))
        self.title = _get_config_val(embed, "title")
        self.url = _get_config_val(embed, "url")
        self.description = _get_config_val(embed, "description")
        self.color = _get_config_val(embed, "color")

        fields = _get_config_val(embed, "fields")
        self.fields = []

        if fields is not None:
            for f in fields:
                self.fields.append(Field(f))

        self.thumbnail_url = _get_config_val(_get_config_val(embed,
                                                             "thumbnail"),"url")

        self.image_url = _get_config_val(_get_config_val(embed, "image"), "url")

        self.footer = Footer(_get_config_val(embed, "footer"))

    def to_json(self):
        """Conbert the embed to json.
        Returns: Dict.

        """
        data = {}

        if self.author is not None:
            data["author"] = self.author.to_json()

        if self.title is not None:
            data["title"] = self.title

        if self.url is not None:
            data["url"] = self.url

        if self.description is not None:
            data["description"] = self.description

        if self.color is not None:
            data["color"] = self.color

        if self.fields is not None:
            data["fields"] = []
            for f in self.fields:
                data["fields"].append(f.to_json())

        if self.thumbnail_url is not None:
            data["thumbnail"] = {"url": self.thumbnail_url}

        if self.image_url is not None:
            data["image"] = {"url": self.image_url}

        if self.footer is not None:
            data["footer"] = self.footer.to_json()

        return data

class Author(object):

    """A webhook author. """

    def __init__(self, author=None):
        """Create a new author

        Args:
            author (dict): The author block config.

        Returns: An author

        """
        self.name = _get_config_val(author, "name")
        self.url = _get_config_val(author, "url")
        self.icon_url = _get_config_val(author, "icon_url")

    def to_json(self):
        """Convert Author to json.

        Returns: Author as jsoni dict.

        """
        data = {}

        if self.name is not None:
            data["name"] = self.name

        if self.url is not None:
            data["url"] = self.url

        if self.icon_url is not None:
            data["icon_url"] = self.icon_url

        return data

class Field(object):

    """Create a Field"""

    def __init__(self, field=None):
        """Create a field.

        Args:
            field (dict): The field config.

        Returns: A field.

        """
        self.name = _get_config_val(field, "name")
        self.value = _get_config_val(field, "value")
        self.inline = _get_config_val(field, "inline")

    def to_json(self):
        """Convert Field to json.

        Returns: Field as json dict.

        """
        data = {}

        if self.name is not None:
            data["name"] = self.name

        if self.value is not None:
            data["value"] = self.value

        if self.inline is not None:
            data["inline"] = self.inline

        return data

class Footer(object):

    """ Create a Footer"""

    def __init__(self, footer=None):
        """Create a footer.

        Kwargs:
            footer (dict): The footer config.

        Returns: A footer

        """
        self.text = _get_config_val(footer, "text")
        self.icon_url = _get_config_val(footer, "icon_url")


    def to_json(self):
        """Convert Footer to json.

        Returns: Footer as json dict.

        """
        data = {}

        if self.text is not None:
            data["text"] = self.text

        if self.icon_url is not None:
            data["icon_url"] = self.icon_url

        return data

def _get_config_val(config, config_key):
        """Helper for reading values from the config file.

        Args:
            config (dict): The config json as a dictionary.
            config_key (str): The key for the value to read.

        Returns: The value, or None

        """

        try:
            value = config[config_key]
        except:
            value = None

        return value


