SQLite Database Setup (Schema + Seed)

This project uses SQLite with separate schema and seed scripts to initialize the database.

📤 Exporting Schema and Seed Files

From an existing database (weather.db):

Export schema (table structure only):

sqlite3 weather.db .schema > schema.sql

Export seed data (table contents):

sqlite3 weather.db

Then inside the SQLite prompt:

.mode insert users
.output seed.sql
SELECT * FROM users;

.mode insert stations
SELECT * FROM stations;

.mode insert user_stations
SELECT * FROM user_stations;

.output stdout
.exit
📥 Initializing a New Database

To create a fresh database and load schema + data:

sqlite3 weather.db < schema.sql
sqlite3 weather.db < seed.sql
✅ Verification

Optional: verify tables were created successfully:

sqlite3 weather.db
.tables
SELECT * FROM users;
SELECT * FROM stations;
SELECT * FROM user_stations;
🧠 Notes
schema.sql contains only table definitions
seed.sql contains INSERT statements for initial data
This approach allows easy setup on any machine and clean version control in Git