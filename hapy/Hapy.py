from pkg_resources import resource_string
from xml.etree import ElementTree

import requests


HEADERS = {
    'accept': 'application/xml'
}


class HapyException(Exception):

    def __init__(self, r):
        super(HapyException, self).__init__(
            ('HapyException: '
             'request(url=%s, method=%s, data=%s), '
             'response(code=%d, text=%s)') % (
                r.url, r.request.method, r.request.body,
                r.status_code, r.text
            )
        )


class Hapy:

    def __init__(self, base_url, username=None, password=None, insecure=True):
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = base_url
        if None not in [username, password]:
            self.auth = requests.auth.HTTPDigestAuth(username, password)
        else:
            self.auth = None
        self.insecure = insecure

    def __http_post(self, url, data):
        r = requests.post(
            url=url,
            data=data,
            headers=HEADERS,
            auth=self.auth,
            verify=not self.insecure,
            allow_redirects=False
        )
        if r.status_code not in [200, 303, 307]:
            raise HapyException(r)
        return r

    def __http_get(self, url):
        r = requests.get(
            url=url,
            headers=HEADERS,
            auth=self.auth,
            verify=not self.insecure
        )
        if r.status_code != 200:
            print r.request.headers
            print r.headers
            raise HapyException(r)
        return r

    def create_job(self, name):
        self.__http_post(
            url=self.base_url,
            data=dict(
                action='create',
                createpath=name
            )
        )

    def add_job_directory(self, path):
        self.__http_post(
            url=self.base_url,
            data=dict(
                action='add',
                addpath=path
            )
        )

    def build_job(self, name):
        pass

    def launch_job(self, name):
        pass

    def rescan_job_directory(self):
        self.__http_post(
            url=self.base_url,
            data=dict(
                action='rescan'
            )
        )

    def pause_job(self, name):
        pass

    def unpause_job(self, name):
        pass

    def terminate_job(self, name):
        pass

    def teardown_job(self, name):
        pass

    def copy_job(self, src_name, dest_name):
        pass

    def checkpoint_job(self, name):
        pass

    def execute_script(self, name, engine, script):
        r = self.__http_post(
            url='%s/job/%s/script' % (self.base_url, name),
            data=dict(
                engine=engine,
                script=script
            )
        )
        tree = ElementTree.fromstring(r.content)
        raw = tree.find('rawOutput')
        if raw is not None:
            raw = raw.text
        html = tree.find('htmlOutput')
        if html is not None:
            html = html.text
        return raw, html

    def submit_configuration(self, name, cxml):
        pass

    def delete_job(self, name):
        script = resource_string(__name__, 'scripts/delete_job.groovy')
        self.execute_script(name, 'groovy', script)
        self.rescan_job_directory()

    def get_jobs(self):
        r = self.__http_get(self.base_url)
        tree = ElementTree.fromstring(r.content)
        jobs = []
        for job in tree.find('jobs').findall('value'):
            jobs.append({tag.tag: tag.text for tag in list(job)})
        return jobs
