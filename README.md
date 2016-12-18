# Catalog App

Download the Catalog app source code files from [this link](https://github.com/bhaskardua/FSWD-Project-5-Item-Catalog/archive/master.zip).

Unzip the downloaded files to a preferred location on your computer.

Make sure you have Python, PostgreSQL, Psycopg2, Sqlalchemy and Flask installed on your computer. If not download a version of these programs suitable for your operating system from here:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Psycopg2](http://initd.org/psycopg/download/)
- [Sqlalchemy](https://www.sqlalchemy.org/download.html)
- [Flask](https://pypi.python.org/pypi/Flask/)

Alternatively, you can download the Udacity vagrant virtual machine which has all the components pre-installed. Follow the instructions [here](https://www.udacity.com/wiki/ud088/vagrant). If you go down this route then remember to place the downloaded Catalog app files in the same folder on the host machine as the vagrant VM, so that the files can be shared with the vagrant instance.

Open your commmand line application and navigate to the folder where you unzipped the downloaded files.

Create a database in PostgreSQL called `catalogwithusers`. Start the PostgresSQL shell using the command `psql`. Issue the command `CREATE DATABASE catalogwithusers`. Exit the shell by typing `\q`.

Setup the required table structure in that database by executing the command `python database_setup.py`. This will setup an empty database using which the Catalog app can now be run. [Optional] You can also run the command `python lotsofitems.py` to populate the database with some dummy data.

Start the web server by executing the following on the command line - `python application.py`.

Access the Catalog app by visiting [`http://localhost:5000/catalog`](http://localhost:5000/catalog) in your web browser. If you are using the vagrant environment make sure the relevant port (5000) is forwarded from the host to the guest machine as per the instructions [here](https://www.vagrantup.com/docs/networking/forwarded_ports.html).

JSON endpoints:

- <http://localhost:5000/catalog.json> - *JSON for the entire catalog*
- <http://localhost:5000/catalog/JSON/categories/> - *JSON list of category names only*
- <http://localhost:5000/catalog/JSON/\<category_name\>/> - *JSON output for a particular category*
- <http://localhost:5000/catalog/JSON/\<category_name\>/\<item_name\>/> - *JSON output for a particular item*
