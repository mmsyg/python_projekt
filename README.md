# Baza danych ksiązek

## Opis
Projekt "Moje Książki" to aplikacja desktopowa stworzona w Pythonie z wykorzystaniem biblioteki tkinter i sqlite. Pozwala ona na zarządzanie własną biblioteczką książek, oferując funkcje takie jak dodawanie, usuwanie, wyszukiwanie książek. Aplikacja korzysta z lokalnej bazy danych SQLite. Dane są importowane i eksportowane do JSON.

## Funkcjonalności
- **Dodawanie książek:** Możliwość wprowadzenia danych książki, takich jak tytuł, autor, rok wydania oraz ISBN.
- **Usuwanie książek:** Możliwość usunięcia wybranej książki z bazy danych poprzez wybranie jej i naciśniecie przyciusku "delete".
- **Wyszukiwanie książek:** Możliwość wyszukiwania książek na podstawie wszystkich dostępnych pól.
- **Wyświetlanie listy książek:** Możliwość przeglądania całej listy dostępnych książek.

## Pliki
- books.py - głowny skrypt aplikacji
- books.db - baza danych SQL
- books.json - dane z bazy danych przechowwyane w JSON (z tąd też aplikacja zczytuje dane wejściowe)
