-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2023 at 07:28 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_bus`
--

-- --------------------------------------------------------

--
-- Table structure for table `passangers`
--

CREATE TABLE `passangers` (
  `passanger_id` int(11) NOT NULL,
  `passanger_name` varchar(255) NOT NULL,
  `passanger_dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  `photo_path` varchar(255) NOT NULL,
  `qr_code_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `passangers`
--

INSERT INTO `passangers` (`passanger_id`, `passanger_name`, `passanger_dob`, `password`, `photo_path`, `qr_code_path`) VALUES
(243448, 'sejal', '2002-04-07', 'sejal123', 'uploads/sejal_photo.jpg', 'uploads/sejal_qrcode.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `passangers`
--
ALTER TABLE `passangers`
  ADD PRIMARY KEY (`passanger_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `passangers`
--
ALTER TABLE `passangers`
  MODIFY `passanger_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=346439;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
