USE tmdb1

CREATE TABLE `tmdb1`.`trademarks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `application_date` VARCHAR(10) NULL,
  `application_lang_code` VARCHAR(2) NULL,
  `second_lang_code` VARCHAR(2) NULL,
  `mark_feature` VARCHAR(4) NULL,
  `wordmark_spec` VARCHAR(200) NULL,
  PRIMARY KEY (`id`));

