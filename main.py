import requests
import json
import concurrent.futures
import itertools
import utility
import tcpserver
import concurrent_fetcher
import converter
import merger


def main():

    root = 'http://localhost:5000'
    register = requests.get(root + '/register')
    access_token = register.json()['access_token']

    home = requests.get(root + '/home', headers={'X-Access-Token' : access_token}).json()

    data = []
    
    data = concurrent_fetcher.futures_initiator(home, root, access_token, data)

    data = converter.convert_to_json(data)

    merged_json = merger.merger(data)

    tcpserver.tcpserver(merged_json)


if __name__ == "__main__":
    main()