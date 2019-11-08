import json
from queue import Queue

from flask import Flask, json, request

from workers import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/repos', methods=["POST"])
def maz():
    final_response = {"results": []}
    per_page = 100
    organizations_base_url = "https://api.github.com/orgs/{org}"
    organizations_repos_url_extension = "repos?page={page}&per_page={per_page}"
    org = request.json['org']
    token = request.json['token']
    headers = {
        'Authorization': 'Bearer ' + token
    }
    if org:

        repos = []
        organizations_url = organizations_base_url.format(org=org)
        response = requests.get(organizations_url, headers=headers)

        if response.status_code == 200:
            response = response.json()
            public_repo_count = response['public_repos']
            no_of_pages = int(public_repo_count / 100) + 1

            queue = Queue()
            for _ in range(1, no_of_pages + 1):
                worker = StargazerWorker(queue)
                worker.daemon = True
                worker.start()
            for i in range(1, no_of_pages + 1):
                queue.put((i, organizations_url, organizations_repos_url_extension, per_page, headers, repos))
            queue.join()

            final_response["results"] = get_top_repos(repos)

            return json.dumps(final_response, indent=4)

        else:
            final_response["results"] = "invalid credentials or something went wrong"
            return json.dumps(final_response, indent=4)

    else:
        final_response["results"] = "Please specify the org parameter"
        return json.dumps(final_response, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090)
