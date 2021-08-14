# -*- coding: utf-8 -*-

import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Fetch GitHub comments')
parser.add_argument('--source', required=True, type=str,
                    help='source path of csv file')
parser.add_argument('--dest', required=True, type=str,
                    help='destination of preprocessed csv file')

args = parser.parse_args()
SOURCE_FILE = args.source
DEST_FILE = args.dest

df = pd.read_csv(SOURCE_FILE)


df['body'] = df['body'].replace(
    r"(@[A-Za-z0-9]+)|(#[A-Za-z0-9_]+)|(\w+:\/\/\S+)", '', regex=True)

df['body'] = df['body'].replace(r"(\n)|(\t)|(\r)", ' ', regex=True)

df['body'] = df['body'].replace(
    r"(\*+)|(`+)|(~+)|(\[x\])|(>)|(-)|(#+)|(`.*?`)|(```.*?```)", '', regex=True)

df['body'] = df['body'].replace(r':[A-Za-z0-9]+:', '', regex=True)

df['body'] = df['body'].replace(r' +', ' ', regex=True)

regrex_pattern = re.compile(pattern="["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)

df['body'] = df['body'].replace(regrex_pattern, '', regex=True)

for index, row in df.iterrows():
    if (len(row['body'].split()) > 100):
        df.drop(index, inplace=True)
df = df.reset_index(drop=True)


df.to_csv(DEST_FILE)

