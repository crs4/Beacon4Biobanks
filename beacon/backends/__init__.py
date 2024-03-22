from beacon import conf

if conf.service.backend == 'fhir':
    from .fhir import analyses, biosamples, cohorts, datasets, g_variants, individuals, runs, filtering_terms
    from .fhir.handlers import filtering_terms_handler, collection_handler, generic_handler
elif conf.service.backend == 'molgenis':
    from .molgenis import analyses, biosamples, cohorts, datasets, g_variants, individuals, runs, filtering_terms
    from .molgenis.handlers import filtering_terms_handler, collection_handler, generic_handler
else:
    raise "configuration error. Backend not available"
