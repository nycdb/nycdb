require 'nyc_geosupport'
require 'smarter_csv'
require 'csv'
require 'sequel'
require 'thor'

BBL_LOOKUP = {
  'MANHATTAN' => '1',
  'BRONX' => '2',
  'THE BRONX' => '2',
  'THE_BRONX' => '2',
  'BROOKLYN' => '3',
  'BLKN' => '3',
  'QUEENS' => '4',
  'QUEENS COUNTY' => '4',
  'STATEN ISLAND' => '5',
  'STATEN_ISLAND' => '5',
  '1' => '1',
  '2' => '2',
  '3' => '3',
  '4' => '4',
  '5' => '5',
  1 => '1',
  2 => '2',
  3 => '3',
  4 => '4',
  5 => '5'
}

def exists(x)
  return false if x.nil? || x.strip == ''
  true
end

# str, str, str, <NYC GeoSupport Client>
def geocode(house, street, boro, geo)
  geo.run(house_number_display_format: house, street_name1: street, b10sc1: boro)

  if geo.response[:work_area_1][:geosupport_return_code] == "00"
    bbl_hash = geo.response[:work_area_2][:bbl]
    bbl_hash[:borough] + bbl_hash[:block] + bbl_hash[:lot]
  end
end

def add_bbl(row, geo)
  row[:bbl] = nil
  boro = BBL_LOOKUP[row[:borough]]
  address = row[:incident_address]
  return if address.nil?
  house = address.split(' ')[0]
  street = address.split(' ')[1..-1].join(' ')

  if exists(boro) && exists(house) && exists(street)
    row[:bbl] = geocode(house, street, boro, geo)
  end

end

def pg_connection_str(user, pass, host, db)
  "postgres://#{user}:#{pass}@#{host}/#{db}"
end

def run(csv_file, user, pass, host, db)
  key_mapping = { :"x_coordinate_(state_plane)" => :x_coordinate,  :"y_coordinate_(state_plane)" => :y_coordinate }

  geo = NycGeosupport.client geo_function: '1A'
  db = Sequel.connect(pg_connection_str(user, pass, host, db))

  SmarterCSV.process(csv_file, :key_mapping => key_mapping).each do |x|
    add_bbl(x, geo)

    db.transaction { db[:complaints_311].insert(x) }
  end
end

class Parse311 < Thor
  class_option :user, :default => 'nycdb'
  class_option :pass, :default => 'nycdb'
  class_option :host, :default => '127.0.0.1'
  class_option :database, :default => 'nycdb'

  desc "parse FILE", "inserts 311 data into postgres"
  def parse(file)
    puts "Processing: #{file}"
    run(file, options[:user], options[:pass], options[:host], options[:database])
  end

  desc "create_table", "Creates complaints_311 table"
  def create_table()
    db = Sequel.connect(pg_connection_str(options[:user], options[:pass], options[:host], options[:database]))
    db.run(IO.read('./schema.sql'))
  end

  desc "drop_table", "Drops complaints_311 table if it exists"
  def drop_table()
    db = Sequel.connect(pg_connection_str(options[:user], options[:pass], options[:host], options[:database]))
    db.run('DROP TABLE IF EXISTS complaints_311')
  end

end

Parse311.start(ARGV)
