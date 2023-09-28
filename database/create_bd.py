import sqlite3 as sl

# TODO: у психологов в таблице указывать имя фото или путь до него
con = sl.connect('../resources/db/connection.db')
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
            number INTEGER NOT NULL, 
            is_done INTEGER NOT NULL DEFAULT(0)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Person(
            id INTEGER UNIQUE NOT NULL,
            date TEXT NOT NULL,
            url TEXT NOT NULL,
            name TEXT DEFAULT('-'),
            age TEXT DEFAULT('-'),
            city TEXT DEFAULT('-'),
            university TEXT DEFAULT('-'),
            problem TEXT DEFAULT('-'),
            promo_code TEXT DEFAULT('-'),
            get_guide INTEGER NOT NULL DEFAULT(0)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Psychologist(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name TEXT NOT NULL,
            about TEXT NOT NULL, 
            photo TEXT NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Transactions(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
            user_id INTEGER REFERENCES Person(id) NOT NULL, 
            date TEXT NOT NULL, time TEXT NOT NULL, 
            psy_id INTEGER REFERENCES Psychologist(id) NOT NULL,
            count_consults INTEGER NOT NULL,
            comment TEXT NOT NULL
        );
    """)
