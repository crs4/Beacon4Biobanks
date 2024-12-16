# Beacon v2.x

<!-- [![Testsuite](https://github.com/EGA-archive/beacon-2.x/workflows/Testsuite/badge.svg)](https://github.com/EGA-archive/beacon-2.x/actions) -->

This repository is an implementation of the [Beacon v2.0 Model](https://github.com/ga4gh-beacon/beacon-v2-Models) and 
extends the [Reference Implementation](https://github.com/EGA-archive/beacon2-ri-api) by implementing a [FHIR](https://hl7.org/fhir/)
endpoint that allows to query /individuals and /biosamples endpoints from a FHIR Store that contains data represented as
FHIR Resources compliant with the [BBMRI Sample Locator](https://samply.github.io/bbmri-fhir-ig/overview.html) model.

For the deployment and the documentation of the Beacon reference implementation please refer to the main [repository](https://github.com/EGA-archive/beacon2-ri-api).

Here only the deployment with a FHIR backend is documented

## Deployment

To deploy a Beacon service that queries data from a FHIR store, it is possible to use Docker.

### Conf file

The docker image needs a configuration file mounted at `/beacon/config.yml` path of the container

To create a `config.yml` file, use the `conf/config.fhir.yml` template and edit it
with the information of your beacon. 

In particular fill:
  - **Info section**: just some data about the beacon
  - **Organization**: information about the organization that is exposing the beacon
  - **Project Info**:
  - **FHIR Store Info**: connection parameters of the FHIR Store to use as backend

### Environment variables

Three environment variables, all related to Nginx, must be set:
  - SERVER_NAME: same as Nginx's server name directive
  - PORT: the port used for the service
  - SSL_ENABLED: true or false to enable SSL (recommended)

### SSL

In case SSL is enabled, the key-certificate pair must be mounted on `/etc/ssl/certs/beacon.key` and 
`/etc/ssl/certs/beacon.cert`  

### Example

The  `/deploy/docker-compose.fhir.yaml` is an example that deploy a Beacon and the FHIR store to query.

An example of a standalone Beacon service that queries an external FHIR store is:

`docker run -e SERVER_NAME=beacon -e PORT=5050 -e SSL_ENABLED=false -v <conf-file>:/beacon/beacon/conf.py -p 5050:5050 crs4/beacon:2.0-fhir`


## Acknowledgments

This work has been partially supported by the following sources:
 * The [European Joint Programme on Rare Disease (EJPRD)](https://www.ejprarediseases.org/) project (grant agreement N. 825575)
