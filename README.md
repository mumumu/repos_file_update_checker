## File update checker on Mercurial Repository

You can check specific file update history on Mercurial Repository and notify it via email.

## Motivation

I wanted to check update history ONLY pep-0008.txt on hg.python.org, but commit mail archive ML was closed -- for PEP editiors only and could not get specific file history log from hg.python.org atom feed. This is a motivation for creating this tool.

## Requirement

- Mercurial
- Python 2.7 or later

## Usage

Usage Example on `*nix`.  
You will register the last command on the job scheduler like crontab.

```
$ cd /tmp
$ hg clone https://hg.python.org/peps
$ python rev_update_checker.py pep-0008.txt you@mail.address /tmp/peps
```

You can change the following setting on `rev_update_checker.py`

```python
NOTIFY_SMTP_SERVER = 'localhost'
NOTIFY_SMTP_PORT = 25
NOTIFY_MAIL_FROM = 'nobody@yourdomain'
```
