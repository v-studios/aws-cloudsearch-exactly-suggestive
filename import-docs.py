#!/usr/bin/env python
# Import the specified JSON export to the new CS domain for testing.
# Batch them to just under 5MB for efficiency.

import json
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from lib import get_doc_client, get_fields

BATCHBYTES = 4 * 1024 * 1024  # 5MB is limit

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def send_batch(csd, batch):
    """Send a batch of docs, return the elided CS upload result."""
    try:
        res = csd.upload_documents(documents=json.dumps(batch),
                                   contentType='application/json')
        res.pop('ResponseMetadata')
        return res
    except Exception as err:
        print('err=%s' % err)
        import pdb; pdb.set_trace()


def main(options):
    csd = get_doc_client(options.domain)
    log.info('Reading file %s' % options.jsonfile)
    docs_json = open(options.jsonfile, 'r').read()
    docs = json.loads(docs_json)
    num_docs = len(docs)
    indices = get_fields(options.domain)
    bytesize = 0
    batch = []
    # JSON file is like: [{id: id1, fields: {field1: [...], field2: [...], ...}]
    # Note that all individual fields are lists, why? So we have to un-list these
    # for non-array indices: owner, center, date_created, nasa_id, title, media_type
    log.info('Sending %s docs...' % num_docs)
    for num, doc in enumerate(docs, 1):
        fields = doc['fields']
        for k, v in fields.items():
            if '-array' not in indices[k]['IndexFieldType']:
                fields[k] = v[0]  # turn list into scalar, not text-array, lteral-array
        batch.append({'type': 'add', 'id': doc['id'], 'fields': fields})
        bytesize = len(repr(batch))
        if bytesize > options.batchbytes:
            res = send_batch(csd, batch)
            log.info('Sent %s%% %s/%s bytesize=%s len=%s res=%s' % (
                int(100 * num / num_docs), num, num_docs, bytesize, len(batch), res))
            batch = []
    res = send_batch(csd, batch)  # send final accumulation
    log.info('Final %s%% %s/%s bytesize=%s len=%s res=%s' % (
        int(100 * num / num_docs), num, num_docs, bytesize, len(batch), res))



if __name__ == '__main__':
    parser = ArgumentParser(description='Import JSON export to CS domain for testing',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--jsonfile', required=True,
                        help='name fo JSON data file')
    parser.add_argument('-d', '--domain', required=True,
                        help='cloudsearch domain name')
    parser.add_argument('-b', '--batchbytes', type=int, default=BATCHBYTES,
                        help='batch size in bytes, 5MB max')
    args = parser.parse_args()
    main(args)
