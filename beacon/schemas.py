from aiohttp import web

from beacon import conf
from .exceptions import SchemaNotSupported, DefaultSchemaNotSpecified

_SCHEMAS = {
    "resource": {
        "ejprd-resources-v0.3": {
            "entityType": "resources",
            "schema": "ejprd-resources-v0.3",
            "name": "EJPRD schema for resources (QB API version)",
            "url": "https://raw.githubusercontent.com/ejp-rd-vp/query_builder_api/master/versions/v3/schema/resource.json",
            "version": "v0.3"
        },
        "ejprd-resources-v1.0.0": {
            "entityType": "resources",
            "schema": "ejprd-resources-v1.0.0",
            "name": "EJPRD schema for resources",
            "url": "https://raw.githubusercontent.com/ejp-rd-vp/vp-api-specs/main/schemas/biobank-registry-schema.json",
            "version": "v1.0.0"
        }
    },
    "analysis": {
        "beacon-analysis-v2.0.0": {
            "entityType": "analysis",
            "schema": "beacon-analysis-v2.0.0",
            "name": "Default schema for a bioinformatics analysis",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/analyses/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "biosample": {
        "beacon-biosample-v2.0.0": {
            "entityType": "biosample",
            "schema": "beacon-biosample-v2.0.0",
            "name": "Default schema for a biological sample",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/biosamples/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "cohort": {
        "beacon-cohort-v2.0.0": {
            "entityType": "cohort",
            "schema": "beacon-cohort-v2.0.0",
            "name": "Default schema for a cohorts",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/cohorts/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "dataset": {
        "beacon-dataset-v2.0.0": {
            "entityType": "dataset",
            "schema": "beacon-dataset-v2.0.0",
            "name": "Default schema for datasets",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/datasets/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "genomic_variation": {
        "beacon-g_variant-v2.0.0": {
            "entityType": "genomicVariation",
            "schema": "beacon-g_variant-v2.0.0",
            "name": "Default schema for a bioinformatics analysis",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "individual": {
        "beacon-individual-v2.0.0": {
            "entityType": "individual",
            "schema": "beacon-individual-v2.0.0",
            "name": "Default schema for a bioinformatics analysis",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/individuals/defaultSchema.json",
            "version": "v2.0.0"
        }
    },
    "run": {
        "beacon-run-v2.0.0": {
            "entityType": "run",
            "schema": "beacon-run-v2.0.0",
            "name": "Default schema for a bioinformatics analysis",
            "url": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/runs/defaultSchema.json",
            "version": "v2.0.0"
        }
    }
}

_ENTRY_TYPES = {
    "resource": {
        "id": "resource",
        "name": "Resource",
        "ontologyTermForThisType": {
            "id": "dcat:Resource",
            "label": "DCAT Resource"
        },
        "partOfSpecification": "VP API Specs",
        "description": "Resource as defined by EJP-RD Resource Metadata Schema. "
                       "It can be one of Biobank,",
        "defaultSchema": {},
        "additionalSupportedSchemas": []
    },
    "analysis": {
        "id": "analysis",
        "name": "Bioinformatics analysis",
        "ontologyTermForThisType": {
            "id": "edam:operation_2945",
            "label": "Analysis"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "Apply analytical methods to existing data of a specific type.",
        "defaultSchema": {},
        "additionallySupportedSchemas": []
    },
    "biosample": {
        "id": "biosample",
        "name": "Biological Sample",
        "ontologyTermForThisType": {
            "id": "NCIT:C70699",
            "label": "Biospecimen"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "Any material sample taken from a biological entity for testing, diagnostic, propagation, "
                       "treatment or research purposes, including a sample obtained from a living organism or "
                       "taken from the biological object after halting of all its life functions. Biospecimen can "
                       "contain one or more components including but not limited to cellular molecules, cells, "
                       "tissues, organs, body fluids, embryos, and body excretory products. [ NCI ]",
        "defaultSchema": {},
        "additionallySupportedSchemas": []
    },
    "cohort": {
        "id": "cohort",
        "name": "Cohort",
        "ontologyTermForThisType": {
            "id": "NCIT:C61512",
            "label": "Cohort"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "A group of individuals, identified by a common characteristic. [ NCI ]",
        "defaultSchema": {},
        "aCollectionOf": [{"id": "individual", "name": "Individuals"}],
        "additionalSupportedSchemas": []
    },
    "dataset": {
        "id": "dataset",
        "name": "Dataset",
        "ontologyTermForThisType": {
            "id": "NCIT:C47824",
            "label": "Data set"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "A Dataset is a collection of records, like rows in a database or cards in a cardholder.",
        "defaultSchema": {},
        "aCollectionOf": [{"id": "genomicVariation", "name": "Genomic Variants"}],
        "additionalSupportedSchemas": []
    },
    "genomicVariation": {
        "id": "genomicVariation",
        "name": "Genomic Variants",
        "ontologyTermForThisType": {
            "id": "SO:0000735",
            "label": "sequence_location"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "The location of a sequence.",
        "defaultSchema": {},
        "additionallySupportedSchemas": []
    },
    "individual": {
        "id": "individual",
        "name": "Individual",
        "ontologyTermForThisType": {
            "id": "NCIT:C25190",
            "label": "Person"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "A human being. It could be a Patient, a Tissue Donor, a Participant, a Human Study Subject, etc.",
        "defaultSchema": {},
        "additionallySupportedSchemas": []
    },
    "run": {
        "id": "run",
        "name": "Sequencing run",
        "ontologyTermForThisType": {
            "id": "NCIT:C148088",
            "label": "Sequencing run"
        },
        "partOfSpecification": "Beacon v2.0.0",
        "description": "The valid and completed operation of a high-throughput sequencing instrument for a single sequencing process. [ NCI ]",
        "defaultSchema": {},
        "additionallySupportedSchemas": []
    },
}


def get_schemas(entity_type):
    return _SCHEMAS[entity_type]


def get_schema(entity_type, schema_name):
    try:
        schema = get_schemas(entity_type)[schema_name]
    except KeyError:
        raise SchemaNotSupported(entity_type, schema_name)

    return schema


def get_default_schema(entity_type):
    for et in conf.service.entry_types:
        if et.type == entity_type:
            schema = get_schema(entity_type, et.default_schema)
            break
    else:
        raise DefaultSchemaNotSpecified
    return schema


def get_schema_from_query_params(entity_type, params):
    if len(params.meta.requested_schemas) == 0:  # gets the default schema
        schema = get_default_schema(entity_type)
    else:  # gets the first supported schema
        for s in params.meta.requested_schemas:
            try:
                schema = get_schema(entity_type, s)
                break
            except SchemaNotSupported:
                continue
        else:
            raise web.HTTPBadRequest(text="Requested schema not supported")
    return schema


def get_entry_types():
    entry_types = {}
    for et in conf.service.entry_types:
        default_schema = get_schema(et.type, et.default_schema)
        other_schemas = [{
            "id": schema_data["schema"],
            "name": schema_data["name"],
            "referenceToSchemaDefinition": schema_data["url"],
            "schemaVersion": schema_data["version"]
        } for schema_name, schema_data in get_schemas(et.type).items() if schema_name != et.default_schema]

        entry_types[et.type] = _ENTRY_TYPES[et.type]
        entry_types[et.type].update({
            "defaultSchema": {
                "id": default_schema["schema"],
                "name": default_schema["name"],
                "referenceToSchemaDefinition": default_schema["url"],
                "schemaVersion": default_schema["version"]
            },
            "additionalSupportedSchemas": other_schemas
        })

    return {et.type: _ENTRY_TYPES[et.type] for et in conf.service.entry_types}
