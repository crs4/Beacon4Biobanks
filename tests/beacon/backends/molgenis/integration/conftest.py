import os.path

import pytest
from molgenis.client import Session
from molgenis.errors import MolgenisRequestError

from beacon import conf

NUM_BIOBANKS = 4
NUM_COLLECTIONS = 14


@pytest.fixture(scope="session", autouse=True, )
def load_test_data(request):
    try:
        session = get_testing_session()
    except Exception:
        print('Connection refused')
    else:
        try:
            session.get_by_id('eu_bbmri_eric_biobanks', 'bbmri:eric-biobank-1')
            print('test data already present')
        except MolgenisRequestError:
            print('loading test data...')
            base_dir = os.path.dirname(__file__)
            session.upload_zip(os.path.join(base_dir, './resources/molgenis_test_data.xlsx'))
            loaded = False
            while not loaded:
                try:
                    biobanks = session.get('eu_bbmri_eric_biobanks')
                    collections = session.get('eu_bbmri_eric_collections')
                except MolgenisRequestError:
                    pass
                else:
                    if len(biobanks) == NUM_BIOBANKS and len(collections) == NUM_COLLECTIONS:
                        loaded = True
            print('loaded')


def get_testing_session():
    s = Session("http://molgenis:8080")
    s.login('admin', 'admin')
    return s
