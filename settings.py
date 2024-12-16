import json

OUTPUT_FOLDER = 'docs/'
info = None

current_edition = '16_12_2024'

with open('info.json') as f:
    info = json.load(f)
