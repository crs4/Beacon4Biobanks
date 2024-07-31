TEST_ENV = 'DEV'
PORT = 5050


def get_base_uri():
    if TEST_ENV == 'PROD':
        return f'https://rd-connect-samples-discovery.bbmri-eric.eu:{PORT}'
    return f'http://localhost:{PORT}'
