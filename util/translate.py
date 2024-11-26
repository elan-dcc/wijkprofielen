from pathlib import Path
import json
from datetime import date
from enum import Enum

class Language(Enum):  
    NL = 'nl'
    EN = 'en'

localedir = str(Path(__file__).resolve().parent.parent / "locales")
dictionary = {}
lang = Language.NL

monthsdic = {
    Language.NL.value: ["Januari", "Februari", "Maart", " April", "Mei", "Juni", "Juli", "Augustus", "September", "Oktober","November", "December"],
    Language.EN.value: ["January", "February" , "March", "April", "May", "June","Juli", "August", "September", "October", "November","December"]
    
}

def change_language(language=lang):
    global dictionary
    global lang
    
    lang = language    
    language = language + '.json'
    
    # I assume people only change the language once. Otherwise, it would
    # be better to open all dictionaries in the parent scope!
    with open(localedir + '/' + language, 'r',  encoding='utf8') as f:
        dictionary = json.load(f)
    
def translate(key):
    value = dictionary.get(key)
    # fallback
    if not value:
        value = key
    return value

def translate_list(mylist):
    return [translate(value) for value in mylist]

def translate_date(month):
    return monthsdic[lang][month-1]
    


    

