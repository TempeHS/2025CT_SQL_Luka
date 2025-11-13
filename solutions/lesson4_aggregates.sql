-- database: ../database/starwars.db

-- Lesson 4 Solutions: Aggregate Functions and GROUP BY
-- This file contains complete solutions for all Lesson 4 activities

-- ============================================
-- Setup: Add affiliation column and data
-- ============================================

ALTER TABLE characters ADD COLUMN affiliation TEXT;

UPDATE characters SET affiliation = 'Rebel Alliance' WHERE name IN ('Luke Skywalker', 'Leia Organa', 'Han Solo', 'Chewbacca');
UPDATE characters SET affiliation = 'Jedi Order' WHERE name IN ('Obi-Wan Kenobi', 'Yoda');
UPDATE characters SET affiliation = 'Galactic Empire' WHERE name = 'Darth Vader';
UPDATE characters SET affiliation = 'Independent' WHERE name = 'R2-D2';
UPDATE characters SET affiliation = 'Galactic Republic' WHERE name IN ('Padmé Amidala', 'Mace Windu');
UPDATE characters SET affiliation = 'Jedi Order' WHERE name = 'Ahsoka Tano';

-- ============================================
-- Basic Aggregate Functions
-- ============================================

-- Query 1: Count how many characters are in the table
SELECT COUNT(*) FROM characters;

-- Query 2: Count characters who have a height recorded
SELECT COUNT(height) FROM characters;

-- Query 3: Find the tallest character's height
SELECT MAX(height) FROM characters;

-- Query 4: Find the shortest character's height
SELECT MIN(height) FROM characters;

-- Query 5: Calculate the average height of all characters
SELECT AVG(height) FROM characters;

-- Query 6: Add up all character heights
SELECT SUM(height) FROM characters;

-- Query 7: Get multiple statistics at once
SELECT 
    COUNT(*) AS total_characters,
    AVG(height) AS average_height,
    MAX(height) AS tallest,
    MIN(height) AS shortest
FROM characters;

-- ============================================
-- GROUP BY - Grouping Data
-- ============================================

-- Query 8: Count how many characters of each species
SELECT species, COUNT(*) AS character_count
FROM characters
GROUP BY species;

-- Query 9: Find the average height for each species
SELECT species, AVG(height) AS average_height
FROM characters
WHERE height IS NOT NULL
GROUP BY species;

-- Query 10: Count characters from each homeworld
SELECT homeworld, COUNT(*) AS character_count
FROM characters
GROUP BY homeworld
ORDER BY character_count DESC;

-- Query 11: Count characters in each affiliation
SELECT affiliation, COUNT(*) AS members
FROM characters
WHERE affiliation IS NOT NULL
GROUP BY affiliation
ORDER BY members DESC;

-- ============================================
-- HAVING - Filtering Groups
-- ============================================

-- Query 12: Show only species with 2 or more characters
SELECT species, COUNT(*) AS character_count
FROM characters
GROUP BY species
HAVING COUNT(*) >= 2;

-- Query 13: Find affiliations with more than the average number of members
SELECT affiliation, COUNT(*) AS member_count
FROM characters
WHERE affiliation IS NOT NULL
GROUP BY affiliation
HAVING COUNT(*) > (
    SELECT AVG(cnt) 
    FROM (
        SELECT COUNT(*) AS cnt 
        FROM characters 
        WHERE affiliation IS NOT NULL 
        GROUP BY affiliation
    )
);

-- Query 14: Count humans by homeworld, only showing planets with 2+ humans
SELECT homeworld, COUNT(*) AS human_count
FROM characters
WHERE species = 'Human'
GROUP BY homeworld
HAVING COUNT(*) >= 2;

-- ============================================
-- COUNT DISTINCT
-- ============================================

-- Query 15: How many different species are there?
SELECT COUNT(DISTINCT species) AS unique_species
FROM characters;

-- Query 16: How many different homeworlds are represented?
SELECT COUNT(DISTINCT homeworld) AS unique_homeworlds
FROM characters;

-- ============================================
-- Practice Exercises
-- ============================================

-- Exercise 1: Find the total height of all characters combined
SELECT SUM(height) AS total_height
FROM characters;

-- Exercise 2: Count characters from each homeworld, sorted alphabetically
SELECT homeworld, COUNT(*) AS character_count
FROM characters
GROUP BY homeworld
ORDER BY homeworld;

-- Exercise 3: Find average height by affiliation
SELECT affiliation, AVG(height) AS avg_height
FROM characters
WHERE height IS NOT NULL AND affiliation IS NOT NULL
GROUP BY affiliation;

-- Exercise 4: Show homeworlds that have exactly 1 character
SELECT homeworld, COUNT(*) AS character_count
FROM characters
GROUP BY homeworld
HAVING COUNT(*) = 1;

-- ============================================
-- CHALLENGE PROBLEM SOLUTION
-- Find which affiliation has the tallest average height,
-- but only include affiliations with 2 or more members
-- ============================================

SELECT 
    affiliation,
    COUNT(*) AS member_count,
    ROUND(AVG(height), 2) AS avg_height
FROM characters
WHERE affiliation IS NOT NULL AND height IS NOT NULL
GROUP BY affiliation
HAVING COUNT(*) >= 2
ORDER BY avg_height DESC;

-- Expected result: Shows affiliations with 2+ members, sorted by average height (tallest first)

-- ============================================
-- Additional Complex Examples
-- ============================================

-- Find species with more characters than the average species count
SELECT species, COUNT(*) AS char_count
FROM characters
GROUP BY species
HAVING COUNT(*) > (
    SELECT AVG(species_count)
    FROM (
        SELECT COUNT(*) AS species_count
        FROM characters
        GROUP BY species
    )
);

-- Show homeworlds with their tallest character
SELECT 
    homeworld,
    MAX(height) AS tallest_character_height,
    COUNT(*) AS character_count
FROM characters
WHERE height IS NOT NULL
GROUP BY homeworld
ORDER BY tallest_character_height DESC;

-- Calculate what percentage each species represents
SELECT 
    species,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM characters), 2) AS percentage
FROM characters
GROUP BY species
ORDER BY count DESC;
