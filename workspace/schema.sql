-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS diagnosis;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_1 TEXT NOT NULL
);

CREATE TABLE diagnosis (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  email TEXT NOT NULL,
  username TEXT NOT NULL,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  dob TEXT NOT NULL,
  sex TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE QR_INFO (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  contact INTEGER NOT NULL,
  Id INTEGER NOT NULL,
  address TEXT NOT NULL,
  age INTEGER NOT NULL,
  kName TEXT NOT NULL,
  kContact INTEGER NOT NULL,
  kId INTEGER NOT NULL,
  kAddress TEXT NOT NULL,
  chronic TEXT NOT NULL,
  allergies TEXT NOT NULL,
  chronic1 TEXT NOT NULL,
  allergies1 TEXT NOT NULL,
  mental TEXT NOT NULL,
  mental1 TEXT NOT NULL,
  medication TEXT NOT NULL,
  medication1 TEXT NOT NULL,
  FOREIGN KEY (Id) REFERENCES diagnosis (id)
)