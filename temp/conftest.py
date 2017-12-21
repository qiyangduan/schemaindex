import pytest

import os
from schemaindex.app.config import cfg as config

import sys
@pytest.fixture(scope="session")
def my_setup(request):
    print('\nDoing setup by putting init file in conftest')
    print(sys.path)

    open(config['main']['init_indicator_file'], 'a').close()

    def fin():
        print ("\nDoing teardown")
    request.addfinalizer(fin)