

CREATE TABLE "errands" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"title" TEXT
);


CREATE TABLE "expenses" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"title" TEXT,
"amount" INTEGER
);


CREATE TABLE "messages" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"author" INTEGER,
"message" TEXT,
"date" TEXT
);


CREATE TABLE "purchases" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"title" TEXT,
"amount" INTEGER,
"date" TEXT
);


CREATE TABLE "receipts" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"title" TEXT,
"amount" REAL,
"user" INTEGER,
"date" TEXT
);


CREATE TABLE "uploads" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"wiki_id" INTEGER,
"description" TEXT,
"filename" TEXT
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
