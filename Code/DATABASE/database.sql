CREATE DATABASE software_engineering;
USE software_engineering;
-- SHOW tables;
-- describe test;
-- SELECT * FROM test;
-- DROP TABLE pointsystem,review,events,donation,post,profile,organizers,clients,users,lost_items;
-- CREATE DATABASE dokimazooo;
-- use dokimazooo;
-- DROP DATABASE software_engineering;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    role ENUM('client', 'organizer') NOT NULL
);

CREATE TABLE post(
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR (50),
description TEXT,
requiredPoints INT,
Category ENUM ('EventDonation','EnvironmentalDonation','MoreDonations'),
Sub_Category ENUM ('EventSponsors','TreeSaving','PeopleInNeed')
);


CREATE TABLE lost_items (
      id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(100) NOT NULL,
 date DATE NOT NULL,
 details TEXT,
 phone_number VARCHAR(15)  -- nullable από προεπιλογή -> 
 );

CREATE TABLE clients (
    clientID INT PRIMARY KEY,
    cl_name VARCHAR(255) NOT NULL,
    friendcode VARCHAR(50),
    FOREIGN KEY (clientID) REFERENCES users(user_id)
);

CREATE TABLE organizers (
    organizerID INT PRIMARY KEY,
    org_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (organizerID) REFERENCES users(user_id)
);

 CREATE TABLE profile (
  id int NOT NULL,
  address varchar(200) DEFAULT NULL,
  bio text,
  friends text,
  PRIMARY KEY (id),
  CONSTRAINT profile_ibfk_1 FOREIGN KEY (id) REFERENCES clients (clientID) ON DELETE CASCADE
);



CREATE TABLE events (
    eventID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    datetime DATETIME NOT NULL,
    organizerID INT,
    maxParticipants INT NOT NULL,
    category ENUM(
        'τεχνολογία',
        'αθλητισμός',
        'πολιτισμός',
        'μουσική',
        'εκπαίδευση',
        'τέχνη',
        'διασκέδαση',
        'επιχειρηματικότητα',
        'υγεία & ευεξία',
        'άλλο'
    ) NOT NULL,
    price DECIMAL(10,2) DEFAULT 0.00,
    duration INT NOT NULL COMMENT 'Διάρκεια σε λεπτά',
    details TEXT,
    FOREIGN KEY (organizerID) REFERENCES organizers(organizerID)
);


CREATE TABLE participation_form (
  id int NOT NULL AUTO_INCREMENT,
  full_name varchar(100) NOT NULL,
  age int DEFAULT NULL,
  phone varchar(20) DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  interests text,
  dietary_preferences text,
  special_requests text,
  accepted_terms tinyint(1) DEFAULT '0',
  event_id int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY event_id (event_id),
  CONSTRAINT participation_form_ibfk_1 FOREIGN KEY (event_id) REFERENCES events (eventID) ON DELETE CASCADE
);

CREATE TABLE pointsystem (
    clientID INT PRIMARY KEY,
    totalpoints DECIMAL(10,2) DEFAULT 0.00,
    extrapoints DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (clientID) REFERENCES clients(clientID)
);


CREATE TABLE donation(
id INT AUTO_INCREMENT PRIMARY KEY,
client_id INT,
post_id INT,
date Date,
methodUsed ENUM('PointExchange','CardInfo'),
pointsUsed INT,
FOREIGN KEY (client_id) REFERENCES clients(clientId),
FOREIGN KEY (post_id) REFERENCES post(id)
);


CREATE TABLE review(
id INT AUTO_INCREMENT PRIMARY KEY,
client_id INT,
event_id INT,
content TEXT,
date DATE,
FOREIGN KEY (client_id) REFERENCES clients(clientId),
FOREIGN KEY (event_id) REFERENCES events(eventID)
);

create table assigned_event (
user_id INT,
event_id INT,
foreign key (user_id) references clients(clientID),
foreign key (event_id) references events(eventID)
);

CREATE TABLE friends (
  user_id INT,
  friend_id INT,
  status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
  PRIMARY KEY (user_id, friend_id),
  FOREIGN KEY (user_id) REFERENCES clients(clientID) ON DELETE CASCADE,
  FOREIGN KEY (friend_id) REFERENCES clients(clientID) ON DELETE CASCADE
);






-- INSERTIONS --
INSERT INTO users (username, email, phone, role) VALUES
('maria_k', 'maria@example.com', '6912345678', 'client'),
('nikos_organizer', 'nikos@events.gr', '6987654321', 'organizer'),
('anna_p', 'anna@example.com', '6901122334', 'client'),
('tech_admin', 'admin@techevents.com', '6970000000', 'organizer'),
('george_v', 'georgev@example.com', '6933221100', 'client');

INSERT INTO post
VALUES
(1,'Διαγωνισμός Φαγητού','Χρειαζόμαστε Σπόνοσερς για διαγωνισμό φαγητού!',2000,'EventDonation','EventSponsors'),
(2,'Φύτευμα Δέντρων','Χρειαζόμαστε χρήματα για να φυτέψουμε δέντρα',1500,'EnvironmentalDonation','TreeSaving');



INSERT INTO organizers (organizerID, org_name) VALUES
(2, 'Nikos Events'),
(4, 'Tech Admin Team');

INSERT INTO events (
    name, location, datetime, maxParticipants, category,
    price, duration, details, organizerID
) VALUES
(
    'Tech Conference 2025',
    'Αθήνα, Μέγαρο Μουσικής',
    '2025-06-10 10:00:00',
    300,
    'τεχνολογία',
    50.00,
    180,
    'Ετήσια τεχνολογική εκδήλωση με παρουσιάσεις και workshops.',
    4
),
(
    'Αγώνας Δρόμου 5K',
    'Θεσσαλονίκη, Νέα Παραλία',
    '2025-07-05 09:00:00',
    200,
    'αθλητισμός',
    10.00,
    90,
    'Φιλανθρωπικός αγώνας δρόμου 5 χλμ για όλες τις ηλικίες.',
    2
),
(
    'Μουσική Βραδιά στο Πάρκο',
    'Περιστέρι, Άλσος',
    '2025-08-15 20:00:00',
    500,
    'μουσική',
    0.00,
    120,
    'Ζωντανή μουσική από τοπικά συγκροτήματα, δωρεάν είσοδος.',
    2
);


INSERT INTO events (name, location, datetime, maxParticipants, category, price, duration, details, organizerID) VALUES
('Σεμινάριο Προγραμματισμού Python', 'Αθήνα, Πολιτιστικό Κέντρο', '2025-09-12 18:00:00', 100, 'εκπαίδευση', 30.00, 120, 'Σεμινάριο για αρχάριους στην Python.', 4),
('Φεστιβάλ Ταινιών', 'Αθήνα, Κινηματογράφος Άστυ', '2025-10-01 20:00:00', 150, 'διασκέδαση', 15.00, 180, 'Προβολή ταινιών ανεξάρτητου κινηματογράφου.', 4),
('Workshop Ψηφιακής Φωτογραφίας', 'Αθήνα, Studio Φωτογραφίας', '2025-11-05 14:00:00', 50, 'τέχνη', 40.00, 240, 'Εκμάθηση τεχνικών ψηφιακής φωτογραφίας.', 4);


INSERT INTO clients (clientID, cl_name, friendcode) VALUES
(1, 'Maria Kalogeropoulou', 'X9F2K7LQ'),
(3, 'Anna Papadopoulou', 'M4T1BVZC'),
(5, 'Giorgos Vasileiou', 'Q8WZ3NJK');

INSERT INTO participation_form 
(id, full_name, age, phone, email, interests, dietary_preferences, special_requests, accepted_terms, event_id)
VALUES
(1, 'basilop', 34, '134523635', 'agssgar', 'WRG', 'AERG', 'AETH', 1, 1),
(2, 'eleni', 22, '12451345', 'arwg', 'eatghery', 'rtujr', 'ergwe', 1, 1),
(3, 'basiloo', 24, '154125125', 'egewewrg', 'aergqerg', 'eqrgqe', 'qergqeg', 1, 1),
(4, 'ergesa', 34, '41251345134', 'gwetgwe', 'wetgwetg', 'wgtwgt', 'wgwe', 1, 1),
(5, 'WGT', 33, '23462364', 'SDTHSRT', 'AERGWETH', 'srth', 'srth', 1, 1),
(6, 'awrg', 34, 'aer', 'aergerag', 'aergaer', 'aergaeaegaeg', 'aegaeg', 1, 1),
(7, 'tgwers', 54, '2362346', 'eshaer', 'aehset', 'agra', 'adfhad', 1, 1);

INSERT INTO pointsystem (clientID, totalpoints, extrapoints) VALUES
(1, 120.50, 15.75),
(3, 85.00, 5.00),
(5, 230.25, 40.50);



INSERT INTO profile (id, address, bio, friends) VALUES
(1, 'Ameriki123', 'Loves art, music and social events. Fdeqrg', 34),
(3, 'Thessaloniki, Greece', 'Passionate about volunteering and event planning.', 1),
(5, 'Patras, Greece', 'Tech enthusiast and live music lover.', 0);

#DESCRIBE TABLE lost_items;
#SELECT * FROM lost_items;
#SELECT * FROM post;

INSERT INTO lost_items (id, name, date, details, phone_number)
VALUES
(1, 'Wallet', '2025-04-11', 'Black leather wallet', '6971234567'),
(2, 'Keys', '2025-05-01', 'Set of 3 keys with keychain', NULL);
    
INSERT INTO friends (user_id, friend_id, status)
VALUES (1, 3, 'pending'),(3, 1, 'accepted'),(5, 1, 'pending'),(1, 5, 'rejected');
 
