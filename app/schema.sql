DROP TABLE IF EXISTS tenant;

CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY, 
    password TEXT, 
    last_seen TEXT NULL, 
    tenant_id INTEGER NULL, 
    fullname TEXT NULL, 
    hp TEXT NULL);

CREATE TABLE IF NOT EXISTS pos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nama TEXT, 
    kab TEXT, 
    lonlat TEXT,
    dpl INTEGER NULL,
    sh FLOAT NULL,
    sk FLOAT NULL,
    sm FLOAT NULL,
    min_wlevel FLOAT NULL,
    max_wlevel FLOAT NULL);

CREATE TABLE IF NOT EXISTS logger (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    sn TEXT, 
    pos_id INTEGER NULL, 
    latest_data DATETIME NULL, 
    latest_up DATETIME NULL, 
    created TEXT NULL);

CREATE TABLE IF NOT EXISTS raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    sn VARCHAR(10),
    received TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS hourly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pos_id INTEGER,
    sampling DATETIME,
    num_data INTEGER default 0,
    rain FLOAT NULL,
    wlevel FLOAT NULL,
    num_alarm INTEGER default 0
);

CREATE TABLE IF NOT EXISTS forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    pos_id INTEGER, 
    tanggal TEXT, 
    rain INTEGER NULL, 
    temperature INTEGER NULL, 
    humidity INTEGER NULL, 
    cloud INTEGER NULL, 
    precipitation INTEGER NULL);

CREATE TABLE IF NOT EXISTS alert_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    sensor_id INTEGER, 
    timestamp TEXT, 
    content TEXT NULL);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY, 
    timestamp TEXT, 
    user TEXT NULL, 
    body TEXT default '');
