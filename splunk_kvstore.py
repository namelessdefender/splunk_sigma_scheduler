import requests
import json
import os
from dotenv import load_dotenv
import logging

requests.packages.urllib3.disable_warnings()
load_dotenv()

class Splunk():

    def __init__(self):

        self.host = os.getenv("SPLUNK_HOST")
        self.auth = (os.getenv("SPLUNK_USER"), os.getenv("SPLUNK_PASSWORD"))
        self.app = os.getenv("SPLUNK_APP")
        self.base_url = "https://%s:8089" % (self.host)


    def delete_lookup_definition(self):

        url = (self.base_url + "/servicesNS/nobody/" + self.app + "/data/transforms/lookups/sigma_rules_lookup")
        r = requests.delete(url, auth=self.auth, verify=False)

        print("%s - [DELETE LOOKUP DEFINITION]" % r.status_code)


    def delete_kvstore(self):

        url = (self.base_url + "/servicesNS/nobody/" + self.app + "/storage/collections/config/sigma_rules_kvstore")
        r = requests.delete(url, auth=self.auth, verify=False)

        print("%s - [DELETE KVSTORE]" % r.status_code)


    def create_lookup_definition(self):

        lookup_definition = {
            'name': 'sigma_rules_lookup',
            'collection': 'sigma_rules_kvstore',
            'external_type': 'kvstore',
            'fields_list': '_key, id, title, description, rule, md5, tags, url'
        }

        url = (self.base_url + "/servicesNS/nobody/" + self.app + "/data/transforms/lookups")
        r = requests.post(url, data=lookup_definition, auth=self.auth, verify=False)

        print("%s - [LOOKUP DEFINITION CREATION]" % r.status_code)


    def define_kvstore(self):
        
        kvstore_definition = [
            'field.id=string',
            'field.title=string',
            'field.description=string',
            'field.rule=string',
            'field.md5=string',
            'field.tags=string',
            'field.url=string'
        ]

        for field in kvstore_definition:
            url = (self.base_url + "/servicesNS/nobody/" + self.app + "/storage/collections/config/sigma_rules_kvstore")
            r = requests.post(url, data=field, auth=self.auth, verify=False)

        print("%s - [KVSTORE DEFINITION CREATION]" % r.status_code)
        

    def create_kvstore(self):

        url = (self.base_url + "/servicesNS/nobody/" + self.app + "/storage/collections/config")
        r = requests.post(url, data="name=sigma_rules_kvstore", auth=self.auth, verify=False)

        print("%s - [KVSTORE CREATION]" % r.status_code)


if __name__ == "__main__":
    splunk = Splunk()
    splunk.delete_kvstore()
    splunk.delete_lookup_definition()
    splunk.create_kvstore()
    splunk.define_kvstore()
    splunk.create_lookup_definition()

