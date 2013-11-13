import os
import tempfile
import time

from pkg_resources import resource_string
from nose.tools import (
    with_setup,
    assert_equals,
    assert_not_equal,
    assert_in,
    assert_not_in
)

import hapy

BASE_URL = 'https://localhost:8443/engine/'

h = None
jobs = None


def setup_func():
    global h, jobs
    h = hapy.Hapy(BASE_URL, username='admin', password='admin')
    jobs = []


def teardown_func():
    for job in jobs:
        try:
            h.terminate_job(job)
            h.teardown_job(job)
        except:
            pass
        h.delete_job(job)


def create(name, cxml='readme'):
    h.create_job(name)
    cxml = resource_string(__name__, 'assets/%s.cxml' % cxml)
    h.submit_configuration(name, cxml)
    jobs.append(name)


def until_status(name, status, attempts=5):
    for _ in xrange(0, attempts):
        s = h.get_job_status(name)
        if s == status:
            return s
        time.sleep(1)
    raise Exception('status %s not reached' % status)


def assert_not_raises(exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exception:
        assert False


@with_setup(setup_func, teardown_func)
def test_instantiate():
    hapy.Hapy(BASE_URL)
    hapy.Hapy(BASE_URL, insecure=False)
    hapy.Hapy(BASE_URL, username='admin')
    hapy.Hapy(BASE_URL, password='admin')
    hapy.Hapy(BASE_URL, username='admin', password='admin')


@with_setup(setup_func, teardown_func)
def test_create():
    name = 'hapy_test_create'
    before = h.get_jobs()
    create(name)
    after = h.get_jobs()
    assert_equals(len(before), len(after) - 1)
    names = [j['shortName'] for j in after]
    assert_in(name, names)


@with_setup(setup_func, teardown_func)
def test_add_job_directory():
    tdir = tempfile.mkdtemp()
    name = os.path.basename(tdir)
    cxml = resource_string(__name__, 'assets/readme.cxml')
    with open(os.path.join(tdir, 'crawler-beans.cxml'), 'w') as fd:
        fd.write(cxml)
    h.add_job_directory(tdir)
    after = h.get_jobs()
    names = [j['shortName'] for j in after]
    assert_in(name, names)
    jobs.append(name)


@with_setup(setup_func, teardown_func)
def test_unbuilt():
    name = 'hapy_test_unbuilt'
    create(name)
    assert_not_raises(Exception, until_status, name, 'Unbuilt')


@with_setup(setup_func, teardown_func)
def test_built():
    name = 'hapy_test_built'
    create(name)
    until_status(name, 'Unbuilt')
    h.build_job(name)
    assert_not_raises(Exception, until_status, name, 'NASCENT')


@with_setup(setup_func, teardown_func)
def test_rescan():
    name = 'hapy_test_rescan'
    h.create_job(name)
    script = resource_string(hapy.__name__, 'scripts/delete_job.groovy')
    h.execute_script(name, 'groovy', script)
    before = h.get_jobs()
    h.rescan_job_directory()
    after = h.get_jobs()
    bnames = [j['shortName'] for j in before]
    assert_in(name, bnames)
    anames = [j['shortName'] for j in after]
    assert_not_in(name, anames)


@with_setup(setup_func, teardown_func)
def test_pause():
    name = 'hapy_test_pause'
    create(name, cxml='ucl')
    until_status(name, 'Unbuilt')
    h.build_job(name)
    until_status(name, 'NASCENT')
    h.launch_job(name)
    until_status(name, 'PAUSED')
    h.unpause_job(name)
    until_status(name, 'RUNNING')
    time.sleep(1)
    h.pause_job(name)
    assert_not_raises(Exception, until_status, name, 'PAUSED')


@with_setup(setup_func, teardown_func)
def test_unpause():
    name = 'hapy_test_unpause'
    create(name, cxml='ucl')
    until_status(name, 'Unbuilt')
    h.build_job(name)
    until_status(name, 'NASCENT')
    h.launch_job(name)
    until_status(name, 'PAUSED')
    h.unpause_job(name)
    assert_not_raises(Exception, until_status, name, 'RUNNING')


@with_setup(setup_func, teardown_func)
def test_terminate():
    name = 'hapy_test_unpause'
    create(name, cxml='ucl')
    until_status(name, 'Unbuilt')
    h.build_job(name)
    until_status(name, 'NASCENT')
    h.launch_job(name)
    until_status(name, 'PAUSED')
    h.unpause_job(name)
    until_status(name, 'RUNNING')
    time.sleep(1)
    h.terminate_job(name)
    assert_not_raises(Exception, until_status, name, 'FINISHED')


@with_setup(setup_func, teardown_func)
def test_teardown():
    name = 'hapy_test_unpause'
    create(name, cxml='ucl')
    until_status(name, 'Unbuilt')
    h.build_job(name)
    until_status(name, 'NASCENT')
    h.launch_job(name)
    until_status(name, 'PAUSED')
    h.teardown_job(name)
    assert_not_raises(Exception, until_status, name, 'Unbuilt')


@with_setup(setup_func, teardown_func)
def test_copy_job():
    src_name = 'hapy_test_copy_job_src'
    create(src_name)
    dest_name = 'hapy_test_copy_job_dest'
    h.copy_job(src_name, dest_name)
    names = [j['shortName'] for j in h.get_jobs()]
    assert_in(dest_name, names)
    assert_equals(
        h.get_job_configuration(src_name),
        h.get_job_configuration(dest_name)
    )
    jobs.append(dest_name)


@with_setup(setup_func, teardown_func)
def test_copy_job_as_profile():
    src_name = 'hapy_test_copy_job_src'
    create(src_name)
    dest_name = 'hapy_test_copy_job_dest'
    h.copy_job(src_name, dest_name, as_profile=True)
    info = h.get_job_info(dest_name)
    print info
    assert_equals('true', info['isProfile'])
    jobs.append(dest_name)


@with_setup(setup_func, teardown_func)
def test_delete():
    name = 'hapy_test_delete'
    h.create_job(name)
    before = h.get_jobs()
    h.delete_job(name)
    after = h.get_jobs()
    assert_equals(len(before), len(after) + 1)
    names = [j['shortName'] for j in after]
    assert_not_in(name, names)


@with_setup(setup_func, teardown_func)
def test_delete_alternate_job_directory():
    tdir = tempfile.mkdtemp()
    name = os.path.basename(tdir)
    cxml = resource_string(__name__, 'assets/readme.cxml')
    with open(os.path.join(tdir, 'crawler-beans.cxml'), 'w') as fd:
        fd.write(cxml)
    h.add_job_directory(tdir)
    tree = h.get_info()
    jdir = tree.find('jobsDir').text
    assert os.path.isfile(os.path.join(jdir, '%s.jobpath' % name))
    h.delete_job(name)
    assert not os.path.isfile(os.path.join(jdir, '%s.jobpath' % name))


@with_setup(setup_func, teardown_func)
def test_get_jobs():
    create('hapy_test_get_jobs')
    names = [j['shortName'] for j in h.get_jobs()]
    assert_in('hapy_test_get_jobs', names)


@with_setup(setup_func, teardown_func)
def test_execute_script():
    create('hapy_test_execute_script')
    script = resource_string(__name__, 'assets/print_jobname.groovy')
    raw, html = h.execute_script('hapy_test_execute_script', 'groovy', script)
    assert_equals('hapy_test_execute_script', raw)
    assert_equals('hapy_test_execute_script', html)


@with_setup(setup_func, teardown_func)
def test_launched():
    name = 'hapy_test_launched'
    create(name)
    until_status(name, 'Unbuilt')
    h.build_job(name)
    until_status(name, 'NASCENT')
    h.launch_job(name)
    assert_not_raises(Exception, until_status, name, 'PAUSED')


@with_setup(setup_func, teardown_func)
def test_submit_configuration():
    name = 'test_submit_configuration'
    h.create_job(name)
    before = h.get_job_configuration(name)
    cxml = resource_string(__name__, 'assets/readme.cxml')
    h.submit_configuration(name, cxml)
    after = h.get_job_configuration(name)
    assert_not_equal(before, after)
    assert_equals(cxml, after)
    jobs.append(name)
