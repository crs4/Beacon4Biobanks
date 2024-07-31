TEST_ENV = 'DEV'
BEARER_TOKEN = ''
TEST_COLLECTION = 'bbmri-eric:ID:EXT_76823:collection:MainCollection'
PROD_PORT = 5062
DEV_PORT = 5050


def get_base_uri():
    if TEST_ENV == 'PROD':
        return f'https://rd-connect-samples-discovery.bbmri-eric.eu:{PROD_PORT}'
    return f'http://localhost:{DEV_PORT}'


def get_headers():
    if TEST_ENV == 'DEV':
        return {'auth-key': 'd1adfc4acd05d93c9738d78593f4a1d89d0c906c3dedfb99ad2a187f77e23099',
                'X-Resource-ID': TEST_COLLECTION.replace(':', '-').replace('_', '-')}
    return {"Content-Type": "application/json", 'Authorization': f'Bearer {BEARER_TOKEN}'}
