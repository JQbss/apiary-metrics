CREATE DATABASE apiary_db;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE apiary_db TO admin;
\c apiary_db
GRANT ALL ON SCHEMA public TO admin;