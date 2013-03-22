# -*- coding: utf8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from datetime import datetime
import hashlib
import os

class BaseModel(object):
    def dict(self):
        """  
        Return object fields and values as a dictionary
        """
        return dict(filter(lambda (k, v): k[0] != '_', 
                           self.__dict__.iteritems()))

    def json(self):
        """  
        Return object fields and values as a JSON string
        """

        def extra_type_handler(obj):
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")

        return json.dumps(self.dict(), default=extra_type_handler)

    def __repr__(self):
        return self.json()

Base = declarative_base(cls=BaseModel)

class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True, autoincrement=True)
    moveid = Column(String(32), nullable=False)
    initiator = Column(String(32), nullable=False)
    adversary = Column(String(32), nullable=False)
    initiator_hold = Column(Integer, nullable=False)
    adversary_hold = Column(Integer)
    initiator_guess = Column(Integer, nullable=False)
    adversary_guess = Column(Integer)

    def __init__(self, initiator, adversary, initiator_hold, initiator_guess):
        self.moveid = hashlib.md5(os.urandom(24)).hexdigest()
        self.initiator = initiator
        self.adversary = adversary
        self.initiator_hold = initiator_hold
        self.initiator_guess = initiator_guess


engine = create_engine('sqlite:///spoof.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
move = Move('asdf', 'sadf', '2', '3')
session.add(move)
session.commit()

