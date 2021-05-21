-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: pcr-data.c26pxtiebcym.us-west-2.rds.amazonaws.com    Database: pcr-data
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
-- SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

-- SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `DEPLOYMENT_DATA`
--

DROP TABLE IF EXISTS `DEPLOYMENT_DATA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DEPLOYMENT_DATA` (
  `p_key` int NOT NULL AUTO_INCREMENT,
  `DEPLOYMENT_ID` varchar(45) NOT NULL,
  `DEPLOYMENT_TYPE` varchar(45) DEFAULT NULL,
  `FAMILY_ID` varchar(45) DEFAULT NULL,
  `NUMBER_OF_RESIDENTS` varchar(45) DEFAULT NULL,
  `NUMBER_OF_ROOMS` varchar(45) DEFAULT NULL,
  `START_TIME` varchar(45) DEFAULT NULL,
  `END_TIME` varchar(45) DEFAULT NULL,
  `STATUS` varchar(45) DEFAULT NULL,
  `CREATED_DATE` date DEFAULT NULL,
  `SYNCED` int DEFAULT NULL,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `M2G`
--

DROP TABLE IF EXISTS `M2G`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `M2G` (
  `p_key` int NOT NULL AUTO_INCREMENT,
  `ts` datetime DEFAULT NULL,
  `dep_id` int NOT NULL,
  `sub_system` varchar(45) DEFAULT NULL,
  `component` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `receiver` varchar(45) DEFAULT NULL,
  `content` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`p_key`),
  UNIQUE KEY `p_key_UNIQUE` (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=791 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ema_data`
--

DROP TABLE IF EXISTS `ema_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ema_data` (
  `suid` int DEFAULT NULL,
  `primkey` varchar(150) NOT NULL,
  `variablename` varchar(150) DEFAULT NULL,
  `answer` blob,
  `dirty` int DEFAULT NULL,
  `language` int DEFAULT NULL,
  `mode` int DEFAULT NULL,
  `version` int DEFAULT NULL,
  `completed` int DEFAULT NULL,
  `synced` int DEFAULT NULL,
  `ts` datetime DEFAULT NULL,
  `dep_id` int DEFAULT NULL,
  `cloud_pkey` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`cloud_pkey`)
) ENGINE=InnoDB AUTO_INCREMENT=3224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ema_phones`
--

DROP TABLE IF EXISTS `ema_phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ema_phones` (
  `phoneid` varchar(45) NOT NULL,
  `ip` varchar(45) NOT NULL,
  `port` varchar(45) NOT NULL,
  `synced` int DEFAULT NULL,
  `ts` datetime NOT NULL,
  `dep_id` varchar(45) NOT NULL,
  `p_key` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ema_storing_data`
--

DROP TABLE IF EXISTS `ema_storing_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ema_storing_data` (
  `time` datetime NOT NULL,
  `event_vct` varchar(100) DEFAULT NULL,
  `stats_vct` varchar(100) DEFAULT NULL,
  `action` int DEFAULT NULL,
  `reward` float DEFAULT NULL,
  `action_vct` varchar(100) DEFAULT NULL,
  `message_name` varchar(100) DEFAULT NULL,
  `uploaded` int DEFAULT NULL,
  `dep_id` int NOT NULL,
  `p_key` bigint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `heart_beat`
--

DROP TABLE IF EXISTS `heart_beat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `heart_beat` (
  `dep_id` int NOT NULL,
  `ts` int NOT NULL,
  `p_key` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `code` int DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `dep_id` int NOT NULL,
  `ts` datetime DEFAULT NULL,
  `p_key` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `missing_M2G`
--

DROP TABLE IF EXISTS `missing_M2G`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missing_M2G` (
  `ts` datetime NOT NULL,
  `p_key` int NOT NULL AUTO_INCREMENT,
  `dep_id` int NOT NULL,
  `local_count` int DEFAULT NULL,
  `cloud_count` int DEFAULT NULL,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `missing_ema_data`
--

DROP TABLE IF EXISTS `missing_ema_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missing_ema_data` (
  `dep_id` int NOT NULL,
  `ts` datetime NOT NULL,
  `local_count` int NOT NULL,
  `cloud_count` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `missing_ema_storing_data`
--

DROP TABLE IF EXISTS `missing_ema_storing_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missing_ema_storing_data` (
  `dep_id` int NOT NULL,
  `ts` datetime NOT NULL,
  `local_count` int NOT NULL,
  `cloud_count` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `missing_files`
--

DROP TABLE IF EXISTS `missing_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missing_files` (
  `p_key` int NOT NULL AUTO_INCREMENT,
  `dep_id` int NOT NULL,
  `ts` datetime DEFAULT NULL,
  `local_count` int DEFAULT NULL,
  `cloud_count` int DEFAULT NULL,
  `missing` int NOT NULL,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reward_data`
--

DROP TABLE IF EXISTS `reward_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reward_data` (
  `empathid` varchar(45) NOT NULL,
  `TimeSent` datetime NOT NULL,
  `RecommSent` int DEFAULT NULL,
  `TimeReceived` datetime DEFAULT NULL,
  `reward_datacol` varchar(45) DEFAULT NULL,
  `Response` int DEFAULT NULL,
  `dep_id` int DEFAULT NULL,
  `p_key` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`p_key`)
) ENGINE=InnoDB AUTO_INCREMENT=1631 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
-- SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-21 17:38:50
