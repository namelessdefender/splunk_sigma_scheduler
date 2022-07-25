import requests
import json
import os
from dotenv import load_dotenv
import logging
from random import choice, randint

requests.packages.urllib3.disable_warnings()
load_dotenv()

class Splunk():

    def __init__(self):

        self.host = os.getenv("SPLUNK_HOST")
        self.auth = (os.getenv("SPLUNK_USER"), os.getenv("SPLUNK_PASSWORD"))
        self.app = os.getenv("SPLUNK_APP")
        self.base_url = "https://%s:8089" % (self.host)


    def update_kvstore(self, rule):

        data = {
            "_key": rule.id,
            "id": rule.id,
            "title": rule.title,
            "description": rule.description,
            "rule": rule.rule,
            "md5": rule.md5,
            "tags": rule.tags,
            "url": rule.url
        }

        data = json.dumps(data)

        url = (self.base_url + "/servicesNS/nobody/" + self.app + "/storage/collections/data/sigma_rules_kvstore")
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}, auth=self.auth, verify=False)

        print(str(response.status_code) + " update kvstore")
        print(response.text)


    def delete_alert(self, rule):
        
        url = self.base_url + "/services/saved/searches/%s" % rule.title

        response = requests.delete(url=url, auth=self.auth, verify=False)

        #print(response.text)


    def create_alert(self, rule):

        self.delete_alert(rule)
        self.update_kvstore(rule)

        url = self.base_url + "/services/saved/searches"

        latest = "-5m@m"
        earliest = "-60m@m"

        rule.rule = "_index_latest=%s _index_earliest=%s index=test-thickmintel " % (latest, earliest) + rule.rule
        if "| table" in rule.rule:
            rule.rule = rule.rule.split(" | table")[0]
            #self.rule = self.rule + " sample_id task_id"

        #cron_schedule = choice(["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"])
        cron_schedule = str(randint(0,60))
        
        data = {
            'output_mode': 'json',
            'name': rule.title,
            'description': rule.description,
            'search': rule.rule,
            'is_scheduled': True,
            'cron_schedule': '%s * * * *' % cron_schedule,
            'schedule_window': '60',
            'dispatch.latest_time': '%s' % latest,
            'dispatch.earliest_time': '%s' % earliest,
            'actions': 'summary_index',
            'action.summary_index._name': 'sigma_hits',
            'action.summary_index._type': 'event'
        }

        response = requests.post(url=url, auth=self.auth, data=data, verify=False)

        #print(response.text)


if __name__ == "__main__":
    pass

