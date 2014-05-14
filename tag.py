import nltk
import json
import re

POSS = ['NN', 'JJ', 'POS', 'IN']

def get_phrase(phrase, d):
  p = phrase.replace('"', '', 100000)
  p = p.split(' ')
  d = d.replace('\n', ' ', 100000)
  d = d.replace('-', ' ', 100000)
  d = d.replace('\\n', ' ', 100000)
  d = d.replace('\\u2014', ' ', 10000)
  d = d.replace(".", " ", 10000)
  d = d.replace(",", " ", 100000)
  d = re.sub(r'\W+', ' ', d)
  text = nltk.word_tokenize(d)
  tags = nltk.pos_tag(text)
  marker = -1
  phraseMarker = 0
  for i in range(len(tags)):
    if tags[i][0].lower() == p[phraseMarker]:
      phraseMarker += 1
      if phraseMarker < len(p):
        pass
      else:
        j = i - phraseMarker
        while j > 0 and tags[j-1][1] in POSS:
          j -= 1
        return tags[j:i-phraseMarker + 1]
        # emit word and return
    else:
      phraseMarker = 0
  return None


def recomb(bits):
  ret = ''
  for i, b in enumerate(bits):
    if b[1] in POSS:
      if i > 0 and b[1] != 'POS':
        ret += ' '
      ret += b[0]
  return ret

collection = {}

def do_file(j):
  for search, block in j.items():
    for item in block['links']:
      title = item['title'] if 'title' in item else None
      link = item['link'] if 'link' in item else None
      desc = item['description']
      what = get_phrase(search, desc)
      if what is not None:
        phrase = recomb(what)
        if phrase not in collection:
          collection[phrase] = {"count": 0, "links": []}
        collection[phrase]["count"] += 1
        if link and title:
          collection[phrase]["links"].append({'title': title, 'link': link})


files = ['try.json']
html = open('html.txt', 'w')
for file in files:
  json_data = open('test.json')
  j = json.load(json_data)
  do_file(j)

with open('OUT.JSON', 'w') as outfile:
  json.dump(collection, outfile)

i = collection.items()
j = sorted(i, key=lambda t: t[1]['count'])
tot = float(reduce(lambda acc,t: acc+t[1]['count'], j, 0))
def pct(c):
  return 100 * float(c)/tot
for phrase, t in j:
  html.write("<tr><td>%d</td><td>%.2f</td><td>%s</td></tr>" % (t['count'], pct(t['count']), phrase))
html.close()
