#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

GITHUB_URL = 'https://api.github.com/search/issues'
GITHUB_QUERY = {'q': 'is:open is:pr user:ow2-proactive'}


def _get_prs_from_github():
    r = requests.get(GITHUB_URL, params=GITHUB_QUERY)
    json_response = r.json()
    list_pr = json_response['items']
    return [
        {
            'url': pr['repository_url'],
            'repo_name': pr['repository_url'].replace('https://api.github.com/repos/', ''),
            'title': pr['title'],
            'pr_url': pr['pull_request']['url']
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
