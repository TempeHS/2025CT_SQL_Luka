#!/usr/bin/env python3
"""
Lesson 9 Solutions: Python and SQL Integration
This file contains complete solutions for all Python sqlite3 activities

NOTE: This file uses the older pattern of passing connections as parameters.
For modern Python, it's better to use context managers (with statements) directly
in each function. See the Jupyter notebook for examples of the context manager pattern.

Context manager pattern (RECOMMENDED):
    try:
        with sqlite3.connect('database/starwars.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters")
            results = cursor.fetchall()
            return results
            # Connection automatically closes, commits on success, rolls back on error
    except sqlite3.Error as e:
        print(f"Error: {e}")

This file demonstrates the older pattern for educational comparison.
"""

import sqlite3
from typing import List, Tuple, Optional


# ============================================
# Part 1: Basic Connection and Queries
# ============================================


def connect_to_database(db_path: str = "database/starwars.db") -> sqlite3.Connection:
    """
    Connect to the SQLite database.

    Args:
        db_path: Path to the database file

    Returns:
        Database connection object
    """
    try:
        conn = sqlite3.connect(db_path)
        print(f"✓ Successfully connected to {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        raise


def get_all_characters(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Retrieve all characters from the database.

    Args:
        conn: Database connection

    Returns:
        List of character tuples
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    characters = cursor.fetchall()
    return characters


def get_character_by_name(conn: sqlite3.Connection, name: str) -> Optional[Tuple]:
    """
    Find a character by name.

    Args:
        conn: Database connection
        name: Character name to search for

    Returns:
        Character tuple or None if not found
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE name = ?", (name,))
    character = cursor.fetchone()
    return character


def get_characters_by_species(conn: sqlite3.Connection, species: str) -> List[Tuple]:
    """
    Find all characters of a given species.

    Args:
        conn: Database connection
        species: Species to filter by

    Returns:
        List of character tuples
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE species = ?", (species,))
    characters = cursor.fetchall()
    return characters


# ============================================
# Part 2: Parameterised Queries (Safe from SQL Injection)
# ============================================


def search_characters(
    conn: sqlite3.Connection,
    species: Optional[str] = None,
    affiliation: Optional[str] = None,
    min_height: Optional[int] = None,
) -> List[Tuple]:
    """
    Search characters with multiple optional filters.

    Args:
        conn: Database connection
        species: Optional species filter
        affiliation: Optional affiliation filter
        min_height: Optional minimum height filter

    Returns:
        List of matching character tuples
    """
    cursor = conn.cursor()
    query = "SELECT * FROM characters WHERE 1=1"
    params = []

    if species:
        query += " AND species = ?"
        params.append(species)

    if affiliation:
        query += " AND affiliation = ?"
        params.append(affiliation)

    if min_height:
        query += " AND height >= ?"
        params.append(min_height)

    cursor.execute(query, params)
    return cursor.fetchall()


def get_tall_characters(conn: sqlite3.Connection, min_height: int) -> List[Tuple]:
    """
    Find characters taller than specified height.

    Args:
        conn: Database connection
        min_height: Minimum height in cm

    Returns:
        List of character tuples
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, species, height 
        FROM characters 
        WHERE height >= ?
        ORDER BY height DESC
    """,
        (min_height,),
    )
    return cursor.fetchall()


# ============================================
# Part 3: INSERT Operations
# ============================================


def add_character(
    conn: sqlite3.Connection,
    name: str,
    species: str,
    homeworld: str,
    height: Optional[int] = None,
    affiliation: Optional[str] = None,
) -> int:
    """
    Add a new character to the database.

    Args:
        conn: Database connection
        name: Character name
        species: Character species
        homeworld: Character homeworld
        height: Optional height in cm
        affiliation: Optional affiliation

    Returns:
        ID of the newly created character
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO characters (name, species, homeworld, height, affiliation)
        VALUES (?, ?, ?, ?, ?)
    """,
        (name, species, homeworld, height, affiliation),
    )

    conn.commit()
    character_id = cursor.lastrowid
    print(f"✓ Added character: {name} (ID: {character_id})")
    return character_id


def add_multiple_characters(conn: sqlite3.Connection, characters: List[Tuple]) -> None:
    """
    Add multiple characters efficiently.

    Args:
        conn: Database connection
        characters: List of character tuples (name, species, homeworld, height, affiliation)
    """
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO characters (name, species, homeworld, height, affiliation)
        VALUES (?, ?, ?, ?, ?)
    """,
        characters,
    )

    conn.commit()
    print(f"✓ Added {cursor.rowcount} characters")


# ============================================
# Part 4: UPDATE Operations
# ============================================


def update_character_affiliation(
    conn: sqlite3.Connection, name: str, new_affiliation: str
) -> None:
    """
    Update a character's affiliation.

    Args:
        conn: Database connection
        name: Character name
        new_affiliation: New affiliation value
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE characters 
        SET affiliation = ? 
        WHERE name = ?
    """,
        (new_affiliation, name),
    )

    conn.commit()
    if cursor.rowcount > 0:
        print(f"✓ Updated {name}'s affiliation to {new_affiliation}")
    else:
        print(f"✗ Character {name} not found")


def update_character_height(
    conn: sqlite3.Connection, name: str, new_height: int
) -> None:
    """
    Update a character's height.

    Args:
        conn: Database connection
        name: Character name
        new_height: New height in cm
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE characters 
        SET height = ? 
        WHERE name = ?
    """,
        (new_height, name),
    )

    conn.commit()
    if cursor.rowcount > 0:
        print(f"✓ Updated {name}'s height to {new_height}cm")
    else:
        print(f"✗ Character {name} not found")


# ============================================
# Part 5: DELETE Operations
# ============================================


def delete_character(conn: sqlite3.Connection, name: str) -> None:
    """
    Delete a character from the database.

    Args:
        conn: Database connection
        name: Character name to delete
    """
    cursor = conn.cursor()

    # First check if character exists
    cursor.execute("SELECT id FROM characters WHERE name = ?", (name,))
    if not cursor.fetchone():
        print(f"✗ Character {name} not found")
        return

    # Delete the character
    cursor.execute("DELETE FROM characters WHERE name = ?", (name,))
    conn.commit()
    print(f"✓ Deleted character: {name}")


def delete_characters_by_affiliation(
    conn: sqlite3.Connection, affiliation: str
) -> None:
    """
    Delete all characters from a specific affiliation.

    Args:
        conn: Database connection
        affiliation: Affiliation to delete
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE affiliation = ?", (affiliation,))
    conn.commit()
    print(f"✓ Deleted {cursor.rowcount} characters from {affiliation}")


# ============================================
# Part 6: Complex Queries with JOINs
# ============================================


def get_characters_with_planets(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Get characters with their planet information.

    Args:
        conn: Database connection

    Returns:
        List of (character_name, species, planet_name, climate) tuples
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT c.name, c.species, p.name, p.climate
        FROM characters c
        INNER JOIN planets p ON c.planet_id = p.id
        ORDER BY c.name
    """
    )
    return cursor.fetchall()


def get_character_vehicles(
    conn: sqlite3.Connection, character_name: str
) -> List[Tuple]:
    """
    Get all vehicles for a specific character.

    Args:
        conn: Database connection
        character_name: Name of the character

    Returns:
        List of (vehicle_name, vehicle_class, cost) tuples
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT v.name, v.vehicle_class, v.cost_in_credits
        FROM vehicles v
        INNER JOIN character_vehicles cv ON v.id = cv.vehicle_id
        INNER JOIN characters c ON cv.character_id = c.id
        WHERE c.name = ?
        ORDER BY v.name
    """,
        (character_name,),
    )
    return cursor.fetchall()


# ============================================
# Part 7: Aggregate Functions and Statistics
# ============================================


def get_species_statistics(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Get statistics for each species.

    Args:
        conn: Database connection

    Returns:
        List of (species, count, avg_height) tuples
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            species,
            COUNT(*) as count,
            ROUND(AVG(height), 1) as avg_height
        FROM characters
        WHERE height IS NOT NULL
        GROUP BY species
        ORDER BY count DESC
    """
    )
    return cursor.fetchall()


def get_affiliation_summary(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Get member counts for each affiliation.

    Args:
        conn: Database connection

    Returns:
        List of (affiliation, member_count) tuples
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT affiliation, COUNT(*) as member_count
        FROM characters
        WHERE affiliation IS NOT NULL
        GROUP BY affiliation
        ORDER BY member_count DESC
    """
    )
    return cursor.fetchall()


# ============================================
# Part 8: Display Functions
# ============================================


def display_characters(
    characters: List[Tuple], columns: Optional[List[str]] = None
) -> None:
    """
    Display characters in a formatted way.

    Args:
        characters: List of character tuples
        columns: Optional list of column names
    """
    if not characters:
        print("No characters found.")
        return

    if columns:
        print(" | ".join(columns))
        print("-" * 80)

    for char in characters:
        print(" | ".join(str(field) for field in char))

    print(f"\nTotal: {len(characters)} character(s)")


def display_statistics(stats: List[Tuple], labels: List[str]) -> None:
    """
    Display statistics in a formatted table.

    Args:
        stats: List of statistic tuples
        labels: Column labels
    """
    print(" | ".join(labels))
    print("-" * 80)

    for row in stats:
        print(" | ".join(str(field) for field in row))


# ============================================
# Practice Exercise Solutions
# ============================================


def exercise1_count_characters(conn: sqlite3.Connection) -> int:
    """Exercise 1: Count total number of characters."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM characters")
    count = cursor.fetchone()[0]
    print(f"Total characters: {count}")
    return count


def exercise2_find_rebels(conn: sqlite3.Connection) -> List[Tuple]:
    """Exercise 2: Find all Rebel Alliance members."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, species, homeworld 
        FROM characters 
        WHERE affiliation = 'Rebel Alliance'
        ORDER BY name
    """
    )
    rebels = cursor.fetchall()
    print(f"Found {len(rebels)} Rebel Alliance members")
    return rebels


def exercise3_average_height_by_affiliation(conn: sqlite3.Connection) -> List[Tuple]:
    """Exercise 3: Calculate average height by affiliation."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            affiliation,
            ROUND(AVG(height), 2) as avg_height
        FROM characters
        WHERE height IS NOT NULL AND affiliation IS NOT NULL
        GROUP BY affiliation
        ORDER BY avg_height DESC
    """
    )
    results = cursor.fetchall()
    print("Average heights by affiliation:")
    for affiliation, avg_height in results:
        print(f"  {affiliation}: {avg_height}cm")
    return results


def exercise4_add_update_delete(conn: sqlite3.Connection) -> None:
    """Exercise 4: Complete CRUD cycle."""
    # Create
    char_id = add_character(conn, "Jyn Erso", "Human", "Vallt", 160, "Rebel Alliance")

    # Read
    character = get_character_by_name(conn, "Jyn Erso")
    print(f"Found character: {character}")

    # Update
    update_character_affiliation(conn, "Jyn Erso", "Rogue One Squadron")

    # Delete
    delete_character(conn, "Jyn Erso")


# ============================================
# Challenge Problem Solution
# ============================================


def challenge_character_report(conn: sqlite3.Connection, character_name: str) -> dict:
    """
    Create a complete report for a character including:
    - Basic info
    - Planet details
    - Vehicles
    - Species statistics

    Args:
        conn: Database connection
        character_name: Name of the character

    Returns:
        Dictionary containing all character information
    """
    cursor = conn.cursor()

    # Basic character info with planet
    cursor.execute(
        """
        SELECT 
            c.name, c.species, c.height, c.affiliation,
            p.name as planet_name, p.climate, p.terrain, p.population
        FROM characters c
        LEFT JOIN planets p ON c.planet_id = p.id
        WHERE c.name = ?
    """,
        (character_name,),
    )

    basic_info = cursor.fetchone()
    if not basic_info:
        return {"error": f"Character '{character_name}' not found"}

    # Character's vehicles
    cursor.execute(
        """
        SELECT v.name, v.model, v.vehicle_class, v.cost_in_credits
        FROM vehicles v
        INNER JOIN character_vehicles cv ON v.id = cv.vehicle_id
        INNER JOIN characters c ON cv.character_id = c.id
        WHERE c.name = ?
    """,
        (character_name,),
    )
    vehicles = cursor.fetchall()

    # Species statistics
    cursor.execute(
        """
        SELECT 
            COUNT(*) as species_count,
            AVG(height) as avg_height,
            MAX(height) as max_height,
            MIN(height) as min_height
        FROM characters
        WHERE species = ?
        AND height IS NOT NULL
    """,
        (basic_info[1],),
    )  # basic_info[1] is species
    species_stats = cursor.fetchone()

    # Build report
    report = {
        "name": basic_info[0],
        "species": basic_info[1],
        "height": basic_info[2],
        "affiliation": basic_info[3],
        "homeworld": {
            "name": basic_info[4],
            "climate": basic_info[5],
            "terrain": basic_info[6],
            "population": basic_info[7],
        },
        "vehicles": [
            {"name": v[0], "model": v[1], "class": v[2], "cost": v[3]} for v in vehicles
        ],
        "species_statistics": {
            "total_members": species_stats[0],
            "average_height": round(species_stats[1], 1) if species_stats[1] else None,
            "tallest": species_stats[2],
            "shortest": species_stats[3],
        },
    }

    return report


def print_character_report(report: dict) -> None:
    """Print the character report in a readable format."""
    if "error" in report:
        print(report["error"])
        return

    print("\n" + "=" * 60)
    print(f"CHARACTER REPORT: {report['name']}")
    print("=" * 60)

    print(f"\nSpecies: {report['species']}")
    print(f"Height: {report['height']}cm")
    print(f"Affiliation: {report['affiliation']}")

    print(f"\nHomeworld: {report['homeworld']['name']}")
    print(f"  Climate: {report['homeworld']['climate']}")
    print(f"  Terrain: {report['homeworld']['terrain']}")
    print(
        f"  Population: {report['homeworld']['population']:,}"
        if report["homeworld"]["population"]
        else "  Population: Unknown"
    )

    print(f"\nVehicles ({len(report['vehicles'])}):")
    if report["vehicles"]:
        for v in report["vehicles"]:
            print(f"  • {v['name']} ({v['class']}) - {v['cost']:,} credits")
    else:
        print("  None")

    print(f"\nSpecies Statistics ({report['species']}):")
    print(f"  Total members: {report['species_statistics']['total_members']}")
    print(f"  Average height: {report['species_statistics']['average_height']}cm")
    print(f"  Tallest: {report['species_statistics']['tallest']}cm")
    print(f"  Shortest: {report['species_statistics']['shortest']}cm")

    print("=" * 60 + "\n")


# ============================================
# Main Demonstration Function
# ============================================


def main():
    """Main function demonstrating all operations."""
    print("=" * 60)
    print("LESSON 9: Python and SQL Integration - Complete Solutions")
    print("=" * 60)

    # Connect to database
    conn = connect_to_database("database/starwars.db")

    try:
        # Part 1: Basic Queries
        print("\n--- Part 1: Basic Queries ---")
        all_chars = get_all_characters(conn)
        print(f"Total characters in database: {len(all_chars)}")

        luke = get_character_by_name(conn, "Luke Skywalker")
        print(f"Found Luke Skywalker: {luke[1] if luke else 'Not found'}")

        # Part 2: Filtered Queries
        print("\n--- Part 2: Filtered Queries ---")
        humans = get_characters_by_species(conn, "Human")
        print(f"Found {len(humans)} humans")

        tall_chars = get_tall_characters(conn, 180)
        print(f"Found {len(tall_chars)} characters taller than 180cm")

        # Part 3: Statistics
        print("\n--- Part 3: Species Statistics ---")
        stats = get_species_statistics(conn)
        display_statistics(stats, ["Species", "Count", "Avg Height"])

        # Part 4: Complex Queries
        print("\n--- Part 4: Characters with Planets ---")
        chars_planets = get_characters_with_planets(conn)
        for name, species, planet, climate in chars_planets[:5]:
            print(f"  {name} ({species}) from {planet} ({climate})")

        # Part 5: Challenge Report
        print("\n--- Part 5: Character Report ---")
        report = challenge_character_report(conn, "Luke Skywalker")
        print_character_report(report)

        print("\n✓ All demonstrations completed successfully!")

    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")

    finally:
        conn.close()
        print("\n✓ Database connection closed")


if __name__ == "__main__":
    main()
