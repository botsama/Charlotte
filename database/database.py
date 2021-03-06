from database import Member
from database import Message
from peewee import fn, JOIN, SQL


class Database(object):
    """An interface to the bot's database."""

    def add_member(self, member_id, username):
        """Adds a member to the database.

        Args:
            member_id: Unique discord id for that member.
            username: Membername and discriminator combination string.

        Returns:
            A member record.
        """
        member = Member.create(member_id=member_id, username=username)
        return member

    def member_exists(self, member_id):
        """Checks whether the chosen member is present in the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            Whether there is a member with that id in the database.
        """
        query = Member.select().where(Member.member_id == member_id)
        return query.exists()

    def get_member(self, member_id):
        """Gets a member from the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            A member record.
        """
        return Member.select().where(Member.member_id == member_id).first()

    def delete_member(self, member_id):
        """Deletes a member from the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            Whether the member was succesfully deleted.
        """
        return Member.delete().where(Member.member_id == member_id).execute()

    def add_message(self, message):
        """Adds a message to the database.

        Args:
            message: A discord message.

        Returns:
            A message record.
        """
        message = Message.create(content    = message.content,
                                 channel_id = message.channel_id,
                                 member     = message.author_id,
                                 date       = message.timestamp)
        return message

    def get_message(self, message_id):
        """Gets a message from the database.

        Args:
            message_id: The message's uid in the database.

        Returns:
            A message record.
        """
        return Message.select().where(Message.id == message_id).first()

    def get_messages_for_member(self, member_id):
        """Gets all messages for the chosen member.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            A list of message records.
        """
        return list(Message.select().where(Message.member == member_id))

    def delete_message(self, message_id):
        """Deletes a message from the database.

        Args:
            message_id: The message's uid in the database.

        Returns:
            Whether the message was succesfully deleted.
        """
        return Message.delete().where(Message.id == message_id).execute()

    def get_top_members_per_message_count(self, top_n=9):
        query = Member.select(Member, fn.Count(Message.id).alias('count')) \
                      .join(Message, JOIN.RIGHT_OUTER) \
                      .group_by(Member) \
                      .order_by(SQL('count').desc()) \
                      .limit(top_n)
        return list(query)

    def get_top_members_per_num_characters(self, top_n=20):
        query = Member.select(Member, fn.SUM(fn.LENGTH(Message.content)).alias('length')) \
                      .join(Message, JOIN.RIGHT_OUTER) \
                      .group_by(Member) \
                      .order_by(SQL('length').desc()) \
                      .limit(top_n)
        return list(query)
