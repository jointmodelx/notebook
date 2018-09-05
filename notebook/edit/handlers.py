#encoding: utf-8
"""Tornado handlers for the terminal emulator."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado import web
from ..base.handlers import IPythonHandler, path_regex
from ..utils import url_escape
# xuyufei add on 2018.08.20
import os

class EditorHandler(IPythonHandler):
    """Render the text editor interface."""
    @web.authenticated
    def get(self, path):
        path = path.strip('/')
        if not self.contents_manager.file_exists(path):
            raise web.HTTPError(404, u'File does not exist: %s' % path)

        # xuyufei add on 2018.08.20
        filepath = os.path.join(self.settings['server_root_dir'], path)
        if os.path.getsize(filepath) > 1024 * 1024:
            raise web.HTTPError(590, u'File is too large to edit: %s' % path)

        basename = path.rsplit('/', 1)[-1]
        self.write(self.render_template('edit.html',
            file_path=url_escape(path),
            basename=basename,
            page_title=basename + " (editing)",
            )
        )

default_handlers = [
    (r"/edit%s" % path_regex, EditorHandler),
]