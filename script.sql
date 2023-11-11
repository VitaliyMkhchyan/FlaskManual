CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    text text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY AUTOINCREMENT,
	name text NOT NULL,
	email text NOT NULL,
	password text NOT NULL,
	avatar BLOB DEFAULT NULL
)
