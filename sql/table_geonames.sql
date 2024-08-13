DROP TABLE IF EXISTS geonames_all ; 
CREATE TABLE geonames_all (
    geonameid INTEGER,
    name VARCHAR(200),
    asciiname VARCHAR(200),
    alternatenames VARCHAR(10000),
    latitude DOUBLE,
    longitude DOUBLE,
    feature_class CHAR(1),
    feature_code VARCHAR(10),
    country_code CHAR(2),
    cc2 VARCHAR(200),
    admin1_code VARCHAR(20),
    admin2_code VARCHAR(80),
    admin3_code VARCHAR(20),
    admin4_code VARCHAR(20),
    population BIGINT,
    elevation INTEGER,
    dem INTEGER,
    timezone VARCHAR(40),
    modification_date DATE
);

INSERT INTO geonames_all SELECT * FROM read_csv("{csv_path}") ; 
ALTER TABLE geonames_all ADD COLUMN geom GEOMETRY ;
UPDATE geonames_all SET geom = ST_POINT(longitude, latitude) ;
ALTER TABLE geonames_all DROP COLUMN latitude ;
ALTER TABLE geonames_all DROP COLUMN longitude ;