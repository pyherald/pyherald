import json

OUTPUT_FOLDER = 'docs/'
info = None

current_edition = '24_12_2021'

with open('info.json') as f:
    info = json.load(f)
