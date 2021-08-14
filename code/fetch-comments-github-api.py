# -*- coding: utf-8 -*-
import argparse
import csv
import math
import os
import time

import requests

BASE_URL = "https://api.github.com/repos/"
API_TYPE = "/issues/comments"

parser = argparse.ArgumentParser(description='Fetch GitHub comments')
parser.add_argument('--repo', required=True, type=str,
                    help='repo urls (example: kubenetes/kubernetes)')
parser.add_argument('--token', required=True,
                    type=str, help='GitHub API token')
parser.add_argument('--sectoken', required=False, type=str,
                    help='secondary GitHub API token')
parser.add_argument('--count', required=False, type=int,
                    help='Number of comments to fetch')
parser.add_argument('--sortby', required=False, type=str,
                    help='sort by created or updated')
parser.add_argument('--perpage', required=False, type=int,
                    help='results per API fetch')
parser.add_argument('--sortdir', required=False, type=str,
                    help='comments sorting direction')
parser.add_argument('--since', required=False, type=str,
                    help='comments to fetch since timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ')

args = parser.parse_args()

REPO_URLS = [args.repo]
API_TOKEN = args.token  # to not get rate limited
SECONDARY_TOKEN = args.sectoken if (args.sectoken is not None) else API_TOKEN
FETCH_COUNT = args.count if (args.count is not None) else 5
SORT_BY = args.sortby if (args.sortby is not None) else "created"
SORT_DIR = args.sortdir if (args.sortdir is not None) else "asc"
PER_PAGE = args.perpage if (args.perpage is not None) else 5
# This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
SINCE = args.since if (args.since is not None) else "2021-07-05T00:00:00Z"

# Fetch Issues of these Repos
comments = {}
print(API_TOKEN)
print(REPO_URLS[0])
for repo_url in REPO_URLS:
    request_url = BASE_URL + repo_url + API_TYPE

    # default values
    comments_list = []
    next_page = 1
    per_page = PER_PAGE
    last_page_count = PER_PAGE
    num_pages = -1

    request_params = {"per_page": per_page, "sort": SORT_BY,
                      "direction": SORT_DIR, "since": SINCE}

    if FETCH_COUNT != -1:
        num_pages = math.ceil(FETCH_COUNT / PER_PAGE)
        last_page_count = FETCH_COUNT % PER_PAGE
        if last_page_count == 0:
            last_page_count = PER_PAGE

    while True:
        # time.sleep(100)
        request_params['page'] = next_page
        if next_page == num_pages:
            request_params["per_page"] = last_page_count
        token = API_TOKEN
        while True:
            print(request_url)
            response = requests.get(url=request_url, params=request_params, headers={
                                    "Authorization": "token " + token})
            if response.status_code == 200:
                break
            else:
                print(response.text)
                token = SECONDARY_TOKEN

                time.sleep(10)

        data = response.json()
        if data == [] and FETCH_COUNT == -1:
            break
        comments_list.extend([{"id": x["id"], "body": x["body"].encode(
            'utf-8'), "created_at": x["created_at"].encode('utf-8')} for x in data])
        next_page = next_page + 1
        if FETCH_COUNT != -1 and next_page > num_pages:
            break
    comments[repo_url] = comments_list

for repo_url in REPO_URLS:
    if not os.path.exists(os.path.dirname(repo_url)):
        try:
            os.makedirs(os.path.dirname(repo_url))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    toCSV = comments[repo_url]
    keys = toCSV[0].keys()
    with open(repo_url + '.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)