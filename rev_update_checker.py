#!/usr/bin/env python

from email.mime.text import MIMEText
import email.utils
import os
import subprocess
import sys
import smtplib
import tempfile


NOTIFY_SMTP_SERVER = 'localhost'
NOTIFY_SMTP_PORT = 25
NOTIFY_MAIL_FROM = 'nobody@yourdomain'


class TargetRepository(object):

    def __init__(self, repository_path):
        self.repository_path = repository_path \
            if os.path.exists(repository_path) else '.'

    def update(self):
        os.chdir(self.repository_path)
        subprocess.check_output(['hg', 'pull'])


class TargetFileRevision(object):

    def __init__(self, target_file_path):
        self.target_file_path = os.path.realpath(target_file_path)
        self.basename = os.path.basename(target_file_path).split('.')[0]
        self.revision_file_path = os.path.join(
            tempfile.gettempdir(), '.%s.txt' % self.basename)

    @property
    def latest(self):
        if not os.path.exists(self.target_file_path):
            raise Exception(
                'target file does not exists: %s' % self.target_file_path)
        hg_log_output = subprocess.check_output(
            [
                'hg', 'log', '-l', '1',
                '--template', '{rev}', self.target_file_path
            ])
        return int(hg_log_output)

    @property
    def previous(self):
        if not os.path.exists(self.revision_file_path):
            return 0
        with open(self.revision_file_path, 'r') as f:
            try:
                return int(f.readline())
            except ValueError:
                raise Exception('revision number is broken')

    @property
    def latest_verbose_log(self):
        return subprocess.check_output(
            ['hg', 'log', '-l', '1', '-p', '-v', self.target_file_path])

    @property
    def latest_log(self):
        return subprocess.check_output(
            [
                'hg', 'log', '-l', '1',
                '--template', '{desc}', self.target_file_path
            ])

    def save_latest(self):
        with open(self.revision_file_path, 'w') as f:
            f.write(str(self.latest))

    def notify_update_by_mail(self, to_mail_addr):
        msg = MIMEText(self.latest_verbose_log)
        from_mail_addr = NOTIFY_MAIL_FROM
        msg['Subject'] = 'Updated %s: %s' % (self.basename, self.latest_log)
        msg['From'] = from_mail_addr
        msg['To'] = to_mail_addr
        msg['Date'] = email.utils.formatdate(localtime=True)
        s = smtplib.SMTP(NOTIFY_SMTP_SERVER, NOTIFY_SMTP_PORT)
        s.sendmail(from_mail_addr, [to_mail_addr], msg.as_string())
        s.close()


if __name__ == '__main__':
    os.environ['HGPLAIN'] = '1'  # disable i18n output
    if len(sys.argv) < 3:
        print 'usage: python rev_update_checker.py ' \
            '[target file] [notify_mail_addr] [cloned_repository_path]'
        sys.exit(1)

    cloned_repository_path = '.' if len(sys.argv) == 3 else sys.argv[3]

    TargetRepository(cloned_repository_path).update()
    revision = TargetFileRevision(sys.argv[1])
    if revision.latest > revision.previous:
        revision.notify_update_by_mail(sys.argv[2])
        revision.save_latest()
