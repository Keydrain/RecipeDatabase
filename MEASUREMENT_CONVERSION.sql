-- MySQL dump 10.13  Distrib 5.6.24, for osx10.8 (x86_64)
--
-- Host: localhost    Database: Recipes
-- ------------------------------------------------------
-- Server version	5.7.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MEASUREMENT_CONVERSION`
--

DROP TABLE IF EXISTS `MEASUREMENT_CONVERSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MEASUREMENT_CONVERSION` (
  `Unit1` varchar(20) NOT NULL COMMENT 'Specified unit in recipe',
  `Unit2` varchar(20) NOT NULL COMMENT 'The standard unit conversion',
  `Conversion_Rate` float NOT NULL COMMENT 'The conversion rate',
  PRIMARY KEY (`Unit1`,`Unit2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEASUREMENT_CONVERSION`
--

LOCK TABLES `MEASUREMENT_CONVERSION` WRITE;
/*!40000 ALTER TABLE `MEASUREMENT_CONVERSION` DISABLE KEYS */;
INSERT INTO `MEASUREMENT_CONVERSION` VALUES ('Celsius','Fahrenheit',33.8),('Cup','Fluid Ounce',8.11537),('Cup','Liter',0.24),('Cup','Mililiter',240),('Cup','Tablespoon',16.2307),('Cup','Teaspoon',48.6922),('Fluid Ounce','Liter',0.0295735),('Fluid Ounce','Mililiter',29.5735),('Fluid Ounce','Tablespoon',2),('Fluid Ounce','Teaspoon',6),('Gallon','Cup',15.7725),('Gallon','Fluid Ounce',128),('Gallon','Liter',3.78541),('Gallon','Mililiter',3785.41),('Gallon','Pint',8),('Gallon','Quart',4),('Gallon','Tablespoon',256),('Gallon','Teaspoon',768),('Gram','Kilogram',0.001),('Liter','Mililiter',1000),('Milligram','Gram',0.001),('Milligram','Kilogram',0.000001),('Ounce','Kilogram',0.0283495),('Ounce','Milligram',28349.5),('Ounce','Pound',0.0625),('Pint','Cup',1.97157),('Pint','Fluid Ounce',16),('Pint','Liter',0.473176),('Pint','Mililiter',473.176),('Pint','Tablespoon',32),('Pint','Teaspoon',96),('Pound','Gram',453.592),('Pound','Kilogram',0.453592),('Pound','Milligram',453592),('Quart','Cup',3.94314),('Quart','Fluid Ounce',32),('Quart','Liter',0.946353),('Quart','Mililiter',946.353),('Quart','Pint',2),('Quart','Tablespoon',64),('Quart','Teaspoon',192),('Tablespoon','Liter',0.0147868),('Tablespoon','Mililiter',14.7868),('Tablespoon','Teaspoon',3),('Teaspoon','Liter',0.00492892),('Teaspoon','Mililiter',4.92892);
/*!40000 ALTER TABLE `MEASUREMENT_CONVERSION` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-16 22:48:59
