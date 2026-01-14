-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: scheduler
-- ------------------------------------------------------
-- Server version	8.0.39

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

--
-- Table structure for table `activities`
--

CREATE DATABASE scheduler;
USE scheduler;

DROP TABLE IF EXISTS `activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `team_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `title` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_at` datetime NOT NULL,
  `end_at` datetime NOT NULL,
  `priority` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `kind` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approval_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_by` int NOT NULL,
  `approved_by` int DEFAULT NULL,
  `approval_comment` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `approved_by` (`approved_by`),
  KEY `ix_activities_team_id` (`team_id`),
  KEY `ix_activities_project_id` (`project_id`),
  KEY `ix_activities_start_at` (`start_at`),
  KEY `ix_activities_created_by` (`created_by`),
  KEY `ix_activities_title` (`title`),
  KEY `ix_activities_category_id` (`category_id`),
  KEY `ix_activities_end_at` (`end_at`),
  CONSTRAINT `activities_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `activities_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`),
  CONSTRAINT `activities_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `activities_ibfk_4` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `activities_ibfk_5` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activities`
--

LOCK TABLES `activities` WRITE;
/*!40000 ALTER TABLE `activities` DISABLE KEYS */;
INSERT INTO `activities` VALUES (1,1,NULL,NULL,'Nueva actividad','','2026-01-12 09:15:00','2026-01-12 09:30:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:50','2026-01-13 00:02:50'),(2,1,NULL,NULL,'Nueva actividad','','2026-01-15 12:30:00','2026-01-15 13:00:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:50','2026-01-13 00:02:50'),(3,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:30:00','2026-01-13 13:00:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:51','2026-01-13 00:02:51'),(4,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:30:00','2026-01-13 13:00:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:51','2026-01-13 00:02:51'),(5,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:30:00','2026-01-13 13:00:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:51','2026-01-13 00:02:51'),(6,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:15:00','2026-01-13 12:45:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:51','2026-01-13 00:02:51'),(7,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:15:00','2026-01-13 12:45:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:52','2026-01-13 00:02:52'),(8,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:15:00','2026-01-13 12:45:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:52','2026-01-13 00:02:52'),(9,1,NULL,NULL,'Nueva actividad','','2026-01-13 12:15:00','2026-01-13 12:45:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:52','2026-01-13 00:02:52'),(10,1,NULL,NULL,'Nueva actividad','','2026-01-13 10:00:00','2026-01-13 11:30:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:02:54','2026-01-13 00:02:54'),(11,1,1,NULL,'Nueva actividad','','2026-01-12 10:30:00','2026-01-12 11:45:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:10','2026-01-13 00:03:10'),(12,1,1,NULL,'Nueva actividad','','2026-01-15 11:00:00','2026-01-15 11:30:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:17','2026-01-13 00:03:17'),(13,1,1,NULL,'Nueva actividad','','2026-01-15 11:00:00','2026-01-15 11:30:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:17','2026-01-13 00:03:17'),(14,1,1,NULL,'Nueva actividad','','2026-01-15 11:30:00','2026-01-15 12:00:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:17','2026-01-13 00:03:17'),(15,1,1,NULL,'Nueva actividad','','2026-01-15 11:30:00','2026-01-15 12:00:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:17','2026-01-13 00:03:17'),(16,1,1,NULL,'Nueva actividad','','2026-01-15 11:30:00','2026-01-15 12:00:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:17','2026-01-13 00:03:17'),(17,1,1,NULL,'Nueva actividad','','2026-01-15 11:30:00','2026-01-15 12:00:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:03:18','2026-01-13 00:03:18'),(18,1,1,NULL,'Nueva actividad','','2026-01-12 09:45:00','2026-01-12 10:15:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:04:01','2026-01-13 00:04:01'),(19,1,1,NULL,'Nueva actividad','','2026-01-12 10:15:00','2026-01-12 17:30:00','MEDIUM','SCHEDULED','TEAM','NONE',1,NULL,'','2026-01-13 00:04:05','2026-01-13 00:04:05'),(20,1,NULL,NULL,'Prueba','No se es una prueba XD','2026-01-13 09:15:00','2026-01-13 10:00:00','MEDIUM','SCHEDULED','PERSONAL_EXTRA','APPROVED',1,1,'','2026-01-13 00:10:53','2026-01-13 00:10:53');
/*!40000 ALTER TABLE `activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_assignments`
--

DROP TABLE IF EXISTS `activity_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_assignments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `activity_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_activity_user` (`activity_id`,`user_id`),
  KEY `ix_activity_assignments_activity_id` (`activity_id`),
  KEY `ix_activity_assignments_user_id` (`user_id`),
  CONSTRAINT `activity_assignments_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`id`),
  CONSTRAINT `activity_assignments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_assignments`
--

LOCK TABLES `activity_assignments` WRITE;
/*!40000 ALTER TABLE `activity_assignments` DISABLE KEYS */;
INSERT INTO `activity_assignments` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,20,1);
/*!40000 ALTER TABLE `activity_assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_category_project_name` (`project_id`,`name`),
  KEY `ix_categories_project_id` (`project_id`),
  KEY `ix_categories_name` (`name`),
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feature_roles`
--

DROP TABLE IF EXISTS `feature_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feature_roles` (
  `feature_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`feature_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `feature_roles_ibfk_1` FOREIGN KEY (`feature_id`) REFERENCES `features` (`id`),
  CONSTRAINT `feature_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feature_roles`
--

LOCK TABLES `feature_roles` WRITE;
/*!40000 ALTER TABLE `feature_roles` DISABLE KEYS */;
INSERT INTO `feature_roles` VALUES (1,15),(2,15);
/*!40000 ALTER TABLE `feature_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `features`
--

DROP TABLE IF EXISTS `features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `features` (
  `id` int NOT NULL AUTO_INCREMENT,
  `slug` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `enabled_for_all` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_features_slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `features`
--

LOCK TABLES `features` WRITE;
/*!40000 ALTER TABLE `features` DISABLE KEYS */;
INSERT INTO `features` VALUES (1,'beta_menu','Menú beta (UI)',1,0),(2,'scheduler_experimental','Scheduler experimental',1,0);
/*!40000 ALTER TABLE `features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memberships`
--

DROP TABLE IF EXISTS `memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memberships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_id` int NOT NULL,
  `user_id` int NOT NULL,
  `team_role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_team_user` (`team_id`,`user_id`),
  KEY `ix_memberships_team_id` (`team_id`),
  KEY `ix_memberships_user_id` (`user_id`),
  CONSTRAINT `memberships_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`),
  CONSTRAINT `memberships_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memberships`
--

LOCK TABLES `memberships` WRITE;
/*!40000 ALTER TABLE `memberships` DISABLE KEYS */;
/*!40000 ALTER TABLE `memberships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `owner_manager_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_projects_name` (`name`),
  KEY `ix_projects_owner_manager_id` (`owner_manager_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`owner_manager_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'Development Team','Equipo solamente para desarrollo',1,NULL);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (11,'ADMIN'),(15,'BETA_TESTER'),(12,'MANAGER'),(14,'MEMBER'),(13,'PROJECT_LEADER');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color_hex` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_teams_project_id` (`project_id`),
  KEY `ix_teams_name` (`name`),
  CONSTRAINT `teams_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `chk_teams_color_hex` CHECK (((`color_hex` is null) or regexp_like(`color_hex`,_utf8mb4'^#[0-9A-Fa-f]{6}$')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,1,'SQA','#34517f'),(2,1,'BackEnd Developer',NULL),(3,1,'FrontEnd Developer',NULL);
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,11),(1,15);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `color_hex` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  CONSTRAINT `chk_users_color_hex` CHECK (((`color_hex` is null) or regexp_like(`color_hex`,_utf8mb4'^#[0-9A-Fa-f]{6}$')))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin@test.com','Admin','$2b$12$rpiGH4GwLRz.5Eh4BHi/Z.SITdRSKIStkCiDGcY0OszYV.lN2/flS',1,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-14 10:57:46
