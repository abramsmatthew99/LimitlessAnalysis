import sqlite3
import os

DATABASE_PATH = 'limitless_decks.db'


class Connection:
    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def _create_tables(self):
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS archetypes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                set_name TEXT NOT NULL,
                collection_number INTEGER NOT NULL,
                UNIQUE (name, set_name, collection_number)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY,
                player_id INTEGER NOT NULL,
                archetype_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (archetype_id) REFERENCES archetypes(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deck_cards (
                id INTEGER PRIMARY KEY,
                deck_id INTEGER NOT NULL,
                card_id INTEGER NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (deck_id) REFERENCES decks(id),
                FOREIGN KEY (card_id) REFERENCES cards(id)
            )
        ''')