-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: find_my_guide
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `trip_name` text,
  `city` tinytext NOT NULL,
  `startDate` date NOT NULL,
  `num_day` int NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('Completed','Due','Cancelled') DEFAULT 'Due',
  `customer_id` int NOT NULL,
  `guide_id` int NOT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `customer_id` (`customer_id`),
  KEY `guide_id` (`guide_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,'Trip To baran','Baran','2021-07-27',0,'2021-07-27','Due',1,1);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` tinytext NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `contact` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_id` (`email_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'shubham','shubh@gmail.com','pbkdf2:sha256:150000$wHRdTWHO$d63545efd52d81218f35b2ba44b6645dab6bef12d897c542c080c471a6b55184',1592348),(2,'Yash Sankhla','gokulnama21@gmail.com','pbkdf2:sha256:150000$U0nLav6l$a553c04de9035722c035b5572a3a2b6798a29ed73b4a0c3043ac61071e9d044c',7976399265);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_blogs`
--

DROP TABLE IF EXISTS `customer_blogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_blogs` (
  `blog_id` int NOT NULL,
  `title` text,
  `description` varchar(255) DEFAULT NULL,
  `img_link_1` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `role` enum('USER','GUIDE') DEFAULT 'USER',
  `customer_id` int NOT NULL,
  KEY `customer_id` (`customer_id`),
  KEY `blog_id` (`blog_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_blogs`
--

LOCK TABLES `customer_blogs` WRITE;
/*!40000 ALTER TABLE `customer_blogs` DISABLE KEYS */;
INSERT INTO `customer_blogs` VALUES (1,NULL,NULL,NULL,'2021-07-27 00:00:00','USER',1);
/*!40000 ALTER TABLE `customer_blogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guides`
--

DROP TABLE IF EXISTS `guides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guides` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` tinytext NOT NULL,
  `email_id` varchar(200) NOT NULL,
  `contact` bigint NOT NULL,
  `city` tinytext NOT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `is_checked` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `status` enum('A','NA') DEFAULT 'A',
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_id` (`email_id`),
  UNIQUE KEY `contact` (`contact`),
  UNIQUE KEY `contact_2` (`contact`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guides`
--

LOCK TABLES `guides` WRITE;
/*!40000 ALTER TABLE `guides` DISABLE KEYS */;
INSERT INTO `guides` VALUES (1,'abc','abc@gmail.com',741258963,'Baran','Male',1,50,'NA','pbkdf2:sha256:150000$0jAxC8Oh$a2b59101f7888cfe036a144f91f6cf55ded1bcc492b7af064233e7cf2a89fa72');
/*!40000 ALTER TABLE `guides` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guides_blogs`
--

DROP TABLE IF EXISTS `guides_blogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guides_blogs` (
  `blog_id` int NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `img_link_1` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `role` enum('USER','GUIDE') DEFAULT 'GUIDE',
  `guide_id` int NOT NULL,
  PRIMARY KEY (`blog_id`),
  UNIQUE KEY `guide_id` (`guide_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guides_blogs`
--

LOCK TABLES `guides_blogs` WRITE;
/*!40000 ALTER TABLE `guides_blogs` DISABLE KEYS */;
/*!40000 ALTER TABLE `guides_blogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rate_status`
--

DROP TABLE IF EXISTS `rate_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guide_id` int NOT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guide_id` (`guide_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_status`
--

LOCK TABLES `rate_status` WRITE;
/*!40000 ALTER TABLE `rate_status` DISABLE KEYS */;
INSERT INTO `rate_status` VALUES (1,1,NULL);
/*!40000 ALTER TABLE `rate_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating` int DEFAULT NULL,
  `guide_id` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guide_id` (`guide_id`),
  KEY `booking_id` (`booking_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES (1,NULL,1,1);
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-28 22:24:46
