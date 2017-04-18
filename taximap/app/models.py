from datetime import datetime, date, timedelta, time
import hashlib
import string
import random
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from collections import OrderedDict
from flask import current_app, request, url_for, jsonify
from flask_login import UserMixin, AnonymousUserMixin
from .utils.exceptions import ValidationError
from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.query import Bundle
from sqlalchemy.sql import func, select
from sqlalchemy import event, distinct, and_
from . import APP_STATIC
import os
from flask import json
import pickle
from sqlalchemy.exc import IntegrityError
from .utils.macros import generate_uuid
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, REAL, DATETIME


class Taxi(db.Model):
    __tablename__ = 'taxi'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    record_id = Column(Integer, primary_key=True)
    id = Column(Integer)
    longitude = Column(REAL)
    latitude = Column(REAL)
    speed = Column(REAL)
    direction = Column(REAL)
    datetime = Column(DATETIME)
    previous_status = Column(Integer)
    current_status = Column(Integer)
    status_diff = Column(Integer)

    def __repr__(self):
        rep = {
            'record_id': self.record_id,
            'id': self.id,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'speed': self.speed,
            'direction': self.direction,
            'datetime': self.datetime,
            'previous_status': self.previous_status,
            'current_status': self.current_status,
            'status_diff': self.status_diff
        }
        return json.dumps(rep)
