-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 23, 2026 at 11:37 AM
-- Server version: 5.7.24
-- PHP Version: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ffbs_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `exporteddata`
--

CREATE TABLE `exporteddata` (
  `csv_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  `csv_path` varchar(500) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `file_id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_type` enum('RGB-D','Depth') NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `upload_date` timestamp NULL DEFAULT NULL,
  `video_path` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`file_id`, `file_name`, `file_type`, `file_path`, `upload_date`, `video_path`) VALUES
(4, 'ffb12Depth_3D.bag', 'Depth', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-03-04 04:35:41', NULL),
(12, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-03-20 11:32:31', NULL),
(42, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-11 06:14:00', NULL),
(52, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-16 13:22:46', NULL),
(53, 'ffb12RGB_2D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12RGB_2D.bag', '2026-04-16 13:24:28', NULL),
(55, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-17 03:51:31', NULL),
(57, 'RGB (2).bag', 'Depth', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\RGB (2).bag', '2026-04-17 03:55:20', NULL),
(58, 'DEPTH (1).bag', 'Depth', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\DEPTH (1).bag', '2026-04-17 03:56:04', NULL),
(59, 'ffb12RGB_2D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12RGB_2D.bag', '2026-04-17 03:56:37', NULL),
(60, 'ffb10Depth_3D.bag', 'Depth', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-17 04:16:46', NULL),
(61, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-17 05:14:16', NULL),
(62, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-17 09:01:48', NULL),
(63, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-17 09:06:29', NULL),
(64, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-17 09:43:44', NULL),
(65, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-17 09:50:01', NULL),
(66, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-17 09:58:45', NULL),
(67, 'ffb12Depth_3D (1).bag', 'Depth', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (1).bag', '2026-04-17 12:19:49', NULL),
(68, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-17 12:34:32', NULL),
(69, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-17 12:35:46', NULL),
(70, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-17 12:46:57', NULL),
(71, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-17 12:51:41', NULL),
(72, 'ffb12Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D.bag', '2026-04-17 12:57:18', NULL),
(73, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-17 13:01:46', NULL),
(74, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 02:43:42', NULL),
(75, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 02:48:17', NULL),
(76, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-18 02:57:12', NULL),
(77, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 03:06:08', NULL),
(78, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 03:09:03', NULL),
(79, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 03:19:57', NULL),
(80, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-18 03:42:14', NULL),
(81, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 03:47:57', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_081\\ffb_prediction_video.mp4'),
(82, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 03:52:09', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_082\\ffb_prediction_video.mp4'),
(83, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-18 04:04:41', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_083\\ffb_prediction_video.mp4'),
(84, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 04:11:32', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_084\\ffb_prediction_video.mp4'),
(85, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 04:35:25', NULL),
(86, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 04:58:13', NULL),
(87, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-18 06:43:35', NULL),
(88, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 06:46:42', NULL),
(89, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 06:50:11', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_089\\ffb_prediction_video.mp4'),
(90, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-18 06:54:53', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_090\\ffb_prediction_video.mp4'),
(91, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-18 10:49:48', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_091\\ffb_prediction_video.mp4'),
(92, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-21 10:38:13', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_092\\ffb_prediction_video.mp4'),
(93, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-21 10:45:16', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_093\\ffb_prediction_video.mp4'),
(94, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-21 10:49:41', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_094\\ffb_prediction_video.mp4'),
(95, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-21 11:21:07', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_095\\ffb_prediction_video.mp4'),
(96, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-21 11:26:10', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_096\\ffb_prediction_video.mp4'),
(97, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-21 11:29:05', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_097\\ffb_prediction_video.mp4'),
(98, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-21 11:31:38', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_098\\ffb_prediction_video.mp4'),
(99, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-21 11:34:21', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_099\\ffb_prediction_video.mp4'),
(100, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-21 11:37:39', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_100\\ffb_prediction_video.mp4'),
(101, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-22 05:39:15', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_101\\ffb_prediction_video.mp4'),
(102, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-22 05:40:44', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_102\\ffb_prediction_video.mp4'),
(103, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-22 05:49:44', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_103\\ffb_prediction_video.mp4'),
(104, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-22 06:06:01', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_104\\ffb_prediction_video.mp4'),
(105, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-22 06:17:20', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_105\\ffb_prediction_video.mp4'),
(106, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-22 08:53:32', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_106\\ffb_prediction_video.mp4'),
(107, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-22 10:03:14', NULL),
(108, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-22 10:06:52', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_108\\ffb_prediction_video.mp4'),
(109, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-22 10:56:28', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_109\\ffb_prediction_video.mp4'),
(110, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-22 11:00:55', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_110\\ffb_prediction_video.mp4'),
(111, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-22 11:07:30', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_111\\ffb_prediction_video.mp4'),
(112, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 00:21:26', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_112\\ffb_prediction_video.mp4'),
(113, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 00:32:14', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_113\\ffb_prediction_video.mp4'),
(114, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 00:42:43', NULL),
(115, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 00:45:35', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_115\\ffb_prediction_video.mp4'),
(116, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 00:50:33', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_116\\ffb_prediction_video.mp4'),
(117, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 00:54:03', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_117\\ffb_prediction_video.mp4'),
(118, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 01:00:04', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_118\\ffb_prediction_video.mp4'),
(119, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 02:26:42', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_119\\ffb_prediction_video.mp4'),
(120, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 02:37:00', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_120\\ffb_prediction_video.mp4'),
(121, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 02:39:24', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_121\\ffb_prediction_video.mp4'),
(122, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 07:44:17', NULL),
(123, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 07:48:19', NULL),
(124, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 07:50:57', NULL),
(125, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 07:55:41', NULL),
(126, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 07:57:41', NULL),
(127, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 08:07:32', NULL),
(128, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 08:38:38', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_128\\ffb_prediction_video.mp4'),
(129, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 08:48:55', NULL),
(130, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 08:53:00', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_130\\ffb_prediction_video.mp4'),
(131, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 09:00:13', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_131\\ffb_prediction_video.mp4'),
(132, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 09:13:06', NULL),
(133, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:18:35', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_133\\ffb_prediction_video.mp4'),
(134, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:21:04', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_134\\ffb_prediction_video.mp4'),
(135, 'ffb10Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb10Depth_3D.bag', '2026-04-23 09:29:28', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_135\\ffb_prediction_video.mp4'),
(136, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 09:38:51', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_136\\ffb_prediction_video.mp4'),
(137, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:40:51', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_137\\ffb_prediction_video.mp4'),
(138, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:46:14', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_138\\ffb_prediction_video.mp4'),
(139, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:52:58', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_139\\ffb_prediction_video.mp4'),
(140, 'ffb11Depth_3D.bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb11Depth_3D.bag', '2026-04-23 09:56:09', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_140\\ffb_prediction_video.mp4'),
(141, 'ffb12Depth_3D (2).bag', 'RGB-D', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\uploads\\ffb12Depth_3D (2).bag', '2026-04-23 11:26:37', 'C:\\Users\\Navya\\Desktop\\Github files\\SEGP-FrontEnd-BackEnd\\src\\App\\app\\sample_141\\ffb_prediction_video.mp4');

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `prediction_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  `mass_prediction` decimal(10,2) NOT NULL,
  `model_version` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `predictions`
--

INSERT INTO `predictions` (`prediction_id`, `file_id`, `mass_prediction`, `model_version`, `created_at`) VALUES
(1, 42, '23.72', 'YOLOv5 + Ellipsoid v1', '2026-04-11 06:14:49'),
(2, 52, '22.06', 'YOLOv5 + Ellipsoid v1', '2026-04-16 13:23:28'),
(3, 55, '23.25', 'YOLOv5 + Ellipsoid v1', '2026-04-17 03:52:18'),
(4, 60, '24.89', 'YOLOv5 + Ellipsoid v1', '2026-04-17 04:17:21'),
(5, 61, '20.58', 'YOLOv5 + Ellipsoid v1', '2026-04-17 05:14:44'),
(6, 63, '23.02', 'YOLOv5 + Ellipsoid v1', '2026-04-17 09:07:14'),
(7, 64, '23.72', 'YOLOv5 + Ellipsoid v1', '2026-04-17 09:44:28'),
(8, 65, '18.14', 'YOLOv5 + Ellipsoid v1', '2026-04-17 09:50:31'),
(9, 66, '23.95', 'YOLOv5 + Ellipsoid v1', '2026-04-17 09:59:22'),
(10, 67, '22.26', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:20:35'),
(11, 68, '27.19', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:35:10'),
(12, 69, '22.51', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:36:39'),
(13, 70, '24.14', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:47:52'),
(14, 71, '25.00', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:52:17'),
(15, 72, '23.97', 'YOLOv5 + Ellipsoid v1', '2026-04-17 12:58:12'),
(16, 73, '24.28', 'YOLOv5 + Ellipsoid v1', '2026-04-17 13:02:24'),
(17, 75, '27.19', 'YOLOv5 + Ellipsoid v1', '2026-04-18 02:48:54'),
(18, 76, '22.68', 'YOLOv5 + Ellipsoid v1', '2026-04-18 02:57:55'),
(19, 77, '24.89', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:06:45'),
(20, 78, '19.73', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:09:31'),
(21, 79, '22.90', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:20:37'),
(22, 80, '21.91', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:43:18'),
(23, 81, '19.29', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:48:26'),
(24, 82, '25.25', 'YOLOv5 + Ellipsoid v1', '2026-04-18 03:52:46'),
(25, 83, '23.78', 'YOLOv5 + Ellipsoid v1', '2026-04-18 04:05:25'),
(26, 84, '25.71', 'YOLOv5 + Ellipsoid v1', '2026-04-18 04:11:58'),
(27, 89, '21.56', 'YOLOv5 + Ellipsoid v1', '2026-04-18 06:50:44'),
(28, 90, '29.86', 'YOLOv5 + Ellipsoid v1', '2026-04-18 06:56:18'),
(29, 91, '20.12', 'YOLOv5 + Ellipsoid v1', '2026-04-18 10:51:02'),
(30, 92, '24.39', 'YOLOv5 + Ellipsoid v1', '2026-04-21 10:39:29'),
(31, 93, '23.81', 'YOLOv5 + Ellipsoid v1', '2026-04-21 10:46:20'),
(32, 94, '19.91', 'YOLOv5 + Ellipsoid v1', '2026-04-21 10:50:40'),
(33, 95, '21.99', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:22:16'),
(34, 96, '24.99', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:27:32'),
(35, 97, '24.53', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:30:09'),
(36, 98, '23.15', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:32:12'),
(37, 99, '24.28', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:35:14'),
(38, 100, '24.18', 'YOLOv5 + Ellipsoid v1', '2026-04-21 11:38:45'),
(39, 101, '19.23', 'YOLOv5 + Ellipsoid v1', '2026-04-22 05:39:50'),
(40, 102, '22.12', 'YOLOv5 + Ellipsoid v1', '2026-04-22 05:41:27'),
(41, 103, '20.74', 'YOLOv5 + Ellipsoid v1', '2026-04-22 05:50:42'),
(42, 104, '22.35', 'YOLOv5 + Ellipsoid v1', '2026-04-22 06:07:17'),
(43, 105, '20.58', 'YOLOv5 + Ellipsoid v1', '2026-04-22 06:17:49'),
(44, 106, '21.26', 'YOLOv5 + Ellipsoid v1', '2026-04-22 08:54:43'),
(45, 108, '25.70', 'YOLOv5 + Ellipsoid v1', '2026-04-22 10:10:46'),
(46, 109, '24.55', 'YOLOv5 + Ellipsoid v1', '2026-04-22 10:57:14'),
(47, 110, '24.45', 'YOLOv5 + Ellipsoid v1', '2026-04-22 11:02:50'),
(48, 111, '19.23', 'YOLOv5 + Ellipsoid v1', '2026-04-22 11:08:47'),
(49, 112, '24.27', 'YOLOv5 + Ellipsoid v1', '2026-04-23 00:23:09'),
(50, 113, '20.85', 'YOLOv5 + Ellipsoid v1', '2026-04-23 00:33:52'),
(51, 115, '22.70', 'YOLOv5 + Ellipsoid v1', '2026-04-23 00:46:21'),
(52, 116, '21.38', 'YOLOv5 + Ellipsoid v1', '2026-04-23 00:52:52'),
(53, 117, '25.34', 'YOLOv5 + Ellipsoid v1', '2026-04-23 00:59:00'),
(54, 118, '19.47', 'YOLOv5 + Ellipsoid v1', '2026-04-23 01:00:33'),
(55, 119, '29.86', 'YOLOv5 + Ellipsoid v1', '2026-04-23 02:27:27'),
(56, 120, '21.02', 'YOLOv5 + Ellipsoid v1', '2026-04-23 02:37:40'),
(57, 121, '29.86', 'YOLOv5 + Ellipsoid v1', '2026-04-23 02:40:05'),
(58, 128, '19.43', 'YOLOv5 + Ellipsoid v1', '2026-04-23 08:40:01'),
(59, 130, '23.37', 'YOLOv5 + Ellipsoid v1', '2026-04-23 08:54:10'),
(60, 131, '29.86', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:01:46'),
(61, 133, '20.84', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:19:33'),
(62, 134, '22.03', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:22:01'),
(63, 135, '25.16', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:30:06'),
(64, 136, '21.61', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:40:06'),
(65, 137, '20.32', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:42:21'),
(66, 138, '22.02', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:47:16'),
(67, 139, '18.67', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:54:08'),
(68, 140, '19.33', 'YOLOv5 + Ellipsoid v1', '2026-04-23 09:56:47'),
(69, 141, '22.69', 'YOLOv5 + Ellipsoid v1', '2026-04-23 11:28:30');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `exporteddata`
--
ALTER TABLE `exporteddata`
  ADD PRIMARY KEY (`csv_id`),
  ADD KEY `file_id` (`file_id`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`file_id`);

--
-- Indexes for table `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`prediction_id`),
  ADD KEY `file_id` (`file_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `exporteddata`
--
ALTER TABLE `exporteddata`
  MODIFY `csv_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `file_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=142;

--
-- AUTO_INCREMENT for table `predictions`
--
ALTER TABLE `predictions`
  MODIFY `prediction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `exporteddata`
--
ALTER TABLE `exporteddata`
  ADD CONSTRAINT `exporteddata_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`) ON DELETE CASCADE;

--
-- Constraints for table `predictions`
--
ALTER TABLE `predictions`
  ADD CONSTRAINT `predictions_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
