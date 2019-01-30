import os
import re
import yaml
import slack
import slack.chat
from aiosmtpd.handlers import Message
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class User(Base):
    __tablename__ = 'course_users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    email = Column(String)
    access_token = Column(String)
    raw = Column(String)
    slack_id = Column(String)

    def __repr__(self):
        return "<User(name='%s', slack_id='%s', email='%s', access_token='%s', raw='%s')>" % (self.name, self.slack_id, self.email, self.access_token, self.raw)


class MessageHandler(Message):
    def __init__(self, *args, **kargs):
        Message.__init__(self, *args, **kargs)

        engine = create_engine('TODO: ХАРДКОР!!!!')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_slack_by_email(session, email):
        try:
            user = self.session.query(User).filter_by(email=email).first()
            return user.slack_id, user.name
        except Exception as e:
            print('ERROR: some problem with ' + email + ' ' + str(e))

            
    def handle_message(self, message):
        """ This method will be called by aiosmtpd server when new mail will
            arrived.
        """
        
        slack_id, slack_name = self.get_slack_by_email(message['To'])
        
        self.send_to_slack(message.get_payload(), slack_id, slack_name)


    def send_to_slack(self, text, slack_id, name):
        print('sending to slack', text, slack_id, name)

        slack.api_token = 'TODO: ХАРДКОР!!!!'
        slack.chat.post_message(
            slack_id,
            text,
            username=name,
            icon_url=None
        )
