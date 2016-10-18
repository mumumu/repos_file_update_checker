#!/usr/bin/env python

from __future__ import print_function

import argparse
import importlib


NOTIFY_SMTP_SERVER = 'localhost'
NOTIFY_SMTP_SERVER_PORT = 25
NOTIFY_MAIL_FROM = 'noreply@localhost'


class PluginLoader(object):

    def __init__(self, plugin_type):
        self.type = plugin_type

    def _load(self, classname):
        module_name = 'plugins.%s' % self.type
        module = importlib.import_module(module_name)
        return getattr(module, classname)

    def load_repository(self, repos_url, local_path):
        return self._load('TargetRepository')(repos_url, local_path)

    def load_revision(self, target_file_path):
        return self._load('TargetFileRevision')(target_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='specific file Revision Update Checker for git, mercurial')
    parser.add_argument(
        'type',
        choices=['git', 'mercurial'],
        help='repository type')
    parser.add_argument(
        'target_file',
        help='revision check target file')
    parser.add_argument(
        'notify_mail_addr',
        help='your mail address')
    parser.add_argument(
        'clone_repos_url',
        help='repository url')
    parser.add_argument(
        'clone_local_path',
        help='clone repository local path')

    args = parser.parse_args()

    plugin = PluginLoader(args.type)
    target_repository = plugin.load_repository(
        args.clone_repos_url,
        args.clone_local_path
    )
    target_repository.update()
    target_revision = plugin.load_revision(args.target_file)
    if target_revision.latest != target_revision.previous:
        target_revision.notify_update_by_mail(
            NOTIFY_MAIL_FROM,
            args.notify_mail_addr,
            NOTIFY_SMTP_SERVER,
            NOTIFY_SMTP_SERVER_PORT
        )
        target_revision.save_latest()
