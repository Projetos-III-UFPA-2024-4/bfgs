# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DBADDR = os.environ.get("DBADDR")
DBPORT = os.environ.get("DBPORT")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBTABLE = os.environ.get("DBTAABLE")