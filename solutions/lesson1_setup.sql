-- database: ../database/starwars.db

-- Lesson 1 Solutions: Introduction to Databases & SQLite Setup
-- This file contains complete solutions for all Lesson 1 activities

-- ============================================
-- Part 1: Create the characters table
-- ============================================

CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT,
    homeworld TEXT
);

-- ============================================
-- Part 2: Insert initial character data
-- ============================================

INSERT INTO characters (name, species, homeworld) VALUES
    ('Luke Skywalker', 'Human', 'Tatooine'),
    ('Leia Organa', 'Human', 'Alderaan'),
    ('Han Solo', 'Human', 'Corellia'),
    ('Chewbacca', 'Wookiee', 'Kashyyyk'),
    ('Obi-Wan Kenobi', 'Human', 'Stewjon'),
    ('Darth Vader', 'Human', 'Tatooine'),
    ('Yoda', 'Yoda''s species', 'Unknown'),
    ('R2-D2', 'Droid', 'Naboo');

-- ============================================
-- Part 3: Practice Exercise
-- Add 3 more characters
-- ============================================

INSERT INTO characters (name, species, homeworld) VALUES
    ('Padmé Amidala', 'Human', 'Naboo'),
    ('Mace Windu', 'Human', 'Haruun Kal'),
    ('Ahsoka Tano', 'Togruta', 'Shili');

-- ============================================
-- Verify the data
-- ============================================

SELECT * FROM characters;

-- ============================================
-- CHALLENGE PROBLEM SOLUTION
-- Create droids table and insert data
-- ============================================

CREATE TABLE IF NOT EXISTS droids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model TEXT,
    function TEXT
);

INSERT INTO droids (name, model, function) VALUES
    ('R2-D2', 'R2-series astromech', 'Repair & Navigation'),
    ('C-3PO', 'Protocol droid', 'Translation'),
    ('BB-8', 'BB-series astromech', 'Reconnaissance');

SELECT * FROM droids;
