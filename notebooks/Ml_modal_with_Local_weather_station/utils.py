import time
from tqdm.notebook import tqdm

GROUP = time.time()

def scroll(es, index, body, scroll='2m', size=1000, timeout=25, **kw):
    if isinstance(timeout, int):
        timeout = '{}s'.format(int(timeout))
    page = es.search(index=index, body=body, scroll=scroll, size=size, timeout=timeout, **kw)
    scroll_id, hits = page['_scroll_id'], page['hits']['hits']
    while len(hits):
        yield hits
        page = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id, hits = page['_scroll_id'], page['hits']['hits']
        
def sensor_query(key=None, nodeid=None, start=None, end=None, k_time="time", group=GROUP):
    match = []
    if key and nodeid:
        match.append({"term": {f'{key}.keyword': nodeid}})
    end = end or 'now'
    if start:
        match.append({"range" : {k_time : {"gte" : start, "lte" : end}}})
    elif end:
        match.append({"range" : {k_time : {"lte" : end}}})
    return { "query": { "bool": {"must": match} } } if match else {}

def download_sensor_data(es, table, key=None, nodeid=None, start=None, end=None, save=True, k_time='time', **kw):
    query = sensor_query(key, nodeid, start, end, k_time=k_time, **kw)
    print(query)
    
    def pull():
        with tqdm(scroll(es, table, query)) as pbar:
            for i, hits in enumerate(pbar):
                hits = [h['_source'] for h in hits]
                times = [h[k_time] for h in hits]
                pbar.write('{}. n hits: {}. {} - {}'.format(i, len(hits), min(times), max(times)))
                for h in hits:
                    yield h
    if not save:
        return list(pull())

    fname = 'data/{}/{}.json'.format(group, nodeid or table)
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    print(f'Pulling node={nodeid} for ({start} -> {end}) ... saving to {fname}')
    with open(fname, 'w') as f:
        for h in pull():
            f.write(json.dumps(h) + '\n')
    print('all done!')
    return fname