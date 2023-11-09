-- Creation of users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email varchar(255) NOT NULL UNIQUE,
  password varchar(255) NOT NULL,
  is_activated BOOLEAN NOT NULL DEFAULT FALSE
);

-- Creation of user_activation_codes table
CREATE TABLE IF NOT EXISTS user_activation_codes (
  id SERIAL PRIMARY KEY,
  code INT NOT NULL,
  user_id INT NOT NULL UNIQUE,
  creation_date TIMESTAMP NOT NULL,
  CONSTRAINT fk_user_activation_codes_users
      FOREIGN KEY(user_id)
    REFERENCES users(id)
);
