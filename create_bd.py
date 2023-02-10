import sqlite3 as sl

# TODO: у психологов в таблице указывать имя фото или путь до него
con = sl.connect('db//connection.db')
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS CheckUp(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            user_id INTEGER REFERENCES Person(id) NOT NULL, 
            type_of_graph TEXT NOT NULL, 
            date TEXT NOT NULL, 
            score INTEGER NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE Consultation(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            tran_id INTEGER REFERENCES Transactions(id) NOT NULL, 
            slot_id INTEGER REFERENCES Slot(id), 
            is_done INTEGER NOT NULL DEFAULT(0)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Person(
            id INTEGER UNIQUE NOT NULL, 
            problems TEXT NOT NULL, 
            sub_id INTEGER NOT NULL DEFAULT(-1)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Psychologist(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name TEXT NOT NULL,
            problems TEXT NOT NULL, 
            about TEXT NOT NULL, 
            photo TEXT NOT NULL, 
            rating INTEGER NOT NULL DEFAULT(0)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Slot(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            psycho_id INTEGER REFERENCES Psychologist(id) NOT NULL, 
            date TEXT NOT NULL, 
            time TEXT NOT NULL, 
            is_free INTEGER DEFAULT(1) NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Subscription(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            user_id INTEGER REFERENCES Person(id) NOT NULL, 
            last_day TEXT NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Transactions(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            user_id INTEGER REFERENCES Person(id) NOT NULL, 
            date TEXT NOT NULL, time TEXT NOT NULL, 
            is_diagnostic NOT NULL DEFAULT (False)
        );
    """)
    #
    # con.execute("""
    #     CREATE TABLE PERSONS (
    #         id TEXT,
    #         problems TEXT,
    #         time_for_check_up TEXT,
    #         last_check_up TEXT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE COMMENTS (
    #         id TEXT,
    #         day DATE,
    #         comment TEXT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE MOOD (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE ANXIETY (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE PROCRASTINATION (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE LONELINESS (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE DOUBT (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    # con.execute("""
    #     CREATE TABLE CONDEMNING (
    #         id TEXT,
    #         monday INT,
    #         tuesday INT,
    #         wednesday INT,
    #         thursday INT,
    #         friday INT,
    #         saturday INT,
    #         sunday INT
    #     );
    #     """)
    #
    #