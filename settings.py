import json

OUTPUT_FOLDER = 'docs/'
info = None

current_edition = '04_02_2022'

with open('info.json') as f:
    info = json.load(f)
