DROP DATABASE SmartTrash;
CREATE DATABASE  IF NOT EXISTS SmartTrash;
USE SmartTrash;

CREATE TABLE IF NOT EXISTS data_sensors (
  id int(11) PRIMARY KEY AUTO_INCREMENT,
  node_id varchar(20) NOT NULL,
  node_type varchar(20) NOT NULL,
  meas_label varchar(20) NOT NULL,
  meas_raw_value double NOT NULL
);


CREATE TABLE IF NOT EXISTS CPosition(
  id INT PRIMARY KEY AUTO_INCREMENT,
  position VARCHAR(50)
);
INSERT INTO CPosition(position) VALUES("Recolector");
INSERT INTO CPosition(position) VALUES("Administrativo");
INSERT INTO CPosition(position) VALUES("Otro");


CREATE TABLE IF NOT EXISTS CEducation(
  id INT PRIMARY KEY AUTO_INCREMENT,
  education VARCHAR(50)
);
INSERT INTO CEducation(education) VALUES("None");
INSERT INTO CEducation(education) VALUES("Primaria");
INSERT INTO CEducation(education) VALUES("Secundaria");
INSERT INTO CEducation(education) VALUES("Bachillerato");
INSERT INTO CEducation(education) VALUES("Licenciatura");
INSERT INTO CEducation(education) VALUES("Otro");

CREATE TABLE IF NOT EXISTS CUserType(
  id INT PRIMARY KEY AUTO_INCREMENT,
  utype VARCHAR(50)
);
INSERT INTO CUserType(utype) VALUES("Admin");
INSERT INTO CUserType(utype) VALUES("Comun");

CREATE TABLE IF NOT EXISTS MUser(
  name VARCHAR(50),
  lastname VARCHAR(105),
  email VARCHAR(50) PRIMARY KEY,
  phone VARCHAR(16),
  address VARCHAR(200),
  position INT(1),
  education INT(1),
  income INT(5),
  utype INT(5),
  bdate DATE,
  password BINARY(60),
  FOREIGN KEY (position) REFERENCES CPosition(id),
  FOREIGN KEY (education) REFERENCES CEducation(id),
  FOREIGN KEY (utype) REFERENCES CUserType(id)
);

CREATE TABLE IF NOT EXISTS MAddress(
  id INT PRIMARY KEY AUTO_INCREMENT,
  lat VARCHAR(20),
  lng VARCHAR(20),
  fulladdress VARCHAR(300),
  street VARCHAR(100),
  urbanity VARCHAR(50),
  num VARCHAR(10),
  neighborhood VARCHAR(50),
  state VARCHAR(50),
  pc VARCHAR(6),
  country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS CContainerType(
  id INT PRIMARY KEY AUTO_INCREMENT,
  ctype VARCHAR(50)
);
INSERT INTO CContainerType(ctype) VALUES("Orgn??nico");
INSERT INTO CContainerType(ctype) VALUES("Inorgn??nico");
INSERT INTO CContainerType(ctype) VALUES("Vidrio");
INSERT INTO CContainerType(ctype) VALUES("Cart??n");
INSERT INTO CContainerType(ctype) VALUES("Papel");
INSERT INTO CContainerType(ctype) VALUES("Bater??as");


CREATE TABLE IF NOT EXISTS MContainer(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  address int(4),
  type int(2),
  capacity int(4),
  FOREIGN KEY (address) REFERENCES MAddress(id),
  FOREIGN KEY (type) REFERENCES CContainerType(id)
);

CREATE TABLE IF NOT EXISTS DToken(
  email VARCHAR(50) PRIMARY KEY,
  token VARCHAR(256),
  creation DATETIME,
  expiration DATETIME,
  FOREIGN KEY (email) REFERENCES MUser(email)
)