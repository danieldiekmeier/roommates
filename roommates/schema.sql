

CREATE TABLE "expenses" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"title" TEXT,
"amount" INTEGER
);


CREATE TABLE "purchases" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"title" TEXT,
"frequency" INTEGER,
"amount" INTEGER,
"votes" TEXT
);


CREATE TABLE "users" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"name" TEXT,
"last_name" TEXT,
"mail" TEXT,
"birthday" TEXT,
"password" TEXT
);


CREATE TABLE "wiki" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"key" TEXT,
"content" TEXT
);
