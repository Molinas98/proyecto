CREATE DATABASE  IF NOT EXISTS `kibo` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `kibo`;
-- MariaDB dump 10.19  Distrib 10.4.24-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: kibo
-- ------------------------------------------------------
-- Server version	10.4.24-MariaDB

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
-- Table structure for table `estados`
--

DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados`
--

LOCK TABLES `estados` WRITE;
/*!40000 ALTER TABLE `estados` DISABLE KEYS */;
INSERT INTO `estados` VALUES (1,'Enviado'),(2,'Aceptado'),(3,'En Proceso'),(4,'Esperando Pago'),(5,'Pago a confirmar'),(6,'Finalizado'),(7,'Cancelado'),(8,'Rechazado'),(9,'Entregado');
/*!40000 ALTER TABLE `estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles_usuarios`
--

DROP TABLE IF EXISTS `niveles_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `niveles_usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nivel` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_usuarios`
--

LOCK TABLES `niveles_usuarios` WRITE;
/*!40000 ALTER TABLE `niveles_usuarios` DISABLE KEYS */;
INSERT INTO `niveles_usuarios` VALUES (1,'Administrador'),(2,'Empleado'),(3,'Cliente');
/*!40000 ALTER TABLE `niveles_usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trabajos`
--

DROP TABLE IF EXISTS `trabajos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trabajos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  `fecha_limite` date DEFAULT NULL,
  `foto_detalles` varchar(255) DEFAULT NULL,
  `documento` varchar(255) DEFAULT NULL,
  `precio` int(11) DEFAULT NULL,
  `comentario` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL,
  `estado_anterior_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_trabajos_usuarios_idx` (`usuario_id`),
  KEY `fk_trabajos_estados1_idx` (`estado_id`),
  KEY `fk_trabajos_estados2_idx` (`estado_anterior_id`),
  CONSTRAINT `fk_trabajos_estados1` FOREIGN KEY (`estado_id`) REFERENCES `estados` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_trabajos_estados2` FOREIGN KEY (`estado_anterior_id`) REFERENCES `estados` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_trabajos_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trabajos`
--

LOCK TABLES `trabajos` WRITE;
/*!40000 ALTER TABLE `trabajos` DISABLE KEYS */;
INSERT INTO `trabajos` VALUES (1,'Hamburgueseada','Quiero 100 adhesiones con los datos de la foto, cambiar la fecha por 1 de abril','Impreso','2023-03-14','/static/files/1.jpeg',NULL,NULL,NULL,'2023-03-05 12:02:46','2023-03-05 12:02:46',4,1,1),(2,'Caratula','Quiero una caratula con la siguiente imagen.','Digital','2023-03-24','/static/files/2.jpeg','/static/files/trabajo_2.pdf',5000,'El trabajo estará listo mañana','2023-03-05 12:03:24','2023-03-05 12:03:24',4,9,9);
/*!40000 ALTER TABLE `trabajos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trabajos_asignados`
--

DROP TABLE IF EXISTS `trabajos_asignados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trabajos_asignados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trabajo_id` int(11) NOT NULL,
  `empleado_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_trabajos_asignados_trabajos1_idx` (`trabajo_id`),
  KEY `fk_trabajos_asignados_usuarios1_idx` (`empleado_id`),
  CONSTRAINT `fk_trabajos_asignados_trabajos1` FOREIGN KEY (`trabajo_id`) REFERENCES `trabajos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_trabajos_asignados_usuarios1` FOREIGN KEY (`empleado_id`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trabajos_asignados`
--

LOCK TABLES `trabajos_asignados` WRITE;
/*!40000 ALTER TABLE `trabajos_asignados` DISABLE KEYS */;
INSERT INTO `trabajos_asignados` VALUES (1,2,1,'2023-03-05 12:03:42','2023-03-05 12:03:42');
/*!40000 ALTER TABLE `trabajos_asignados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `celular` varchar(45) DEFAULT NULL,
  `activo` tinyint(4) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `nivel_usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_usuarios_niveles_usuarios1_idx` (`nivel_usuario_id`),
  CONSTRAINT `fk_usuarios_niveles_usuarios1` FOREIGN KEY (`nivel_usuario_id`) REFERENCES `niveles_usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Tadeo','Molinas','tade25.molinas@gmail.com','$2b$12$sYzX77L8tCY2eg/.PUWTYe78gZeOXWfVEEo1wUu6Ipd0er.VOwVni','0992843527',1,'2023-02-27 16:54:02','2023-02-27 16:54:02',1),(2,'Javiers','Paredez','javier.paredez@gmail.com','$2b$12$KbQqGYkv1k2ol6F9tZ0cL.blU3FP2sxBeVFgf8WLDp30Y2Bxipbj2','0992125432',1,'2023-02-27 16:54:30','2023-03-05 10:59:00',2),(3,'Marcelo','Aranda','marcelo.aranda@gmail.com','$2b$12$KCQLpUJTtk9q51Y7xP.YxeD8V7hKtCbnlVECeLCYgmKEeL23WLCzu','0981504323',1,'2023-02-27 16:55:02','2023-02-27 16:55:02',2),(4,'Juan','Caballero','juan.caballero@gmail.com','$2b$12$7DV5U61DEx05vqW6ssFt1uEnHCYUhJJR.ozrLP3nPtwUK9Aftu77y','0971453212',1,'2023-02-27 17:06:30','2023-02-27 17:06:30',3),(5,'María','Palacios','maria.palacios@gmail.com','$2b$12$NLuYvF9qdiVEQ0UjWpGxgO20wLckq6X6YQLh60voyFDgWm5xMTHiC','0975436534',1,'2023-03-01 11:45:49','2023-03-01 11:45:49',3),(6,'Lucas','Amarilla','lucas.amarilla@gmail.com','$2b$12$WsSJW3vwQorB2qUD3wAepeOT5KTf3BiwPOBEvTccZfErkHzc8/ppG','0994322315',1,'2023-03-04 16:52:06','2023-03-04 16:52:06',3);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-05 12:10:09
