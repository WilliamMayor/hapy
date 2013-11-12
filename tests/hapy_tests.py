import os
import tempfile

from pkg_resources import resource_string
from nose.tools import assert_equals, assert_in, assert_not_in

import hapy

BASE_URL = 'https://localhost:8443/engine/'

h = None
jobs = None


def setup():
    global h, jobs
    h = hapy.Hapy(BASE_URL, username='admin', password='admin')
    jobs = []


def teardown():
    for job in jobs:
        h.delete_job(job)


def create(name):
    h.create_job(name)
    jobs.append(name)


def test_instantiate():
    hapy.Hapy(BASE_URL)
    hapy.Hapy(BASE_URL, insecure=False)
    hapy.Hapy(BASE_URL, username='admin')
    hapy.Hapy(BASE_URL, password='admin')
    hapy.Hapy(BASE_URL, username='admin', password='admin')


def test_create():
    before = h.get_jobs()
    create('hapy_test_create')
    after = h.get_jobs()
    assert_equals(len(before), len(after) - 1)
    names = [j['shortName'] for j in after]
    assert_in('hapy_test_create', names)


def test_delete():
    h.create_job('hapy_test_delete')
    before = h.get_jobs()
    h.delete_job('hapy_test_delete')
    after = h.get_jobs()
    assert_equals(len(before), len(after) + 1)
    names = [j['shortName'] for j in after]
    assert_not_in('hapy_test_delete', names)


def test_get_jobs():
    create('hapy_test_get_jobs')
    names = [j['shortName'] for j in h.get_jobs()]
    assert_in('hapy_test_get_jobs', names)


def test_execute_script():
    create('hapy_test_execute_script')
    script = resource_string(__name__, 'assets/print_jobname.groovy')
    raw, html = h.execute_script('hapy_test_execute_script', 'groovy', script)
    assert_equals('hapy_test_execute_script', raw)
    assert_equals('hapy_test_execute_script', html)


def test_add_job_directory():
    tdir = tempfile.mkdtemp()
    cxml = resource_string(__name__, 'assets/readme.cxml')
    with open(os.path.join(tdir, 'crawler-beans.cxml'), 'w') as fd:
        fd.write(cxml)
    h.add_job_directory(tdir)
    after = h.get_jobs()
    names = [j['shortName'] for j in after]
    assert_in(os.path.basename(tdir), names)
    jobs.append(os.path.basename(tdir))
