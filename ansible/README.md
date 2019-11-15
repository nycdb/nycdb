## NYCDB Ansible playbooks

There are two nycdb playbooks: playbook.yml setups a server ready to install the database at /srv/nycdb. api.yml runs the public api at https://api.nycdb.info

To use, setup an Debian Buster server and configure your ansible hosts file. It might end up looking something like this:

``` yaml
nycdb:
  hosts:
    xx.xx.xx.xx:
  vars:
    ansible_user: root
    ansible_ssh_private_key_file: /path/to/your/ssh/key
    ansible_python_interpreter: /usr/bin/python3
    ansible_ssh_common_args: '-o IdentitiesOnly=yes'
```

Set the environment variable `NYCDB_SSH_PUBLIC_KEY_FILE` to the path for the public ssh key you would like to use  for the nycdb user.

``` sh
export NYCDB_SSH_PUBLIC_KEY_FILE=/path/to/ssh/key.pub
```

Then run the playbook: ``` ansible-playbook playbook.yml ```


After it's done. SSH into the server

``` sh
ssh -o IdentitiesOnly=yes -i /path/to/ssh/key nycdb@xx.xx.xx.xx
```

and run:

``` sh
cd /srv/nyc-db
make -j 2 nyc-db DB_PASSWORD=[password from /ansible/credentials/nycdb_psql_pass]

```
