## Branch: OPERATIONS
_____

This branch deals with "experimentation" level coding.

* **20-05-2021**: Currently creating the DB structure for book-names storing and indexing with keywords.

* Currently, this system is being built using postgres, but this is very easy to switch to any other database. As I am using SQLAlchemy as the ORM for the database.
* **23-06-2022**: Added loading configuration from yaml file using config.yaml
    - Bug fixes while exiting program loop using `over` command.
```yaml
db-credentials:
  db-user: "username"
  db-password: "password"
```

**Pending works:**

- Extracting book context/subject from the book title.
- Using `NLP` to complete word tokens from book titles and make better sense of book titles.
- Index book titles with keywords, for better searching facility.
- Google API call to get other book's details.
- search using `ISBN` of book.

*Future work includes, book downloading option*
