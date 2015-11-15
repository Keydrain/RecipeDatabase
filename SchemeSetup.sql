-- MySQL Script generated by MySQL Workbench
-- Sun Nov 15 13:49:48 2015
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema Recipes
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Recipes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Recipes` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `Recipes` ;

-- -----------------------------------------------------
-- Table `Recipes`.`INSTRUCTION_LIST`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`INSTRUCTION_LIST` (
	`Direction_No` INT NOT NULL COMMENT '',
	`Directions` LONGTEXT NOT NULL COMMENT '',
	`Prep_Time` VARCHAR(45) NULL COMMENT '',
	`Difficulty` INT NULL COMMENT '',
	PRIMARY KEY (`Direction_No`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`AMOUNT_REQUIRED`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`AMOUNT_REQUIRED` (
	`Recipe_No` INT NOT NULL COMMENT '',
	`Ingredient_No` INT NOT NULL COMMENT '',
	`Amount` DOUBLE NOT NULL COMMENT '',
	`Unit` VARCHAR(10) NOT NULL COMMENT '',
	PRIMARY KEY (`Recipe_No`, `Ingredient_No`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`SOURCE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`SOURCE` (
	`Source_No` INT NOT NULL COMMENT '',
	`Name` VARCHAR(45) NULL COMMENT '',
	`Reference` VARCHAR(45) NOT NULL COMMENT 'Type should be like: website, blog, cook book, home recipe, etc',
	`Type` VARCHAR(45) NOT NULL COMMENT '',
	`Author-optional` VARCHAR(45) NULL COMMENT '',
	PRIMARY KEY (`Source_No`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`RECIPE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`RECIPE` (
	`Recipe_No` INT NOT NULL COMMENT '',
	`Name` VARCHAR(45) NOT NULL COMMENT '',
	`Description` MEDIUMTEXT NOT NULL COMMENT '',
	`Quantity` DOUBLE NULL COMMENT '',
	`Type` VARCHAR(45) NOT NULL COMMENT 'make type a set of appetizer, side dish, main course, & desert',
	`Photo` VARCHAR(45) NULL COMMENT '',
	`Direction_No` INT NOT NULL COMMENT '',
	`Source_No` INT NOT NULL COMMENT '',
	INDEX `Direction_No_idx` (`Direction_No` ASC)  COMMENT '',
	PRIMARY KEY (`Recipe_No`)  COMMENT '',
	INDEX `Source_No_idx` (`Source_No` ASC)  COMMENT '',
	CONSTRAINT `Direction_No`
		FOREIGN KEY (`Direction_No`)
		REFERENCES `Recipes`.`INSTRUCTION_LIST` (`Direction_No`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT `Amount_Required`
		FOREIGN KEY (`Recipe_No`)
		REFERENCES `Recipes`.`AMOUNT_REQUIRED` (`Recipe_No`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT `Source_No`
		FOREIGN KEY (`Source_No`)
		REFERENCES `Recipes`.`SOURCE` (`Source_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`NUTRITIONAL_FACTS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`NUTRITIONAL_FACTS` (
	`Nutrition_No` INT NOT NULL COMMENT '',
	`Calories` INT NOT NULL COMMENT '',
	`Protient` DOUBLE NULL COMMENT '',
	`Sugar` DOUBLE NULL COMMENT '',
	`Sodium` DOUBLE NULL COMMENT '',
	`Fat` DOUBLE NULL COMMENT '',
	PRIMARY KEY (`Nutrition_No`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`MEASUREMENT_CONVERSION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`MEASUREMENT_CONVERSION` (
	`Unit` VARCHAR(10) NOT NULL COMMENT '',
	`Standard_Unit` VARCHAR(10) NOT NULL COMMENT '',
	`Unit_to_Standard_Value` FLOAT NOT NULL COMMENT '',
	PRIMARY KEY (`Standard_Unit`, `Unit`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`INGREDIENT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`INGREDIENT` (
	`Ingredient_No` INT NOT NULL COMMENT '',
	`Name` VARCHAR(45) NOT NULL COMMENT '',
	`Type` VARCHAR(45) NOT NULL COMMENT '',
	`Description` TINYTEXT NOT NULL COMMENT '',
	`Contains_Dairy` BINARY NOT NULL COMMENT '',
	`Contains_Glutten` BINARY NOT NULL COMMENT '',
	`Nutritional_No` INT NOT NULL COMMENT '',
	UNIQUE INDEX `Nutritional_No_UNIQUE` (`Nutritional_No` ASC)  COMMENT '',
	PRIMARY KEY (`Ingredient_No`)  COMMENT '',
	INDEX `Amount_Required_idx` (`Ingredient_No` ASC)  COMMENT '',
	CONSTRAINT `Amount_Required`
		FOREIGN KEY (`Ingredient_No`)
		REFERENCES `Recipes`.`AMOUNT_REQUIRED` (`Ingredient_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT `Nutritional_Facts`
		FOREIGN KEY (`Nutritional_No`)
		REFERENCES `Recipes`.`NUTRITIONAL_FACTS` (`Nutrition_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`COOKWARE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`COOKWARE` (
	`Direction_No` INT NOT NULL COMMENT '',
	`Cookware` VARCHAR(45) NOT NULL COMMENT '',
	PRIMARY KEY (`Cookware`, `Direction_No`)  COMMENT '',
	CONSTRAINT `Instruction_List`
		FOREIGN KEY (`Direction_No`)
		REFERENCES `Recipes`.`INSTRUCTION_LIST` (`Direction_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`VITAMIN`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`VITAMIN` (
	`Nutrition_No` INT NOT NULL COMMENT '',
	`Vitamin` VARCHAR(45) NOT NULL COMMENT '',
	PRIMARY KEY (`Vitamin`, `Nutrition_No`)  COMMENT '',
	CONSTRAINT `Nutritional_Facts`
		FOREIGN KEY (`Nutrition_No`)
		REFERENCES `Recipes`.`NUTRITIONAL_FACTS` (`Nutrition_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
