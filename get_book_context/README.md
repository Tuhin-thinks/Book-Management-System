## Branch: OPERATIONS
_____

This branch deals with "experimentation" level coding.

* **20-05-2021**: Currently creating the DB structure for booknames storing and indexing with keywords.

[config.py](Database/config.py) stores the database credentials.
    
    username = "postgres username"
    password = "your postgresql password"

* Currently this system is being built using postgres, but this is very easy to switch to any other database. As I am using SQLAlchemy as the ORM for the database.

**Pending works:**

- Extracting book context/subject from the book title.
- Using NLP to complete word tokens from book titles and make better sense of book titles.
- Index book titles with keywords, for better searching facility.
- Google API call to get's other book's details.
- search using ISBN of book.

*Future work includes, book downloading option*
