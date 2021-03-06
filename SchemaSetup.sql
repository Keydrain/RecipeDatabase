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
-- #INSTRUCTION_LIST
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`INSTRUCTION_LIST` (
	`Direction_No` INT NOT NULL COMMENT 'References the recipe the directions are intended for',
	`Directions` LONGTEXT NOT NULL COMMENT 'The list of directions',
	`Prep_Time` VARCHAR(16) NULL COMMENT 'Estimated preperation time- does not need to exist',
	`Difficulty` INT NULL COMMENT 'Ranked Easy, Medium, Hard- does not need to exist ',
	PRIMARY KEY (`Direction_No`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`AMOUNT_REQUIRED`
-- #AMOUNT_REQUIRED
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`AMOUNT_REQUIRED` (
	`Recipe_No` INT NOT NULL COMMENT 'References the recipe the ingredient is intended for',
	`Ingredient_No` INT NOT NULL COMMENT 'References the ingredient list of the recipe',
	`Amount` DOUBLE NOT NULL COMMENT 'Amount required for the recipe',
	`Unit` VARCHAR(20) NOT NULL COMMENT 'The amount measurment for the recipe',
	PRIMARY KEY (`Recipe_No`, `Ingredient_No`),
	INDEX `Ingredient_No_idx` (`Ingredient_No`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`SOURCE`
-- #SOURCE
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`SOURCE` (
	`Source_No` INT NOT NULL COMMENT 'Source number',
	`Name` VARCHAR(45) NULL COMMENT 'Name of source',
	`Reference` VARCHAR(45) NOT NULL COMMENT 'Source information, i.e. url or book title',
	`Type` VARCHAR(45) NOT NULL COMMENT 'Type should be like: website, blog, cook book, home recipe, etc',
	`Author` VARCHAR(45) NULL COMMENT 'Include author if availabe- not required',
	PRIMARY KEY (`Source_No`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`RECIPE`
-- #RECIPE
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`RECIPE` (
	`Recipe_No` INT NOT NULL COMMENT '',
	`Name` VARCHAR(45) NOT NULL COMMENT 'Recipe Name',
	`Description` MEDIUMTEXT NOT NULL COMMENT 'Recipe description',
	`Quantity` DOUBLE NULL COMMENT 'Amount the recipe makes- assumes servings',
	`Calories` INT NOT NULL COMMENT 'Number of Calories of the recipe',
	`Type` VARCHAR(45) NOT NULL COMMENT 'TypeL appetizer, side dish, main course, or desert',
	`Photo` VARCHAR(45) NULL COMMENT 'Photo of finished recipe- not required',
	`Direction_No` INT NOT NULL COMMENT 'References the list of directions',
	`Source_No` INT NOT NULL COMMENT 'References the source of the recipe',
	INDEX `Direction_No_idx` (`Direction_No`),
	PRIMARY KEY (`Recipe_No` ASC),
	INDEX `Source_No_idx` (`Source_No`),
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
-- #NURTRUITIONAL_FACTS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`NUTRITIONAL_FACTS` (
	`Nutrition_No` INT NOT NULL COMMENT 'References an ingredient',
	`Units` VARCHAR(40) NOT NULL COMMENT 'Units used for standard measurements',
	`Calories` INT NOT NULL COMMENT 'Number of Calories- required for DB schema',
	`Protien` VARCHAR(20) NULL COMMENT 'Amount of Protient- not required',
	`Sugar` VARCHAR(20) NULL COMMENT 'Amount of Sugar- not required',
	`Sodium` VARCHAR(20) NULL COMMENT 'Amount of Sodium- not required',
	`Fat` VARCHAR(20) NULL COMMENT 'Amount of fat- not required',
	PRIMARY KEY (`Nutrition_No`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`MEASUREMENT_CONVERSION`
-- #MEASUREMNT_CONVERSION
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`MEASUREMENT_CONVERSION` (
	`Unit1` VARCHAR(20) NOT NULL COMMENT 'Specified unit in recipe',
	`Unit2` VARCHAR(20) NOT NULL COMMENT 'The standard unit conversion',
	`Conversion_Rate` FLOAT NOT NULL COMMENT 'The conversion rate',
	PRIMARY KEY (`Unit1`, `Unit2`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`INGREDIENT`
-- #INGREDIENT
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`INGREDIENT` (
	`Ingredient_No` INT NOT NULL COMMENT 'Ingrdient required in the recipe',
	`Name` VARCHAR(90) NOT NULL COMMENT 'Ingredient Name',
	`Type` VARCHAR(45) NOT NULL COMMENT 'Type: meat, veggie, etc',
	`Description` TINYTEXT NOT NULL COMMENT 'Describes the ingredient',
	`Contains_Dairy` BINARY NOT NULL COMMENT 'Boolean for latouse information',
	`Contains_Glutten` BINARY NOT NULL COMMENT 'Boolean for glutten infomormation',
	`Nutrition_No` INT NOT NULL COMMENT 'References its nutitional facts',
	UNIQUE INDEX `Nutrition_No_UNIQUE` (`Nutrition_No`) ,
	PRIMARY KEY (`Ingredient_No`),
	INDEX `Ingredient_No_idx` (`Ingredient_No`),
	CONSTRAINT `Ingredient_Amount`
		FOREIGN KEY (`Ingredient_No`)
		REFERENCES `Recipes`.`AMOUNT_REQUIRED` (`Ingredient_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT `Nutrition_Fact`
		FOREIGN KEY (`Nutrition_No`)
		REFERENCES `Recipes`.`NUTRITIONAL_FACTS` (`Nutrition_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`COOKWARE`
-- #COOKWARE
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS `Recipes`.`COOKWARE` (
-- 	`Direction_No` INT NOT NULL COMMENT 'References the directions',
-- 	`Cookware` VARCHAR(45) NOT NULL COMMENT 'The list of cookware recommended for the recipe',
-- 	PRIMARY KEY (`Cookware`, `Direction_No`),
-- 	CONSTRAINT `Instruction_List`
-- 		FOREIGN KEY (`Direction_No`)
-- 		REFERENCES `Recipes`.`INSTRUCTION_LIST` (`Direction_No`)
-- 		ON DELETE NO ACTION
-- 		ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Recipes`.`VITAMIN`
-- #VITAMIN
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Recipes`.`VITAMIN` (
	`Nutrition_No` INT NOT NULL COMMENT 'References the nutrition number of a given ingredient',
	`Vitamin` VARCHAR(45) NOT NULL COMMENT 'Name of the Vitamin Present',
	PRIMARY KEY (`Vitamin`, `Nutrition_No`),
	CONSTRAINT `Nutritional_Facts`
		FOREIGN KEY (`Nutrition_No`)
		REFERENCES `Recipes`.`NUTRITIONAL_FACTS` (`Nutrition_No`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
