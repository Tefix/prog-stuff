import sqlite3
import customtkinter as ctk
from tkinter import ttk

# Глобальные переменные
entries = {}
tree = None
search_entry = None

# --- DB Setup ---

def create_tables():
    queries = [
        """CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director_id INTEGER,
            release_year INTEGER,
            genre_id INTEGER,
            duration INTEGER,
            rating REAL,
            language_id INTEGER,
            country_id INTEGER,
            description TEXT,
            FOREIGN KEY (director_id) REFERENCES directors(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id),
            FOREIGN KEY (language_id) REFERENCES languages(id),
            FOREIGN KEY (country_id) REFERENCES countries(id)
        );"""
    ]
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        print("Kõik tabelid loodud.")
    except sqlite3.Error as e:
        print("Tabelite loomise viga:", e)
    finally:
        conn.close()

# --- Andmete lisamine abitabelitesse ---

def lisa_element(tabeli_nimi, silt):
    def salvesta():
        nimi = entry.get()
        if nimi:
            try:
                conn = sqlite3.connect("movies.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT OR IGNORE INTO {tabeli_nimi} (name) VALUES (?)", (nimi,))
                conn.commit()
                print(f"{silt} lisatud")
                top.destroy()
            except sqlite3.Error as e:
                print(f"Viga {silt.lower()} lisamisel:", e)
            finally:
                conn.close()
    top = ctk.CTkToplevel()
    top.title(f"Lisa {silt}")
    ctk.CTkLabel(top, text=f"{silt}:").pack(pady=5)
    entry = ctk.CTkEntry(top)
    entry.pack(pady=5)
    ctk.CTkButton(top, text="Salvesta", command=salvesta).pack(pady=10)

# --- Kasulikud funktsioonid ---

def saa_valikud(tabel):
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM {tabel}")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Viga valikute saamisel tabelist {tabel}:", e)
        return []
    finally:
        conn.close()

def saa_id(tabel, nimi):
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {tabel} WHERE name = ?", (nimi,))
        return cursor.fetchone()[0]
    except:
        return None
    finally:
        conn.close()

def clear_entries(entries):
    for entry in entries.values():
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, ctk.END)
        elif isinstance(entry, ttk.Combobox):
            entry.set("")

def validate_entries(entries):
    for key, entry in entries.items():
        if isinstance(entry, ctk.CTkEntry) and not entry.get():
            print(f"{key} ei saa olla tühi")
            return False
        if isinstance(entry, ttk.Combobox) and not entry.get():
            print(f"{key} tuleb valida")
            return False
    return True

def insert_movie(entries):
    if not validate_entries(entries):
        return
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        data = {
            'title': entries['title'].get(),
            'release_year': int(entries['release_year'].get()),
            'duration': int(entries['duration'].get()),
            'rating': float(entries['rating'].get()),
            'description': entries['description'].get(),
            'director_id': saa_id("directors", entries['director'].get()),
            'genre_id': saa_id("genres", entries['genre'].get()),
            'language_id': saa_id("languages", entries['language'].get()),
            'country_id': saa_id("countries", entries['country'].get())
        }

        cursor.execute("""
            INSERT INTO movies (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description)
            VALUES (:title, :director_id, :release_year, :genre_id, :duration, :rating, :language_id, :country_id, :description)
        """, data)
        conn.commit()
        print("Film lisatud")
        load_data_to_tree()
    except sqlite3.Error as e:
        print("Viga filmi lisamisel:", e)
    finally:
        conn.close()

def load_data_to_tree():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.title, d.name, m.release_year, g.name, m.duration, m.rating, l.name, c.name, m.description
            FROM movies m
            LEFT JOIN directors d ON m.director_id = d.id
            LEFT JOIN genres g ON m.genre_id = g.id
            LEFT JOIN languages l ON m.language_id = l.id
            LEFT JOIN countries c ON m.country_id = c.id
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    except sqlite3.Error as e:
        print("Viga andmete laadimisel:", e)
    finally:
        conn.close()

def search_movie():
    query = search_entry.get().lower().strip()
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.title, d.name, m.release_year, g.name, m.duration, m.rating, l.name, c.name, m.description
            FROM movies m
            LEFT JOIN directors d ON m.director_id = d.id
            LEFT JOIN genres g ON m.genre_id = g.id
            LEFT JOIN languages l ON m.language_id = l.id
            LEFT JOIN countries c ON m.country_id = c.id
        """)
        for row in cursor.fetchall():
            if query in row[0].lower():
                tree.insert("", "end", values=row)
    except sqlite3.Error as e:
        print("Viga otsingul:", e)
    finally:
        conn.close()

# --- GUI ---

def create_gui():
    global entries, tree, search_entry

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Filmide andmebaas")
    root.geometry("1000x800")

    ctk.CTkLabel(root, text="Filmide andmebaas", font=("Arial", 24)).pack(pady=20)

    form_frame = ctk.CTkFrame(root)
    form_frame.pack(pady=10)

    fields = [
        ("Pealkiri", "title"),
        ("Väljalaskeaasta", "release_year"),
        ("Kestus", "duration"),
        ("Hinne", "rating"),
        ("Kirjeldus", "description")
    ]

    entries = {}

    for i, (label, key) in enumerate(fields):
        ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(form_frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[key] = entry

    # Comboboxid
    combo_fields = [
        ("Režissöör", "director", "directors"),
        ("Žanr", "genre", "genres"),
        ("Keel", "language", "languages"),
        ("Riik", "country", "countries")
    ]

    for i, (label, key, table) in enumerate(combo_fields, start=len(fields)):
        ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        values = saa_valikud(table)
        combo = ttk.Combobox(form_frame, values=values, state="readonly")
        combo.grid(row=i, column=1, padx=10, pady=5)
        entries[key] = combo

    # Nupud
    ctk.CTkButton(root, text="Sisesta film", command=lambda: insert_movie(entries)).pack(pady=5)
    ctk.CTkButton(root, text="Tühjenda väljad", command=lambda: clear_entries(entries)).pack(pady=5)
    ctk.CTkButton(root, text="Loo tabelid", command=create_tables).pack(pady=5)

    # Lisa valikud
    lisa_frame = ctk.CTkFrame(root)
    lisa_frame.pack(pady=10)
    for nimi, tabel in [("Režissöör", "directors"), ("Žanr", "genres"), ("Keel", "languages"), ("Riik", "countries")]:
        ctk.CTkButton(lisa_frame, text=f"Lisa {nimi}", command=lambda t=tabel, n=nimi: lisa_element(t, n)).pack(side="left", padx=5)

    # Otsing
    otsing_frame = ctk.CTkFrame(root)
    otsing_frame.pack(pady=10)
    search_entry = ctk.CTkEntry(otsing_frame, placeholder_text="Otsi pealkirja järgi...")
    search_entry.pack(side="left", padx=10)
    ctk.CTkButton(otsing_frame, text="🔍 Otsi", command=search_movie).pack(side="left")

    # Treeview
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ["Pealkiri", "Režissöör", "Aasta", "Žanr", "Kestus", "Hinne", "Keel", "Riik", "Kirjeldus"]
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(fill="both", expand=True)

    load_data_to_tree()
    root.mainloop()

# --- Start ---
if __name__ == "__main__":
    create_gui()
