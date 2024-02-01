import sqlite3
import json
import tkinter as tk
from tkinter import ttk, Frame, Label, Entry
from ttkthemes import ThemedTk, ThemedStyle

# funkcja do łączenia  się z bazą sql
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

#funkcja do tworzenia tabeli w bazie danych z wykorzystaniem sqlite
def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
                     (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn TEXT)''')
    except sqlite3.Error as e:
        print(e)

#funkcja do wyczyszczenia tabeli z wykorzystaniem sqlite
def clear_table(conn):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM books")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

#funkcja dodająca rekord do tabeli z wykorzystaniem sqlite
def insert_book(conn, title, author, year, isbn):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                  (title, author, year, isbn))
        conn.commit()

    except sqlite3.Error as e:
        print(e)

#funkcja usuwająca rekord z tabeli z wykorzystaniem sqlite
def delete_book(conn, book_id):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

#funcja do wyszukiwania po dowolnym z pól z wykorzystaniem sqlite
def search_books(conn, keyword):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ? OR isbn LIKE ?", ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        return c.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []

#funkcja do wyświetlania książek
def list_books(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        return c.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []

#eksportowanie danych z tabeli do jsona
def export_to_json(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        with open('books.json', 'w') as f:
            json.dump([{'id': book[0], 'title': book[1], 'author': book[2], 'year': book[3],'isbn': book[4]} for book in books], f, indent=4)
    except sqlite3.Error as e:
        print(e)


#funkcja do importu danych z .json do tabeli
def import_from_json(conn, filepath):
        try:
            with open(filepath, 'r') as f:
                books = json.load(f)
                for book in books:
                    insert_book(conn, book['title'], book['author'], book['year'], book['isbn'])
        except sqlite3.Error as e:
            print(e)
        except FileNotFoundError:
            print("ERROR json file not found")
#klasa aplikacji
class BooksApp:
    def __init__(self, root):
        self.conn = create_connection("books.db") #łączenie się z baza sql
        if self.conn is not None:
            create_table(self.conn) #tworzenie tabeli, jesli nie istnieje
            clear_table(self.conn) #wyczyszczenie jej
            import_from_json(self.conn,'books.json') #import do tabeli danych z json

        self.root = root
        self.root.title("My books")

        # ustawienie stylu ttkthemes
        self.style = ThemedStyle(root)
        self.style.theme_use("black")

        #dostosowanie wyglądu przycisków
        self.style.configure('TButton', background='navy', foreground='white')

        #stworzenie górnej ramki dla przycików
        top_frame = Frame(root)
        top_frame.pack(side="top")

        # tworzenie przycisków funkcujnych z wykorzystaniem ttk.Button i TButton, i przypisanie im odpowienich funkcji
        ttk.Button(top_frame, text="Insert Book", command=lambda: self.show_frame("insert")).pack(side="left")
        ttk.Button(top_frame, text="Search Books", command=lambda: self.show_frame("search")).pack(side="left")
        ttk.Button(top_frame, text="Delete Book", command=self.delete_book).pack(side="left")
        ttk.Button(top_frame, text="Quit", command=self.quit_app).pack(side="left")

        # tworzenie ramek dla insert i serach
        self.insert_frame = self.create_insert_frame()
        self.search_frame = self.create_search_frame()

        #ustawianie stylu dla elementu Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)  # Adjust row height
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # tworzenie kolumn z Treeview
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year", "ISBN"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Title", width=150, anchor='center')
        self.tree.column("Author", width=150, anchor='center')
        self.tree.column("Year", width=100, anchor='center')
        self.tree.column("ISBN", width=150, anchor='center')
        self.tree.pack(fill="both", expand=True)

        self.list_books()



    #ramka z polami do wstawiania nowej pozycji
    def create_insert_frame(self):
        frame = Frame(self.root)
        Label(frame, text="Title").grid(row=0, column=0)
        self.title_entry = ttk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        Label(frame, text="Author").grid(row=1, column=0)
        self.author_entry = ttk.Entry(frame)
        self.author_entry.grid(row=1, column=1)

        Label(frame, text="Year").grid(row=2, column=0)
        self.year_entry = ttk.Entry(frame)
        self.year_entry.grid(row=2, column=1)

        Label(frame, text="ISBN").grid(row=3, column=0)
        self.isbn_entry = ttk.Entry(frame)
        self.isbn_entry.grid(row=3, column=1)

        ttk.Button(frame, text="Insert", command=self.insert_book).grid(row=4, column=0, columnspan=2)
        return frame
   #ramka z elementami do wyszukiwania krotek
    def create_search_frame(self):
        frame = Frame(self.root)
        self.search_entry = ttk.Entry(frame)
        self.search_entry.grid(row=0, column=1)
        ttk.Button(frame, text="Search", command=self.search_books, style='TButton').grid(row=1, column=0, columnspan=2)

        return frame
    #ta funkcja służy do warunkowego wyświetlania pól do wyszukiwania i i wprowadzania, w azleżnośći od wciśniętego przycisku
    def show_frame(self, action):
        self.list_books()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        if action == "insert":
            self.insert_frame.pack()
        elif action == "search":
            self.search_frame.pack()
    #wprowadznie książki (zczytywanie z pól do w prowadzania danych)
    def insert_book(self):
        insert_book(self.conn, self.title_entry.get(), self.author_entry.get(), self.year_entry.get(),
                    self.isbn_entry.get())
        self.list_books()
        self.export_to_json()
        self.clear_entries()
    #usuwanie ksiązki, którą zaznaczymy
    def delete_book(self):
        selected_item = self.tree.selection()  # pobiera zaznaczenie z Treeview
        if selected_item:
            book_id = self.tree.item(selected_item[0])['values'][
                0]  #pobiera ID książki z pierwszej kolumny zaznaczonego wiersza
            try:
                delete_book(self.conn, book_id)  # usuwa książkę z bazy danych
                self.list_books()
                self.export_to_json()
            except sqlite3.Error as e:
                print(e)
        else:
            print("nie zaznaczono książki do usunięcia")
            #
    def search_books(self):
        keyword = self.search_entry.get()
        results = search_books(self.conn, keyword)
        self.show_results(results)
# funkcja pommocnicza do exportownaia danych z bazy do json
    def export_to_json(self):
        export_to_json(self.conn)
#zamknięcie okienka
    def quit_app(self):
        self.conn.close()
        self.root.quit()
    #funkcja pomocnicza wyśiwtlająca wszytkie elmenty w tabeli
    def list_books(self):
        books = list_books(self.conn)
        self.show_results(books)
 #wyswitelnie bazy ksiazek z zadanym parametrem
    def show_results(self, results):
        self.tree.delete(*self.tree.get_children())
        for book in results:
            self.tree.insert('', 'end', values=book)
#wyczyszczenie pól do wprowadzania po zatwierdzeniu
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)


if __name__ == '__main__':
    #nicjalizacja głównego okna aplikacji Tkinter
    root = tk.Tk()
    root.geometry('600x400')
    # inicjalizacja aplikacji książek i przekazanie głównego okna jako parametr
    app = BooksApp(root)
    #głowna pętla programu
    root.mainloop()
