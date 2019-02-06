#!/usr/bin/env python
# Take word or phrase from CLI, ask for prefix-matching album names
# using text-array albums_text against each word in phrase.

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import json
from lib import get_doc_client
import sys

FACET_LA = 'albums'             # literal-array facet name
FACET_TA = 'albums_text'        # corresponding case-insensitive text-array
FACET_NAME = 'albums'           # for printing sample output

def main(args):
    if len(sys.argv) < 2:
        print('Specify one or more query words')
        exit(1)
    csd = get_doc_client(args.domain)

    # Build compound query:
    #   (and (prefix field=albums_text Q1) ... (prefix field=album_text Q2))
    queries = ["(prefix field='%s' '%s')" % (FACET_TA, q) for q in args.query]
    query = '(and %s)' % ''.join(queries)
    print('q=%s' % query)

    res = csd.search(
        queryParser='structured',
        query=query,
        returnFields=FACET_LA,  # have to return something, else we get everything
        size=1000,              # we only get facets for returned hits, so need a bunch
        cursor='initial',       # we're not going to do multiple pages
        facet=json.dumps({FACET_LA: {'sort': 'bucket', 'size': 20}}),  # 'alpha' or 'count'
    )
    httpres = res.pop('ResponseMetadata')
    facets = res.pop('facets')[FACET_LA]['buckets']
    hits = res.pop('hits')
    found = hits['found']
    if found == 0:
        print('Found jack :-(')
        exit(2)
    print('found=%s hit0=%s' % (found, hits['hit'][0]))
    for facet in facets:
        print('count=%5d %s=%s' % (facet['count'], FACET_NAME, facet['value']))


if __name__ == '__main__':
    parser = ArgumentParser(description=('Take word or phrase from CLI, ask for prefix-matching'
                                         ' album names using text-array album_text against each'
                                         ' word in phrase.'),
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--domain', required=True,
                        help='cloudsearch domain name')
    parser.add_argument('-q', '--query', required=True, nargs='+',
                        help='query wodcloudsearch domain name')
    args = parser.parse_args()
    main(args)

