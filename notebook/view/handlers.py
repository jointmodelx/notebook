#encoding: utf-8
"""Tornado handlers for viewing HTML files."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado import web
from ..base.handlers import IPythonHandler, path_regex
from ..utils import url_escape, url_path_join
# add by xuyufei 2018.08.20
import os

class ViewHandler(IPythonHandler):
    """Render HTML files within an iframe."""
    @web.authenticated
    def get(self, path):
        path = path.strip('/')
        if not self.contents_manager.file_exists(path):
            raise web.HTTPError(404, u'File does not exist: %s' % path)

        # xuyufei add on 2018.08.20
        filepath = os.path.join(self.settings['server_root_dir'], path)
        if os.path.getsize(filepath) > 1024 * 1024:
            raise web.HTTPError(590, u'File is too large to view it, file path: %s' % path)

        basename = path.rsplit('/', 1)[-1]
        file_url = url_path_join(self.base_url, 'files', url_escape(path))
        self.write(
            self.render_template('view.html', file_url=file_url, page_title=basename)
        )

default_handlers = [
    (r"/view%s" % path_regex, ViewHandler),
]
