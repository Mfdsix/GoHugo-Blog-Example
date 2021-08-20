import requests
import os, shutil
import re

folder = 'content/post'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

baseUrl = "https://api.currentsapi.services/v1/"
key = "youkey"

# top headline
response = requests.get("%slatest-news?apiKey=%s" % (baseUrl, key))
posts = response.json()['news']

for i in posts:
    header = '+++\ntitle = "%s"\ndescription = "%s"\ntags = [\n"%s",\n]\ndate = %s\nauthor = "%s"\n+++\n\n''' % (i['title'], i['description'][0:35], i['category'][0], i['published'].replace(" +0000", "Z").replace(" ", "T"), i['author'])
    content = i['description']
    try:
        filename = "%s/%s.md" % (folder, re.sub(r'[^a-zA-Z0-9]', "-", i['title'].lower().replace(" ", "-")))
        file = open(filename, "w")
        file.write(header + content)
    except Exception as e:
        print("failed to generate file", e)


