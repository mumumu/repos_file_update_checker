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
NOTIFY_MAIL_FROM = 'noreply@localhost'
```

Finally, you execute update check command.
You will register the last command on the job scheduler like crontab.

```
$ python rev_update_checker.py -h
usage: rev_update_checker.py [-h]
                             {git,mercurial} target_file notify_mail_addr
                             clone_repos_url clone_local_path

specific file Revision Update Checker for git, mercurial

positional arguments:
  {git,mercurial}   repository type
  target_file       revision check target file
  notify_mail_addr  your mail address
  clone_repos_url   repository url
  clone_local_path  clone repository local path

optional arguments:
  -h, --help        show this help message and exit
```

- on git

```
$ python rev_update_checker.py git pep-0008.txt you@yourmail.address https://github.com/python/peps.git /path/to/your_local_repos
```

- on mercurial

```
$ python rev_update_checker.py mercurial pep-0008.txt you@yourmail.address https://hg.python.org/peps/ /path/to/your_local_repos
```
