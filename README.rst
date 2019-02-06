=====================================
 AWS CloudSearch: Exactly Suggestive
=====================================

This sample code is intended to accompany a blog post and presentation
about using AWS CloudSearch to get exact queries as well as
human-friendly suggestions of the exact names.

create-domain-indexes.py
========================

Use this to create a new index and domains, or update indexes on an
existing domain. If an index already exists, it won't be updated. If
any index changes, it will initiate reindexing. For example::

  ./create-indexes.py --domain exactly-suggestive --update

The indexes it creates are:

* ``title``: text index which is single valued (only one title is possible)
* ``albums``: exact-match literal-array (multivalued, case-sensitive,
  no stemming/splitting)
  case-insensitive, with stemming/splitting)
* ``albums_text``: for the suggester, a text-array (multivalued,
  case-insenstive, with stemming and splitting)

import-docs.py
==============

We've created a ``sample-docs.json`` file with titles and albums
pulled from production, but all the details redacted. When the data
has no albums, we inject 1-4 Rock'n'Roll album names so you can
experiment with suggesters.

You can import this (or a modified set of of docs) like::

  ./import-docs.py --jsonfile sample-docs.json --domain exactly-suggestive

  INFO:__main__:Reading file sample-docs.json
  INFO:__main__:Sending 166331 docs...

The importer batches updates into about 4MB chunk size to avoid
CloudSearch bottlenecks that would occur with
single-doc-at-a-time-updates. Never the less, it can take a while to
send and ingest those docs. Afterwards, it may take a while for
CloudSearch to to actually index these documents so they are
searchable.

00:20:00?

TODO: maybe I should have a --maxdocs instead of sending all 166K?
