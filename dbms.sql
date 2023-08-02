show databases;
-- CREATE DATABASE dbms;
USE dbms;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `username` varchar(15) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `register_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `confirmed` tinyint(1) DEFAULT '0',
  `aadhar` varchar(12) UNIQUE,
  `phone` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`username`)
) AUTO_INCREMENT=0;

INSERT INTO users(username,name,email, password,confirmed, aadhar, phone, address) 
VALUES
('abhi-1','Abhinav', 'abhinav@gmail.com', '$2b$12$Bt4zoCLzUNfOKRmXn3syOerpgvd1fI2XLtlQwg/q/baf0lTrPYDaa',1, '123456789021', '9988765432', 'Kengari, Bangalore'), -- 1234 
('john1','John Munroe','johnm@gmail.com','$2b$12$i8fo0Ar90iR/CohzoK48oecWpdPDLh19xkbYc6Km94iOLVtTxIGhe',1,'652187548990','9978451180', 'Rajarajeshwari Nagar, Bangalore'), -- qwer 
('jessicah','Jessica Hyde','jessicah@gmail.com','$2b$12$/uwl8W2t2y.rT6Qhlq.byuNHJ9s28sdZp9m.x/Uqm8ko7VukXQVka',1,'254917548990','8754451340', 'Banashankari, Bangalore'), -- utopia
('alice95','Alice Hopper','aliceh@gmail.com','$2b$12$T6RPkcKGH5NMl9xVucBvS.OggMpIuBwRpo.w/PRLTKc0MSLEeEEPS',1,'489002567890','79732519987', 'M K R Nagar, Mysore') -- 9876
; 

-- SELECT * FROM users;

DROP TABLE IF EXISTS `vehicle`;

CREATE TABLE `vehicle` (
  `username` varchar(15) NOT NULL,
  `lp_number` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `engine_number` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `model` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `brand` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reg_date` date,
  `exp_date` date,
  PRIMARY KEY (`lp_number`),
  FOREIGN KEY `vehicle`(`username`) REFERENCES `users`(`username`) ON DELETE CASCADE
) ;

INSERT INTO vehicle VALUES
('abhi-1', 'KA04MD4567', '52WVC10338', 'Alto', 'Maruti Suzuki', '2010-10-12', '2030-10-12'),
('abhi-1', 'KA03PD1267', '32PQC76565', 'Wagon-R', 'Maruti Suzuki', '2013-10-12', '2033-10-12'),
('abhi-1', 'KA02QW4523', '12MWC10465', 'Innova', 'Toyota', '2003-10-12', '2028-10-12'),
('abhi-1', 'KA04DW9483', '84BPC12133', 'Creta', 'Hundai', '2020-10-12', '2035-10-12'),
('abhi-1', 'KA04KL2563', '14WGA93621', 'Activa 125', 'Honda', '2010-03-22', '2025-03-22'),
('abhi-1', 'MH01QW4526', '12PWN83298', 'Supra', 'Toyota', '2009-08-11', '2029-08-11'),
('john1', 'KL21CR9865', '12PRF32574', 'K10 Autogear', 'Maruti Suzuki', '2016-10-12', '2036-10-12'),
('john1', 'KL43OY9873', '13MRK12435', 'Fortuner', 'Toyota', '2010-05-23', '2030-05-23'),
('john1', 'KA01NG0979', '43GDT13453', 'santro', 'Hundai', '2020-02-19', '2035-02-19'),
('john1', 'TN02PL8090', '56WSA97651', 'Access 125', 'Suzuki', '2010-03-22', '2025-03-22'),
('john1', 'TN32XW5434', '76JKE89848', 'Duke 300', 'KTM', '2018-08-11', '2033-08-11'),
('jessicah', 'KL21CR9568', '12PRF32784', 'Alto', 'Maruti Suzuki', '2018-07-02', '2033-07-02'),
('jessicah', 'KA03NG1799', '43GDT13498', 'i10', 'Hyundai', '2021-05-12', '2036-05-12'),
('jessicah', 'KL43OY1734', '13MRK12934', 'Innova', 'Toyota', '2019-12-01', '2034-12-01'),
('jessicah', 'TN02PL5790', '56WSA97611', 'Gixxer SF', 'Suzuki', '2020-01-15', '2035-01-15'),
('jessicah', 'TN32XW1089', '76JKE89234', 'RC 390', 'KTM', '2017-09-19', '2032-09-19'),
('jessicah', 'KL21CR8745', '12PRF32124', 'Swift', 'Maruti Suzuki', '2016-03-28', '2031-03-28'),
('jessicah', 'KA01NG2315', '43GDT13462', 'Grand i10', 'Hyundai', '2018-11-05', '2033-11-05'),
('jessicah', 'KL43OY9876', '13MRK12437', 'Corolla', 'Toyota', '2015-02-23', '2030-02-23'),
('jessicah', 'TN02PL8102', '56WSA97659', 'Hayate EP', 'Suzuki', '2021-02-28', '2036-02-28'),
('jessicah', 'TN32XW4397', '76JKE89819', '390 Adventure', 'KTM', '2020-06-14', '2035-06-14'),
('jessicah', 'KL21CR9765', '12PRF32847', 'Dzire', 'Maruti Suzuki', '2019-10-20', '2034-10-20'),
('jessicah', 'KA01NG9971', '43GDT13675', 'Venue', 'Hyundai', '2022-01-07', '2037-01-07'),
('jessicah', 'KL43OY1847', '13MRK12087', 'Yaris', 'Toyota', '2017-04-18', '2032-04-18'),
('jessicah', 'TN02PL6490', '56WSA97236', 'Burgman Street', 'Suzuki', '2018-11-30', '2033-11-30'),
('alice95', 'TN92PL6498', '56WSA97296', 'bonda', 'Suzuki', '2018-11-30', '2033-11-30'),
('alice95', 'KL76TG1243', '45RGE2345', 'City', 'Honda', '2020-01-01', '2035-01-01'),
('alice95', 'TN32WX8342', '67FGH2345', 'Pulsar', 'Bajaj', '2019-05-15', '2034-05-15'),
('alice95', 'KA04PK3218', '89TGH5678', 'i20', 'Hyundai', '2021-06-30', '2036-06-30'),
('alice95', 'KL23CD4321', '12JKL3456', 'Swift', 'Maruti Suzuki', '2018-11-21', '2033-11-21'),
('alice95', 'TN09MN4567', '34VFR5678', 'Verna', 'Hyundai', '2017-07-03', '2032-07-03'),
('alice95', 'MH02JK7890', '90POI1234', 'Scorpio', 'Mahindra', '2015-09-20', '2030-09-20'),
('alice95', 'KL12MB3175', '56MNB7890', 'Creta', 'Hyundai', '2016-03-11', '2031-03-11')
;

-- SELECT * FROM vehicle where username = 'abhi-1'; 

DROP TABLE IF EXISTS `insurance`;

CREATE TABLE `insurance` (
  `username` varchar(15) NOT NULL,
  `lp_number` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `i_number` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `i_company` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `i_amount` int DEFAULT 0,
  `reg_date` date,
  `exp_date` date,
  PRIMARY KEY (`i_number`),
  FOREIGN KEY `insurance`(`lp_number`) REFERENCES `vehicle`(`lp_number`) ON DELETE CASCADE
) ;

INSERT INTO insurance VALUES
('abhi-1', 'KA04KL2563', '637217845298216', 'Reliance', 65000, '2023-01-12', '2024-01-12'),
('abhi-1', 'KA03PD1267', '836846738507839', 'Bajaj Allianz', 330000, '2022-10-12', '2023-10-12'),
('abhi-1', 'KA02QW4523', '978201638265927', 'Tata AIG', 375000, '2023-02-12', '2025-10-12'),
('abhi-1', 'KA04DW9483', '476928472580829', 'Reliance', 750000, '2022-6-30', '2023-12-30'),
('john1', 'KL43OY9873', '091871727491315', 'Oriental Insurance', 1200000, '2022-05-23', '2023-05-23'),
('john1', 'KA01NG0979', '155767046244332', 'SBI', 350000, '2021-02-19', '2024-02-19'),
('john1', 'TN02PL8090', '415220575296297', 'Liberty', 45000, '2022-03-22', '2023-03-22'),
('john1', 'TN32XW5434', '903325142409389', 'SBI', 127000, '2022-08-11', '2023-08-11'),
('jessicah', 'KL43OY9873', '073526145862315', 'Bajaj Allianz', 1100000, '2020-05-23', '2021-05-23'),
('jessicah', 'KA01NG0979', '819047236152331', 'HDFC Ergo', 300000, '2022-02-19', '2025-02-19'),
('jessicah', 'TN02PL8090', '263904572806214', 'Tata AIG', 55000, '2020-03-22', '2021-03-22'),
('jessicah', 'TN32XW5434', '704932163468732', 'ICICI Lombard', 136000, '2021-08-11', '2022-08-11'),
('jessicah', 'KL21CR9568', '967458311242110', 'Oriental Insurance', 1250000, '2019-07-02', '2024-07-02'),
('jessicah', 'KA03NG1799', '134678435229784', 'SBI', 400000, '2020-05-12', '2025-05-12'),
('jessicah', 'KL43OY1734', '328640192455901', 'Liberty', 60000, '2018-12-01', '2023-12-01'),
('jessicah', 'TN02PL5790', '719635248678259', 'Bajaj Allianz', 90000, '2019-01-15', '2024-01-15'),
('jessicah', 'TN32XW1089', '819047236152332', 'HDFC Ergo', 250000, '2016-09-19', '2021-09-19'),
('alice95', 'TN32WX8342', '465172038415267', 'ICICI Lombard', 800000, '2022-09-01', '2023-09-01'),
('alice95', 'KL23CD4321', '584739102754268', 'Bajaj Allianz', 250000, '2021-06-15', '2024-06-15'),
('alice95', 'TN09MN4567', '146835907532149', 'HDFC Ergo', 60000, '2022-01-01', '2023-01-01'),
('alice95', 'MH02JK7890', '298136405792340', 'Tata AIG', 90000, '2022-11-30', '2023-11-30'),
('alice95', 'KL12MB3175', '679834150923874', 'SBI', 1500000, '2022-04-22', '2023-04-22')
;

DROP TABLE IF EXISTS `violations`;

CREATE TABLE `violations` (
  `username` varchar(15) NOT NULL,
  `lp_number` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `challen_number` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type_of_violation` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fine_amount` int DEFAULT 1000,
  `v_date` date,
  `v_time` time,
  PRIMARY KEY (`challen_number`),
  FOREIGN KEY `violations`(`lp_number`) REFERENCES `vehicle`(`lp_number`) ON DELETE CASCADE
) ;

INSERT INTO violations VALUES
('abhi-1', 'KA04MD4567', 'B/21/1433/57223', 'Rajajinagar 1st block', 'signal jump', 1000, '2021-10-12', '12:30:10'),
('abhi-1', 'KA04MD4567', 'B/20/2423/21243', 'Nayandhalli Junction', 'overspeeding', 1500, '2021-05-12', '17:40:23'),
('abhi-1', 'KA04MD4567', 'B/18/4213/93723', 'Jayanagar 4th Block', 'rash driving', 2000, '2018-02-26', '10:13:35'),
('abhi-1', 'KA02QW4523', 'B/22/4213/93753', 'Nayandhalli Junction', 'signal jump', 1000, '2022-04-22', '06:55:35'),
('abhi-1', 'KA02QW4523', 'B/20/4213/94523', 'Silk Board signal', 'overspeeding', 1500, '2020-07-02', '18:08:12'),
('abhi-1', 'KA04KL2563', 'B/21/4213/24723', 'University Quarters', 'no helmet', 500, '2021-11-17', '11:27:52'),
('john1', 'KL43OY9873', 'B/21/4322/12343', 'Nayandhalli Junction', 'signal jump', 1000, '2021-11-12', '12:30:10'),
('john1', 'KL43OY9873', 'B/22/2373/93223', 'University Quarters', 'overspeeding', 2000, '2021-05-12', '17:40:23'),
('john1', 'TN32XW5434', 'B/22/8973/12223',  'Silk Board signald', 'no helmet', 1000, '2021-11-17', '11:27:52'),
('jessicah', 'KL21CR9865', 'B/23/7634/43215', 'Magadi road near SBI ATM', 'signal jump', 1000, '2022-01-02', '12:50:20'),
('jessicah', 'KL21CR9865', 'B/24/7634/46775', 'Magadi road near SBI ATM', 'overspeeding', 1500, '2022-03-17', '08:20:10'),
('jessicah', 'KL21CR9865', 'B/25/7234/99985', 'K.R Market Bus stand', 'driving on the wrong side of the road', 2000, '2022-05-23', '16:45:55'),
('jessicah', 'KL21CR9865', 'B/26/1334/87665', 'Rajajinagar 1st block', 'parking violation', 500, '2022-07-14', '19:10:40'),
('jessicah', 'KL21CR9865', 'B/27/7334/87866', 'Jayanagar 4th Block', 'not wearing seatbelt', 1000, '2022-09-30', '15:35:30'),
('jessicah', 'KL43OY9873', 'B/28/4534/43787', 'Jayanagar 4th Block', 'driving on the wrong side of the road', 2000, '2022-02-10', '11:15:40'),
('jessicah', 'KL43OY9873', 'B/29/6634/48766', 'MG road signal', 'signal jump', 1000, '2022-04-20', '14:25:10'),
('jessicah', 'KL43OY9873', 'B/30/7634/87668', 'Jayanagar 4th Block', 'parking violation', 500, '2022-06-30', '17:50:20'),
('jessicah', 'KL43OY9873', 'B/31/8634/45655', 'Silk Board signal', 'not wearing seatbelt', 1000, '2022-08-28', '08:15:50'),
('jessicah', 'KA01NG0979', 'B/32/4534/86456', 'Kengeri bus stand', 'driving on the wrong side of the road', 2000, '2022-03-11', '10:05:30'),
('jessicah', 'KA01NG0979', 'B/33/8734/42217', 'Kengeri bus stand', 'signal jump', 1000, '2022-05-19', '16:30:15'),
('jessicah', 'KA01NG0979', 'B/34/8834/42315', 'K.R Market Bus stand', 'not wearing seatbelt', 1000, '2022-07-22', '13:20:45'),
('alice95', 'KA04PK3218', 'B/23/4577/67663', 'Kodihalli signal', 'signal jump', 1000, '2022-02-05', '15:17:42'),
('alice95', 'TN32WX8342', 'B/19/7576/96753', 'MG road signal', 'no helmet', 500, '2021-03-12', '19:20:33'),
('alice95', 'TN32WX8342', 'B/21/5676/55563', 'MG Road Metro Station', 'overspeeding', 1500, '2022-01-06', '08:12:25'),
('alice95', 'KL12MB3175', 'B/24/7655/57655', 'Koramangala 6th Block', 'drunk driving', 5000, '2022-12-20', '22:45:15'),
('alice95', 'KL12MB3175', 'B/20/5773/98777', 'Koramangala 6th Block', 'signal jump', 1000, '2022-01-22', '10:55:50'),
('alice95', 'TN09MN4567', 'B/22/6753/67867', 'Bellandur flyover', 'riding without license', 2000, '2022-02-14', '14:30:10'),
('alice95', 'KA04PK3218', 'B/18/5443/96877', 'K.R Market Bus stand', 'using mobile while driving', 1000, '2022-01-02', '11:10:20'),
('alice95', 'KL12MB3175', 'B/25/2233/93678', 'MG Road Metro Station', 'parking violation', 500, '2022-02-25', '16:55:30'),
('alice95', 'MH02JK7890', 'B/26/3413/67823', 'Koramangala 6th Block', 'rash driving', 1500, '2022-02-27', '09:40:55'),
('alice95', 'MH02JK7890', 'B/27/4233/34366', 'MG Road Metro Station', 'parking violation', 2000, '2022-02-28', '18:15:40')
;

-- -----------------------------------------------------------------------------------------------------------------------------------

-- code for removing all tables
DROP TABLE IF EXISTS `violations`;
DROP TABLE IF EXISTS `insurance`;
DROP TABLE IF EXISTS `vehicle`;
DROP TABLE IF EXISTS `users`;
-- ------------------------------

-- ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'DumbDBMS(100)';

-- USE mysql;
-- SELECT User, Host, plugin FROM mysql.user;
-- UPDATE user SET plugin='mysql_native_password' WHERE User='abhi';

-- CREATE USER 'abhi'@'localhost' IDENTIFIED BY '1234';
-- GRANT ALL ON mysql.* TO 'abhi'@'localhost';
-- GRANT ALL PRIVILEGES ON *.* TO 'abhi'@'localhost' WITH GRANT OPTION;