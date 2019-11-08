import requests


def get_repos(page, organizations_url, organizations_repos_url_extension, per_page, headers, repos):
    url = organizations_url + "/" + organizations_repos_url_extension
    url = url.format(page=page, per_page=per_page)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        repos.extend(response)


def get_top_repos(repos):
    sorted_response = sorted(repos, key=lambda i: i['stargazers_count'])

    if len(sorted_response) >= 3:
        top_repos = [{'name': item['name'], 'stars': item['stargazers_count']} for item in
                     reversed(sorted_response[-3:])]
    else:
        top_repos = [{'name': item['name'], 'stars': item['stargazers_count']} for item in
                     reversed(sorted_response[-len(sorted_response):])]
    data = []
    for repo in top_repos:
        repo = {'name': repo['name'], 'stars': repo['stars']}
        data.append(repo)

    return data
