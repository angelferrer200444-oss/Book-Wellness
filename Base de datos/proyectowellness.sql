-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-07-2026 a las 16:53:01
-- Versión del servidor: 10.1.38-MariaDB
-- Versión de PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
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

CREATE TABLE `lecturas` (
  `id_lectura` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_libro` int(11) NOT NULL,
  `estado` enum('por_leer','leyendo','terminado','pausado') COLLATE utf8mb4_unicode_ci DEFAULT 'por_leer',
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `paginas_leidas` int(11) DEFAULT '0',
  `capitulos_leidos` int(11) DEFAULT '0',
  `tiempo_minutos` int(11) DEFAULT '0',
  `pagina_actual` int(11) DEFAULT '0',
  `fecha_limite` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lecturas`
--

INSERT INTO `lecturas` (`id_lectura`, `id_usuario`, `id_libro`, `estado`, `fecha_inicio`, `fecha_fin`, `paginas_leidas`, `capitulos_leidos`, `tiempo_minutos`, `pagina_actual`, `fecha_limite`) VALUES
(2, 22, 41, '', '2026-06-20', '2026-06-20', 21, 3, 2, 21, NULL),
(3, 22, 43, '', '2026-06-20', '2026-06-20', 12, 3, 0, 12, '2026-07-09'),
(4, 6, 44, '', '2026-02-11', '2026-06-20', 13, 3, 5, 13, '2026-06-27'),
(5, 6, 46, '', '2026-06-20', '2026-06-20', 9, 2, 1, 9, NULL),
(6, 23, 91, '', '2026-07-11', '2026-07-15', 76, 9, 0, 61, NULL),
(8, 23, 92, '', '2026-07-12', '2026-07-14', 10, 17, 0, 137, NULL),
(11, 23, 124, 'por_leer', '0000-00-00', NULL, 0, 4, 0, 33, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `titulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `autor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `formato` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genero` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `es_agregado_manualmente` tinyint(4) DEFAULT NULL,
  `num_caps` int(11) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `portada` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pendiente',
  `key_libro` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paginas_totales` int(11) DEFAULT NULL,
  `id_google` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anio` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
(87, 'Adultery', 'Paulo Coelho', 'Descripción no disponible', NULL, 'Married people, fiction, Politicians, fiction, Fiction, romance, contemporary, Man-woman relationships, Fiction', NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/10132983-L.jpg', 'pendiente', '/works/OL20828419W', 304, '', '2015'),
(91, 'They Came to Baghdad', 'Agatha Christie', 'E-book exclusive extras: \'Agatha Christie in Baghdad,\' extensive selections from Agatha Christie: An Autobiography. Plus: Christie biographer Charles Osborne\'s essay on They Came to Baghdad.Agatha Christie first visited Baghdad as a tourist in 1927; many years later she would become a resident of the exotic and then open city, and it was here, and while on archaeological digs throughout Iraq with her husband, Sir Max Mallowan, that Agatha Christie wrote some of her most important works.They Came to Baghdad is one of Agatha Christie\'s highly successful forays into the spy thriller genre. In this novel, Baghdad is the chosen location for a secret superpower summit. But the word is out, and an underground organisation is plotting to sabotage the talks.Into this explosive situation stumbles Victoria Jones, a young woman with a yearning for adventure who gets more than she bargains for when a wounded secret agent dies in her hotel room. Now, if only she could make sense of his final words: \'Lucifer... Basrah... Lefarge...\'', 'Libro Físico', 'English Spy stories, Fiction, Mystery, Conspiracy, French literature', NULL, 23, 23, 'https://covers.openlibrary.org/b/id/12846782-L.jpg', 'leyendo', '/works/OL472215W', 199, '', '1993'),
(92, 'La casa entre los pinos', 'Ana Reyes', '<p> <b>Dos muertes súbitas y misteriosas en idénticas circunstancias.</b> </p> <p> <b>Un thriller psicológico absorbente que Reese Witherspoon seleccionó para su club de lectura.</b> </p> <p>Maya no está pasando por su mejor momento. Acaba de dejar un medicamento que regula los ataques de pánico, sufre síndrome de abstinencia, lleva días sin dormir y bebe demasiado. Por eso, cuando frente a la pantalla de su móvil revive lo ocurrido el verano de sus diecisiete años no sabe si puede confiar en la lucidez de su mente. Las imágenes de seguridad de una cafetería registran la muerte súbita de una joven. Junto a ella está Frank Bellamy. Ni siquiera se han rozado, pero Maya sabe que él es el responsable, igual que lo fue de la muerte de Aubrey siete años atrás.</p> <p>Maya no tiene otra salida que investigar sobre los enigmas del pasado para poder resolver los del presente. Y para ello tendrá que regresar a la cabaña del bosque y adentrarse en los recuerdos que la aterrorizan.</p> <p> <b>La crítica ha dicho:</b> <br> «Un misterio escalofriante sobre la memoria y el deseo». <br> <i>The Times</i> </p> <p>«Un thriller del que es imposible despegarse... Un viaje salvaje que me ha transportado volando de un capítulo al siguiente». <br> Reese Witherspoon</p> <p>«Magnífico». <br> M. W. Craven</p> <p>«Una adictiva, inteligente e inquietante historia de suspense psicológico sobre la complejidad de la amistad femenina y la fragilidad de los recuerdos». <br> Alafair Burke</p> <p>«Me encantó. Lo leí del tirón, totalmente enganchada y ansiosa por conocer la verdad». <br> Lisa Gardner</p> <p>«Una mezcla absorbente de thriller psicológico y cuento de hadas muy oscuro. Explora las múltiples maneras en que los recuerdos nos fallan y cómo pueden también liberarnos». <br> Riley Sager</p>', 'Ebook', 'Fiction / Thrillers / Psychological, Fiction / Thrillers / Supernatural', NULL, 38, 23, 'https://books.google.com/books/publisher/content?id=-rwgEQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73HiqUJ83Mq81HgpdmXguq6vCkYvRx9M3RTt0pYRFX2c9BGjeTR4wVtv11BxlLNM1QTXIP57ExfJT-vOzouGIf1rqHd5ytCXsyO8fzJRsCSDXHKtv2bFe459RsLS_IaZ7_mstVT&source=gbs_api', 'leyendo', '', 338, '-rwgEQAAQBAJ', '2024-10-10'),
(95, 'La Policía de la Memoria', 'Yoko Ogawa', '<p> <b>Una poderosa y delicada novela, de tintes orwellianos, sobre el control social y la memoria.</b> </p> <p>En una pequeña isla se produce un misterioso fenómeno. Un día desaparecen los pájaros, al siguiente podría desaparecer cualquier cosa: los peces, los árboles... Peor aún, también se desvanecerá la memoria de ellos, al igual que las emociones y sensaciones que llevaban asociadas. Nadie sabrá ni recordará entonces qué eran. Hay incluso una policía dedicada a perseguir a los que conservan la capacidad de recordar lo que ya no existe. En esa isla vive una joven escritora que, tras la muerte de su madre, intenta escribir una novela mientras trata de proteger a su editor, que está en peligro porque forma parte de los pocos que recuerdan. La ayudará un anciano al que empiezan a fallarle las fuerzas. Mientras, lentamente, nuestra protagonista va dando forma a su novela: es el relato de una mecanógrafa cuyo jefe acaba reteniéndola contra su voluntad en un altillo. Una obra sobre el poder de la memoria y sobre la pérdida.</p>', NULL, 'Fiction / General', NULL, NULL, 23, 'https://books.google.com/books/publisher/content?id=Xc0QEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE72_7rH211KTyleZYj2O0KmxeJZgNWa2awvU3dff4RkgEia3S3bktY9cVGBck-4Ggpi0LZrSOVwewa67lsYdT5qumawviHQBPVpqPWYKMrBNWoweKm3xmLwcrpsy9kCQo_b36G1l&source=gbs_api', 'pendiente', '', 400, 'Xc0QEAAAQBAJ', '2021-02-10'),
(96, 'El invencible verano de Liliana', 'Cristina Rivera Garza', '<p> <b>«Más allá de las partes que hablan con franqueza del inmenso amor entre las hermanas, El invencible verano de Liliana es en sí mismo un acto de amor para Liliana. Una expansión de la hermandad compartida entre mujeres, que también se llama feminismo.» Nayeli García Sánchez</b> </p> <p>«El 16 de julio de 1990, <b>Liliana Rivera Garza, mi hermana, fue víctima de un feminicidio</b>. Era una muchacha de 20 años, estudiante de arquitectura. Tenía años tratando de terminar su relación con un novio de la preparatoria que insistía en no dejarla ir. La decisión de él fue que ella no tendría una vida sin él.</p> <p> <i>El invencible verano de Liliana</i> es una excavación en la vida de una mujer brillante y audaz que careció, como nosotros mismos, del lenguaje necesario para identificar, denunciar y luchar contra la violencia sexista y el terrorismo de pareja. Este libro es para celebrar su paso por la tierra y para decirle que, claro que sí, <b>al patriarcado lo vamos a tirar</b>.» Cristina Rivera Garza</p> <p>*Premio Rodolfo Walsh 2022*</p> <p>*Premio Mazatlán de Literatura 2022*</p> <p>*Premio Xavier Villaurrutia de Escritores para Escritores 2021*</p> <p>*Premio Nuevo León Alfonso Reyes 2021*</p> <p>*Premio Iberoamericano de Letras José Donoso 2021*</p>', NULL, 'Biography & Autobiography / Literary Figures, Social Science / Women\'s Studies', NULL, NULL, 23, 'https://books.google.com/books/publisher/content?id=gcUrEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE71TGCoRNYKakvrUkKVTxs9csWRkxJk--04yMr1tG9NgWV0nW2ns2qBpciS0krx2zczhmsJcZL7Vz0ZqAHIsZqPcECJoFYbZcJN7gPIJuqpI4YefCt2bd3pcZB7yAPH87-7VvqF6&source=gbs_api', 'pendiente', '', 304, 'gcUrEAAAQBAJ', '2021-04-23'),
(107, 'Pokémon Escuela De Entrenadores', 'ActorBrian', 'Imagina que todos los protagonista de cada videojuego de la saga pokemon lo pongamos en una jaula y lo veamos pelear. Ja-Ja-Ja no es para tanto.  Esta historia es para fanes pokemon, ¿si quieres reirte un poco y difrutar de tus entrenadores favoritos?, pues imagina que todos sean de secundaria en una clase del instituto de entrenadores pokemon, donde convivirán entre ellos en una clase lleno de las historias mas locas y divertidas que veras.  Aclaraciones:  Antes de nada me quiero asegurar de algunas cosas como ejemplo:  Para los nombres de los personajes  usare los nombre del juego, osea Serena se llamara Serena, ¡Los estoy viendo AmourShipping!, no sera la misma Serena del anime.  <Uno se va de su asiento>...  Ok, Para las personalidades me guiare del manga, Pokemon Adventure, si no lo leíste pues Looser, Nah solo bromeo, te aconsejo el manga es buenisimo y si no aparece un personaje de pokemon significa que hará su aparición pronto, con todo aclarado, disfruta de mi obra 😊. Todos los derechos reservados', 'Digital', 'fanfic, batallas, aventura, escuela, pokemon', 1, 119, 23, 'https://res.cloudinary.com/jklaybsr/image/upload/v1783792735/hpuso516nkaq6gcvqjhb.jpg', 'pendiente', NULL, 0, NULL, ''),
(108, 'El club de los poetas muertos', 'N. H. Kleinbaum', 'A una prestigiosa academia de educación más bien estricta y conservadora llega un nuevo profesor, el señor Keating, dispuesto a enseñar a los chicos nuevos metodos de aprendizaje a través de la poesía y las letras y nuevas ídeas que no congeniarán para nada con la academia, mediante el lema Carpe diem (aprovecha el tiempo) este profesor guiará a su ejercito de alumnos...y las consecuencias podrán ser trágicas... Este libro fue llevado al cine con gran éxito.', NULL, 'No disponible', 0, NULL, 23, 'https://covers.openlibrary.org/b/id/9279160-L.jpg', 'pendiente', '/works/OL20640389W', 172, '', '1991'),
(114, 'Soy un gato', 'Natsume Soseki', '\"Soy un gato, aunque todavía no tengo nombre\". Así comienza la primera y más hilarante novela de Natsume Soseki, una auténtica obra maestra de la literatura japonesa, que narra las aventuras de un desdeñoso felino que cohabita, de modo accidental, con un grupo de grotescos personajes, miembros todos ellos de la bienpensante clase media tokiota: el dispéptico profesor Kushami y su familia, teóricos dueños de la casa donde vive el gato; el mejor amigo del profesor, el charlatán e irritante Meitei; o el joven estudioso Kangetsu, que día sí, día no, intenta arreglárselas para conquistar a la hija de los vecinos. Escrita justo antes de su aclamada novela Botchan, Soy un gato es una sátira descarnada de la burguesía Meiji. Dotada de un ingenio a prueba de bombas y de un humor sardónico, recorre las peripecias de un voluble filósofo gatuno que no se cansa de hacer los comentarios más incisivos sobre la disparatada tropa de seres humanos con la que le ha tocado convivir.', NULL, 'Fiction / Literary', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=d1VVEQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE72b67ZouSbrFinQDe_DCsvpOLzOps-ZgHC8vjR4ZUx5q6baddTuRAGT7olLraYJMuzm7L50p4ESCuFzFmawzc3QzwAcl9qdBJc0Z_8fl_1kBmfNnP0F4kyKsHrlL9CIrKqGcWOD&source=gbs_api', 'pendiente', '', 656, 'd1VVEQAAQBAJ', '2010-04-05'),
(115, 'Sword Art Online', 'Reki Kawahara', 'Un jugador solitario llamado Kirito , que tuvo la suerte de jugar la versión beta del primer VRMMORPG, « Sword Art Online » (SAO), se encontraba entre los 10.000 jugadores atrapados en el juego durante el primer día de su lanzamiento oficial. La única forma de escapar era completar todos los pisos de Aincrad, el castillo flotante donde se desarrolla el juego, y derrotar al jefe final. Morir en el juego significaba morir en la vida real, debido al NerveGear , una consola que simulaba los controles del personaje redirigiendo las señales cerebrales. Dos años después del inicio de este juego mortal, de los diez mil jugadores originales, quedaban menos de siete mil, con veinticinco pisos por completar.', 'Digital', 'Isekai, Acción, Aventura, Fantasía, Romance', 1, 25, 23, 'https://res.cloudinary.com/jklaybsr/image/upload/v1784041241/j0zud3delzzmwadgp6s3.jpg', 'pendiente', NULL, 360, NULL, '2003'),
(119, 'El secreto', 'Donna Tartt', '<p> <b>30 ANIVERSARIO</b> <br> <b>POR LA AUTORA DE </b> <i> <b>EL JILGUERO</b> </i> <b>, GANADORA DEL PREMIO PULITZER</b> </p> <p> <p> <b>UNO DE LOS MEJORES LIBROS DE LA HISTORIA SEGÚN LOS LECTORES DE <i>THE GUARDIAN</i> </b> </p> <p> <p>«La historia del misterioso asesinato que sigue fascinando treinta años después.» <br> <b>BBC</b> </p> <p> <p>«Una auténtica maravilla. [...] Contundente, sólida e impecablemente contada.» <br> <i> <b>The New York Times</b> </i> </p> <p>«Donna Tartt es una escritora increíblemente buena: profunda, sugerente. Una narradora extraordinaria.» <br> <b>Stephen King</b> </p> <p> <p>La vida no es fácil en un college de Nueva Inglaterra si eres un chico modesto y falto de afecto que llega de California, y Richard Papen lo sabe; por eso agradece que lo admitan en un pequeño grupo de cinco estudiantes capitaneados por un profesor de literatura clásica con mucho carisma y pocos escrúpulos.</p> <p>Los chicos sueltan comentarios en griego y se ríen de la ingenuidad y la torpeza de los demás, pero bien mirado se pasan el día bebiendo y engullendo pastillas. Hasta que un mal día lo que parecían chiquilladas adquieren una gravedad inesperada. Es entonces cuando Richard y su pandilla descubren qué difícil es vivir sin máscaras y qué fácil es matar sin remordimientos.</p> <p> <i>El secreto</i>, primera novela de la gran Donna Tartt, se cuenta entre las mejores obras del siglo XX.</p> <p> <b>La crítica ha dicho:</b> <br> «Si alguna vez pensaste que estudiar Letras era solo corregir comas y leer en bata junto a una chimenea, este libro te va a sacar de tu error. <i>El secreto</i> es como si <i>El club de los poetas muertos</i> y un thriller psicológico tuvieran un hijo oscuro y elegante. Secretos y culpa para recordarte que no todo lo que brilla es oro, ni todo lo clásico es inocente.» <br> Ana Trasobares, <i>Esquire </i> </p> <p>«El único libro que desearía haber escrito». <br> Camilla Läckberg, <i>Elle</i> </p> <p>«Uno de esos libros nacidos para ser clásicos instantáneos. Una lectura perfecta para estar en el sofá, tapado, con la única necesidad de devorar sus páginas (advertencia: tiene un alto componente adictivo, que su longitud no cause rechazo a los curiosos). [...] Durante sus páginas se puede disfrutar con todo: el misterio, el lujo, amores no correspondidos... El propio college semeja un elemento vivo más. Cualquier enamorado de la estética dark academia (hola, Miércoles Adams) encontrará aquí el santo grial». <br> Alba Álvarez (autora de Pellejos), <i> Vogue</i> </p> <p>«Una novela imposible de abandonar hasta la última página.» <br> John Grisham</p> <p>«La voz de Tartt no es como la de sus contemporáneos. Su bello lenguaje, su intrincado argumento y sus fascinantes personajes ya se notan de lejos en su debut.» <br> <i>Cosmopolitan</i> </p> <p>«Vestida como un diminuto gentleman andrógino, con zapatos Oxford, chalecos y corbatas y peinada con un <i>bob </i>imperturbable (desde Tom Wolfe, ningún escritor había hecho tan bien lo del <i>autobranding</i>), a Tartt la rodeaba un relato fabuloso, una historia que se ha demostrado no del todo o casi nada cierta que hablaba de gentileza del Sur y dinero viejo. [ <i>El secreto</i>] se ha convertido en un libro de culto, muy citado, leído y disfrutado.» <br> Begoña Gómez Urzaiz, <i>El País</i> </p> <p>«Como entretenimiento de ritmo feroz, es un éxito magnífico.» <br> <i>The New York Times </i> </p> <p>«Una novela descomunal, fascinante e arrolladora.» <br> <i>Vanity Fair</i> </p> <p>«Inquietante, convincente y maravilloso. [...] Repleto de referencias literarias, con un estilo elegante y una atmósfera que recuerdan más al siglo XIX que el XX.» <br> <i>The Time</i> </p>', NULL, 'Fiction / General', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=qZ3tAgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70cWsfuo-xFkiA6OuqRZs1a4eYLh2M0tEmGDed1MAKmwW4Was00EvKgCS3-LjkffkuKYzYlPK_Ww2D_Qr-CMRwBeTCpnWwl99n_I12ANnSZwqNWxpSfwQ8cuJMs20g850JqTO2D&source=gbs_api', 'pendiente', '', 776, 'qZ3tAgAAQBAJ', '2014-03-13'),
(124, 'Cosas pequeñas como esas', 'Claire Keegan', 'Qué quietud había ahí arriba, pero ¿por qué nunca estaba en paz? El día aún no despuntaba, y Furlong miró hacia el río oscuro y brillante cuya superficie reflejaba partes equivalentes del pueblo iluminado. Eran tantas las cosas que se veían mejor, cuando no estaban tan cerca. No pudo decir cuál prefería; si la vista del pueblo o su reflejo en el agua. Invierno de 1985 en un pequeño pueblo irlandés. Bill Furlong es un hombre amable y un trabajador infatigable, vende carbón y madera. Su única preocupación es que a su esposa y a sus cinco hijas no les falte nada. Lleva una vida tranquila y rutinaria, hasta que un día, mientras entrega un pedido en el convento del pueblo, se involucra en una situación que le devuelve otra imagen de su pasado, dejándolo en medio de una encrucijada definitiva: por un lado, seguir su instinto de autopreservación y mirar hacia abajo, por el otro, actuar con coraje y hacer lo correcto, sin importar las consecuencias. Claire Keegan, una de las voces más potentes de la literatura irlandesa contemporánea, se detiene con perspicacia en esas pequeñas cosas que hacen la diferencia y construye una novela de una delicadeza conmovedora. &quot;En Cosas pequeñas como esas, Claire Keegan crea escenas con asombrosa claridad y lucidez. Esta es la historia de lo que sucedió en Irlanda, contado con simpatía y precisión emocional.&quot; Colm Tóibín', 'Ebook', 'Literary Criticism / Women Authors, Fiction / General', 0, 7, 23, 'https://books.google.com/books/publisher/content?id=i91EEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73XjLzLggM0tFuhxTp9bG5esxKG6INF82zw-py1P1SPL_PbmSgPqwP_HKokeO32xZbeXwDWlK2908X1-SWt75X1PfAjRnz46UxFphE5EX1vnjlNbjLNKSTvMOnXUhZ--KojyQ-S&source=gbs_api', 'leyendo', '', 96, 'i91EEAAAQBAJ', '2021-09-24'),
(126, 'Jurassic Park', 'Michael Crichton', ' El multimillonario John Hammond utiliza ADN extraído de mosquitos fosilizados para clonar dinosaurios y construir un parque temático exclusivo en la Isla Nublar. Antes de abrir al público, invita a un grupo de científicos (incluyendo al matemático Ian Malcolm, el paleontólogo Alan Grant y la paleobotánica Ellie Sattler) para evaluar su seguridad. Sin embargo, la codicia y el sabotaje informático provocan que los sistemas de seguridad fallen, dejando a los visitantes atrapados junto a dinosaurios depredadores.', 'Digital', 'ciencia ficción, tecno-thriller, aventuras', 1, 68, 23, 'https://res.cloudinary.com/jklaybsr/image/upload/v1784580493/pl4rrers3feqphyjg9tl.jpg', 'pendiente', NULL, 480, NULL, '1990'),
(127, 'La máquina del tiempo', 'H. G. Wells', '<p> <b>La obra pionera de los viajes en el tiempo, escrita por uno de los padres de la ciencia ficción.</b> </p> <p> <b>Cubierta diseñada por Adrià Molins.</b> <br> <b>Traducción de José C. Vales.</b> <br> —Hace mucho tiempo tuve la idea de una máquina... <br> —¡Para viajar en el tiempo! —exclamó el jovencito. <br> —Y podría viajar absolutamente en cualquier dirección en el tiempo y en el espacio, dependiendo del gusto del piloto. <br> <i>La máquina del tiempo</i> fue la primera obra de éxito de G. H. Wells y pionera en los Viajes en el tiempo. A finales del siglo XX, un hombre idea una máquina con la que asegura poder viajar en el tiempo. Ante la incredulidad de los científicos de la época, el Viajero del Tiempo consigue llegar al futuro, donde, tras una serie de aventuras, aterrizará a un mundo aterrador habitado por unos seres extraños llamados Eloi y Morlocks.</p>', NULL, 'Fiction / Classics, Fiction / Science Fiction / General', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=KAuSDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73YYy-qUX3xKZGbRIu4Hy-O0cjN292dTBG9lxTS6guHUakny_gZ4kljHK1QmwXUh_-Z6z8xnSuMUXs67v4ioyfzzKbc04cWWUPgULL4HbgZTLBw6bzWYVvIkV8ssoU8Wr0rHFAX&source=gbs_api', 'pendiente', '', 224, 'KAuSDwAAQBAJ', '2019-06-18'),
(128, 'La paciente silenciosa / The Silent Patient', 'Alex Michaelides', '<b>«El<i> thriller</i> perfecto» (según A.J. Finn, autor de<i> La mujer en la ventana</i>) que está conmocionando a treinta y siete países y cuyos derechos han sido comprados para una adaptación cinematográfica producida por Brad Pitt.<br><br></b>SOLO ELLA SABE LO QUE SUCEDIÓ.<br><br>SOLO YO PUEDO HACERLA HABLAR.<br><br>Alicia Berenson, una pintora de éxito, dispara cinco tiros en la cabeza de su marido, y no vuelve a hablar nunca más. Su negativa a emitir palabra alguna convierte una tragedia doméstica en un misterio que atrapa la imaginación de toda Inglaterra.<br><br>Theo Faber, un ambicioso psicoterapeuta forense obsesionado con el caso, está empeñado en desentrañar el misterio de lo que ocurrió aquella noche fatal y consigue una plaza en The Grove, la unidad de seguridad en el norte de Londres a la que Alicia fue enviada hace seis años y en la que sigue obstinada en su silencio. Pronto descubre que el mutismo de la paciente está mucho más enraizado de lo que pensaba. Pero, si al final hablara, ¿estaría dispuesto a escuchar la verdad?<br><br><b>ENGLISH DESCRIPTION<br><br>On the list of the Best 2019 Mystery / Thrillers Books of <i>Publishers Weekly</i></b><br><br><b>The instant #1 <i>New York Times </i>bestseller<br></b><br>\"An unforgettable―and Hollywood-bound―new thriller... A mix of Hitchcockian suspense, Agatha Christie plotting, and Greek tragedy.\". <b>―<i>Entertainment Weekly<br></i></b><br><b><i>The Silent Patient</i> is a shocking psychological thriller of a woman’s act of violence against her husband―and of the therapist obsessed with uncovering her motive.</b><br><br>Alicia Berenson’s life is seemingly perfect. A famous painter married to an in-demand fashion photographer, she lives in a grand house with big windows overlooking a park in one of London’s most desirable areas. One evening her husband Gabriel returns home late from a fashion shoot, and Alicia shoots him five times in the face, and then never speaks another word.<br><br>Alicia’s refusal to talk, or give any kind of explanation, turns a domestic tragedy into something far grander, a mystery that captures the public imagination and casts Alicia into notoriety. The price of her art skyrockets, and she, the silent patient, is hidden away from the tabloids and spotlight at the Grove, a secure forensic unit in North London.<br><br>Theo Faber is a criminal psychotherapist who has waited a long time for the opportunity to work with Alicia. His determination to get her to talk and unravel the mystery of why she shot her husband takes him down a twisting path into his own motivations―a search for the truth that threatens to consume him....', NULL, 'Fiction / Thrillers / Psychological, Fiction / Thrillers / Suspense', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=gGWREAAAQBAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE73l4VZwideSvGo_lQ6cKXnXoVyGLpIkoyFlQkwZPRk96UgsJ26nsBQgGes-gPOiSU4dsbs90UZ2bJTLynSwXQvTFwcG74DW5wmdZTGXRLhyxv6xrnqh93C6VK8malfe6WNWI_N0&source=gbs_api', 'pendiente', '', 384, 'gGWREAAAQBAJ', '2020-01-21'),
(130, 'El nombre del viento (Crónica del asesino de reyes 1)', 'Patrick Rothfuss', '<p> <b>Atípica, profunda y sincera, </b> <i> <b>El nombre del viento</b> </i> <b> es una novela de aventuras, de historias dentro de otras historias, de misterio, de amistad, de amor, de magia y de superación.</b> </p> <p> <p> <b>La novela que ha consagrado a Patrick Rothfuss como fenómeno editorial de los últimos años.</b> </p> <p>En una posada en tierra de nadie, un hombre se dispone a relatar, por primera vez, la auténtica historia de su vida. Una historia que únicamente él conoce y que ha quedado diluida tras los rumores, las conjeturas y los cuentos de taberna que le han convertido en un personaje legendario a quien todos daban ya por muerto: Kvothe... músico, mendigo, ladrón, estudiante, mago, héroe y asesino.</p> <p>Ahora va a revelar la verdad sobre sí mismo. Y para ello debe empezar por el principio: su infancia en una troupe de artistas itinerantes, los años malviviendo como un ladronzuelo en las calles de una gran ciudad y su llegada a una universidad donde esperaba encontrar todas las respuestas que había estado buscando.</p> <p> <b>«Viajé, amé, perdí, confié y me traicionaron».</b> </p> <p>«He robado princesas a reyes agónicos. Incendié la ciudad de Trebon. He pasado la noche con Felurian y he despertado vivo y cuerdo. Me expulsaron de la Universidad a una edad a la que a la mayoría todavía no los dejan entrar. He recorrido de noche caminos de los que otros no se atreven a hablar ni siquiera de día. He hablado con dioses, he amado a mujeres y he escrito canciones que hacen llorar a los bardos.</p> <p> <p>Me llamo Kvothe. Quizá hayas oído hablar de mí».</p> <p> <b>La crítica ha dicho...</b> <br> «Una estupenda y fuera de lo común novela de aventuras fantásticas». <br> Justo Navarro, <i>El País</i> </p> <p>«Sin duda <i>El nombre del viento</i> se convertirá en un clásico». <br> <i>The Times</i> </p> <p>«Un libro para quien conoce el mágico poder de las palabras». <br> Ricard Ruiz Garzón, <i>El Periódico de Catalunya</i> </p> <p>«Una aventura insólita y preciosa. Puntuación: Sobresaliente». <br> Manu González, <i>Qué Leer</i> </p> <p>«No sucede a menudo, pero <i>El nombre del viento</i> de Patrick Rothfuss sí es tan bueno como dicen las reseñas». <br> <i>Locus</i> </p> <p>«A veces, con suerte y unas cuantas recomendaciones de buenos amigos, se vuelve a descubrir otro paraíso en el que quedarse, un par de semanas, unos cuantos días. Y eso es justo lo que me ha pasado con <i>El nombre del viento</i>». <br> Toni Rodero, <i>La Voz de Avilés</i> </p>', NULL, 'Fiction / Fantasy / General, Fiction / Action & Adventure', 0, NULL, 23, 'https://books.google.com/books/content?id=QeYF9kTMypgC&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73MXtzVCieYub9rZHtYthHq7lGzi3ytUEZJyW7NFZzQ1aDiusuf7i5_5zHFRXb1naW8JVqVV4Us9ACbaikSKkKdiM3xdyFk6wTXfR4Im35yG3mGnGRusBQ_hVh69mMatCV-6aJn&source=gbs_api', 'pendiente', '', 880, 'QeYF9kTMypgC', '2011-11-18'),
(131, 'Moby Dick', 'Herman Melville', 'Este ebook presenta &quot;Moby Dick&quot;, con un indice dinámico y detallado. Moby-Dick es una novela de Herman Melville publicada en 1851. Narra la travesía del barco ballenero Pequod en la obsesiva y autodestructiva persecución de una gran ballena blanca (cachalote) impulsada por el capitán Ahab. Al margen de la persecución y evolución de sus personajes, el tema de la novela es eminentemente enciclopédico al incluir detalladas y extensas descripciones de la caza de las ballenas en el siglo XIX y multitud de otros detalles sobre la vida marinera de la época. Quizá por ello la novela no tuvo ningún éxito comercial en su primera publicación, aunque con posterioridad haya servido para cimentar la reputación del autor y situarlo entre los mejores escritoires estadounidenses. Herman Melville (1819 – 1891) - novelista y poeta norteamericano y una de las principales figuras de la historia de la literatura. Con apenas veinte años, Melville comenzó una serie de viajes por todo el mundo que más adelante le servirían como base e inspiración para varias de sus novelas, incluyendo varios años trabajando como ballenero y pasando varias aventuras en las islas del Pacífico. El mar y su mundo son fundamentales en la obra de Melville, como ya se aprecia en Mardi o Taipi.', NULL, 'Fiction / Classics, Fiction / Literary', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=4KJjDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70MfFVJyjVOE04PMYVzrtYOiMzkr_xMSu75U2TK49WneHtzrwkKSLzX-wxQddZ-sTidjhCCbiRWc-KZjitZTIbLJ8TPb-dgLxNOKUPpmp5DeeGF5D_FKmZS14LesNzuBfaWBwpe&source=gbs_api', 'pendiente', '', 599, '4KJjDwAAQBAJ', '2013-11-27'),
(132, 'El retrato de Dorian Gray', 'Oscar Wilde', '\"El retrato de Dorian Gray\" es una obra maestra de Oscar Wilde que explora los temas de la belleza, la moralidad y la corrupción del alma. Se ambienta en una Londres victoriana donde Dorian, un joven de extraordinaria belleza, desea conservar su juventud a cualquier costo, lo que lo lleva a hacer un pacto con su retrato, permitiendo que este ultime su decadencia en lugar de él. A través de un estilo brillante y epigramático, Wilde teje un relato provocador que cuestiona la superficialidad de la sociedad y el conflicto entre el arte y la vida, reflejando así el contexto estético de su época. La prosa de Wilde, rica en descripciones y sutilezas, invita al lector a adentrarse en los dilemas morales del protagonista, convirtiendo la novela en una meditación sobre las consecuencias de una vida dedicada al hedonismo. Oscar Wilde, nacido en 1854, se convirtió en uno de los escritores más emblemáticos del movimiento esteticista. Criado en un entorno intelectual, su educación en el Trinity College de Dublín y su estudio en Oxford le brindaron una sólida base cultural. Su inclinación por el arte y la crítica social se manifiesta en \"El retrato de Dorian Gray\", donde proyecta sus propias inquietudes sobre la dualidad entre la apariencia y la realidad, así como su experiencia personal con las convenciones de la sociedad victoriana. Recomiendo encarecidamente a los lectores que se sumerjan en \"El retrato de Dorian Gray\", no solo como un relato fascinante, sino como una profunda reflexión sobre las implicancias de la búsqueda de la belleza y la verdad. La obra de Wilde desafía y seduce, logrando que cada lector evalúe sus propios valores y creencias. Sin duda, es un texto relevante que sigue resonando en la contemporaneidad.', NULL, 'Fiction / Classics, Fiction / Literary', 0, NULL, 23, 'https://books.google.com/books/publisher/content?id=AsPiEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70BByKovAkKZlsQygHkBvv6N2M1Evxq21h6xHxrJldIJ4Wib2mcJrzvcaNthtcHs9p69DkeJapIj-m27IOagDcjzLTroS0EbxD59_zWbKD7vvZ3BFHZw3TgSvX-wjXNQEm4LoTT&source=gbs_api', 'pendiente', '', 304, 'AsPiEAAAQBAJ', '2023-11-27'),
(133, '1984', 'George Orwell', '<p><b>75th ANNIVERSARY EDITION</b></p><p><b>“Orwell saw, to his credit, that the act of falsifying reality is only secondarily a way of changing perceptions. It is, above all, a way of asserting power.”—<i>The New Yorker</i></b></p><p>In <i>1984</i>, London is a grim city in the totalitarian state of Oceania where Big Brother is always watching you and the Thought Police can practically read your mind. Winston Smith is a man in grave danger for the simple reason that his memory still functions. Drawn into a forbidden love affair, Winston finds the courage to join a secret revolutionary organization called The Brotherhood, dedicated to the destruction of the Party. Together with his beloved Julia, he hazards his life in a deadly match against the powers that be.</p><p>Lionel Trilling said of Orwell’s masterpiece “<i>1984</i> is a profound, terrifying, and wholly fascinating book. It is a fantasy of the political future, and like any such fantasy, serves its author as a magnifying device for an examination of the present.” Though the year 1984 now exists in the past, Orwell’s dystopian classic remains an urgent call for the individual willing to speak truth to power.</p>', NULL, 'Fiction / Classics, Fiction / Literary, Fiction / Dystopian, Fiction / Political', 0, NULL, 23, 'https://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE73xHLG4HL8nd7kT7AZBJwDfwm3IWq4ZflbRa1C7GeXwsdq428FQ0Z1h9KEVzrwYFuWH53JqyX3VC0QSC_jQ5LEF_tCL7DIuqD5UznwAot8sLMwtOLYcIiDx1bvZHAQoPW0uxCb2&source=gbs_api', 'pendiente', '', 648, 'kotPYEqx7kMC', '2013-09-03'),
(134, 'Ensayo sobre la ceguera', 'José Saramago', '<p> <b>2022: AÑO SARAMAGO</b> </p> <p> <b>Una novela</b> <b>y</b> <b>un autor que nos alertan sobre «la responsabilidad de tener ojos cuando otros los perdieron».</b> </p> <p> <i>«Dentro de nosotros hay algo que no</i> <i>tiene nombre, esa cosa es lo que somos».</i> </p> <p>Un hombre parado ante un semáforo en rojo se queda ciego súbitamente. Es el primer caso de una «ceguera blanca» que se expande de manera fulminante. Internados en cuarentena o perdidos en la ciudad, los ciegos tendrán que enfrentarse con lo más primitivo en la naturaleza humana: la voluntad de sobrevivir a cualquier precio.</p> <p> <i>Ensayo sobre la ceguera</i> es la ficción de un autor que nos alerta sobre «la responsabilidad de tener ojos cuando otros los perdieron». José Saramago traza en este libro una imagen aterradora y conmovedora de los tiempos que estamos viviendo. En un mundo así, ¿cabrá alguna esperanza?</p> <p>El lector conocerá una experiencia imaginativa única. En un punto donde se cruzan literatura y sabiduría, José Saramago nos obliga a parar, cerrar los ojos y ver. Recuperar la lucidez y rescatar el afecto son dos propuestas fundamentales de una novela que es, también, una reflexión sobre la ética del amor y la solidaridad.</p> <p> <b>La crítica ha dicho:</b> <br> «Una metáfora que, cuando se publicó, lo mismo podía valer para el sida que para el abandono de los mayores. En esta novela, la ceguera llega sin avisar y produce un deslumbramiento blanco permanente. De nuevo, desfilan lo mejor y lo peor de la especie. Como en las guerras». <br> Tereixa Constenla, <i> El País</i> </p> <p>«Saramago siempre ha demostrado una imaginación audaz como novelista. Ésta es su obra más sorprendente e inquietante». <br> Harold Bloom</p> <p>«No hay cinismo ni moraleja, sólo un reconocimiento lúcido y compasivo de las cosas tal como son, una cualidad que sólo puede calificarse honestamente como sabiduría». <br> <i>The New York Times</i> </p> <p>«Hay novelas, como ésta, que después de leídas continuarán iluminando túneles en la conciencia, abriendo puertas de habitaciones a las que no nos habíamos asomado pese a estar dentro de nosotros». <br> Juan José Millás</p> <p>«Saramago vuelve comprensible una realidad huidiza, con parábolas sostenidas por la imaginación, la compasión y la ironía». <br> Comité Nobel</p> <p>«Un hombre con una sensibilidad y una capacidad de ver y de entender que están muy por encima de lo que en general vemos y entendemos los comunes mortales». <br> Héctor Abad Faciolince</p> <p>«Saramago es un ejemplo, un estilo dignísimo de vida y literatura, que demuestra la posibilidad de navegar a contracorriente [...]. Su palabra tiene el valor de un anticongelante, de un remedio personal contra los vendavales de cinismo que nos envuelven». <br> Luis García Montero</p> <p>«Yo no sé, ni quiero saberlo, de dónde ha sacado Saramago ese diabólico tono narrativo, duro y piadoso a un tiempo, [...] que le permite contar tan cerca del corazón y a la vez tan cerca de la historia». <br> Luis Landero</p> <p>«Saramago escribe novelas sobre los mitos para desmitificarlos, [...] siempre para abordar la realidad que le rodea, para tratar de los problemas actuales que son de todos, y para que todo quede claro desde el principio». <br> Rafael Conte, <i>Babelia</i> </p> <p>«Como Günter Grass o Cees Nooteboom, Saramago aspira a enlazar con un público que desborde límites nacionales». <br> <i>El País</i> </p>', NULL, 'Fiction / Literary', 0, NULL, 23, 'https://books.google.com/books/content?id=tKjAj5rDY0sC&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70Kg8tJ3v7ZkwYfkbfHs1mqx66pmxYuDgkJXG0c7NYtfl3hktj6rgZIWTBuqAnFgarW4xB6OzkuPGbPufg_woaYI6ev8oEqN9X0flgxDUJ0iajSylWD6yYIlI3LDm1unkCqoEwX&source=gbs_api', 'pendiente', '', 400, 'tKjAj5rDY0sC', '2010-07-15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notas_lectura`
--

CREATE TABLE `notas_lectura` (
  `id_nota` int(11) NOT NULL,
  `id_lectura` int(11) NOT NULL,
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
  `tipo_reflexion` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `respuesta_reflexion` text COLLATE utf8mb4_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notas_lectura`
--

INSERT INTO `notas_lectura` (`id_nota`, `id_lectura`, `como_te_sientes`, `que_aprendiste`, `palabras_nuevas`, `personaje_destacado`, `escena_impacto`, `continuara`, `parecer_sesion`, `recuerdo_vida`, `notas_observaciones`, `buscaba_al_leer`, `encontro_lo_buscado`, `tipo_reflexion`, `respuesta_reflexion`) VALUES
(12, 7, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí', NULL, NULL),
(11, 6, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí', NULL, NULL),
(10, 4, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí', NULL, NULL),
(9, 4, '😊 Feliz', '', '', '', '', 'Sí, continuaré leyendo', '', '', '', 'Aprender', 'Sí', NULL, NULL),
(13, 7, '😮 Sorprendido', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, 'si', NULL, NULL, 'objetivo', 'Entretenerme'),
(14, 7, '😌 Tranquilo', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, 'fua', NULL, NULL, 'personaje', 'yony'),
(15, 6, '😰 Ansioso', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'vida', ''),
(16, 8, '😊 Feliz', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'personaje', ''),
(17, 8, '😊 Feliz', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'encontraste', 'Sí'),
(18, 8, '😊 Feliz', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'objetivo', 'Entretenerme'),
(19, 10, '🤔 Reflexivo', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'aprendiste', 'Un poquito de todo.'),
(20, 6, '🤔 Reflexivo', NULL, NULL, NULL, NULL, 'Sí, continuaré leyendo', NULL, NULL, '', NULL, NULL, 'vida', 'si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `objetivos_personales`
--

CREATE TABLE `objetivos_personales` (
  `id_objetivo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('custom','tiempo_diario','racha_dias','paginas_por_sesion','libros_por_mes','vocabulario_nuevo','constancia_semanal','libros_por_genero') COLLATE utf8mb4_unicode_ci NOT NULL,
  `meta_valor` int(11) NOT NULL,
  `progreso_actual` int(11) DEFAULT '0',
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `completado` tinyint(1) DEFAULT '0',
  `genero_objetivo` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `Porcentaje` decimal(5,2) NOT NULL,
  `Logro_objetivo` enum('logro','objetivo') COLLATE utf8mb4_unicode_ci NOT NULL,
  `descrupcion_custom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Name_custom` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas_encuesta`
--

CREATE TABLE `preguntas_encuesta` (
  `id_pregunta` int(11) NOT NULL,
  `nivel` enum('principiante','intermedio','maestro') COLLATE utf8mb4_unicode_ci NOT NULL,
  `texto_pregunta` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_campo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `preguntas_encuesta`
--

INSERT INTO `preguntas_encuesta` (`id_pregunta`, `nivel`, `texto_pregunta`, `nombre_campo`) VALUES
(1, 'principiante', '¿Qué te motivó a comenzar a leer?', 'motivacion'),
(2, 'principiante', '¿Qué tipo de historias te llaman más la atención?', 'tipo_historias'),
(3, 'principiante', '¿Has terminado algún libro anteriormente?', 'libro_anterior'),
(4, 'principiante', '¿Cuánto tiempo crees que puedes dedicar a la lectura cada día?', 'tiempo_diario'),
(5, 'principiante', '¿Prefieres libros cortos o largos?', 'longitud_libro'),
(6, 'principiante', '¿Qué formato prefieres?', 'formato'),
(7, 'principiante', '¿Qué géneros te llaman la atención?', 'generos'),
(8, 'principiante', '¿Qué esperas conseguir con Book Wellness?', 'expectativa'),
(9, 'principiante', '¿Tienes algunas obras en mente para empezar tu lectura?', 'obras_mente'),
(10, 'principiante', '¿Qué tan importante es para ti mantener una racha de lectura?', 'importancia_racha'),
(11, 'intermedio', '¿Cuáles son tus géneros favoritos?', 'generos_favoritos'),
(12, 'intermedio', '¿Qué autor disfrutas más?', 'autor_favorito'),
(13, 'intermedio', '¿Cuántos libros lees aproximadamente al año?', 'libros_anio'),
(14, 'intermedio', '¿Qué formato utilizas con mayor frecuencia?', 'formato_frecuente'),
(15, 'intermedio', '¿Sueles leer varios libros al mismo tiempo?', 'varios_libros'),
(16, 'intermedio', '¿Qué tan seguido abandonas un libro?', 'abandona_libros'),
(17, 'intermedio', '¿Prefieres descubrir autores nuevos?', 'autores_nuevos'),
(18, 'intermedio', '¿Qué valoras más al elegir un libro?', 'valor_libro'),
(19, 'intermedio', '¿Te gusta participar en retos de lectura?', 'retos_lectura'),
(20, 'intermedio', '¿Qué esperas que Book Wellness haga por ti?', 'objetivo_bookwellness'),
(41, 'maestro', '¿Cuáles son tus géneros favoritos?', 'generos_favoritos'),
(42, 'maestro', '¿Qué autores consideras imprescindibles?', 'autores_imprescindibles'),
(43, 'maestro', '¿Lees varios libros simultáneamente?', 'lectura_simultanea'),
(44, 'maestro', '¿Cómo organizas tus lecturas?', 'organizacion_lecturas'),
(45, 'maestro', '¿Qué criterio utilizas para elegir tu siguiente libro?', 'criterio_siguiente_libro'),
(46, 'maestro', '¿Qué tan dispuesto estás a salir de tu zona de confort?', 'zona_confort'),
(47, 'maestro', '¿Qué tan importantes son las recomendaciones personalizadas para ti?', 'recomendaciones_personalizadas'),
(48, 'maestro', '¿Qué tipo de retos disfrutas más?', 'tipo_retos'),
(49, 'maestro', '¿Qué aspecto valoras más en una historia?', 'aspecto_historia'),
(50, 'maestro', '¿Qué esperas encontrar en Book Wellness que otras aplicaciones no ofrecen?', 'expectativa_app');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recomendaciones_cache`
--

CREATE TABLE `recomendaciones_cache` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `titulo` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `autor` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `portada` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paginas` int(11) DEFAULT NULL,
  `generos` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anio` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_google` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_generacion` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `recomendaciones_cache`
--

INSERT INTO `recomendaciones_cache` (`id`, `id_usuario`, `titulo`, `autor`, `descripcion`, `portada`, `paginas`, `generos`, `anio`, `id_google`, `fecha_generacion`) VALUES
(11, 6, 'Los Juegos del Hambre - Trilogía Los Juegos del Hambre', 'Suzanne Collins', 'Los Juegos del Hambre, una de las sagas más exitosas de todos los tiempos reunida en un bonito estuche. Este pack contiene los tres títulos de la trilogía Los Juegos del Hambre: Los Juegos de Hambre En una oscura versión del futuro próximo, doce chicos y doce chicas se ven obligados a participar en un reality show llamado Los Juegos del Hambre. Solo hay una regla: matar o morir. En llamas Contra todo pronóstico, Katniss Everdeen y Peeta Mellark han sobrevivido a Los Juegos del Hambre. Deberían sentirse aliviados, pero saben que la tensión crece en el Capitolio, que los gobierna a todos. Sinsajo Los supervivientes de Los Juegos del Hambre no están a salvo. Un meticuloso plan se extiende contra el Capitolio... Y este necesita un símbolo, el emblema de la rebelión: el Sinsajo.', 'https://via.placeholder.com/200x300?text=Sin+Portada', 0, 'Juvenile Fiction', '2019-03-07', '89tu0AEACAAJ', '2026-07-08 19:05:11'),
(10, 6, 'Cien años de soledad', 'Gabriel García Márquez', 'Señalada como «catedral gótica del lenguaje», este clásico del siglo XX es el enorme y espléndido tapiz de la saga de la familia Buendía, en la mítica aldea de Macondo. UNO DE LOS 5 LIBROS MÁS IMPORTANTES DE LOS ÚLTIMOS 125 AÑOS SEGÚN THE NEW YORK TIMES Un referente imprescindible de la vida y la narrativa latinoamericana. «Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo». Con estas palabras empieza la novela ya legendaria en los anales de la literatura universal, una de las aventuras literarias más fascinantes de nuestro siglo. Millones de ejemplares de Cien años de soledad leídos en todas las lenguas y el Premio Nobel de Literatura coronando una obra que se había abierto paso «boca a boca» -como gusta decir al escritor- son la más palpable demostración de que la aventura fabulosa de la familia Buendía-Iguarán, con sus milagros, fantasías, obsesiones, tragedias, incestos, adulterios, rebeldías, descubrimientos y condenas, representaba al mismo tiempo el mito y la historia, la tragedia y el amor del mundo entero. Pablo Neruda dijo... «El Quijote de nuestro tiempo.»', 'http://books.google.com/books/content?id=kmAQCwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 311, 'Fiction', '2015-12-03', 'kmAQCwAAQBAJ', '2026-07-08 19:05:11'),
(9, 6, '1984', 'George Orwell', '75th ANNIVERSARY EDITION “Orwell saw, to his credit, that the act of falsifying reality is only secondarily a way of changing perceptions. It is, above all, a way of asserting power.”—The New Yorker In 1984, London is a grim city in the totalitarian state of Oceania where Big Brother is always watching you and the Thought Police can practically read your mind. Winston Smith is a man in grave danger for the simple reason that his memory still functions. Drawn into a forbidden love affair, Winston finds the courage to join a secret revolutionary organization called The Brotherhood, dedicated to the destruction of the Party. Together with his beloved Julia, he hazards his life in a deadly match against the powers that be. Lionel Trilling said of Orwell’s masterpiece, “1984 is a profound, terrifying, and wholly fascinating book. It is a fantasy of the political future, and like any such fantasy, serves its author as a magnifying device for an examination of the present.” Though the year 1984 now exists in the past, Orwell’s novel remains an urgent call for the individual willing to speak truth to power.', 'http://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 309, 'Fiction', '2013-09-03', 'kotPYEqx7kMC', '2026-07-08 19:05:11'),
(24, 22, 'Orgullo y prejuicio', 'Jane Austen', 'Orgullo y prejuicio (Pride and Prejudice), publicada por primera vez el 28 de enero de 1813 como una obra anónima, es la más famosa de las novelas de Jane Austen y una de las primeras comedias románticas en la historia del género. Su primera frase es, además, una de las más famosas en la literatura inglesa: “Es una verdad mundialmente reconocida que un hombre soltero, poseedor de una gran fortuna, necesita una esposa.” Cuando Jane Austen escribió la novela, apenas tenía veinte años, y compartía habitación con su hermana. La primera redacción de la obra data del periodo 1796-1797; inicialmente recibió el título de \"Primeras impresiones\" (First Impressions), pero nunca fue publicado con ese nombre. En 1797 el padre de Jane lo ofreció a un editor, que lo rechazó. Jane Austen revisó la obra en 1809-1810 y de nuevo en 1812, y la ofreció entonces, con el apoyo de su hermano Henry, a otro editor, que había publicado Sentido y sensibilidad el año anterior. Finalmente fue publicada y pronto gozó de gran éxito. Satírica, profunda y mordaz a un tiempo, la obra de Jane Austen nace de la observación de la vida doméstica y de un profundo conocimiento de la condición humana. Orgullo y prejuicio ha fascinado a generaciones de lectores por sus inolvidables personajes y su desopilante retrato de una sociedad, la Inglaterra victoriana y rural, tan contradictoria como absurda. Esta novela, donde Austen relata la historia de las cinco hermanas Bennet y las tribulaciones de sus respectivos amoríos, ha sido llevada al cine en reiteradas ocasiones, se ha versionado en cómic y en musicales, lo que demuestra su actualidad e interés contemporáneos.', 'http://books.google.com/books/content?id=ojyzDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 328, 'Drama', '2016-07-01', 'ojyzDwAAQBAJ', '2026-07-08 19:16:58'),
(25, 22, 'Cien años de soledad', 'Gabriel García Márquez', 'Señalada como «catedral gótica del lenguaje», este clásico del siglo XX es el enorme y espléndido tapiz de la saga de la familia Buendía, en la mítica aldea de Macondo. UNO DE LOS 5 LIBROS MÁS IMPORTANTES DE LOS ÚLTIMOS 125 AÑOS SEGÚN THE NEW YORK TIMES Un referente imprescindible de la vida y la narrativa latinoamericana. «Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo». Con estas palabras empieza la novela ya legendaria en los anales de la literatura universal, una de las aventuras literarias más fascinantes de nuestro siglo. Millones de ejemplares de Cien años de soledad leídos en todas las lenguas y el Premio Nobel de Literatura coronando una obra que se había abierto paso «boca a boca» -como gusta decir al escritor- son la más palpable demostración de que la aventura fabulosa de la familia Buendía-Iguarán, con sus milagros, fantasías, obsesiones, tragedias, incestos, adulterios, rebeldías, descubrimientos y condenas, representaba al mismo tiempo el mito y la historia, la tragedia y el amor del mundo entero. Pablo Neruda dijo... «El Quijote de nuestro tiempo.»', 'http://books.google.com/books/content?id=kmAQCwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 311, 'Fiction', '2015-12-03', 'kmAQCwAAQBAJ', '2026-07-08 19:16:58'),
(26, 25, 'Orgullo y prejuicio', 'Jane Austen', 'Las novelas de JANE AUSTEN (1775-1817) suelen girar en torno al paso de la juventud a la edad adulta, el consiguiente acceso a la sociedad y el natural corolario de este proceso en el medio en que estas relaciones se desarrollan -el matrimonio-, así como sus consecuencias. ORGULLO Y PREJUICIO se teje alrededor de las relaciones que se establecen entre dos grupos familiares en la Inglaterra rural: por una parte el matrimonio Bennet con sus cinco hijas -entre las que destaca especialmente Elizabeth, despierta y vivaz-, y por otra el rico Charles Bingley y sus dos hermanas, junto con su aún más rico amigo Fitzwilliam Darcy. Marcados en un principio por los prejuicios y los malos entendidos, los vínculos sociales y sentimentales entre los miembros de una y otra parte van madurando y matizándose a lo largo de la novela para acabar alcanzando un buen fin. Otras obras de Jane Austen en esta colección: «Emma» (LB 1784).', 'http://books.google.com/books/content?id=MHvfwAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 448, 'Fiction', '2002', 'MHvfwAEACAAJ', '2026-07-08 22:13:44'),
(27, 25, 'Cien años de soledad', 'Gabriel García Márquez', 'Señalada como «catedral gótica del lenguaje», este clásico del siglo XX es el enorme y espléndido tapiz de la saga de la familia Buendía, en la mítica aldea de Macondo. UNO DE LOS 5 LIBROS MÁS IMPORTANTES DE LOS ÚLTIMOS 125 AÑOS SEGÚN THE NEW YORK TIMES Un referente imprescindible de la vida y la narrativa latinoamericana. «Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo». Con estas palabras empieza la novela ya legendaria en los anales de la literatura universal, una de las aventuras literarias más fascinantes de nuestro siglo. Millones de ejemplares de Cien años de soledad leídos en todas las lenguas y el Premio Nobel de Literatura coronando una obra que se había abierto paso «boca a boca» -como gusta decir al escritor- son la más palpable demostración de que la aventura fabulosa de la familia Buendía-Iguarán, con sus milagros, fantasías, obsesiones, tragedias, incestos, adulterios, rebeldías, descubrimientos y condenas, representaba al mismo tiempo el mito y la historia, la tragedia y el amor del mundo entero. Pablo Neruda dijo... «El Quijote de nuestro tiempo.»', 'http://books.google.com/books/content?id=kmAQCwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 311, 'Fiction', '2015-12-03', 'kmAQCwAAQBAJ', '2026-07-08 22:13:44'),
(314, 23, 'La constelación de los personajes en Cien años de soledad', 'Jimena Tórres Galarza', '', 'https://via.placeholder.com/200x300?text=Sin+Portada', 0, '', '1988', '', '2026-07-21 17:23:19'),
(315, 23, 'Gone Girl', 'Perfection Learning Corporation', 'Descripción no disponible', 'http://books.google.com/books/content?id=gX0vzgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 0, '', '2019', 'gX0vzgEACAAJ', '2026-07-21 17:23:19'),
(316, 23, 'El conde de Montecristo', 'Alexandre Dumas', 'Grandes Clásicos Literatura Random House nos brinda esta magnífica edición de una novela de enorme poder de sugestión, a través de la figura del hombre solitario que, tras sobrevivir a una vil traición, regresa para hacer justicia. El conde de Montecristo es uno de los clásicos más populares de todos los tiempos. Desde su publicación, en 1844, no ha dejado de seducir al gran público con la inolvidable historia de su protagonista. Edmond Dantés es un joven marinero, honrado y cándido, que lleva una existencia tranquila. Quiere casarse con la hermosa Mercedes, pero su vida se verá arruinada cuando su mejor amigo, Ferdinand, deseoso de conquistar a su prometida, le traicione vilmente. Condenado a cumplir una condena que no merece en la siniestra prisión del castillo de If, Edmond vivirá una larga pesadilla de trece años. Obsesionado por su inesperado destino, dejará de lado sus convicciones en torno al bien y al mal, y se dedicará a tramar la venganza perfecta. Historia transida de densidad moral y cívica, El conde de Montecristo es, hoy como ayer, una novela amena, iluminadora y fascinante en sus múltiples dimensiones.', 'http://books.google.com/books/content?id=3c2Fxe2lMaYC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 1320, 'Fiction', '2011-02-04', '3c2Fxe2lMaYC', '2026-07-21 17:23:19'),
(317, 23, 'Un mundo feliz / Brave New World', 'Aldous Huxley', 'Un mundo feliz es un clásico de la literatura del siglo XX, una sombría metáfora de un futuro posible. Con ironía mordiente, el genial autor inglés plasma una sombría metáfora sobre el futuro, muchas de cuyas previsiones se han materializado, acelerada e inquietantemente, en los últimos años. La novela describe un mundo en el que finalmente se han cumplido los peores vaticinios: triunfan los dioses del consumo y la comodidad, y el orbe se organiza en diez zonas en apariencia seguras y estables. Sin embargo, este mundo ha sacrificado valores humanos esenciales, y sus habitantes son procreados in vitro a imagen y semejanza de una cadena de montaje... ENGLISH DESCRIPTION Now more than ever: Aldous Huxley\'s enduring masterwork must be read and understood by anyone concerned with preserving the human spirit \"A masterpiece. ... One of the most prophetic dystopian works.\" —Wall Street Journal Aldous Huxley is rightly considered a prophetic genius and one of the most important literary and philosophical voices of the 20th Century, and Brave New World is his masterpiece. From the author of The Doors of Perception, Island, and countless other works of fiction, non-fiction, philosophy, and poetry, comes this powerful work of speculative fiction that has enthralled and terrified readers for generations. Brave New World remains absolutely relevant to this day as both a cautionary dystopian tale in the vein of the George Orwell classic 1984, and as thought-provoking, thoroughly satisfying entertainment.', 'http://books.google.com/books/content?id=CG-SEAAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 0, 'Fiction', '2023-03-21', 'CG-SEAAAQBAJ', '2026-07-21 17:23:19'),
(318, 23, 'El espía que surgió del frío', 'John le Carré', 'El primer retrato del espionaje en la Guerra Fría: una obra magistral que describe un mundo sombrío, solitario y amoral, en que los espías nunca ganan. Alec Leamas, el antiguo responsable del espionaje inglés en Alemania Oriental, tiene una cuenta casi personal que saldar con sus viejos rivales. Todos sus agentes han muerto o han sido detenidos. Pero Londres le ofrece la oportunidad de superar su frustración mediante una operación sucia y arriesgada que permitirá liquidar al máximo dirigente del espionaje de Alemania Oriental. Y Alec Leamas acepta el riesgo y la sordidez de la operación. Es un buen espía, un profesional, y sabe que el doble juego, o triple, forma parte de las reglas. Sin embargo, a medida que se adentra en la trama va comprendiendo que aquél no es su juego, que no encarna el papel de un héroe en busca de rehabilitación sino el de un pobre peón caído en desgracia que está siendo manipulado en algo más sucio yarriesgado de lo que nunca hubiera estado dispuesto a asumir.', 'http://books.google.com/books/content?id=iqanvBDPkNMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 224, 'Fiction', '2011-07-08', 'iqanvBDPkNMC', '2026-07-21 17:23:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_encuesta`
--

CREATE TABLE `respuestas_encuesta` (
  `id_respuesta` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `respuesta` text COLLATE utf8mb4_unicode_ci,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `respuestas_encuesta`
--

INSERT INTO `respuestas_encuesta` (`id_respuesta`, `id_usuario`, `id_pregunta`, `respuesta`, `fecha`) VALUES
(1, 40, 1, NULL, '2026-07-21 23:54:17'),
(2, 40, 2, NULL, '2026-07-21 23:54:17'),
(3, 40, 3, NULL, '2026-07-21 23:54:17'),
(4, 40, 4, NULL, '2026-07-21 23:54:17'),
(5, 40, 5, NULL, '2026-07-21 23:54:17'),
(6, 40, 6, NULL, '2026-07-21 23:54:17'),
(7, 40, 7, NULL, '2026-07-21 23:54:17'),
(8, 40, 8, NULL, '2026-07-21 23:54:17'),
(9, 40, 9, NULL, '2026-07-21 23:54:17'),
(10, 40, 10, NULL, '2026-07-21 23:54:17'),
(11, 41, 1, NULL, '2026-07-22 00:06:00'),
(12, 41, 2, NULL, '2026-07-22 00:06:00'),
(13, 41, 3, NULL, '2026-07-22 00:06:00'),
(14, 41, 4, NULL, '2026-07-22 00:06:00'),
(15, 41, 5, NULL, '2026-07-22 00:06:00'),
(16, 41, 6, NULL, '2026-07-22 00:06:00'),
(17, 41, 7, NULL, '2026-07-22 00:06:00'),
(18, 41, 8, NULL, '2026-07-22 00:06:00'),
(19, 41, 9, NULL, '2026-07-22 00:06:00'),
(20, 41, 10, NULL, '2026-07-22 00:06:00'),
(21, 42, 1, NULL, '2026-07-22 08:44:41'),
(22, 42, 2, NULL, '2026-07-22 08:44:41'),
(23, 42, 3, NULL, '2026-07-22 08:44:41'),
(24, 42, 4, NULL, '2026-07-22 08:44:41'),
(25, 42, 5, NULL, '2026-07-22 08:44:41'),
(26, 42, 6, NULL, '2026-07-22 08:44:41'),
(27, 42, 7, NULL, '2026-07-22 08:44:41'),
(28, 42, 8, NULL, '2026-07-22 08:44:41'),
(29, 42, 9, NULL, '2026-07-22 08:44:41'),
(30, 42, 10, NULL, '2026-07-22 08:44:41'),
(31, 44, 1, 'Compartir con otros', '2026-07-22 09:02:01'),
(32, 44, 2, 'reales', '2026-07-22 09:02:01'),
(33, 44, 3, 'pocos', '2026-07-22 09:02:01'),
(34, 44, 4, '15_30', '2026-07-22 09:02:01'),
(35, 44, 5, 'largos', '2026-07-22 09:02:01'),
(36, 44, 6, 'ebook', '2026-07-22 09:02:01'),
(37, 44, 7, 'clasicos, psicologico', '2026-07-22 09:02:01'),
(38, 44, 8, 'Aprender', '2026-07-22 09:02:01'),
(39, 44, 9, 'no', '2026-07-22 09:02:01'),
(40, 44, 10, 'muy_importante', '2026-07-22 09:02:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id_sesion` int(11) NOT NULL,
  `id_lectura` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_hora_inicio` datetime NOT NULL,
  `fecha_hora_fin` datetime DEFAULT NULL,
  `tiempo_planeado_minutos` int(11) DEFAULT NULL,
  `tiempo_real_minutos` int(11) DEFAULT NULL,
  `paginas_leidas` int(11) DEFAULT NULL,
  `sentimiento` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `cap_inicio` int(11) DEFAULT NULL,
  `cap_fin` int(11) DEFAULT NULL,
  `cap_leidos` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  `nivel_actual` enum('principiante','intermedio','avanzado') COLLATE utf8mb4_unicode_ci DEFAULT 'principiante',
  `total_libros_leidos` int(11) DEFAULT '0',
  `total_paginas_leidas` int(11) DEFAULT '0',
  `promedio_paginas_sesion` decimal(5,2) DEFAULT '0.00',
  `genero_preferido` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password`, `fecha_registro`, `nivel_actual`, `total_libros_leidos`, `total_paginas_leidas`, `promedio_paginas_sesion`, `genero_preferido`) VALUES
(6, 'Ender', 'enderdg2010@gmail.com', 'ene102010', '2026-06-01 10:07:48', 'principiante', 0, 0, '0.00', ''),
(22, 'popo', 'popeto123@gmail.com', '123', '2026-06-07 13:50:45', 'principiante', 0, 0, '0.00', ''),
(23, 'Angel Ferrer', 'angelferrer200444@gmail.com', '31276323', '2026-07-08 22:14:06', 'principiante', 0, 0, '0.00', ''),
(24, 'Manolo', 'manaloecchi@gmail.com', '12345678', '2026-07-21 19:25:54', 'principiante', 0, 0, '0.00', ''),
(27, 'Manolo', 'alaskalee@gmail.com', '12345678', '2026-07-21 20:50:20', 'principiante', 0, 0, '0.00', ''),
(28, 'Subaru', 'subarunatsuki@gmail.com', '12345678', '2026-07-21 20:53:24', 'principiante', 0, 0, '0.00', ''),
(30, 'Emilia', 'emilia@gmail.com', '1234', '2026-07-21 22:19:51', 'principiante', 0, 0, '0.00', ''),
(31, 'Juan', 'josejose@gmail.com', '31276323', '2026-07-21 22:34:10', 'principiante', 0, 0, '0.00', ''),
(32, 'Marjorie', 'marjorie123@gmail.com', '1234', '2026-07-21 22:45:58', 'principiante', 0, 0, '0.00', ''),
(33, 'Pokemon', 'Pokemon123@gmail.com', '1234', '2026-07-21 23:00:43', 'principiante', 0, 0, '0.00', ''),
(34, 'Doctor', 'doctor@gmail.com', '1234', '2026-07-21 23:12:32', 'principiante', 0, 0, '0.00', ''),
(35, 'Angel Ferrer', 'stephenkig@gmail.com', '1234', '2026-07-21 23:16:17', 'principiante', 0, 0, '0.00', ''),
(37, 'doctora', 'doctora@gmail.com', '1234', '2026-07-21 23:31:46', 'principiante', 0, 0, '0.00', ''),
(38, 'hielo', 'hielo@gmail.com', '1234', '2026-07-21 23:42:20', 'principiante', 0, 0, '0.00', ''),
(39, 'iguana', 'iguana@gmail.com', '1234', '2026-07-21 23:51:01', 'principiante', 0, 0, '0.00', ''),
(40, 'Angel Ferrer', 'angel@gmail.com', '2345', '2026-07-21 23:54:02', 'principiante', 0, 0, '0.00', ''),
(41, 'Pikachu', 'pikapi@gmail.com', '1234', '2026-07-22 00:05:30', 'principiante', 0, 0, '0.00', ''),
(42, 'Loco', 'loco@gmail.com', '1234', '2026-07-22 08:44:00', 'principiante', 0, 0, '0.00', ''),
(44, 'Angel Ferrer', 'fangel@gmail.com', '1234', '2026-07-22 09:01:35', 'principiante', 0, 0, '0.00', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_encuesta_temporal`
--

CREATE TABLE `usuario_encuesta_temporal` (
  `id_usuario` int(11) NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `lecturas`
--
ALTER TABLE `lecturas`
  ADD PRIMARY KEY (`id_lectura`),
  ADD UNIQUE KEY `uk_lectura_usuario` (`id_lectura`,`id_usuario`),
  ADD UNIQUE KEY `unico_libro_usuario` (`id_usuario`,`id_libro`),
  ADD KEY `FK_1` (`id_libro`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`);

--
-- Indices de la tabla `notas_lectura`
--
ALTER TABLE `notas_lectura`
  ADD PRIMARY KEY (`id_nota`),
  ADD KEY `id_lectura` (`id_lectura`);

--
-- Indices de la tabla `objetivos_personales`
--
ALTER TABLE `objetivos_personales`
  ADD PRIMARY KEY (`id_objetivo`),
  ADD KEY `FK_10` (`id_usuario`);

--
-- Indices de la tabla `preguntas_encuesta`
--
ALTER TABLE `preguntas_encuesta`
  ADD PRIMARY KEY (`id_pregunta`);

--
-- Indices de la tabla `recomendaciones_cache`
--
ALTER TABLE `recomendaciones_cache`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `respuestas_encuesta`
--
ALTER TABLE `respuestas_encuesta`
  ADD PRIMARY KEY (`id_respuesta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_pregunta` (`id_pregunta`);

--
-- Indices de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD PRIMARY KEY (`id_sesion`),
  ADD KEY `FK_2` (`id_lectura`,`id_usuario`),
  ADD KEY `FK_3` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `uk_usuarios_correo` (`correo`);

--
-- Indices de la tabla `usuario_encuesta_temporal`
--
ALTER TABLE `usuario_encuesta_temporal`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `lecturas`
--
ALTER TABLE `lecturas`
  MODIFY `id_lectura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;

--
-- AUTO_INCREMENT de la tabla `notas_lectura`
--
ALTER TABLE `notas_lectura`
  MODIFY `id_nota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `objetivos_personales`
--
ALTER TABLE `objetivos_personales`
  MODIFY `id_objetivo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `preguntas_encuesta`
--
ALTER TABLE `preguntas_encuesta`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `recomendaciones_cache`
--
ALTER TABLE `recomendaciones_cache`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=319;

--
-- AUTO_INCREMENT de la tabla `respuestas_encuesta`
--
ALTER TABLE `respuestas_encuesta`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id_sesion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

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
-- Filtros para la tabla `respuestas_encuesta`
--
ALTER TABLE `respuestas_encuesta`
  ADD CONSTRAINT `respuestas_encuesta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `respuestas_encuesta_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas_encuesta` (`id_pregunta`);

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
