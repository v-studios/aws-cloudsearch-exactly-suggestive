import boto3


def get_fields(domain):
    """Return dict of fields and definitions.

    field_name: {'IndexFieldName': 'thename', IndexFieldType': 'thetype', 'TypeSpecificOptions': {...}}
    """
    csc = boto3.client('cloudsearch')
    res = csc.describe_index_fields(DomainName=domain)['IndexFields']
    return {f['Options']['IndexFieldName']: f['Options'] for f in res}


def get_search_domain(domain):
    """Return dict of CS domain specifics including search/doc endpoints, ARN."""
    return boto3.client('cloudsearch').describe_domains(DomainNames=[domain])['DomainStatusList'][0]


def get_search_client(domain):
    """Return a boto3 client for the given seaarch domain_name."""
    cs_domain = get_search_domain(domain)
    return boto3.client('cloudsearchdomain',
                        endpoint_url='https://' + cs_domain['SearchService']['Endpoint'])


def get_doc_client(domain):
    """Return a boto3 client for the given seaarch domain_name."""
    cs_domain = get_search_domain(domain)
    return boto3.client('cloudsearchdomain',
                        endpoint_url='https://' + cs_domain['DocService']['Endpoint'])
