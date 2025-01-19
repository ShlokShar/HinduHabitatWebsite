import json
import time
import uuid
import pytz
import requests
import re
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
import os
from dotenv import load_dotenv