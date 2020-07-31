#!/usr/bin/env python
# Query Insight and list windows servers and owners
# initial version
######

import requests
import subprocess
import json
import os

jira_user = os.environ.get('JIRA_USERNAME')
jira_pass = os.environ.get('JIRA_PASSWORD')
jira_server = "https://atlassian.dpgmedia.net/jira/rest/insight/1.0/iql/objects?objectSchemaId=1&iql="
resultssize = '&resultPerPage=5000'
iql = 'objectType="Windows" AND Status=Active'

os.system("echo 'host,os,type,virtual,fullname,waveid,primary function' > /tmp/insight-windows-owners.csv")
outfile=open('/tmp/insight-windows-owners.csv', 'a+')

# main
try:
    response = requests.get(jira_server + iql + resultssize, auth=(jira_user, jira_pass))
    content_win = json.loads(response.content)

    for winres in content_win['objectEntries']:
        host = winres['name']
        host = '"' + host + '"'
        try:
            osType=list(filter(lambda attr: attr['objectTypeAttributeId'] == 259, winres['attributes']))[0]
            if len(osType['objectAttributeValues']) and 'value' in osType['objectAttributeValues'][0]:
                os = osType['objectAttributeValues'][0]['value']
            else:
                os = "Unknown"
            os = '"' + os + '"'
        except Exception as e:
            pass
        srvtype="\"WindowsServer\""
        virtual=""
        try:
            isVirtual=list(filter(lambda attr: attr['objectTypeAttributeId'] == 249, winres['attributes']))[0]
            if len(isVirtual['objectAttributeValues']) and 'value' in isVirtual['objectAttributeValues'][0]:
                virtual = isVirtual['objectAttributeValues'][0]['value']
            else:
                virtual = "Unknown"
            virtual = '"' + virtual + '"'
        except Exception as e:
            pass
        fullname=""
        try:
            fullName=list(filter(lambda attr: attr['objectTypeAttributeId'] == 243, winres['attributes']))[0]
            if len(fullName['objectAttributeValues']) and 'value' in fullName['objectAttributeValues'][0]:
                fullname = fullName['objectAttributeValues'][0]['value']
            else:
                fullname = "Unknown"
            fullname = '"' + fullname + '"'
        except Exception as e:
            pass
        waveid=""
        primaryfunction=""
        try:
            primaryFunction=list(filter(lambda attr: attr['objectTypeAttributeId'] == 247, winres['attributes']))[0]
            if len(primaryFunction['objectAttributeValues']) and 'value' in primaryFunction['objectAttributeValues'][0]:
                primaryfunction = primaryFunction['objectAttributeValues'][0]['value']
            else:
                primaryfunction = "Unknown"
            primaryfunction = primaryfunction.replace('\n', ' ')
            primaryfunction = '"' + primaryfunction + '"'
        except Exception as e:
            pass
        print(host,os,srvtype,virtual,fullname,waveid,primaryfunction,sep=',',file=outfile)
        print(host,os,srvtype,virtual,fullname,waveid,primaryfunction,sep=',')
    outfile.close()

except KeyboardInterrupt:
    print ("Interrupted by Keyboard...")

except Exception as e:
    print ("An error or exception occurred: %s" % e)
    raise
