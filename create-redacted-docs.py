#!/usr/bin/env python
# Create JSON based on redacted production data, with bogus album names if missing.

import json
import random

ALBUMS = ('Revolver', 'Highway 61 Revisited', 'What\'s Going On',
          'London Calling', 'Blonde on Blonde', 'White Album', 'Sunrise',
          'Kind of Blue', 'Velvet Underground & Nico', 'Abbey Road',
          'Are You Experienced', 'Blood on the Tracks', 'Innervisions',
          'Live at the Apollo', 'Rumours', 'The Joshua Tree', 'Blue',
          'Bringing It All Back Home', 'Let It Bleed', 'Music From Big Pink',
          'The Rise and Fall of Ziggy Stardust', 'Tapestry', 'Hotel California',
          'Please Please Me', 'Forever Changes', 'Never Mind the Bollocks',
          'The Dark Side of the Moon', 'Horses', 'A Love Supreme',
          'It Takes a Nation of', 'At The Fillmore East')

docs_json = open('avail-search.out.json', 'r', encoding='utf8').read()
docs = json.loads(docs_json)
outdocs = []
for doc in docs:
    fields = doc['fields']
    albums = fields.get('album',
                        random.sample(ALBUMS, random.randrange(1, 5)))
    outdocs.append({'id': doc['id'],
                    'fields': {'albums': albums,
                               'title': fields['title'][0]}})

with open('sample-docs.json', 'w', encoding='utf8') as out:
    out.write(json.dumps(outdocs, sort_keys=True, indent=2))

