CREATE DATABASE IF NOT EXISTS db;

USE db;

CREATE TABLE IF NOT EXISTS `trademarks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `application_date` VARCHAR(10) NULL,
  `application_lang_code` VARCHAR(2) NULL,
  `second_lang_code` VARCHAR(2) NULL,
  `mark_feature` VARCHAR(4) NULL,
  `mark_verb_ele_text` VARCHAR(300) NULL,
  PRIMARY KEY (`id`));

