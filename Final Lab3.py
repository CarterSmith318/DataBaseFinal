import pyodbc
import csv

# Set up connection parameters
server = 'DESKTOP-UABTB2M'
database = 'master'
trusted_connection = True

# Connect to SQL Server instance and create database
conn = pyodbc.connect(f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};Trusted_Connection=yes;autocommit=True;")
cursor = conn.cursor()
try:
    cursor.execute(f"CREATE DATABASE Library")
except pyodbc.ProgrammingError as err:
    print(err)
else:
    print(f"Database Library created successfully")

# Connect to newly created database
conn = pyodbc.connect(f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database=Library;Trusted_Connection=yes;")
c('28000', '[28000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Login failed for user \'DESKTOP-UABTB2M\\carte\'. (18456) (SQLDriverConnect); [28000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Cannot open database "Library" requested by the login. The login failed. (4060); [28000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Login failed for user \'DESKTOP-UABTB2M\\carte\'. (18456); [28000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Cannot open database "Library" requested by the login. The login failed. (4060)')
ursor = conn.cursor()

# Create tables with columns and constraints
cursor.execute('''
    CREATE TABLE Book (
        ISBN VARCHAR(20) PRIMARY KEY,
        Title VARCHAR(100) NOT NULL,
        PubDate DATE NOT NULL,
        Copies INT NOT NULL,
        AuthorID INT NOT NULL FOREIGN KEY REFERENCES Author(AuthorID),
        PubID INT NOT NULL FOREIGN KEY REFERENCES Pub(PubID),
        LocID INT NOT NULL FOREIGN KEY REFERENCES Location(LocID)
    );
''')

cursor.execute('''
    CREATE TABLE Author (
        AuthorID INT PRIMARY KEY,
        Name VARCHAR(100) NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE Pub (
        PubID INT PRIMARY KEY,
        PubName VARCHAR(100) NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE Location (
        LocID INT PRIMARY KEY,
        Locations VARCHAR(100) NOT NULL,
        Shelf VARCHAR(20) NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE BookUser (
        BorrowerID INT PRIMARY KEY,
        BName VARCHAR(100) NOT NULL,
        ISBN VARCHAR(20) NOT NULL FOREIGN KEY REFERENCES Book(ISBN)
    );
''')

cursor.commit()

# Load data from CSV file into Book and Author tables
filename = "Final_LibraryBookData.csv"
with open(filename, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert data into Author table
        cursor.execute("INSERT INTO Author (AuthorID, Name) VALUES (?, ?);", (row["AuthorID"], row["AuthorName"]))
        conn.commit()

        # Insert data into Book table
        cursor.execute("INSERT INTO Book (ISBN, Title, PubDate, Copies, AuthorID, PubID, LocID) VALUES (?, ?, ?, ?, ?, ?, ?);", 
                       (row["ISBN"], row["Title"], row["PubDate"], row["Copies"], row["AuthorID"], row["PubID"], row["LocID"]))
        conn.commit()

# Close database connection
conn.close()
