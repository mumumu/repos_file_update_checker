## File update checker on Git or Mercurial Repository

You can check specific file update history on Mercurial or Git Repository and notify it via email.

## Motivation

I wanted to check update history ONLY pep-0008.txt on hg.python.org, but commit mail archive ML was closed -- for PEP editiors only and could not get specific file history log from hg.python.org atom feed. This is a motivation for creating this tool.

## Requirement

This program is tested only on `*nix`. Patches are welcome.

- Mercurial or git
- Python 2.7 or later

## Usage

```
$ git clone git@github.com:mumumu/repos_file_update_checker.git
```

You can change the following setting on `rev_update_checker.py`

```python
NOTIFY_SMTP_SERVER = 'localhost'
NOTIFY_SMTP_PORT = 25
NOTIFY_MAIL_FROM = 'nobody@yourdomain'
```

Finally, you execute update check command.
You will register the last command on the job scheduler like crontab.

- on mercurial

```
$ python rev_update_checker.py --type=mercurial pep-0008.txt you@yourmail.address https://hg.python.org/peps/ /tmp/tmp_peps_dir
```

- on git

```
$ python rev_update_checker.py --type=git pep-0008.txt you@yourmail.address https://github.com/python/peps.git /tmp/tmp_peps_dir
```
