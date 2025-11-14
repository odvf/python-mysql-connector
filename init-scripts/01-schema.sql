-- =====================================================
-- MySQL Database Schema
-- =====================================================

-- Drop database if exists and create new one
CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

-- =====================================================
-- Table: user
-- =====================================================
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: playlist
-- =====================================================
CREATE TABLE IF NOT EXISTS playlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: playlist_subscriber
-- =====================================================
CREATE TABLE IF NOT EXISTS playlist_subscriber (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (playlist_id) REFERENCES playlist(id) ON DELETE CASCADE,
    UNIQUE KEY unique_subscription (user_id, playlist_id, deleted_at),
    INDEX idx_user_id (user_id),
    INDEX idx_playlist_id (playlist_id),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: song
-- =====================================================
CREATE TABLE IF NOT EXISTS song (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volume DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    duration INT NOT NULL COMMENT 'Duration in seconds',
    name VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    metadata JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_duration (duration)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: playlist_queue
-- =====================================================
CREATE TABLE IF NOT EXISTS playlist_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    played_at TIMESTAMP NULL DEFAULT NULL,
    finished_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES song(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_song_id (song_id),
    INDEX idx_added_at (added_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: lyric
-- =====================================================
CREATE TABLE IF NOT EXISTS lyric (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL,
    language VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES song(id) ON DELETE CASCADE,
    UNIQUE KEY unique_song_language (song_id, language),
    INDEX idx_song_id (song_id),
    INDEX idx_language (language)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
