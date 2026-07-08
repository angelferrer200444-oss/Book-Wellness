-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 08-07-2026 a las 23:28:53
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lecturas`
--

INSERT INTO `lecturas` (`id_lectura`, `id_usuario`, `id_libro`, `estado`, `fecha_inicio`, `fecha_fin`, `paginas_leidas`, `capitulos_leidos`, `tiempo_minutos`, `pagina_actual`, `fecha_limite`) VALUES
(2, 22, 41, '', '2026-06-20', '2026-06-20', 21, 3, 2, 21, NULL),
(3, 22, 43, '', '2026-06-20', '2026-06-20', 12, 3, 0, 12, '2026-07-09'),
(4, 6, 44, '', '2026-02-11', '2026-06-20', 13, 3, 5, 13, '2026-06-27'),
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
  `anio` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_libro`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `autor`, `descripcion`, `formato`, `genero`, `es_agregado_manualmente`, `num_caps`, `id_usuario`, `portada`, `categoria`, `key_libro`, `paginas_totales`, `id_google`, `anio`) VALUES
(41, 'Dino IQ (Smart Kids)', 'Roger Priddy', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 10, 22, 'https://covers.openlibrary.org/b/id/1170398-L.jpg', 'leyendo', '/works/OL3260124W', 45, NULL, NULL),
(43, 'The lord of the rings', 'Jude Fisher', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 12, 22, 'https://covers.openlibrary.org/b/id/393983-L.jpg', 'leyendo', '/works/OL5753836W', 65, NULL, NULL),
(44, 'Dinosaur Babies', 'Leonie Bennett', 'Did dinosaurs lay eggs in nests? How big were the eggs? What were the shells like? Did mother dinosaurs care for their babies? These and other questions about the birth and care of dinosaur babies are answered in this fascinating peek into the home lives of these reptiles. The simple text and exciting illustrations along with the tantalizing information will capture the interest of all young readers. Developed by literacy experts, Dinosaur Babies features controlled text with appropriate vocabulary, grammar, and sentence structure for emergent readers. Dinosaur Babies is part of Bearport\'s I Love Reading: Dino World series.', 'Libro Físico', NULL, NULL, 7, 6, 'https://covers.openlibrary.org/b/id/1998640-L.jpg', 'leyendo', '/works/OL5837360W', 244, NULL, NULL),
(45, 'Aiki ne waza', 'Autor desconocido', 'Descripción no disponible', NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/13585127-L.jpg', 'pendiente', '/works/OL34818907W', 192, NULL, NULL),
(46, 'Hermano Lobo', 'Autor desconocido', 'Descripción no disponible', 'Libro Físico', NULL, NULL, 25, 6, 'https://covers.openlibrary.org/b/id/14474590-L.jpg', 'leyendo', '/works/OL25379493W', 224, NULL, NULL),
(64, 'Official Roster of the Soldiers of the State of Ohio in the War of the Rebellion, 1861-1866', 'Ohio. Roster Commission', 'Descripción no disponible', NULL, NULL, NULL, NULL, 6, 'https://books.google.com/books/content?id=mHxIAQAAMAAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73JjK6M_kY6Nk_LFplwbVWEj359jcnVt5bPAp2i8LLDHEuQ0vlQuvY5CotohueE9c6KnTTIjRuyUk0AZW22ruXy_Wgz965tv3OboFazmu-9HngF8HPFiDy54NCgA6pzHnqSe-qw&source=gbs_api', 'leyendo', '', 800, 'mHxIAQAAMAAJ', '1886'),
(68, 'Dos putas en una moto', 'PEDRO', '', NULL, 'misterio', 1, NULL, 6, '/static/uploads/db9699d1d5aebb7264c0568bb9fda1f4.jpg', 'pendiente', NULL, 321, NULL, '1456'),
(69, 'Dos putas en una moto2', 'waza', '', NULL, 'misterio', 1, NULL, 6, '/static/uploads/1786b2947d0846c3b6f9f006e719f727tplv-jj85edgx6n-image-origin.jpeg', 'pendiente', NULL, 12, NULL, '1234'),
(71, 'Dinosaurs', 'Dougal Dixon, David Lambert', 'It\'s a weird world out there... dazzle your friends with wacky facts and more from this mega new series. Did you know... A charging Triceratops could gore an enemy to death with its three terrifying horns. Dinosaur literally means \"terrible lizard.\" The heart of a Sauropod dinosaur would probably have weighed a staggering one ton. A full-color, fun, and informative series, Secret Worlds offers a chance to get your teeth deep into a wide range of fascinating subjects from nature, history, and science. Every title has: Easy-to-read narrative text written by a specialist who combines expert knowledge with an entertaining and fresh style. Superb color photography that entices the reader into the subject world with close-up views and dramatic shots. Weird World feature boxes that reveal a wealth of wacky facts. Tried-and-tested websites to check out the latest info. A mega reference section with even more facts and figures for the enthusiast. Suitable for children aged ten and up -- as well as every other family member who is curious about the subject.', 'Ebook', 'Juvenile Nonfiction / Animals / Dinosaurs & Prehistoric Creatures, Juvenile Nonfiction / History / Prehistoric', 0, 12, 6, 'https://books.google.com/books/content?id=B8vdJ-1iWWUC&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE70ciVT-jW1WbVgQhK9blzH7hmm1GLnr1qnkcHPl-6FK94BOLkT263Koi72B3aIJ3bl9MqqeGbEhk8jtUK5nZdtt1LqLbU7t36tU1d4k7j-jrzsxtjMhrIRUHU9rjDmYRMM1ARiP&source=gbs_api', 'leyendo', '', 96, 'B8vdJ-1iWWUC', '2001'),
(85, 'Dino bites!', 'Algy Craig Hall', 'A cumulative story finds a hungry dinosaur munching and crunching and searching for lunch until his appetite leads him to a buzzing noise, a hop, and a wriggle before he encounters a big surprise.', NULL, 'Dinosaurs, Juvenile fiction, Size, Stories in rhyme, Fiction', NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/13387665-L.jpg', 'pendiente', '/works/OL19964494W', NULL, '', '2013'),
(87, 'Adultery', 'Paulo Coelho', 'Descripción no disponible', NULL, 'Married people, fiction, Politicians, fiction, Fiction, romance, contemporary, Man-woman relationships, Fiction', NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/10132983-L.jpg', 'pendiente', '/works/OL20828419W', 304, '', '2015');

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
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notas_lectura`
--

INSERT INTO `notas_lectura` (`id_nota`, `id_lectura`, `como_te_sientes`, `que_aprendiste`, `palabras_nuevas`, `personaje_destacado`, `escena_impacto`, `continuara`, `parecer_sesion`, `recuerdo_vida`, `notas_observaciones`, `buscaba_al_leer`, `encontro_lo_buscado`) VALUES
(12, 7, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí'),
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
-- Estructura de tabla para la tabla `recomendaciones_cache`
--

DROP TABLE IF EXISTS `recomendaciones_cache`;
CREATE TABLE IF NOT EXISTS `recomendaciones_cache` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `titulo` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `autor` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `portada` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paginas` int DEFAULT NULL,
  `generos` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anio` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_google` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_generacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `recomendaciones_cache`
--

INSERT INTO `recomendaciones_cache` (`id`, `id_usuario`, `titulo`, `autor`, `descripcion`, `portada`, `paginas`, `generos`, `anio`, `id_google`, `fecha_generacion`) VALUES
(11, 6, 'Los Juegos del Hambre - Trilogía Los Juegos del Hambre', 'Suzanne Collins', 'Los Juegos del Hambre, una de las sagas más exitosas de todos los tiempos reunida en un bonito estuche. Este pack contiene los tres títulos de la trilogía Los Juegos del Hambre: Los Juegos de Hambre En una oscura versión del futuro próximo, doce chicos y doce chicas se ven obligados a participar en un reality show llamado Los Juegos del Hambre. Solo hay una regla: matar o morir. En llamas Contra todo pronóstico, Katniss Everdeen y Peeta Mellark han sobrevivido a Los Juegos del Hambre. Deberían sentirse aliviados, pero saben que la tensión crece en el Capitolio, que los gobierna a todos. Sinsajo Los supervivientes de Los Juegos del Hambre no están a salvo. Un meticuloso plan se extiende contra el Capitolio... Y este necesita un símbolo, el emblema de la rebelión: el Sinsajo.', 'https://via.placeholder.com/200x300?text=Sin+Portada', 0, 'Juvenile Fiction', '2019-03-07', '89tu0AEACAAJ', '2026-07-08 19:05:11'),
(10, 6, 'Cien años de soledad', 'Gabriel García Márquez', 'Señalada como «catedral gótica del lenguaje», este clásico del siglo XX es el enorme y espléndido tapiz de la saga de la familia Buendía, en la mítica aldea de Macondo. UNO DE LOS 5 LIBROS MÁS IMPORTANTES DE LOS ÚLTIMOS 125 AÑOS SEGÚN THE NEW YORK TIMES Un referente imprescindible de la vida y la narrativa latinoamericana. «Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo». Con estas palabras empieza la novela ya legendaria en los anales de la literatura universal, una de las aventuras literarias más fascinantes de nuestro siglo. Millones de ejemplares de Cien años de soledad leídos en todas las lenguas y el Premio Nobel de Literatura coronando una obra que se había abierto paso «boca a boca» -como gusta decir al escritor- son la más palpable demostración de que la aventura fabulosa de la familia Buendía-Iguarán, con sus milagros, fantasías, obsesiones, tragedias, incestos, adulterios, rebeldías, descubrimientos y condenas, representaba al mismo tiempo el mito y la historia, la tragedia y el amor del mundo entero. Pablo Neruda dijo... «El Quijote de nuestro tiempo.»', 'http://books.google.com/books/content?id=kmAQCwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 311, 'Fiction', '2015-12-03', 'kmAQCwAAQBAJ', '2026-07-08 19:05:11'),
(9, 6, '1984', 'George Orwell', '75th ANNIVERSARY EDITION “Orwell saw, to his credit, that the act of falsifying reality is only secondarily a way of changing perceptions. It is, above all, a way of asserting power.”—The New Yorker In 1984, London is a grim city in the totalitarian state of Oceania where Big Brother is always watching you and the Thought Police can practically read your mind. Winston Smith is a man in grave danger for the simple reason that his memory still functions. Drawn into a forbidden love affair, Winston finds the courage to join a secret revolutionary organization called The Brotherhood, dedicated to the destruction of the Party. Together with his beloved Julia, he hazards his life in a deadly match against the powers that be. Lionel Trilling said of Orwell’s masterpiece, “1984 is a profound, terrifying, and wholly fascinating book. It is a fantasy of the political future, and like any such fantasy, serves its author as a magnifying device for an examination of the present.” Though the year 1984 now exists in the past, Orwell’s novel remains an urgent call for the individual willing to speak truth to power.', 'http://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 309, 'Fiction', '2013-09-03', 'kotPYEqx7kMC', '2026-07-08 19:05:11'),
(24, 22, 'Orgullo y prejuicio', 'Jane Austen', 'Orgullo y prejuicio (Pride and Prejudice), publicada por primera vez el 28 de enero de 1813 como una obra anónima, es la más famosa de las novelas de Jane Austen y una de las primeras comedias románticas en la historia del género. Su primera frase es, además, una de las más famosas en la literatura inglesa: “Es una verdad mundialmente reconocida que un hombre soltero, poseedor de una gran fortuna, necesita una esposa.” Cuando Jane Austen escribió la novela, apenas tenía veinte años, y compartía habitación con su hermana. La primera redacción de la obra data del periodo 1796-1797; inicialmente recibió el título de \"Primeras impresiones\" (First Impressions), pero nunca fue publicado con ese nombre. En 1797 el padre de Jane lo ofreció a un editor, que lo rechazó. Jane Austen revisó la obra en 1809-1810 y de nuevo en 1812, y la ofreció entonces, con el apoyo de su hermano Henry, a otro editor, que había publicado Sentido y sensibilidad el año anterior. Finalmente fue publicada y pronto gozó de gran éxito. Satírica, profunda y mordaz a un tiempo, la obra de Jane Austen nace de la observación de la vida doméstica y de un profundo conocimiento de la condición humana. Orgullo y prejuicio ha fascinado a generaciones de lectores por sus inolvidables personajes y su desopilante retrato de una sociedad, la Inglaterra victoriana y rural, tan contradictoria como absurda. Esta novela, donde Austen relata la historia de las cinco hermanas Bennet y las tribulaciones de sus respectivos amoríos, ha sido llevada al cine en reiteradas ocasiones, se ha versionado en cómic y en musicales, lo que demuestra su actualidad e interés contemporáneos.', 'http://books.google.com/books/content?id=ojyzDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 328, 'Drama', '2016-07-01', 'ojyzDwAAQBAJ', '2026-07-08 19:16:58'),
(25, 22, 'Cien años de soledad', 'Gabriel García Márquez', 'Señalada como «catedral gótica del lenguaje», este clásico del siglo XX es el enorme y espléndido tapiz de la saga de la familia Buendía, en la mítica aldea de Macondo. UNO DE LOS 5 LIBROS MÁS IMPORTANTES DE LOS ÚLTIMOS 125 AÑOS SEGÚN THE NEW YORK TIMES Un referente imprescindible de la vida y la narrativa latinoamericana. «Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo». Con estas palabras empieza la novela ya legendaria en los anales de la literatura universal, una de las aventuras literarias más fascinantes de nuestro siglo. Millones de ejemplares de Cien años de soledad leídos en todas las lenguas y el Premio Nobel de Literatura coronando una obra que se había abierto paso «boca a boca» -como gusta decir al escritor- son la más palpable demostración de que la aventura fabulosa de la familia Buendía-Iguarán, con sus milagros, fantasías, obsesiones, tragedias, incestos, adulterios, rebeldías, descubrimientos y condenas, representaba al mismo tiempo el mito y la historia, la tragedia y el amor del mundo entero. Pablo Neruda dijo... «El Quijote de nuestro tiempo.»', 'http://books.google.com/books/content?id=kmAQCwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 311, 'Fiction', '2015-12-03', 'kmAQCwAAQBAJ', '2026-07-08 19:16:58');

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
