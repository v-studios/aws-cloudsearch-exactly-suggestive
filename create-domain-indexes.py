#!/usr/bin/env python
# Create Domain with 'title, and exact 'albums' with 'albums_text' suggester.

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import OrderedDict

import boto3

from lib import get_fields

# We must create 'albums' before 'albums_text' which uses 'albums' as its source
INDEXES = OrderedDict({
    'albums': {
        'IndexFieldName': 'albums',
        'IndexFieldType': 'literal-array',
        'LiteralArrayOptions': {'FacetEnabled': True,
                                'ReturnEnabled': True,
                                'SearchEnabled': True}},
    'albums_text':  {
        'IndexFieldName': 'albums_text',
        'IndexFieldType': 'text-array',
        'TextArrayOptions': {'AnalysisScheme': '_en_default_',
                             'HighlightEnabled': True,  # don't need, but OK
                             'ReturnEnabled': True,
                             'SourceFields': 'albums'}},
    'title': {
        'IndexFieldName': 'title',
        'IndexFieldType': 'text',
        'TextOptions': {'AnalysisScheme': '_en_default_',
                        'HighlightEnabled': True,  # don't need, but OK
                        'ReturnEnabled': True,
                        'SortEnabled': True}},
})


def main(args):
    csc = boto3.client('cloudsearch')

    # Create the domain if it doesn't exist
    res = csc.describe_domains(DomainNames=[args.domain])
    if res['DomainStatusList'] == []:
        print('Creating domain, this can take a while.')
        csc.create_domain(DomainName=args.domain)

    # Create or update the indexes
    if res['DomainStatusList'] and not args.update:
        print('Existing domain, use "--update" to update indexes')
        exit(1)
    print('Updating indices...')
    fields_now = get_fields(args.domain)
    need_reindex = False
    for name, field in INDEXES.items():
        if name in fields_now and field == fields_now[name]:
            print('Skipping same definition for field=%s' % name)
            continue
        print('Update field=%s' % name)
        if name not in fields_now:
            print('Create  field=%s' % field)
        else:
            print('Update  field=%s' % field)
            print('Current field=%s' % fields_now[name])
        res = csc.define_index_field(DomainName=args.domain, IndexField=field)
        state = res['IndexField']['Status']['State']
        version = res['IndexField']['Status']['UpdateVersion']
        print('Index "%s" State=%s Version=%s' % (field['IndexFieldName'], state, version))
        if state == 'RequiresIndexDocuments':
            need_reindex = True

    print('Indexing docs...')
    if need_reindex:
        res = csc.index_documents(DomainName=args.domain)
        print('Indexing fields: %s' % res['FieldNames'])
    else:
        print('Indexing docs not needed')


if __name__ == '__main__':
    parser = ArgumentParser(description=('Create "title", and exact "albums" with humane'
                                         ' text "albums_text" suggester'),
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--domain', required=True,
                        help='cloudsearch domain name')
    parser.add_argument('-u', '--update', default=False, action='store_true',
                        help='cloudsearch domain name')
    args = parser.parse_args()
    main(args)
