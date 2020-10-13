import concurrent.futures
import requests
import json

def fetcher(currentpath, root, access_token):
    route = requests.get(root + currentpath, headers={'X-Access-Token' : access_token}).json()
    data_from_links = []
    if "data" in route:
        if "mime_type" in route:
            data_from_links.append(tuple([route["data"], route["mime_type"]]))
        else:
            data_from_links.append(tuple([route["data"], "json"]))

    follow_up_routes = []

    if "link" in route:
        for link in route["link"].items():
            follow_up_routes.append(link[1])
            
    return follow_up_routes, data_from_links

def futures_initiator(home, root, access_token, data_from_links):
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:

        futures = [
            ex.submit(fetcher, link[1], root, access_token) 
            for link in home['link'].items()
        ]

        while futures:
            done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            for fut in done:
                data_from_links.extend(fut.result()[1])
                if len(fut.result()[0]) != 0:
                    for link in fut.result()[0]:
                        futures.add(ex.submit(fetcher, link, root, access_token))
    return data_from_links