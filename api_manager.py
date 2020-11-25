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

    def __init__(self):
        with open("goodreads_key", "r") as f:
            self.dev_key = f.read()
            last_run = datetime.datetime.now()

    def goodreads_get(self, url):
        waiting = True
        while waiting:
            now = datetime.datetime.now()
            time_between_runs = now - self.last_run
            if time_between_runs < datetime.timedelta(seconds=0.5):
                time.sleep(0.5)
            else:
                waiting = False
        self.last_run = datetime.datetime.now()
        print(datetime.datetime.now())
        http = urllib3.PoolManager()
        r = http.request('Get', url)
        string_xml = r.data
        return string_xml