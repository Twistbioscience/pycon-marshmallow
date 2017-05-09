# pycon-marshmallow
Demonstration of Marshmallow schema, SQLAlchemy mutables and SQLAlchemy integration

# Prerequisites
1. Install Python 3.6
2. Install Postgres >9.5 or run an instance of Postgres.app
3. Create a database called pycon_marshmallow
4. Create virtual env
5. Install requirements.txt - psycopg2 installation can require the path to pg_config
6. Open terminal, navigate to repo directory, activate virtual env and add path to PYTHONPATH - easiest is export PYTHONPATH=.

# Available demos

There are 3 scripts in increasing order of complexity:
1. marshmallow_demo demonstrates the use of marshmallow in a sqlalchemy json field
2. mutable_demo demonstrates using mutables nad marshmallow to automatically track changes within the json data
3. graph_demo brings everything together while also demonstrating nested mutation tracking


#Credits

SQLAlchemy was developed by Mike Bayer and other contributors. Licensed under the MIT license - http://www.sqlalchemy.org for more information
Marshmallow was developed by Steven Loria and other contributors. http://marshmallow.readthedocs.io/ for more information

