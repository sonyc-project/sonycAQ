import time
from tqdm.notebook import tqdm
import pandas as pd
import requests
import math

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

def praxis_data_download(st_date_utc, en_date_utc, avg_over_min):
    # Import and format Praxis data
    uri = 'https://aws.southcoastscience.com/topicMessages?topic=nyu/brooklyn/loc/3/particulates&' \
    'startTime=%s&endTime=%s&checkpoint=**:/%i:00' \
    % (st_date_utc, en_date_utc, avg_over_min)
    
    praxis_df = pd.DataFrame([])

    while uri != '':
        header = {"authorization": "api-key nyu-brooklyn"}
        response = requests.get(uri, headers=header)
        json = response.json()

        data = {}

        data['ts'] = pd.to_datetime([ele['rec'] for ele in json['Items']]).tz_convert(tz='US/Eastern')

        data['praxis_pm1_vals'] = [ele['val']['pm1'] for ele in json['Items']]
        data['praxis_pm2p5_vals'] = [ele['val']['pm2p5'] for ele in json['Items']]
        data['praxis_pm10_vals'] = [ele['val']['pm10'] for ele in json['Items']]

        data['praxis_pm1_vals_adj'] = [ele['exg']['rn20']['pm1'] for ele in json['Items']]
        data['praxis_pm2p5_vals_adj'] = [ele['exg']['rn20']['pm2p5'] for ele in json['Items']]
        data['praxis_pm10_vals_adj'] = [ele['exg']['rn20']['pm10'] for ele in json['Items']]

    #     praxis_df = pd.DataFrame(data).set_index('ts').resample(avg_over).mean()

        if 'next' in json:
            uri = json['next']
        else:
            uri = ''
        praxis_df = pd.concat([praxis_df, pd.DataFrame(data)])

        time.sleep(0.5)
    praxis_df = praxis_df.set_index('ts').resample('%iT' % avg_over_min).mean()
    return praxis_df

def calculate_us_epa_aqi(Conc):

    c = (math.floor(10 * Conc)) / 10
    if (c >= 0 and c < 12.1):
        AQI = Linear(50, 0, 12, 0, c)
    elif (c >= 12.1 and c < 35.5):
        AQI = Linear(100, 51, 35.4, 12.1, c)
    elif (c >= 35.5 and c < 55.5):
        AQI = Linear(150, 101, 55.4, 35.5, c)
    elif (c >= 55.5 and c<150.5):
        AQI = Linear(200, 151, 150.4, 55.5, c)
    elif (c >= 150.5 and c < 250.5):
        AQI = Linear(300, 201, 250.4, 150.5, c)
    elif (c >= 250.5 and c < 350.5):
        AQI = Linear(400, 301, 350.4, 250.5, c)
    elif (c >= 350.5 and c < 500.5):
        AQI = Linear(500, 401, 500.4, 350.5, c)
    else:
        c = 500
        AQI = Linear(500, 401, 500.4, 350.5, c)
    return AQI;
    
def Linear(AQIhigh, AQIlow, Conchigh, Conclow, Conc):
    a = ((Conc-Conclow) / (Conchigh-Conclow)) * (AQIhigh-AQIlow) + AQIlow
    linear = round(a)
    return linear

