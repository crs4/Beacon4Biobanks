FILTER_SPEC = {
    "terms": {
        "ordo": {
            "type": "ontology",
            "attribute": "diagnosis_available",
            "label": "Disease using an orphanet code (e.g., ordo:Orphanet_589)",
            "operator": "in",
            "mapper": lambda v: v.replace("ordo:Orphanet_", "ORPHA:"),
        },
        "Orphanet_": {  # legacy filter for Orphanet code for to support old vp api spec
            "type": "custom",
            "attribute": "diagnosis_available",
            "label": "Disease using an orphanet code (e.g., Orphanet_589)",
            "operator": "in",
            "mapper": lambda v: v.replace("Orphanet_", "ORPHA:"),
        },
        "ejprd:Biobank": {
            "type": "ontology",
            "attribute": "",
            "label": "The type ejprd:Biobank",
            "operator": "",
            "mapper": lambda v: "",
        },
        "dct:spatial": {
            "type": "alphanumeric",
            "label": "Country using ISO 2 digit format",
            "attribute": "country",
            "operator": "in",
            "mapper": lambda v: v
        },
        "country": {
            "type": "alphanumeric",
            "label": "Country using ISO 2 digit format",
            "attribute": "country",
            "operator": "in",
            "mapper": lambda v: v
        }
    },
    "resources": [{
        "id": "ordo",
        "name": "Orphanet Ontology",
        "url": "https://www.orphadata.com/data/ontologies/ordo/last_version/ORDO_en_4.4.owl",
        "version": "4.4",
        "namespacePrefix": "ordo",
        "iriPrefix": "http://www.orpha.net/ORDO/"
    }, {
        "id": "dcat",
        "name": "DCAT 2 Vocabulary",
        "url": "https://www.w3.org/ns/dcat2.ttl",
        "version": "2.0",
        "namespacePrefix": "dcat",
        "iriPrefix": "http://www.w3.org/ns/dcat#"
    }, {
        "id": "dct",
        "name": "DCMI Metadata Terms",
        "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "version": "2020-01-20",
        "namespacePrefix": "dct",
        "iriPrefix": "http://purl.org/dc/terms/"
    }, {
        "id": "rdf",
        "name": "Resource Description Framework",
        "url": "https://www.w3.org/TR/rdf11-concepts/",
        "version": "2020-01-20",
        "namespacePrefix": "rdf",
        "iriPrefix": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    }, {
        "id": "ejp-rd",
        "name": "EJP-RD Vocabulary",
        "url": "https://w3id.org/ejp-rd/",
        "version": "",
        "namespacePrefix": "ejp-rd",
        "iriPrefix": "https://w3id.org/ejp-rd/vocabulary#"
    }, {
        "id": "sio",
        "name": "Semantic Science Ontology",
        "url": "http://semanticscience.org/ontology/sio.owl",
        "version": "",
        "namespacePrefix": "sio",
        "iriPrefix": "http://semanticscience.org/ontology/"
    }, {
        "id": "ncit",
        "name": "NCIT",
        "url": "http://purl.obolibrary.org/obo/ncit.owl",
        "version": "2023-101-19",
        "namespacePrefix": "ncit",
        "iriPrefix": "http://purl.obolibrary.org/obo/NCIT_"
    }]
}


def get_filter_spec(ot):
    if ot == 'ejprd:Biobank':
        return ot
    else:
        curie_prefix, curie_value = ot.split(':')
        try:
            return FILTER_SPEC['terms'][curie_prefix]
        except KeyError:
            return None
