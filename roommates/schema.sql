-- Since we're prototyping, let's drop the tables
-- if they already exist.

--DROP TABLE IF EXISTS set_member_questions;
--DROP TABLE IF EXISTS set_questions;
--DROP TABLE IF EXISTS set_members;
--DROP TABLE IF EXISTS sets;

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    last_name TEXT,
    mail TEXT,
    birthday TEXT,
    password TEXT
)