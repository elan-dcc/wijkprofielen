from pathlib import Path
import json
from datetime import date
import locale
from enum import Enum

class Language(Enum):  
    NL = 'nl'
    EN = 'en'

localedic= {Language.NL.value: 'nl_NL.UTF8', Language.EN.value: 'en_US.UTF8'}

localedir = str(Path(__file__).resolve().parent.parent / "locales")
dictionary = {}
lang = Language.NL

def change_language(language=lang):
    global dictionary
    global lang
    
    lang = language    
    language = language + '.json'
    
    # I assume people only change the language once. Otherwise, it would
    # be better to open all dictionaries in the parent scope!
    with open(localedir + '\\' + language, 'r',  encoding='utf8') as f:
        dictionary = json.load(f)
    
def translate(key):
    value = dictionary.get(key)
    # fallback
    if not value:
        value = key
    return value

def translate_list(mylist):
    return [translate(value) for value in mylist]

def translate_date(year, month, day):
    d = date(year, month, day)
    locale.setlocale(locale.LC_ALL, localedic[lang])
    return d.strftime("%B %Y")
    


    

