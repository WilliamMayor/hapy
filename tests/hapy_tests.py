from pkg_resources import resource_string
from xml.etree import ElementTree

import requests

from mock import (
    patch,
    Mock
)
from nose.tools import (
    raises,
    assert_is_none,
    assert_equals
)

import hapy

BASE_URL = 'https://localhost:8443'
h = None


def setup():
    global h
    h = hapy.Hapy(BASE_URL)


def test_url_normalise():
    h1 = hapy.Hapy('http://localhost:8443')
    h2 = hapy.Hapy('http://localhost:8443/')
    assert_equals(h1.base_url, h2.base_url)


def test_auth_nothing():
    h = hapy.Hapy(BASE_URL)
    assert_is_none(h.auth)


def test_auth_no_password():
    h = hapy.Hapy(BASE_URL, username='username')
    assert_is_none(h.auth)


def test_auth_no_username():
    h = hapy.Hapy(BASE_URL, password='password')
    assert_is_none(h.auth)


def test_auth():
    h = hapy.Hapy(
        BASE_URL,
        username='username',
        password='password'
    )
    a = requests.auth.HTTPDigestAuth('username', 'password')
    assert_equals(
        a.username,
        h.auth.username
    )
    assert_equals(
        a.password,
        h.auth.password
    )


@raises(hapy.HapyException)
@patch('hapy.hapy.requests')
def test_get_wrong_code(mock_requests):
    r = Mock()
    r.status_code = 404
    r.request = Mock()
    mock_requests.get.return_value = r
    h._http_get('url')


@raises(hapy.HapyException)
@patch('hapy.hapy.requests')
def test_post_wrong_code(mock_requests):
    r = Mock()
    r.status_code = 404
    r.request = Mock()
    mock_requests.post.return_value = r
    h._http_post('url', data='data')


@raises(hapy.HapyException)
@patch('hapy.hapy.requests')
def test_put_wrong_code(mock_requests):
    r = Mock()
    r.status_code = 404
    r.request = Mock()
    mock_requests.put.return_value = r
    h._http_put('url', data='data')


@patch('hapy.hapy.requests')
def test_create_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_create_job'
    h.create_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine',
        data=dict(
            action='create',
            createpath=name
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_add_job_directory(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    path = '/test_add_job_directory'
    h.add_job_directory(path)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine',
        data=dict(
            action='add',
            path=path
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_build_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_build_job'
    h.build_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='build'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_supply_timeout(mock_requests):
    h = hapy.Hapy(BASE_URL, timeout=0.005)
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_build_job'
    h.build_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='build'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=0.005
    )


@patch('hapy.hapy.requests')
def test_launch_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_launch_job'
    h.launch_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='launch'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_rescan_job_directory(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    h.rescan_job_directory()
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine',
        data=dict(
            action='rescan'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_pause_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_pause_job'
    h.pause_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='pause'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_unpause_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_unpause_job'
    h.unpause_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='unpause'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_terminate_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_terminate_job'
    h.terminate_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='terminate'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_teardown_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_teardown_job'
    h.teardown_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='teardown'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_copy_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    src_name = 'test_copy_job'
    dest_name = 'test_copy_job_copy'
    h.copy_job(src_name, dest_name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % src_name,
        data=dict(
            copyTo=dest_name
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_copy_job_as_profile(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    src_name = 'test_copy_job'
    dest_name = 'test_copy_job_copy'
    h.copy_job(src_name, dest_name, as_profile=True)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % src_name,
        data=dict(
            copyTo=dest_name,
            asProfile='on'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_checkpoint_job(mock_requests):
    r = Mock()
    r.status_code = 303
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_checkpoint_job'
    h.checkpoint_job(name)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        data=dict(
            action='checkpoint'
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )


@patch('hapy.hapy.requests')
def test_execute_script(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_execute_script.xml'
    )
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_execute_script'
    engine = 'groovy'
    script = ''
    raw, html = h.execute_script(name, engine, script)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s/script' % name,
        data=dict(
            engine=engine,
            script=script
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )
    assert_is_none(raw)
    assert_is_none(html)


@patch('hapy.hapy.requests')
def test_execute_script_raw(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_execute_script_raw.xml'
    )
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_execute_script'
    engine = 'groovy'
    script = 'rawOut.print("a")'
    raw, html = h.execute_script(name, engine, script)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s/script' % name,
        data=dict(
            engine=engine,
            script=script
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )
    assert_equals("raw", raw)
    assert_is_none(html)


@patch('hapy.hapy.requests')
def test_execute_script_html(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_execute_script_html.xml'
    )
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_execute_script'
    engine = 'groovy'
    script = 'htmlOut.print("a")'
    raw, html = h.execute_script(name, engine, script)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s/script' % name,
        data=dict(
            engine=engine,
            script=script
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )
    assert_equals("html", html)
    assert_is_none(raw)


@patch('hapy.hapy.requests')
def test_execute_script_both(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_execute_script_both.xml'
    )
    r.request = Mock()
    mock_requests.post.return_value = r
    name = 'test_execute_script'
    engine = 'groovy'
    script = 'htmlOut.print("a")\nrawOut.print("b")'
    raw, html = h.execute_script(name, engine, script)
    mock_requests.post.assert_called_with(
        url='https://localhost:8443/engine/job/%s/script' % name,
        data=dict(
            engine=engine,
            script=script
        ),
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        allow_redirects=False,
        timeout=None
    )
    assert_equals("raw", raw)
    assert_equals("html", html)


@patch('hapy.hapy.requests')
def test_submit_configuration(mock_requests):
    r = Mock()
    r.status_code = 200
    r.request = Mock()
    r.content = resource_string(
        __name__,
        'assets/test_get_job_info.xml'
    )
    mock_requests.get.return_value = r
    r = Mock()
    r.status_code = 200
    r.request = Mock()
    mock_requests.put.return_value = r
    name = 'test_submit_configuration'
    h.submit_configuration(name, 'cxml')
    mock_requests.put.assert_called_with(
        url=('https://localhost:8443/engine/job/'
             'test/jobdir/crawler-beans.cxml'),
        data='cxml',
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        timeout=None
    )


def test_tree_to_dict_leaf():
    text = ElementTree.fromstring('<root>something</root>')
    d = dict(root='something')
    assert_equals(d, h._Hapy__tree_to_dict(text))


def test_tree_to_dict_single_child():
    text = ElementTree.fromstring('<root><child>something</child></root>')
    d = dict(root=dict(child='something'))
    assert_equals(d, h._Hapy__tree_to_dict(text))


def test_tree_to_dict_multiple_child():
    text = ElementTree.fromstring(
        '<root><child>something</child><child>something else</child></root>'
    )
    d = dict(root=dict(child=['something', 'something else']))
    assert_equals(d, h._Hapy__tree_to_dict(text))


@patch('hapy.hapy.requests')
def test_get_info(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_get_info.xml'
    )
    r.request = Mock()
    mock_requests.get.return_value = r
    info = h.get_info()
    mock_requests.get.assert_called_with(
        url='https://localhost:8443/engine',
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        timeout=None
    )
    assert_equals('3.1.1', info['engine']['heritrixVersion'])


@patch('hapy.hapy.requests')
def test_get_job_info(mock_requests):
    r = Mock()
    r.status_code = 200
    r.content = resource_string(
        __name__,
        'assets/test_get_job_info.xml'
    )
    r.request = Mock()
    mock_requests.get.return_value = r
    name = 'test_get_job_info'
    info = h.get_job_info(name)
    mock_requests.get.assert_called_with(
        url='https://localhost:8443/engine/job/%s' % name,
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        timeout=None
    )
    assert_equals('test', info['job']['shortName'])


@patch('hapy.hapy.requests')
def test_get_job_configuration(mock_requests):
    name = 'test_get_job_configuration'
    cxml = resource_string(
        __name__,
        'assets/test_get_job_configuration.xml'
    )
    xml = resource_string(
        __name__,
        'assets/test_get_job_info.xml'
    )

    def side_effect(**kwargs):
        r = Mock()
        r.status_code = 200
        r.request = Mock()
        r.content = cxml if ('cxml' in kwargs['url']) else xml
        return r

    mock_requests.get.side_effect = side_effect
    config = h.get_job_configuration(name)
    mock_requests.get.assert_called_with(
        url='https://localhost:8443/engine/job/test/jobdir/crawler-beans.cxml',
        auth=None,
        verify=False,
        headers={'accept': 'application/xml'},
        timeout=None
    )
    assert_equals(cxml, config)
