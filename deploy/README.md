# Deployment instructions

## Prerequisites

You should have installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Blazectl](https://github.com/samply/blazectl)

## Installation

All of the commands should be executed from the deploy directory.

```bash
cd deploy
```

### Light up the FHIR Store and the Beacon

#### Up the containers

```bash
docker-compose up -d --build
```

#### Load the data

To load the FHIR store we execute the following commands:

```bash
blazectl --server http://localhost:8080/fhir upload fhir_resources/organizations 
blazectl --server http://localhost:8080/fhir upload fhir_resources/cases
```

#### Check the logs

Check the logs until the beacon is ready to be queried:

```bash
docker-compose logs -f beacon
```

## Usage

You can query the beacon using GET or POST. Below, you can find some examples of usage:

> For simplicity (and readability), we will be using [HTTPie](https://github.com/httpie/httpie).

### Using GET

Querying this endpoit it should return the 13 variants of the beacon (paginated):

```bash
http GET http://localhost:5050/api/biosamples
```

### Using POST

You can use POST to make the previous query. With a `request.json` file like this one:

```json
{
    "meta": {
        "apiVersion": "2.0"
    },
    "query": {
        "filters": [{
            "id": "ordo:Orphanet_589"
        }]
    }
}

```

You can execute:

```bash
curl \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "meta": {
        "apiVersion": "2.0"
    },
    "query": {
       "filters": [{
            "id": "ordo:Orphanet_589"
        }]
    }
}' \
  http://localhost:5050/api/biosamples
```