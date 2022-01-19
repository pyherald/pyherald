import json

OUTPUT_FOLDER = 'docs/'
info = None

current_edition = '20_01_2022'

with open('info.json') as f:
    info = json.load(f)
