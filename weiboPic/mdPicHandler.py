import requests
import os
import re

apiurl = "https://api.berryapi.net/sina"    # berryapi's api
filelist = os.listdir()
heads = {'AppKey':""}						# not sure whether it's necessary


def getWeiboUrl(addr):
    if addr.startswith('http'):                # use picture from the Internet
        data = {'url': addr}
        r = requests.post(apiurl, headers=heads, data=data)
    else:                                       # use local picture
        p = open(addr, 'rb')
        dir = addr.split("\\")
        files = {'file': (dir[len(dir)-1], p, 'image/jpeg', {})}
        r = requests.post(apiurl, headers=heads, files=files)
    j = r.json()
    if j['msg'] != 'ok': return 'failed'
    return r.json()['data']['images']['large']


def replacePicAddr(filedir):
    f = open(filedir)
    texts = []
    for s in f.readlines():
        matchObj = re.match(r'!\[(.*)\].*\((.*?)\)', s, re.M | re.I)
        if matchObj == None:
            texts += [s]
        else:
            addr = matchObj.group(2)
            texts += [s.replace(addr, getWeiboUrl(addr))]
    f.close()
    f = open(filedir, 'r+')
    for line in texts:
        f.write(line)
    f.close()
    print(filedir, 'has been successfully converted!')


if __name__ == "__main__":

    # try to discover md files in the directory
    for name in filelist:
        if name.endswith('.md') | name.endswith('.markdown'):
            replacePicAddr(name)
