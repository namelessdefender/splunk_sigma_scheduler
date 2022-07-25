import sys
import json
import hashlib
import sigma_tracker
import splunk_alerts
import argparse

db = sigma_tracker.Tracker()
splunk = splunk_alerts.Splunk()

parser = argparse.ArgumentParser(description='Process Sigma rules.')
parser.add_argument('url', help='the url of the Sigma rule')
args = parser.parse_args()

class Rule:

    def __init__(self, id, title, description, rule, md5, tags, url):
        self.id = id
        self.title = title
        self.description = description
        self.rule = rule
        self.md5 = md5
        self.tags = tags
        self.url = url


def convert(url):
    data = sys.stdin.readlines()
    if data:
        data = data[0].replace("[{", "{").replace("}]", "}")
        data = json.loads(data)

        data['md5'] = hashlib.md5(data['rule'][0].encode('utf-8')).hexdigest()

        if data['tags']:
            tags = [tag.split("attack.")[1] for tag in data['tags'] if tag.startswith("attack.t")]
            data['tags'] = ",".join(tags)
        else:
            data['tags'] = None

        url = "https://github.com/SigmaHQ/sigma/blob/master/rules/" +  "/".join(url.split("/")[2:])

        rule = Rule(data['id'], data['title'], data['description'], data['rule'][0], data['md5'], data['tags'], url)

        db.process(rule)
        splunk.create_alert(rule)


convert(args.url)