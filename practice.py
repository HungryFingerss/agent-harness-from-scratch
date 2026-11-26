import shutil
import sqlite3
import tools

import os
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

shutil.copy("Chinook_Sqlite.sqlite", "Copy_Chinook_Sqlite.sqlite")

tools.connection = sqlite3.connect('Copy_Chinook_Sqlite.sqlite')
tools.cur = tools.connection.cursor()

print("practice_test===", tools.update_email(58, "manoj.new@gmail.com"))

print(groq_key[:4])
