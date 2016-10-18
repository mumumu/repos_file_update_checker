# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
import email.utils
import os
import smtplib
import tempfile


class TargetRepositoryBase(object):

    def __init__(self, repository_url, repository_local_path):
        self.repository_url = repository_url
        self.repository_local_path = repository_local_path

    def clone(self):
        raise NotImplementedError

    def _update_internal(self):
        raise NotImplementedError

    def update(self):
        if not os.path.exists(self.repository_local_path):
            self.clone()
        self._update_internal()


class TargetFileRevisionBase(object):

    def __init__(self, repository_type, target_file_path):
        self.target_file_path = os.path.realpath(target_file_path)
        self.basename = os.path.basename(target_file_path).split('.')[0]
        self.revision_file_path = os.path.join(
            tempfile.gettempdir(), '.%s.%s.txt' % (repository_type, self.basename))

    @property
    def latest(self):
        raise NotImplementedError

    @property
    def latest_verbose_log(self):
        raise NotImplementedError

    @property
    def latest_log(self):
        raise NotImplementedError

    def check_revision_number(self):
        raise NotImplementedError

    @property
    def previous(self):
        if not os.path.exists(self.revision_file_path):
            return 0
        return self.check_revision_number()

    def save_latest(self):
        with open(self.revision_file_path, 'w') as f:
            f.write(str(self.latest))

    def notify_update_by_mail(self, mail_from, mail_to, smtp_server, smtp_server_port):
        msg = MIMEText(self.latest_verbose_log)
        msg['Subject'] = 'Updated %s: %s' % (self.basename, self.latest_log)
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Date'] = email.utils.formatdate(localtime=True)
        s = smtplib.SMTP(smtp_server, smtp_server_port)
        s.sendmail(mail_from, [mail_to], msg.as_string())
        s.close()
