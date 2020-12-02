import datetime
import time
import urllib3

# API Manager for centalizing interractions with the Goodreads API


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class API_Manager():
    dev_key = ""
    last_run = datetime.datetime.now()
    number_of_calls = 0

    def __init__(self):
        # TODO - temporarily hardcode the key
        # with open("goodreads_key", "r") as f:
        #     self.dev_key = f.read()
        # Hardcoding key for now
        dev_key = "qcXIjujzhYVHOFU4SszgQ"
        last_run = datetime.datetime.now()
        number_of_calls = 0

    def goodreads_get(self, url, query_params={}):
        waiting = True
        while waiting:
            now = datetime.datetime.now()
            time_between_runs = now - self.last_run
            if time_between_runs < datetime.timedelta(seconds=0.5):
                time.sleep(0.5)
            else:
                waiting = False
        self.last_run = datetime.datetime.now()
        self.number_of_calls += 1
        http = urllib3.PoolManager()
        r = http.request('Get', url, fields=query_params)
        string_xml = r.data
        return string_xml
