--database: ../database/starwars.db

-- Lesson 2 Solutions: Selecting and Filtering Data
-- This file contains complete solutions for all Lesson 2 activities

-- ============================================
-- Basic SELECT Queries
-- ============================================

-- Query 1: View all characters and all columns
SELECT * FROM characters;

-- Query 2: View only names and species
SELECT name, species FROM characters;

-- Query 3: View columns in a different order
SELECT homeworld, name, species FROM characters;

-- ============================================
-- WHERE Clause - Filtering
-- ============================================

-- Query 4: Find all human characters
SELECT * FROM characters WHERE species = 'Human';

-- Query 5: Find all characters from Tatooine
SELECT name, homeworld FROM characters WHERE homeworld = 'Tatooine';

-- Query 6: Find all characters who are NOT human
SELECT name, species FROM characters WHERE species != 'Human';

-- ============================================
-- Combining Conditions with AND/OR
-- ============================================

-- Query 7: Find humans from Tatooine
SELECT name, species, homeworld 
FROM characters 
WHERE species = 'Human' AND homeworld = 'Tatooine';

-- Query 8: Find characters who are either Droids OR from Naboo
SELECT name, species, homeworld 
FROM characters 
WHERE species = 'Droid' OR homeworld = 'Naboo';

-- Query 9: Find humans from either Tatooine or Alderaan
SELECT name, species, homeworld 
FROM characters 
WHERE species = 'Human' AND (homeworld = 'Tatooine' OR homeworld = 'Alderaan');

-- ============================================
-- Pattern Matching with LIKE
-- ============================================

-- Query 10: Find all characters whose names start with 'L'
SELECT name FROM characters WHERE name LIKE 'L%';

-- Query 11: Find all characters whose names end with 'o'
SELECT name FROM characters WHERE name LIKE '%o';

-- Query 12: Find all characters with 'Darth' in their name
SELECT name FROM characters WHERE name LIKE '%Darth%';

-- Query 13: Find all species containing 'oid'
SELECT DISTINCT species FROM characters WHERE species LIKE '%oid%';

-- ============================================
-- Practice Exercises
-- ============================================

-- Exercise 1: Find all characters from Kashyyyk
SELECT name, homeworld FROM characters WHERE homeworld = 'Kashyyyk';

-- Exercise 2: Find all characters who are NOT droids
SELECT name, species FROM characters WHERE species != 'Droid';

-- Exercise 3: Find all humans NOT from Tatooine
SELECT name, species, homeworld 
FROM characters 
WHERE species = 'Human' AND homeworld != 'Tatooine';

-- Exercise 4: Find all characters whose names contain 'Sky'
SELECT name FROM characters WHERE name LIKE '%Sky%';

-- ============================================
-- CHALLENGE PROBLEM SOLUTION
-- Find characters whose species contains "oid" AND homeworld starts with 'N'
-- ============================================

SELECT name, species, homeworld 
FROM characters 
WHERE species LIKE '%oid%' AND homeworld LIKE 'N%';

-- Expected result: R2-D2 (species: Droid, homeworld: Naboo)
