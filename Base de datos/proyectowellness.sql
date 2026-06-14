-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-06-2026 a las 02:08:29
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
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `titulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `autor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `num_paginas` int(11) DEFAULT NULL,
  `formato` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genero` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `es_agregado_manualmente` tinyint(4) DEFAULT NULL,
  `num_caps` int(11) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `portada` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pendiente',
  `key_libro` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `autor`, `descripcion`, `num_paginas`, `formato`, `genero`, `es_agregado_manualmente`, `num_caps`, `id_usuario`, `portada`, `categoria`, `key_libro`) VALUES
(16, 'Dino', 'Jonathan Litton', 'Discover lots of little dinosaurs in this playful book of colors. Bright artwork, concentric shapes, and a cheerful rhyming story make learning come alive!', NULL, NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/7446583-L.jpg', 'pendiente', NULL),
(19, 'The Fellowship of the Ring', 'J.R.R. Tolkien', 'One Ring to rule them all, One Ring to find them, One Ring to bring them all and in the darkness bind them.\n\n“A unique, wholly realized other world, evoked from deep in the well of Time, massively detailed, absorbingly entertaining, profound in meaning.”—The New York Times\n\nIn ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others. But the One Ring was taken from him, and though he sought it throughout Middle-earth, it remained lost to him. After many ages it fell into the hands of Bilbo Baggins, as told in The Hobbit. In a sleepy village in the Shire, young Frodo Baggins finds himself faced with an immense task, as his elderly cousin Bilbo entrusts the Ring to his care. Frodo must leave his home and make a perilous journey across Middle-earth to the Cracks of Doom, there to destroy the Ring and foil the Dark Lord in his evil purpose.', NULL, NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/14627060-L.jpg', 'pendiente', NULL),
(20, 'Half of a Yellow Sun', 'Chimamanda Ngozi Adichie', 'Half of a Yellow Sun is a novel by Nigerian author Chimamanda Ngozi Adichie. Published in 2006 by Fourth Estate, the novel tells the story of the Biafran War through the perspective of the characters Olanna, Ugwu, and Richard.', NULL, NULL, NULL, NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/8472660-L.jpg', 'pendiente', NULL),
(21, 'Así es la puta vida', 'Jordi WILD', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/14631230-L.jpg', 'leyendo', NULL),
(24, 'La puta de Babilonia', 'Autor desconocido', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/13955665-L.jpg', 'pendiente', NULL),
(25, 'The Summit Of The Gods', 'Yumemakura Baku', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/7467078-L.jpg', 'leyendo', NULL),
(26, 'Harry Potter and the Cursed Child : the Journey', 'Harry Potter Theatrical Productions, Jody Revenson', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 6, 'https://covers.openlibrary.org/b/id/13570336-L.jpg', 'pendiente', NULL),
(27, 'Life Is Strange', 'Zoe Thorogood', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/13618772-L.jpg', 'leyendo', NULL),
(29, 'Sin título', 'Autor desconocido', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 22, 'https://covers.openlibrary.org/b/id/14627060-L.jpg', 'pendiente', 'None'),
(35, 'The Institute', 'Stephen King', 'In the middle of the night, in a house on a quiet street in suburban Minneapolis, intruders silently murder Luke Ellis’s parents and load him into a black SUV. The operation takes less than two minutes. Luke will wake up at The Institute, in a room that looks just like his own, except there’s no window. And outside his door are other doors, behind which are other kids with special talents—telekinesis and telepathy—who got to this place the same way Luke did: Kalisha, Nick, George, Iris, and ten-year-old Avery Dixon. They are all in Front Half. Others, Luke learns, graduated to Back Half, “like the roach motel,” Kalisha says. “You check in, but you don’t check out.”\n\nIn this most sinister of institutions, the director, Mrs. Sigsby, and her staff are ruthlessly dedicated to extracting from these children the force of their extranormal gifts. There are no scruples here. If you go along, you get tokens for the vending machines. If you don’t, punishment is brutal. As each new victim disappears to Back Half, Luke becomes more and more desperate to get out and get help. But no one has ever escaped from the Institute.\n\nAs psychically terrifying as Firestarter, and with the spectacular kid power of It, The Institute is Stephen King’s gut-wrenchingly dramatic story of good vs. evil in a world where the good guys don’t always win.', NULL, NULL, NULL, NULL, NULL, 24, 'https://covers.openlibrary.org/b/id/10712767-L.jpg', 'leyendo', '/authors/OL19981A'),
(36, 'Christine', 'Stephen King', 'A love triangle involving 17-year-old misfit Arnie Cunningham, his new girlfriend and a haunted 1958 Plymouth Fury. Dubbed Christine by her previous owner, Arnie&#39;s first car is jealous, possessive and deadly. \n([source][1])\n\n\n  [1]: https://stephenking.com/library/novel/christine.html', NULL, NULL, NULL, NULL, NULL, 24, 'https://covers.openlibrary.org/b/id/14655985-L.jpg', 'leyendo', '/authors/OL19981A'),
(38, 'Five Little Pigs', 'Agatha Christie', 'Sixteen years after Caroline Crale has been convicted of the murder of her husband, Amyas Crale, her daughter, Carla Lemarchant, approaches Poirot to investigate the case. Poirot embarks optimistically upon an unprecedented challenge, but soon fears that the case may be as cut and dried as it had first appeared.', NULL, NULL, NULL, NULL, NULL, 24, 'https://covers.openlibrary.org/b/id/14578138-L.jpg', 'pendiente', '/authors/OL27695A'),
(44, 'They Came to Baghdad', 'Agatha Christie', 'E-book exclusive extras: &#39;Agatha Christie in Baghdad,&#39; extensive selections from Agatha Christie: An Autobiography. Plus: Christie biographer Charles Osborne&#39;s essay on They Came to Baghdad.Agatha Christie first visited Baghdad as a tourist in 1927; many years later she would become a resident of the exotic and then open city, and it was here, and while on archaeological digs throughout Iraq with her husband, Sir Max Mallowan, that Agatha Christie wrote some of her most important works.They Came to Baghdad is one of Agatha Christie&#39;s highly successful forays into the spy thriller genre. In this novel, Baghdad is the chosen location for a secret superpower summit. But the word is out, and an underground organisation is plotting to sabotage the talks.Into this explosive situation stumbles Victoria Jones, a young woman with a yearning for adventure who gets more than she bargains for when a wounded secret agent dies in her hotel room. Now, if only she could make sense of his final words: &#39;Lucifer... Basrah... Lefarge...&#39;', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/12846782-L.jpg', 'leyendo', '/works/OL472215W'),
(45, 'Jurassic Park', 'Michael Crichton', 'Jurassic Park is a 1990 science fiction novel written by Michael Crichton. A cautionary tale about genetic engineering, it presents the collapse of an amusement park showcasing genetically re-created dinosaurs to illustrate the mathematical concept of chaos theory and its real-world implications. A sequel titled The Lost World, also written by Crichton, was published in 1995. In 1997, both novels were re-published as a single book titled Michael Crichton&#39;s Jurassic World. In 1996 it was awarded the Secondary BILBY Award.\n\nAlso contained in:\n[Congo/Jurassic Park](https://openlibrary.org/works/OL8475707W)\n[Michael Crichton&#39;s Jurassic World](https://openlibrary.org/works/OL14950507W)', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/12882940-L.jpg', 'pendiente', '/works/OL46881W'),
(46, 'Noches blancas', 'Фёдор Михайлович Достоевский, Raúl Rodríguez Cano', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/10861094-L.jpg', 'leyendo', '/works/OL24338863W'),
(47, 'Soy un gato', 'Natsumi Soseki', '«Soy un gato, aunque todavía no tengo nombre.» Así comienza la primera y más hilarante novela de Natsume Sseki, una auténtica obra maestra de la literatura japonesa, que narra las aventuras de un desdeñoso felino que cohabita, de modo accidental, con un grupo de grotescos personajes, miembros todos ellos de la bienpensante clase media tokiota: el dispéptico profesor Kushami y su familia, teóricos dueños de la casa donde vive el gato; el mejor amigo del profesor, el charlatán e irritante Meitei; o el joven estudioso Kangetsu, que día sí, día no, intenta arreglárselas para conquistar a la hija de los vecinos. Escrita justo antes de su aclamada novela Botchan, Soy un gato es una sátira descarnada de la burguesía Meiji. Dotada de un ingenio a prueba de bombas y de un humor sardónico, recorre las peripecias de un voluble filósofo gatuno que no se cansa de hacer los comentarios más incisivos sobre la disparatada tropa de seres humanos con la que le ha tocado convivir.', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/7298644-L.jpg', 'pendiente', '/works/OL16797024W'),
(48, 'The Silent Patient', 'Alex Michaelides', '## [The Silent Patient PDF](https://chesserresources.com/doc/the-silent-patient-by-alex-michaelides/)\n\nAlicia Berenson’s life is seemingly perfect. One evening her husband Gabriel returns home late from a fashion shoot, and Alicia shoots him five times in the face, and then never speaks another word. Alicia’s refusal to talk, or give any kind of explanation, turns a domestic tragedy into something far grander, a mystery that captures the public imagination and casts Alicia into notoriety. The price of her art skyrockets, and she, the silent patient, is hidden away from the tabloids and spotlight at the Grove, a secure forensic unit in North London. Theo Faber is a criminal psychotherapist who has waited a long time for the opportunity to work with Alicia. His determination to get her to talk and unravel the mystery of why she shot her husband takes him down a twisting path into his own motivations–a search for the truth that threatens to consume him.', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/9407338-L.jpg', 'pendiente', '/works/OL19096402W'),
(49, 'Crimen y castigo', 'Фёдор Михайлович Достоевский', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/14083544-L.jpg', 'pendiente', '/works/OL35099756W'),
(50, 'Death on the Nile', 'Agatha Christie', 'The tranquillity of a cruise along the Nile was shattered by the discovery that Linnet Ridgeway ( Linnet Doyle) had been shot through the head. She was young, stylish, rich and beautiful. A girl who had everything... until she lost her life.\n\nHercule Poirot recalled an earlier outburst by a fellow passenger: &#39;I&#39;d like to put my dear little pistol against her head and just press the trigger.&#39; Yet in this exotic setting nothing was ever quite what it seemed...', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/14066646-L.jpg', 'pendiente', '/works/OL471724W'),
(51, 'La senda del perdedor', 'Charles Bukowski', 'Descripción no disponible', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/7373211-L.jpg', 'pendiente', '/works/OL17207322W'),
(52, 'That&#39;s Not My Name', 'Autor desconocido', 'She thought she had her life back. She was wrong.\n\nIt was a mistake to trust him.\n\nShivering and bruised, a teen wakes up on the side of a dirt road with no memory of how she got there—or who she is. A passing officer takes her to the police station, and not long after, a frantic man arrives. He&#39;s been searching for her for hours. He has her school ID, her birth certificate, and even family photos.\n\nHe is her father. Her name is Mary. Or so he says.\n\nWhen Lola slammed the car door and stormed off into the night, Drew thought they just needed some time to cool off. Except Lola disappeared, and the sheriff, his friends, and the whole town are convinced Drew murdered his girlfriend. Forget proving his innocence, he needs to find her before it&#39;s too late. The longer Lola is missing, the fewer leads there are to follow…and the more danger they both are in.', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/15155355-L.jpg', 'pendiente', '/works/OL37563803W'),
(53, 'The Stormlight Archive 1', 'Brandon Sanderson', 'GraphicAudio® A Movie in Your Mind® proudly releases THE WAY OF KINGS, the first of ten planned titles in New York Times Bestselling author, Brandon Sanderson’s epic fantasy series, THE STORMLIGHT ARCHIVE.\n\nRoshar is a world of stone and storms. Uncanny tempests of incredible power sweep across the rocky terrain so frequently that they have shaped ecology and civilization alike. Animals hide in shells, trees pull in branches, and grass retracts into the soilless ground. Cities are built only where the topography offers shelter.\n\nIt has been centuries since the fall of the 10 consecrated orders known as the Knights Radiant, but their Shardblades and Shardplate remain: mystical swords and suits of armor that transform ordinary men into near-invincible warriors. Wars were fought for them, and won by them. One such war rages on the Shattered Plains. There, Kaladin has been reduced to slavery. In a war that makes no sense, where 10 armies fight separately against a single foe, he struggles to save his men and to fathom the leaders who consider them expendable.\n\nBrightlord Dalinar Kholin commands one of those other armies. Like his brother, the late king, he is fascinated by an ancient text called The Way of Kings. Troubled by visions of ancient times and the Knights Radiant, he has begun to doubt his own sanity.\n\nAcross the ocean, an untried young woman named Shallan seeks to train under an eminent scholar and notorious heretic, Dalinar&#39;s niece, Jasnah. Though she genuinely loves learning, Shallan&#39;s motives are less than pure. As she plans a daring theft, her research for Jasnah hints at secrets of the Knights Radiant and the true cause of the war.\n\nDirector Rose Supan says, “Brandon Sanderson is at the top of his game with THE STORMLIGHT ARCHIVES. It&#39;s an honor to direct this story. The actors as well as our production team are thrilled to be a part of the process as well. I can proudly proclaim that the listener is in for a truly immersive experience!”\n\n© 2010 by Brandon Sanderson. Recorded with the permission of the Author and Dragonsteel Enterainment, LLC Production. All rights reserved. ℗ 2016 The Cutting Corporation. All rights reserved.', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/14587753-L.jpg', 'leyendo', '/works/OL37894320W'),
(54, 'Un vampiro en Maracaibo', 'Norberto José Olívar', 'Un neurótico profesor de historia anda tras la pista de un hombre obsesionado en beber sangre y alcanzar la vida eterna: un vampiro que ronda la calurosa ciudad de Maracaibo, en Venezuela. Un detective jubilado se convierte en su aliado y su mejor informante.', NULL, NULL, NULL, NULL, NULL, 23, 'https://covers.openlibrary.org/b/id/15227831-L.jpg', 'leyendo', '/works/OL2168045W');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
