# DelightfulDiscordDlogger
Simple logging through discord webhooks.

# Installation
This package can be installed with pip:
`pip install git+https://github.com/KyleS22/DelightfulDiscordDlogger`

# Usage
There are two ways to use the package. 

Inside a python script:

```
from deligthtful_discord_dlogger.logger import Logger

l = Logger(json_path="path_to_config.json")

l.log_message(title, description,...)
```

or using the CLI `dddlog`:

```
Usage: dddlog TITLE DESCRIPTION <flags>
  optional flags:        --json_config | --content | --fields | --color |
                         --thumbnail_url | --image_url | --footer | --new_embed

For detailed information on this command, run:
  dddlog --help
  
```

# Config
You must set up a `config.json` for any bot you wish to use.  This is specified using the `--json_config` option.  It is possible to omit this flag if you set up a default config at the path `~/delightful_discord_logger/config.json`.

Config files have the following format.  Most fields are optional, but the `content` or `embed` field must be used at least once.  Also, the `webhook_url` field must be present, as it is what accesses the discord webhook.

```
{
  "webhook_url": "url_here,
  "username": "optional_username",
  "avatar_url": "optional_url",
  "content": "this is a message, optional only if you use an embed.",
  "embeds": [
    {
      "author": {
        "name": "My Bot",
        "url": "optional_url",
        "icon_url": "optional_icon_url"
      },
      "title": "Title",
      "url": "optional_url",
      "description": "This is the message content.",
      "color": 15258703,
      "fields": [
        {
          "name": "Field 1",
          "value": "THis is field 1",
          "inline": true
        },
        {
          "name": "Field 2",
          "value": "This is field 2",
          "inline": true
        }
      ],
      "thumbnail": {
        "url": "optional_thumbnail_url"
      },
      "image": {
        "url": "optional_image_url"
      },
      "footer": {
        "text": "optinal footer text",
        "icon_url": "optional_footer_image_url"
      }
    }
  ]
}
```

