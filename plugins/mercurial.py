# -*- coding: utf-8 -*-

import os
import subprocess

from . import TargetRepositoryBase, TargetFileRevisionBase


os.environ['HGPLAIN'] = '1'  # disable i18n output


class TargetRepository(TargetRepositoryBase):

    def clone(self):
        subprocess.check_output(
            ['hg',
             'clone',
             '--quiet',
             self.repository_url,
             self.repository_local_path]
        )

    def _update_internal(self):
        os.chdir(self.repository_local_path)
        subprocess.check_output(['hg', 'pull', '-u'])


class TargetFileRevision(TargetFileRevisionBase):

    @property
    def latest(self):
        if not os.path.exists(self.target_file_path):
            raise Exception(
                'target file does not exists: %s' % self.target_file_path)
        hg_log_output = subprocess.check_output(
            [
                'hg', 'log', '-l', '1',
                '--template', '{rev}', self.target_file_path
            ]).decode('utf-8')
        return int(hg_log_output)

    @property
    def latest_verbose_log(self):
        return subprocess.check_output(
            ['hg', 'log', '-l', '1', '-p', '-v', self.target_file_path]).decode('utf-8')

    @property
    def latest_log(self):
        return subprocess.check_output(
            [
                'hg', 'log', '-l', '1',
                '--template', '{desc}', self.target_file_path
            ]).decode('utf-8')

    def check_revision_number(self):
        with open(self.revision_file_path, 'r') as f:
            try:
                return int(f.readline())
            except ValueError:
                raise Exception('revision number is broken')
