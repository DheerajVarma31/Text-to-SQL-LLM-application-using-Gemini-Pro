from dotenv import load_dotenv
load_dotenv()## load all environment variables from .env file
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## configure AI key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
