-- schema.sql
-- This file defines the schema for interactive story

-- Table to store registered users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);

-- Table for books
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);

-- Table for chapters per book
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    chapter_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    is_dynamic BOOLEAN DEFAULT 0,
    FOREIGN KEY(book_id) REFERENCES books(id)
);

-- Table to track the current story state of a user
CREATE TABLE IF NOT EXISTS user_story_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    current_chapter_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(current_chapter_id) REFERENCES chapters(id)
);

-- Table for choices within a chapter
CREATE TABLE IF NOT EXISTS chapter_choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    choice_text TEXT NOT NULL,
    leads_to_chapter_id INTEGER NOT NULL,
    FOREIGN KEY(chapter_id) REFERENCES chapters(id),
    FOREIGN KEY(leads_to_chapter_id) REFERENCES chapters(id)
);
