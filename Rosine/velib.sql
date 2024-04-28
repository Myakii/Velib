-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 27 avr. 2024 à 23:33
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `velib`
--

-- --------------------------------------------------------

--
-- Structure de la table `favoris`
--

CREATE TABLE `favoris` (
  `id_favoris` int(10) NOT NULL,
  `id_user` int(10) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `data_json` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `favoris`
--

INSERT INTO `favoris` (`id_favoris`, `id_user`, `nom`, `data_json`) VALUES
(7002, 1, 'Dimanche soir', '{\"stationcode\": \"7002\", \"name\": \"Vaneau - S\\u00e8vres\", \"is_installed\": \"OUI\", \"capacity\": 35, \"numdocksavailable\": 10, \"numbikesavailable\": 24, \"mechanical\": 19, \"ebike\": 5, \"is_renting\": \"OUI\", \"is_returning\": \"OUI\", \"duedate\": \"2024-04-27T10:31:52+00:00\", \"coordonnees_geo\": {\"lon\": 2.3204218259346, \"lat\": 48.848563233059}, \"nom_arrondissement_communes\": \"Paris\", \"code_insee_commune\": null}'),
(5110, 1, 'Lieux à visiter en vélo', '{\"stationcode\": \"5110\", \"name\": \"Lac\\u00e9p\\u00e8de - Monge\", \"is_installed\": \"OUI\", \"capacity\": 23, \"numdocksavailable\": 14, \"numbikesavailable\": 5, \"mechanical\": 2, \"ebike\": 3, \"is_renting\": \"OUI\", \"is_returning\": \"OUI\", \"duedate\": \"2024-04-27T10:33:50+00:00\", \"coordonnees_geo\": {\"lon\": 2.3519663885235786, \"lat\": 48.84389286531899}, \"nom_arrondissement_communes\": \"Paris\", \"code_insee_commune\": null}');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
