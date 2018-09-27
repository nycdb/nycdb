## NYCDB Ansible playbook

In the ` /ansible ` folder there are two playbooks. playbook.yml setups a server ready to install the database at /srv/nycdb. api.yml runs the public api at https://api.nycdb.info

To use, create a fresh debian stretch server and configure your ansible hosts file. It might end up looking something like this:

```
[nycdb]
xx.xx.xx.xx ansible_user=root ansible_ssh_private_key_file=/path/to/ssh/key
```

Then run the playbook: ``` cd ansible && ansible-playbook playbook.yml ```

After it's done. SSH into the server and run:

``` bash
cd /srv/nyc-db
make -j 2 nyc-db DB_PASSWORD=[password from /ansible/credentials/nycdb_psql_pass]

```
