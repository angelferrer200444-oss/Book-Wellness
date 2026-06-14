-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 06-06-2026 a las 17:35:25
-- Versión del servidor: 8.4.7
-- Versión de PHP: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyectowellness`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lecturas`
--

DROP TABLE IF EXISTS `lecturas`;
CREATE TABLE IF NOT EXISTS `lecturas` (
  `id_lectura` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_libro` int NOT NULL,
  `estado` enum('por_leer','leyendo','terminado','pausado') COLLATE utf8mb4_unicode_ci DEFAULT 'por_leer',
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id_lectura`),
  UNIQUE KEY `uk_lectura_usuario` (`id_lectura`,`id_usuario`),
  KEY `FK_0` (`id_usuario`),
  KEY `FK_1` (`id_libro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `id_libro` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `autor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `num_paginas` int DEFAULT NULL,
  `formato` enum('fisico','digital','audiolibro') COLLATE utf8mb4_unicode_ci DEFAULT 'fisico',
  `genero` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `es_agregado_manualmente` tinyint(1) DEFAULT '0',
  `num_caps` int NOT NULL,
  PRIMARY KEY (`id_libro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notas_sesion`
--

DROP TABLE IF EXISTS `notas_sesion`;
CREATE TABLE IF NOT EXISTS `notas_sesion` (
  `id_nota` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int NOT NULL,
  `contenido` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_nota`),
  KEY `FK_6` (`id_sesion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `objetivos_personales`
--

DROP TABLE IF EXISTS `objetivos_personales`;
CREATE TABLE IF NOT EXISTS `objetivos_personales` (
  `id_objetivo` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `tipo` enum('custom','tiempo_diario','racha_dias','paginas_por_sesion','libros_por_mes','vocabulario_nuevo','constancia_semanal','libros_por_genero') COLLATE utf8mb4_unicode_ci NOT NULL,
  `meta_valor` int NOT NULL,
  `progreso_actual` int DEFAULT '0',
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `completado` tinyint(1) DEFAULT '0',
  `genero_objetivo` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `Porcentaje` decimal(5,2) NOT NULL,
  `Logro_objetivo` enum('logro','objetivo') COLLATE utf8mb4_unicode_ci NOT NULL,
  `descrupcion_custom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Name_custom` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_objetivo`),
  KEY `FK_10` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `palabras_nuevas`
--

DROP TABLE IF EXISTS `palabras_nuevas`;
CREATE TABLE IF NOT EXISTS `palabras_nuevas` (
  `id_palabra` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int NOT NULL,
  `palabra` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_palabra`),
  KEY `FK_4` (`id_sesion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personajes`
--

DROP TABLE IF EXISTS `personajes`;
CREATE TABLE IF NOT EXISTS `personajes` (
  `id_personaje` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int NOT NULL,
  `nombre_personaje` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_libro` int NOT NULL,
  PRIMARY KEY (`id_personaje`),
  KEY `FK_5` (`id_sesion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

DROP TABLE IF EXISTS `sesiones`;
CREATE TABLE IF NOT EXISTS `sesiones` (
  `id_sesion` int NOT NULL AUTO_INCREMENT,
  `id_lectura` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_hora_inicio` datetime NOT NULL,
  `fecha_hora_fin` datetime DEFAULT NULL,
  `tiempo_planeado_minutos` int DEFAULT NULL,
  `tiempo_real_minutos` int DEFAULT NULL,
  `paginas_leidas` int DEFAULT NULL,
  `sentimiento` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `cap_inicio` int DEFAULT NULL,
  `cap_fin` int DEFAULT NULL,
  `cap_leidos` int DEFAULT NULL,
  PRIMARY KEY (`id_sesion`),
  KEY `FK_2` (`id_lectura`,`id_usuario`),
  KEY `FK_3` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  `nivel_actual` enum('principiante','intermedio','avanzado') COLLATE utf8mb4_unicode_ci DEFAULT 'principiante',
  `total_libros_leidos` int DEFAULT '0',
  `total_paginas_leidas` int DEFAULT '0',
  `promedio_paginas_sesion` decimal(5,2) DEFAULT '0.00',
  `genero_preferido` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `uk_usuarios_correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password`, `fecha_registro`, `nivel_actual`, `total_libros_leidos`, `total_paginas_leidas`, `promedio_paginas_sesion`, `genero_preferido`) VALUES
(6, 'Ender', 'enderdg2010@gmail.com', 'ene102010', '2026-06-01 10:07:48', 'principiante', 0, 0, 0.00, '');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `lecturas`
--
ALTER TABLE `lecturas`
  ADD CONSTRAINT `FK_0` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_1` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`) ON DELETE RESTRICT;

--
-- Filtros para la tabla `notas_sesion`
--
ALTER TABLE `notas_sesion`
  ADD CONSTRAINT `FK_6` FOREIGN KEY (`id_sesion`) REFERENCES `sesiones` (`id_sesion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `objetivos_personales`
--
ALTER TABLE `objetivos_personales`
  ADD CONSTRAINT `FK_10` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `palabras_nuevas`
--
ALTER TABLE `palabras_nuevas`
  ADD CONSTRAINT `FK_4` FOREIGN KEY (`id_sesion`) REFERENCES `sesiones` (`id_sesion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `personajes`
--
ALTER TABLE `personajes`
  ADD CONSTRAINT `FK_5` FOREIGN KEY (`id_sesion`) REFERENCES `sesiones` (`id_sesion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD CONSTRAINT `FK_2` FOREIGN KEY (`id_lectura`,`id_usuario`) REFERENCES `lecturas` (`id_lectura`, `id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
