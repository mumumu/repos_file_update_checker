# -*- coding: utf-8 -*-

import os
import subprocess
import io

from . import TargetRepositoryBase, TargetFileRevisionBase


class TargetRepository(TargetRepositoryBase):

    def clone(self):
        subprocess.check_output(
            ['git',
             'clone',
             self.repository_url,
             self.repository_local_path]
        )

    def _update_internal(self):
        os.chdir(self.repository_local_path)
        subprocess.check_output(['git', 'pull'])


class TargetFileRevision(TargetFileRevisionBase):

    @property
    def _latest_revision_io(self):
        return io.StringIO(
            subprocess.check_output(
                [
                    'git', 'log', '-1', self.target_file_path
                ]
            ).decode('utf-8')
        )

    @property
    def latest(self):
        if not os.path.exists(self.target_file_path):
            raise Exception(
                'target file does not exists: %s' % self.target_file_path)
        return self._latest_revision_io.readline().strip().split(' ')[1]

    @property
    def latest_verbose_log(self):
        return subprocess.check_output(
            ['git', 'log', '-1', '-p', self.target_file_path]).decode('utf-8')

    @property
    def latest_log(self):
        return self._latest_revision_io.readlines()[4].strip()

    def check_revision_number(self):
        with open(self.revision_file_path, 'r') as f:
            return f.readline().strip()
