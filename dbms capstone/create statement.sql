-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema GBC_Superstore
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema GBC_Superstore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `GBC_Superstore` DEFAULT CHARACTER SET utf8 ;
USE `GBC_Superstore` ;

-- -----------------------------------------------------
-- Table `GBC_Superstore`.`country_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`country_details` (
  `country_id` INT NOT NULL AUTO_INCREMENT,
  `country_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`country_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`region_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`region_details` (
  `region_id` INT NOT NULL AUTO_INCREMENT,
  `region_name` VARCHAR(45) NOT NULL,
  `country_id` INT NULL,
  PRIMARY KEY (`region_id`),
  INDEX `country_id_idx` (`country_id` ASC) VISIBLE,
  CONSTRAINT `country_id`
    FOREIGN KEY (`country_id`)
    REFERENCES `GBC_Superstore`.`country_details` (`country_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`state_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`state_details` (
  `state_id` INT NOT NULL AUTO_INCREMENT,
  `state_name` VARCHAR(45) NOT NULL,
  `region_id` INT NULL,
  PRIMARY KEY (`state_id`),
  INDEX `region_id_idx` (`region_id` ASC) VISIBLE,
  CONSTRAINT `region_id`
    FOREIGN KEY (`region_id`)
    REFERENCES `GBC_Superstore`.`region_details` (`region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`regional_manager_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`regional_manager_details` (
  `manager_id` INT NOT NULL AUTO_INCREMENT,
  `manager_name` VARCHAR(45) NOT NULL,
  `region_id` INT NULL,
  PRIMARY KEY (`manager_id`),
  INDEX `region_id_idx` (`region_id` ASC) VISIBLE,
  CONSTRAINT `region_id_link_manger`
    FOREIGN KEY (`region_id`)
    REFERENCES `GBC_Superstore`.`region_details` (`region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`city_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`city_details` (
  `postal_code` INT NOT NULL,
  `city_name` VARCHAR(45) NOT NULL,
  `state_id` INT NULL,
  PRIMARY KEY (`postal_code`),
  INDEX `state_id_idx` (`state_id` ASC) VISIBLE,
  CONSTRAINT `state_id`
    FOREIGN KEY (`state_id`)
    REFERENCES `GBC_Superstore`.`state_details` (`state_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`customer_segment_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`customer_segment_details` (
  `segment_id` INT NOT NULL AUTO_INCREMENT,
  `segment_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`segment_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`customer_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`customer_details` (
  `customer_id` VARCHAR(45) NOT NULL,
  `customer_name` VARCHAR(45) NOT NULL,
  `segment_id` INT NULL,
  INDEX `segment_id_idx` (`segment_id` ASC) VISIBLE,
  PRIMARY KEY (`customer_id`),
  CONSTRAINT `segment_id`
    FOREIGN KEY (`segment_id`)
    REFERENCES `GBC_Superstore`.`customer_segment_details` (`segment_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`category_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`category_details` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`sub_category_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`sub_category_details` (
  `sub_category_id` INT NOT NULL AUTO_INCREMENT,
  `sub_category_name` VARCHAR(45) NOT NULL,
  `category_id` INT NULL,
  PRIMARY KEY (`sub_category_id`),
  INDEX `category_id_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `GBC_Superstore`.`category_details` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`product_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`product_details` (
  `product_id` VARCHAR(45) NOT NULL,
  `product_name` VARCHAR(250) NOT NULL,
  `sub_category_id` INT NULL,
  PRIMARY KEY (`product_id`),
  INDEX `sub_category_id_idx` (`sub_category_id` ASC) VISIBLE,
  CONSTRAINT `sub_category_id`
    FOREIGN KEY (`sub_category_id`)
    REFERENCES `GBC_Superstore`.`sub_category_details` (`sub_category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`shiping_mode_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`shiping_mode_details` (
  `shipping_mode_id` INT NOT NULL AUTO_INCREMENT,
  `shipping_mode_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`shipping_mode_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`order_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`order_details` (
  `order_id` VARCHAR(45) NOT NULL,
  `order_date` DATE NOT NULL,
  `shipping_date` DATE NULL,
  `shipping_mode_id` INT NULL,
  `customer_id` VARCHAR(45) NULL,
  `returned` TINYINT NOT NULL DEFAULT 0,
  `postal_code` INT NULL,
  INDEX `shiping_mode_id_idx` (`shipping_mode_id` ASC) VISIBLE,
  INDEX `customer_id_idx` (`customer_id` ASC) VISIBLE,
  PRIMARY KEY (`order_id`),
  INDEX `postal_code_idx` (`postal_code` ASC) VISIBLE,
  CONSTRAINT `shipping_mode_id`
    FOREIGN KEY (`shipping_mode_id`)
    REFERENCES `GBC_Superstore`.`shiping_mode_details` (`shipping_mode_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `GBC_Superstore`.`customer_details` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postal_code`
    FOREIGN KEY (`postal_code`)
    REFERENCES `GBC_Superstore`.`city_details` (`postal_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `GBC_Superstore`.`sales_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GBC_Superstore`.`sales_details` (
  `sales_id` INT NOT NULL AUTO_INCREMENT,
  `total_sale` DECIMAL NULL,
  `order_id` VARCHAR(45) NULL,
  `product_id` VARCHAR(45) NULL,
  `quantity` INT NOT NULL,
  `discount` DECIMAL NULL,
  `profit` DECIMAL NULL,
  PRIMARY KEY (`sales_id`),
  INDEX `order_id_idx` (`order_id` ASC) VISIBLE,
  INDEX `product_id_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `order_id`
    FOREIGN KEY (`order_id`)
    REFERENCES `GBC_Superstore`.`order_details` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `GBC_Superstore`.`product_details` (`product_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
