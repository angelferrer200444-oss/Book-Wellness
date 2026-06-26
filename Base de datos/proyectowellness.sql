-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 26-06-2026 a las 07:53:35
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
  `paginas_leidas` int DEFAULT '0',
  `capitulos_leidos` int DEFAULT '0',
  `tiempo_minutos` int DEFAULT '0',
  `pagina_actual` int DEFAULT '0',
  `fecha_limite` date DEFAULT NULL,
  PRIMARY KEY (`id_lectura`),
  UNIQUE KEY `uk_lectura_usuario` (`id_lectura`,`id_usuario`),
  UNIQUE KEY `unico_libro_usuario` (`id_usuario`,`id_libro`),
  KEY `FK_1` (`id_libro`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lecturas`
--

INSERT INTO `lecturas` (`id_lectura`, `id_usuario`, `id_libro`, `estado`, `fecha_inicio`, `fecha_fin`, `paginas_leidas`, `capitulos_leidos`, `tiempo_minutos`, `pagina_actual`, `fecha_limite`) VALUES
(2, 22, 41, '', '2026-06-20', '2026-06-20', 21, 3, 2, 21, NULL),
(3, 22, 43, '', '2026-06-20', '2026-06-20', 12, 3, 0, 12, '2026-07-09'),
(4, 6, 44, '', '2026-06-20', '2026-06-20', 13, 3, 5, 13, '2026-06-27'),
(5, 6, 46, '', '2026-06-20', '2026-06-20', 9, 2, 1, 9, NULL);

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
  `formato` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genero` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `es_agregado_manualmente` tinyint DEFAULT NULL,
  `num_caps` int DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `portada` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pendiente',
  `key_libro` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paginas_totales` int DEFAULT NULL,
  `id_google` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_libro`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `autor`, `descripcion`, `formato`, `genero`, `es_agregado_manualmente`, `num_caps`, `id_usuario`, `portada`, `categoria`, `key_libro`, `paginas_totales`, `id_google`) VALUES
(41, 'Dino IQ (Smart Kids)', 'Roger Priddy', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 10, 22, 'https://covers.openlibrary.org/b/id/1170398-L.jpg', 'leyendo', '/works/OL3260124W', 45, NULL),
(43, 'The lord of the rings', 'Jude Fisher', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 12, 22, 'https://covers.openlibrary.org/b/id/393983-L.jpg', 'leyendo', '/works/OL5753836W', 65, NULL),
(44, 'Dinosaur Babies', 'Leonie Bennett', 'Did dinosaurs lay eggs in nests? How big were the eggs? What were the shells like? Did mother dinosaurs care for their babies? These and other questions about the birth and care of dinosaur babies are answered in this fascinating peek into the home lives of these reptiles. The simple text and exciting illustrations along with the tantalizing information will capture the interest of all young readers. Developed by literacy experts, Dinosaur Babies features controlled text with appropriate vocabulary, grammar, and sentence structure for emergent readers. Dinosaur Babies is part of Bearport\'s I Love Reading: Dino World series.', 'Libro Físico', NULL, NULL, 5, 6, 'https://covers.openlibrary.org/b/id/1998640-L.jpg', 'leyendo', '/works/OL5837360W', 24, NULL),
(45, 'Aiki ne waza', 'Autor desconocido', 'Descripción no disponible', NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/13585127-L.jpg', 'pendiente', '/works/OL34818907W', 192, NULL),
(46, 'Hermano Lobo', 'Autor desconocido', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 25, 6, 'https://covers.openlibrary.org/b/id/14474590-L.jpg', 'leyendo', '/works/OL25379493W', 224, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notas_lectura`
--

DROP TABLE IF EXISTS `notas_lectura`;
CREATE TABLE IF NOT EXISTS `notas_lectura` (
  `id_nota` int NOT NULL AUTO_INCREMENT,
  `id_lectura` int NOT NULL,
  `como_te_sientes` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `que_aprendiste` text COLLATE utf8mb4_unicode_ci,
  `palabras_nuevas` text COLLATE utf8mb4_unicode_ci,
  `personaje_destacado` text COLLATE utf8mb4_unicode_ci,
  `escena_impacto` text COLLATE utf8mb4_unicode_ci,
  `continuara` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `parecer_sesion` text COLLATE utf8mb4_unicode_ci,
  `recuerdo_vida` text COLLATE utf8mb4_unicode_ci,
  `notas_observaciones` text COLLATE utf8mb4_unicode_ci,
  `buscaba_al_leer` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `encontro_lo_buscado` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_nota`),
  KEY `id_lectura` (`id_lectura`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notas_lectura`
--

INSERT INTO `notas_lectura` (`id_nota`, `id_lectura`, `como_te_sientes`, `que_aprendiste`, `palabras_nuevas`, `personaje_destacado`, `escena_impacto`, `continuara`, `parecer_sesion`, `recuerdo_vida`, `notas_observaciones`, `buscaba_al_leer`, `encontro_lo_buscado`) VALUES
(11, 6, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí'),
(10, 4, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí'),
(9, 4, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí');

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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password`, `fecha_registro`, `nivel_actual`, `total_libros_leidos`, `total_paginas_leidas`, `promedio_paginas_sesion`, `genero_preferido`) VALUES
(6, 'Ender', 'enderdg2010@gmail.com', 'ene102010', '2026-06-01 10:07:48', 'principiante', 0, 0, 0.00, ''),
(22, 'popo', 'popeto123@gmail.com', '123', '2026-06-07 13:50:45', 'principiante', 0, 0, 0.00, '');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `lecturas`
--
ALTER TABLE `lecturas`
  ADD CONSTRAINT `FK_0` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_1` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`) ON DELETE CASCADE;

--
-- Filtros para la tabla `objetivos_personales`
--
ALTER TABLE `objetivos_personales`
  ADD CONSTRAINT `FK_10` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

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
