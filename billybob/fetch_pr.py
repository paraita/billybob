#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

GITHUB_URL = 'https://api.github.com/search/issues'
GITHUB_QUERY = {'q': 'is:open is:pr user:ow2-proactive'}


def _get_prs_from_github():
    r = requests.get(GITHUB_URL, params=GITHUB_QUERY)
    json_response = r.json()
    list_pr = json_response['items']
    api_url = 'https://api.github.com/repos/'
    repo_url_good = 'https://github.com/'
    gh_url = 'https://github.com/'
    return [
        {
            'url': pr['repository_url'].replace(api_url, repo_url_good),
            'repo_name': pr['repository_url'].replace(api_url, ''),
            'title': pr['title'],
            'pr_url': pr['pull_request']['url'].replace(api_url,
                                                        gh_url).replace('pulls',
                                                                        'pull'),
        }
        for pr in list_pr
        ]


def _get_prs_from_bitbucket():
    return []


def get_prs(host):
    prs = {}
    if host == 'github':
        prs['github'] = _get_prs_from_github()
    elif host == 'bitbucket':
        prs['bitbucket'] = _get_prs_from_bitbucket()
    elif host == 'everywhere':
        prs['github'] = _get_prs_from_github()
        prs['bitbucket'] = _get_prs_from_bitbucket()
    return prs
