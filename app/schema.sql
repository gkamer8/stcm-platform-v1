DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  admin BOOL
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
