# Lesson 10 Solution: Database Technology Comparison

## Your Name: [Solution Template]

## Date: [Current Date]

---

## Part 1: SQL Analysis

### What is SQL?

SQL (Structured Query Language) is a standardised programming language specifically designed for managing and manipulating relational databases. It allows users to create, read, update, and delete data stored in tables with defined relationships.

### Advantages of SQL Databases

1. **Data Integrity**: Strong ACID properties (Atomicity, Consistency, Isolation, Durability) ensure reliable transactions
2. **Structured Data**: Fixed schema enforces data consistency and validation
3. **Complex Queries**: Powerful JOIN operations and aggregate functions for sophisticated analysis
4. **Relationships**: Foreign keys maintain referential integrity between related tables
5. **Mature Technology**: Decades of development, extensive tooling, and large community
6. **Standardisation**: SQL is standardised across many database systems (with some variations)
7. **Transaction Support**: Built-in support for multi-step operations that must complete together

### Disadvantages of SQL Databases

1. **Rigid Schema**: Changing table structure can be difficult and require migrations
2. **Scaling Challenges**: Horizontal scaling (adding more servers) is more complex than vertical scaling
3. **Fixed Structure**: Not ideal for semi-structured or unstructured data
4. **Performance**: JOIN operations on very large datasets can be slow
5. **Learning Curve**: Requires learning SQL syntax and understanding relational concepts

### Best Use Cases for SQL

- **Banking Systems**: Financial transactions requiring ACID compliance
- **E-commerce**: Product catalogues with complex relationships (orders, customers, inventory)
- **Student Information Systems**: Structured data with many relationships (students, courses, enrolments)
- **Healthcare Records**: Patient data with strict consistency and integrity requirements
- **Any Application Requiring**: Complex queries, transactions, and referential integrity

---

## Part 2: ORM (Object-Relational Mapping) Analysis

### What is an ORM?

An ORM (Object-Relational Mapping) is a programming technique that creates a "bridge" between object-oriented programming languages (like Python) and relational databases. It allows developers to interact with databases using objects and methods in their programming language rather than writing raw SQL queries.

### How ORMs Work

ORMs translate Python code into SQL queries automatically:

- Python classes represent database tables
- Class instances represent table rows
- Class attributes represent table columns
- Methods handle CRUD operations transparently

Example:

```python
# ORM Code (SQLAlchemy)
character = Character(name="Luke Skywalker", species="Human")
session.add(character)
session.commit()

# Translates to SQL:
# INSERT INTO characters (name, species) VALUES ('Luke Skywalker', 'Human');
```

### Advantages of ORMs

1. **Language Integration**: Write database code in your programming language (Python, not SQL)
2. **Abstraction**: Don't need to know SQL syntax in detail
3. **Database Independence**: Can switch database systems with minimal code changes
4. **Reduced Boilerplate**: Less repetitive code for common operations
5. **Security**: Built-in protection against SQL injection attacks
6. **Type Safety**: Programming language's type system helps catch errors
7. **Developer Productivity**: Faster development for standard CRUD operations

### Disadvantages of ORMs

1. **Performance Overhead**: Generated SQL may not be optimally efficient
2. **Complexity**: Learning curve for the ORM framework itself
3. **Limited Control**: Complex queries may be difficult or impossible to express
4. **N+1 Problem**: Can generate excessive database queries if not careful
5. **Debugging**: Harder to see and optimise the actual SQL being executed
6. **Abstraction Leaks**: Sometimes you still need to know SQL for complex operations

### When to Use ORMs

- **Rapid Development**: When development speed is more important than query optimisation
- **Standard CRUD**: Applications with mostly simple create, read, update, delete operations
- **Team Experience**: When team is more comfortable with programming than SQL
- **Database Portability**: When you might switch database systems
- **Modern Web Frameworks**: Django, Flask, Ruby on Rails all include ORMs

### When to Use Raw SQL

- **Complex Queries**: Sophisticated JOINs, subqueries, and aggregate operations
- **Performance Critical**: When every millisecond counts
- **Database-Specific Features**: Using unique features of your database system
- **Reporting**: Complex analytical queries and data aggregation
- **Learning**: When learning database concepts and SQL skills

---

## Part 2.5: Hands-On Comparison Activities

### Practical Code Examples: SQL vs ORM vs NoSQL

Below are practical examples showing the same operations in all three approaches. In the Jupyter notebook version, you can run these examples yourself!

#### Activity 1: Get All Characters

**SQL Approach:**

```python
import sqlite3

conn = sqlite3.connect('database/starwars.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT name, species FROM characters LIMIT 5")
results = cursor.fetchall()

for row in results:
    print(f"{row['name']} - {row['species']}")

conn.close()
```

**ORM Approach (Peewee):**

```python
from peewee import *

db = SqliteDatabase('database/starwars.db')

class Character(Model):
    name = CharField()
    species = CharField()
    homeworld = CharField()
    height = IntegerField(null=True)

    class Meta:
        database = db
        table_name = 'characters'

characters = Character.select().limit(5)

for char in characters:
    print(f"{char.name} - {char.species}")
```

**NoSQL Equivalent (MongoDB):**

```javascript
// MongoDB query:
db.characters.find({}, { name: 1, species: 1, _id: 0 }).limit(5);

// Results would be JSON documents:
// {"name": "Luke Skywalker", "species": "Human"}
// {"name": "Leia Organa", "species": "Human"}
```

**Key Observations:**

- **SQL:** Requires connection management, explicit query string
- **ORM:** More Pythonic, objects instead of dictionaries
- **NoSQL:** Data stored as documents (JSON-like), query syntax varies by database

---

#### Activity 2: Filter Characters (WHERE clause)

**SQL Approach:**

```python
cursor.execute("""
    SELECT name, homeworld
    FROM characters
    WHERE species = 'Human'
""")
results = cursor.fetchall()
```

**ORM Approach:**

```python
humans = Character.select().where(Character.species == 'Human')

for human in humans:
    print(f"{human.name} from {human.homeworld}")
```

**NoSQL Equivalent:**

```javascript
db.characters.find({ species: "Human" }, { name: 1, homeworld: 1, _id: 0 });
```

**Key Observations:**

- **SQL:** String-based WHERE clause with quotes
- **ORM:** Python expressions (`Character.species == 'Human'`) - more intuitive!
- **NoSQL:** JSON-based query syntax

---

#### Activity 3: Sorting (ORDER BY)

**SQL Approach:**

```python
cursor.execute("""
    SELECT name, height
    FROM characters
    WHERE height IS NOT NULL
    ORDER BY height DESC
    LIMIT 5
""")
```

**ORM Approach:**

```python
tallest = (Character
           .select()
           .where(Character.height.is_null(False))
           .order_by(Character.height.desc())
           .limit(5))
```

**NoSQL Equivalent:**

```javascript
db.characters
  .find({ height: { $ne: null } }, { name: 1, height: 1, _id: 0 })
  .sort({ height: -1 })
  .limit(5);
```

**Key Observations:**

- **SQL:** `ORDER BY height DESC` - standard SQL syntax
- **ORM:** `.order_by(Character.height.desc())` - method chaining, very readable
- **NoSQL:** `.sort({"height": -1})` - JSON-based sorting (-1 = descending)

---

#### Activity 4: Aggregation (COUNT, AVG)

**SQL Approach:**

```python
cursor.execute("""
    SELECT species,
           COUNT(*) as count,
           AVG(height) as avg_height
    FROM characters
    WHERE height IS NOT NULL
    GROUP BY species
    ORDER BY count DESC
""")
```

**ORM Approach:**

```python
from peewee import fn

stats = (Character
         .select(Character.species,
                 fn.COUNT(Character.id).alias('count'),
                 fn.AVG(Character.height).alias('avg_height'))
         .where(Character.height.is_null(False))
         .group_by(Character.species)
         .order_by(fn.COUNT(Character.id).desc()))
```

**NoSQL Equivalent:**

```javascript
db.characters.aggregate([
  {
    $match: { height: { $ne: null } },
  },
  {
    $group: {
      _id: "$species",
      count: { $sum: 1 },
      avg_height: { $avg: "$height" },
    },
  },
  {
    $sort: { count: -1 },
  },
]);
```

**Key Observations:**

- **SQL:** `GROUP BY` with aggregate functions (`COUNT`, `AVG`)
- **ORM:** `fn.COUNT()`, `fn.AVG()` - Python functions wrapping SQL functions
- **NoSQL:** Aggregation pipeline (series of stages) instead of single query

---

#### Activity 5: Insert New Record

**SQL Approach:**

```python
cursor.execute("""
    INSERT INTO characters (name, species, homeworld, height)
    VALUES (?, ?, ?, ?)
""", ("Ahsoka Tano", "Togruta", "Shili", 170))

conn.commit()
print(f"Inserted character with ID: {cursor.lastrowid}")
```

**ORM Approach:**

```python
new_char = Character.create(
    name="Mace Windu",
    species="Human",
    homeworld="Haruun Kal",
    height=188
)
print(f"Created character object with ID: {new_char.id}")
```

**NoSQL Equivalent:**

```javascript
db.characters.insertOne({
  name: "Ahsoka Tano",
  species: "Togruta",
  homeworld: "Shili",
  height: 170,
  weapons: ["dual lightsabers"], // Can add fields freely!
  master: "Anakin Skywalker", // No schema restrictions
});
```

**Key Observations:**

- **SQL:** Parameterised INSERT with `?` placeholders, must `commit()`
- **ORM:** `.create()` method - like creating a Python object, auto-saves
- **NoSQL:** Flexible schema - can add any fields without pre-defining them!

---

#### Activity 6: Update Record

**SQL Approach:**

```python
cursor.execute("""
    UPDATE characters
    SET height = ?
    WHERE name = ?
""", (168, "Ahsoka Tano"))

conn.commit()
```

**ORM Approach:**

```python
# Fetch, modify, save
ahsoka = Character.get(Character.name == "Ahsoka Tano")
ahsoka.height = 168
ahsoka.save()

# Or bulk update
updated_count = (Character
                 .update(height=188)
                 .where(Character.name == "Mace Windu")
                 .execute())
```

**NoSQL Equivalent:**

```javascript
db.characters.updateOne({ name: "Ahsoka Tano" }, { $set: { height: 168 } });

// Or update multiple:
db.characters.updateMany(
  { species: "Human" },
  { $set: { category: "humanoid" } }
);
```

**Key Observations:**

- **SQL:** `UPDATE ... SET ... WHERE` - explicit SQL command
- **ORM:** Two ways: fetch+modify+save (object-oriented) or bulk update (SQL-like)
- **NoSQL:** `$set` operator - MongoDB's update syntax uses operators

---

#### Activity 7: Delete Record

**SQL Approach:**

```python
cursor.execute("""
    DELETE FROM characters
    WHERE name IN ('Ahsoka Tano', 'Mace Windu')
""")

conn.commit()
```

**ORM Approach:**

```python
deleted_count = (Character
                 .delete()
                 .where(Character.name.in_(['Ahsoka Tano', 'Mace Windu']))
                 .execute())
```

**NoSQL Equivalent:**

```javascript
db.characters.deleteOne({ name: "Ahsoka Tano" });

// Or delete multiple:
db.characters.deleteMany({ name: { $in: ["Ahsoka Tano", "Mace Windu"] } });
```

**Key Observations:**

- **SQL:** `DELETE FROM ... WHERE` - must specify WHERE (or delete all!)
- **ORM:** `.delete().where()` - method chaining, safer (harder to forget WHERE)
- **NoSQL:** Explicit `deleteOne()` vs `deleteMany()` - prevents accidental mass deletions

---

### Code Comparison Summary Table

| Operation     | SQL                        | ORM                                | NoSQL                         |
| ------------- | -------------------------- | ---------------------------------- | ----------------------------- |
| **Query all** | `SELECT * FROM ...`        | `Model.select()`                   | `db.collection.find()`        |
| **Filter**    | `WHERE species = 'Human'`  | `.where(Model.species == 'Human')` | `{"species": "Human"}`        |
| **Sort**      | `ORDER BY height DESC`     | `.order_by(Model.height.desc())`   | `.sort({"height": -1})`       |
| **Limit**     | `LIMIT 5`                  | `.limit(5)`                        | `.limit(5)`                   |
| **Aggregate** | `COUNT(*), AVG(height)`    | `fn.COUNT(), fn.AVG()`             | Aggregation pipeline          |
| **Insert**    | `INSERT INTO ... VALUES`   | `Model.create()`                   | `insertOne({...})`            |
| **Update**    | `UPDATE ... SET ... WHERE` | `.update().where()`                | `updateOne({}, {"$set": {}})` |
| **Delete**    | `DELETE FROM ... WHERE`    | `.delete().where()`                | `deleteOne({})`               |

---

## Part 3: NoSQL Databases

### What is NoSQL?

NoSQL (Not Only SQL) databases are non-relational databases designed for flexible, scalable storage of diverse data types. Unlike SQL databases with fixed schemas and tables, NoSQL databases use various data models like documents, key-value pairs, graphs, or wide-column stores.

### Common Types of NoSQL Databases

1. **Document Stores** (MongoDB, CouchDB): Store data as JSON-like documents
2. **Key-Value Stores** (Redis, DynamoDB): Simple key-value pairs
3. **Column-Family Stores** (Cassandra, HBase): Column-oriented storage
4. **Graph Databases** (Neo4j): Store nodes and relationships

### Advantages of NoSQL

1. **Flexible Schema**: Can store different structures in the same collection
2. **Horizontal Scaling**: Easily add more servers to handle increased load
3. **High Performance**: Optimised for specific data access patterns
4. **Unstructured Data**: Better for JSON, XML, binary data
5. **Cloud-Native**: Designed for distributed systems
6. **Developer-Friendly**: JSON/document format matches application objects

### Disadvantages of NoSQL

1. **Eventual Consistency**: May not have immediate consistency across all nodes
2. **Limited Relationships**: JOIN operations are not built-in or efficient
3. **Less Mature**: Fewer tools, standards, and experienced developers
4. **Query Limitations**: Cannot easily perform complex analytical queries
5. **Data Duplication**: Often requires storing redundant data
6. **No Standard Language**: Each system has its own query language

### SQL vs NoSQL Comparison

| Aspect           | SQL                       | NoSQL                             |
| ---------------- | ------------------------- | --------------------------------- |
| **Schema**       | Fixed, predefined         | Flexible, dynamic                 |
| **Scaling**      | Vertical (bigger servers) | Horizontal (more servers)         |
| **Data Model**   | Tables with relationships | Documents, key-value, graphs      |
| **Transactions** | Full ACID support         | Often eventual consistency        |
| **Queries**      | Complex SQL queries       | Simpler, specific access patterns |
| **Best For**     | Structured, related data  | Unstructured, high-volume data    |
| **Examples**     | PostgreSQL, MySQL, SQLite | MongoDB, Redis, Cassandra         |

### Best Use Cases for NoSQL

- **Social Media**: User profiles, posts, comments with varying structures
- **Real-Time Analytics**: High-volume data ingestion and analysis
- **Content Management**: Articles, media with different attributes
- **IoT Applications**: Sensor data from millions of devices
- **Gaming**: Player profiles, game states, leaderboards
- **Caching**: Temporary storage of frequently accessed data

---

## Part 4: Choosing the Right Technology

### Decision Framework

**Choose SQL when you need:**

- ✓ Complex relationships between data entities
- ✓ Strong consistency guarantees (ACID)
- ✓ Complex queries and reporting
- ✓ Structured data with a stable schema
- ✓ Financial or critical data requiring integrity

**Choose NoSQL when you need:**

- ✓ Flexible, evolving data structures
- ✓ Massive scale (millions of reads/writes per second)
- ✓ Simple data access patterns
- ✓ High availability over consistency
- ✓ Rapid development with changing requirements

**Choose an ORM when:**

- ✓ Using SQL but want productivity benefits
- ✓ Team is more comfortable with programming than SQL
- ✓ Application has standard CRUD operations
- ✓ Database portability is important

**Use Raw SQL when:**

- ✓ Performance is critical
- ✓ Complex analytical queries are needed
- ✓ Learning database concepts
- ✓ Fine-tuned control over queries

---

## Part 5: Real-World Example Analysis

### Example 1: Online Shop

**Requirements:**

- Product catalogue with categories
- Customer accounts and order history
- Inventory management
- Payment processing

**Recommendation:** **SQL Database (PostgreSQL or MySQL)**

**Reasoning:**

- Strong relationships: orders → customers, orders → products, products → categories
- Transactions critical: payments must be ACID-compliant
- Complex queries needed: sales reports, inventory across warehouses
- Fixed data structure: products, customers, orders are well-defined
- Data integrity essential: can't have orders without valid products

**Would use ORM:** Yes, for application development (Django ORM, SQLAlchemy)  
**Would use raw SQL:** Yes, for complex reporting and analytics

---

### Example 2: Social Media Platform

**Requirements:**

- User profiles with varying attributes
- Posts, comments, likes (high volume)
- Real-time feeds
- Millions of users

**Recommendation:** **Hybrid Approach - NoSQL + SQL**

**Reasoning:**

- User profiles: NoSQL (MongoDB) - flexible schema for varying profile data
- Activity feeds: NoSQL (Redis) - fast caching and real-time updates
- Relationships: SQL (PostgreSQL) - friend connections, follow relationships
- Analytics: SQL - user engagement metrics and reporting

This demonstrates that real applications often combine multiple database technologies, choosing each for its strengths.

---

### Example 3: Star Wars Database (Our Project)

**Requirements:**

- Characters, planets, vehicles with relationships
- Fixed data structure
- Learning environment
- Complex queries for analysis

**Recommendation:** **SQL Database (SQLite)**

**Reasoning:**

- Educational context: learning SQL fundamentals
- Clear relationships: characters ↔ planets, characters ↔ vehicles
- Fixed schema: well-defined data structure
- Complex queries: practice JOINs, subqueries, aggregates
- Simple setup: SQLite requires no server
- Small dataset: doesn't need NoSQL scaling

**Would NOT use NoSQL because:**

- Data is highly structured and relational
- Need to practise SQL skills
- Complex queries are the learning objective
- No scaling requirements

---

## Part 6: Reflection Questions

### 1. When would you choose a NoSQL database over SQL?

I would choose NoSQL when:

- Data structure is undefined or changes frequently (e.g., user-generated content)
- Application requires massive horizontal scaling
- Data is naturally document-oriented (e.g., JSON from APIs)
- High availability is more important than immediate consistency
- Access patterns are simple and predictable

Example: Building a mobile app backend that stores JSON user profiles with different attributes per user type, requiring millions of reads/writes per second.

### 2. What are the main benefits of using an ORM?

Main benefits:

- **Productivity**: Write less code for common database operations
- **Maintainability**: Changes to database structure reflected in code
- **Security**: Automatic protection against SQL injection
- **Portability**: Switch databases with minimal code changes
- **Type Safety**: Catch errors at compile time rather than runtime
- **Integration**: Work with objects that match your application logic

The biggest benefit is developer productivity - you can build applications faster by working in your programming language instead of constantly switching between Python and SQL.

### 3. Would you use SQL or NoSQL for a banking application? Why?

**Definitely SQL** for a banking application.

Reasons:

1. **ACID Transactions**: Financial transactions must be atomic (all-or-nothing)
2. **Data Integrity**: Cannot have inconsistent balances or invalid references
3. **Relationships**: Accounts, customers, transactions, branches are all related
4. **Auditability**: Need complex queries to track all transactions
5. **Consistency**: Must have immediate consistency across all operations
6. **Regulatory Compliance**: Banking regulations require data integrity guarantees

Banking is the classic use case where SQL's strengths (consistency, integrity, transactions) are absolutely essential. The eventual consistency model of many NoSQL databases would be unacceptable for financial data.

---

## Part 7: Your Own Example

### Application: School Library Management System

**Requirements:**

- Book catalogue with multiple copies
- Student borrowing records
- Librarian accounts
- Fines and payment tracking
- Book reservations
- Reading history reports

**Technology Choice:** SQL Database (PostgreSQL) with ORM (SQLAlchemy)

**Reasoning:**

**Why SQL:**

1. **Clear relationships**: Students borrow books, books have authors, loans have fines
2. **Data integrity**: Can't have a loan without a valid student and book
3. **Transactions**: Borrowing process involves multiple steps (check availability, create loan, update inventory)
4. **Complex queries**: Reports like "most popular books" or "students with overdue books" require JOINs and aggregates
5. **Fixed schema**: Library data structure is stable and well-defined

**Why Use an ORM:**

1. **Development speed**: Librarian portal needs standard CRUD for books, students
2. **Team skill**: School developers more comfortable with Python than SQL
3. **Security**: Built-in protection for student data access
4. **Web framework**: Would use Flask/Django which include ORMs

**When to use raw SQL:**

- Monthly reports: "Books borrowed per category"
- Analytics: "Peak borrowing times"
- Data exports: Generate CSV files for archives
- Performance-critical searches: Book availability checking

**Why NOT NoSQL:**

- Data is highly structured with many relationships
- Referential integrity is crucial (can't have loan for non-existent book)
- Need complex reporting queries
- Dataset size doesn't require NoSQL scaling
- Consistency is more important than eventual consistency

**Database Schema (simplified):**

```
students (id, name, class, email)
books (id, title, isbn, category)
book_copies (id, book_id, location, status)
loans (id, student_id, copy_id, borrow_date, due_date, return_date)
fines (id, loan_id, amount, paid)
```

This demonstrates SQL's strength: clearly defined relationships with referential integrity ensuring the system remains consistent.

---

## Conclusion

**Key Learnings:**

1. SQL excels at structured data with complex relationships
2. NoSQL excels at flexible schemas and massive scale
3. ORMs improve productivity but sacrifice some control
4. Real applications often use multiple database technologies
5. Choose based on your specific requirements, not trends

**Personal Reflection:**
Throughout this course, working with SQL has shown me how powerful relational databases are for structured data. The ability to JOIN tables, use aggregate functions, and ensure data integrity makes SQL ideal for many applications. While NoSQL has its place for specific use cases like social media or IoT, SQL remains essential for understanding data relationships and building reliable systems.

The Star Wars database project demonstrated that even simple applications benefit from SQL's structure - being able to query "characters with vehicles from Incom Corporation on temperate planets" shows the power of relational thinking.

For future projects, I would:

- Start with SQL for most applications with structured data
- Use an ORM for rapid development of standard features
- Write raw SQL for complex analytical queries
- Consider NoSQL only when scaling or schema flexibility truly requires it
- Always prioritise data integrity and consistency for critical systems

---

**Completed by:** [Student Name]  
**Date:** [Submission Date]  
**Time Spent:** [e.g., 30 minutes]
