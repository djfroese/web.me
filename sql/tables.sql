CREATE TABLE Posts (
id integer primary key asc autoincrement,
title text,
body text,
created datetime,
modified datetime
);

CREATE TABLE Users (
id integer primary key asc autoincrement,
username text unique,
pw text,
email text unique,
firstname text,
lastname text,
created datetime,
modifited datetime
);

CREATE TABLE Images (
id integer primary key asc autoincrement,
url text,
pid integer,
album integer,
data blob
);
