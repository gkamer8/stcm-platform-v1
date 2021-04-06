DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS decisions;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  admin BOOL
);

/*

Notes:
- Time is stored as integer seconds since unix epoch
- Passed should be initalized as 0

*/

CREATE TABLE decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT,
  date INTEGER NOT NULL,
  title TEXT NOT NULL,
  passed BOOL NOT NULL,
  userid INTEGER NOT NULL
);

CREATE TABLE votes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  decisionid INTEGER NOT NULL,
  for BOOL NOT NULL,
  userid ID NOT NULL,
  date INTEGER NOT NULL
);

/*

Passwords and usernames are:

- gkamer, Gordon7899
- jsimpson, mr.simp
- apetty, c0rn

*/

INSERT INTO user (username, password, email, name, admin)
VALUES ('gkamer', 'pbkdf2:sha256:150000$tk6M45tZ$b2ae89d8be66e905b54c21af7e0bebae8eef25fb2e2c4b142dda1999d2f50aef', 'gkamer@college.harvard.edu', 'Gordon Kamer', 1);

INSERT INTO user (username, password, email, name, admin)
VALUES ('jsimpson', 'pbkdf2:sha256:150000$ifdeTFcz$7925d81c44ff050eae36af7d2ed0d672ecc852e793f3a7d19f769cd19a878a56', 'jaredsimpson@college.harvard.edu', 'Jared Simpson', 1);

INSERT INTO user (username, password, email, name, admin)
VALUES ('apetty', 'pbkdf2:sha256:150000$8DCzJskO$a1444a9797c7ed9d02e214f10a8edbeb394373fb4ea76178ac7ef8896bfedbb8', 'alexpetty@college.harvard.edu', 'Alex Petty', 1);

/* Decisions */

INSERT INTO decisions (description, date, title, passed, userid)
VALUES ('Purchase 5 shares of Gamestop', 617683682, 'Buy 5 GME', 0, 0);

INSERT INTO decisions (description, date, title, passed, userid)
VALUES ('Admit Dean Farris as a partner with the title squirt analyst.', 1617683682, 'Admit Dean Farris', 0, 0);

INSERT INTO decisions (description, date, title, passed, userid)
VALUES ('Sell 5 shares of Callaway at around $500', 1617083682, 'Sell 5 ELY', 0, 0);

INSERT INTO decisions (description, date, title, passed, userid)
VALUES ('Purchase 2 shares of AMC due to its enormous potential as a shit post stock.', 1417683682, 'Buy 2 AMC', 0, 0);
