Ovaj projekat predstavlja implementaciju stone igre Atoll u jeziku Python, razvijenu za predmet Veštačka inteligencija. Igra se odvija na heksagonalnoj tabli.

Pravila igre: https://www.marksteeregames.com/Atoll_rules.pdf

Modovi igre:
-Čovek protiv Čoveka (PvP)
-Čovek protiv Računara (PvE)
AI Agent: Koristi Minimax algoritam sa Alpha-Beta odsecanjem.
Heuristika: AI donosi odluke koristeći BFS (Breadth-First Search) za pronalaženje najkraćeg puta do povezivanja ostrva.
Prilagodljivost: Podržane veličine stranica table: 3, 5, 7 i 9.
GUI: Grafički interfejs realizovan pomoću tkinter biblioteke.
Tehnologije:
-Python 3.x
-Tkinter (za GUI)
-NumPy (za podršku matricama)
Struktura projekta
-main.py – Ulazna tačka aplikacije, upravljanje GUI-jem i tokom igre.
-tabla.py – Logika igre, provera pobede i generisanje heksagonalne mreže.
-ai.py – Implementacija Minimax algoritma i heurističke funkcije.
-mats.py – Matematičke funkcije za konverziju koordinata (Hex u Pixel i obrnuto).
