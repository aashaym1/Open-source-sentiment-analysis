## Generating Test Data

### Fetch GitHub Issue comments

Use the `fetch-comments-github-api.py` script to fetch issue comments. This uses GitHub REST API
```
 # how to fetch GitHub comments sample
 python code/fetch-comments-github-api.py --repo kubernetes/kubernetes --token "ghp_blablabla"
```
---
Use this to see all available options
```
python code/fetch-comments-github-api.py --help 

usage: fetch-comments-github-api.py [-h] --repo REPO --token TOKEN [--sectoken SECTOKEN] [--count COUNT] [--sortby SORTBY] [--perpage PERPAGE] [--sortdir SORTDIR]
                                    [--since SINCE]

Fetch GitHub comments

optional arguments:
  -h, --help           show this help message and exit
  --repo REPO          repo urls (example: kubenetes/kubernetes)
  --token TOKEN        GitHub API token
  --sectoken SECTOKEN  secondary GitHub API token
  --count COUNT        Number of comments to fetch
  --sortby SORTBY      sort by created or updated
  --perpage PERPAGE    results per API fetch
  --sortdir SORTDIR    comments sorting direction
  --since SINCE        comments to fetch since timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
```
---

### Processing the comments

Process the comments and remove unwanted items using `preprocessing.py`
```
# Install pandas dependency for dataframe operations
pip install pandas

# Run the preprocessing script

python code/preprocessing.py --help
---
usage: preprocessing.py [-h] --source SOURCE --dest DEST

Fetch GitHub comments

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE  source path of csv file
  --dest DEST      destination of preprocessed csv file
```