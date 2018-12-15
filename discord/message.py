import json


class Message(object):
    """A discord message as described here:
    https://discordapp.com/developers/docs/resources/channel#message-object
    A message can be either received through the gateway websocket or sent to the REST API.

    Args:
        content: The contents of the message.
        channel_id: The id of the channel the message will be written to.
        user: The unique id of the user who sent/sends the message.
        username: The current username#discriminator combo for that user.
        timestamp: The time of the message.
        attachment: The file that will be attached to the message.
    """

    def __init__(self, content, channel_id, user, username, timestamp=None, attachment=None):
        if attachment != None:
            raise NotImplementedError("Can't add attachments to messages yet.")
        self.content    = content
        self.channel_id = channel_id
        self.user       = user
        self.username   = username
        self.attachment = attachment

    @staticmethod
    def from_payload(payload):
        """Creates a Message from a Payload by extracting relevant items.

        Args:
            payload: A MESSAGE_CREATE payload.

        Returns:
            A message.
        """
        data = payload.data
        return Message(content    = data["content"],
                       channel_id = data["channel_id"],
                       user       = data["author"]["id"],
                       username   = data["author"]["username"] + "#" + data["author"]["discriminator"],
                       timestamp  = data["timestamp"])

    def to_json(self):
        """Encodes the message in json in a format recognized by discord's APIs.

        Returns:
            A json string.
        """
        payload =  {
            "content": self.content,
            "tts": False,
            "file": self.attachment,
            "embed": None,
            "payload_json": None
        }
        return json.dumps(payload)
