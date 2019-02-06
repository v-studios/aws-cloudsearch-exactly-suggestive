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

