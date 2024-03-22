from beacon.backends.fhir.cql.models import FHIRResource


class Library(FHIRResource):
    def __init__(self, version_id, last_updated, data, id, url):
        self.version_id = version_id
        self.last_updated = last_updated
        self.data = data
        self.id = id
        self.url = url
        super(Library, self).__init__({
            "meta": {
                "versionId": self.version_id,
                "lastUpdated": self.last_updated
            },
            "content": [{
                "contentType": 'text/cql',
                "data": self.data
            }],
            "resourceType": "Library",
            "id": self.id,
            "url": self.url
        })
