require 'nyc_geosupport'
require 'smarter_csv'
require 'csv'
require 'sequel'
require 'thor'
Sequel.split_symbols = true

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

# modifies row
def add_bbl(row, geo)
  row[:bbl] = nil
  boro = BBL_LOOKUP[row[:borough]]
  address = row[:incident_address]
  return unless exists(address) and address.include?(' ')
  house = address.split(' ')[0]
  street = address.split(' ')[1..-1].join(' ')

  if exists(boro) && exists(house) && exists(street)
    row[:bbl] = geocode(house, street, boro, geo)
  end
end

# {} -> new hash
# basically a non-mutating version of add_bbl
def row_with_bbl(row, geo)
  _row = row.dup
  add_bbl(_row, geo)
  _row
end

def pg_connection_str(user, pass, host, db)
  "postgres://#{user}:#{pass}@#{host}/#{db}"
end

def blank_to_nil(val)
  return nil if val == ''
  val
end

def split_files(csv_file, user, pass, host, db)
  File.open(csv_file) do |f|
    header = f.readline
    count = 0
    s = StringIO.new
    s.write(header)
    f.each_line do |line|
      s.write(line)
      count += 1
      next if count < 10_000
      s.rewind
      run(s, user, pass, host, db)
      count = 0
      s = StringIO.new
      s.write(header)
    end
    s.rewind
    run(s, user, pass, host, db) # final run
  end
end

def run(csv_file, user, pass, host, db)
  key_mapping = { :"x_coordinate_(state_plane)" => :x_coordinate,  :"y_coordinate_(state_plane)" => :y_coordinate }
  geo = NycGeosupport.client geo_function: '1A'
  db = Sequel.connect(pg_connection_str(user, pass, host, db))

  options = { :key_mapping => key_mapping, :chunk_size => 1000, :row_sep => "\n", :col_sep => ",", :quot_char => '"' }
  
  SmarterCSV.process(csv_file, options).each do |chunk|
    batch = chunk.map { |row| row_with_bbl(row, geo) }
    db.transaction do 
      batch.each do |item|
        db[:complaints_311].insert(item)
      end
    end 
  end
  
end

class Parse311 < Thor
  class_option :user, :default => 'nycdb'
  class_option :pass, :default => 'nycdb'
  class_option :host, :default => '127.0.0.1'
  class_option :database, :default => 'nycdb'

  desc "parse FILE", "inserts 311 data into postgres"
  option :split
  def parse(file)
    if options[:split]
      split_files(file, options[:user], options[:pass], options[:host], options[:database])
    else
      run(file, options[:user], options[:pass], options[:host], options[:database])
    end
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
