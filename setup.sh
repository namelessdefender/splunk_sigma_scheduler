# https://github.com/SigmaHQ/sigma
# pip3 install sigmatools

#######################################################################
## 1. Pulls down current Sigma rule set                              ##
## 2. Iterates through target rule folders                           ##
## 3. Converts rule to JSON                                          ##
## 4. Hashes rule logic                                              ##
## 5. Deletes previous kvstore and definitions                       ##
## 6. Adds rules to a local database                                 ##
## 7. Adds rules to a Splunk kvstore                                 ##
## 8. Pushes rule logic as a scheduled alert with a Log Event action ##
#######################################################################

rm -rf ~/sigma
git clone https://github.com/SigmaHQ/sigma ~/sigma

python3 splunk_kvstore.py

for file in ~/sigma/rules/windows/process_creation/*.yml; do
    echo $file
    ~/sigma/tools/sigmac -t splunk $file --config sysmon --output-fields id,title,description,tags --output-format json | jq -c '' | python3 convert.py $file
done

for file in ~/sigma/rules/windows/network_connection/*.yml; do
    echo $file
    ~/sigma/tools/sigmac -t splunk $file --config sysmon --output-fields id,title,description,tags --output-format json | jq -c '' | python3 convert.py $file
done
