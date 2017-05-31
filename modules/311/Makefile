DB_HOST ?= '127.0.0.1'
DB_DATABASE ?= nycdb
DB_USER ?= nycdb
DB_PASSWORD ?= nycdb

export LD_LIBRARY_PATH := $(shell pwd)/version-17a_17.1/lib/
export GEOFILES := $(shell pwd)/version-17a_17.1/fls/
export LIBGEO_PATH := $(shell pwd)/version-17a_17.1/lib/libgeo.so

setup: download
# 	ignoring errors here because the gems might be already installed
#       as is the case with the ansible setup
	-gem install bundler --no-ri --no-rdoc
	-bundle install

run:
	ruby parse.rb create_table --user=$(DB_USER) --host=$(DB_HOST) --pass=$(DB_PASSWORD) --database=$(DB_DATABASE)
	ruby parse.rb parse --user=$(DB_USER) --host=$(DB_HOST) --pass=$(DB_PASSWORD) --database=$(DB_DATABASE) 311.csv


download: gdelx_17a.zip version-17a_17.1 311.csv


gdelx_17a.zip:
	wget http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/gdelx_17a.zip

version-17a_17.1: 
	unzip gdelx_17a.zip

311.csv:
	wget https://data.cityofnewyork.us/api/views/7y5a-jzir/rows.csv?accessType=DOWNLOAD -O 311.csv

clean:
	rm -f 311.csv
	ruby parse.rb drop_table --user=$(DB_USER) --host=$(DB_HOST) --pass=$(DB_PASSWORD) --database=$(DB_DATABASE)


.PHONY: setup run download clean
