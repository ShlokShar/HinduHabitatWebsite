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
import flask
import os