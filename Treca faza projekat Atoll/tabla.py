import numpy as np
import mats
import math
from collections import deque

CIRCLE_RADIUS = 12

def undo_move(tabla, koordinate):
    if koordinate in tabla:
        tabla[koordinate]['status'] = 'free'
def get_island_id_and_color(i, j, radius):

    x = j - radius
    y = i - radius
    z = -x - y
    
    if y == -radius: 
        return (0, "GREEN") if x < z else (1, "RED")
    elif x == radius: 
        return (2, "GREEN") if y < z else (3, "RED")
    elif z == -radius: 
        return (4, "GREEN") if x > y else (5, "RED")
    elif y == radius: 
        return (6, "GREEN") if x > z else (7, "RED")
    elif x == -radius: 
        return (8, "GREEN") if y > z else (9, "RED")
    elif z == radius: 
        return (10, "GREEN") if x < y else (11, "RED")
    
    return None, None 

def generate_atoll_matrix(radius):
    if radius % 2 == 0 or radius > 9 or radius < 3:
        raise Exception("Duzina stranice mora biti neparna (3, 5, 7, 9)")
    size = 2 * radius + 1
    matrix = [[None for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            x = j - radius
            y = i - radius
            z = -x - y
            dist = max(abs(x), abs(y), abs(z))

            if dist > radius:
                matrix[i][j] = "null"
                continue
            if dist < radius:
                matrix[i][j] = (i, j) 
                continue

            count_max = 0
            if abs(x) == radius: count_max += 1
            if abs(y) == radius: count_max += 1
            if abs(z) == radius: count_max += 1

            if count_max >= 2:
                matrix[i][j] = "null"
            else:
                
                _, color = get_island_id_and_color(i, j, radius)
                matrix[i][j] = color
    return matrix

def generate_polja(matrix, radius):
    size = 2 * radius + 1
    recnik = {}
    igriva_koordinate = []

    for i in range(size):
        for j in range(size):
            val = matrix[i][j]
            if val == "null" or val is None:
                continue

            status = ""
            je_igrivo = False
            
            island_id = None

            if val == "GREEN":
                status = "zeleno ostrvo"
                island_id, _ = get_island_id_and_color(i, j, radius)
            elif val == "RED":
                status = "crveno ostrvo"
                island_id, _ = get_island_id_and_color(i, j, radius)
            elif isinstance(val, tuple):
                status = "free"
                je_igrivo = True

            recnik[(i, j)] = {
                "status": status,
                "island_id": island_id 
            }

            if je_igrivo:
                igriva_koordinate.append((i, j))

    if igriva_koordinate:
        min_i = min(k[0] for k in igriva_koordinate)
        max_i = max(k[0] for k in igriva_koordinate)
        min_diag = min(k[0] + k[1] for k in igriva_koordinate)
        max_diag = max(k[0] + k[1] for k in igriva_koordinate)

    for koordinate, podaci in recnik.items():
        i, j = koordinate
        status = podaci['status']
        col_index = i - min_i
        
        if min_i <= i <= max_i:
            slovo = chr(65 + col_index)
        else:
            slovo = None

        diag_val = i + j
        if min_diag <= diag_val <= max_diag:
            broj = str(diag_val - min_diag + 1)
        else:
            broj = None

        podaci['slovo'] = slovo
        podaci['broj'] = broj

        if "ostrvo" in status:
            podaci['oznaka'] = "Ostrvo"
        elif slovo and broj:
            podaci['oznaka'] = f"{slovo}{broj}"
        else:
            podaci['oznaka'] = "Nepoznato"

    return recnik

def get_neighbors(i, j):
    directions = [
        (0, 1), (0, -1), 
        (1, 0), (-1, 0), 
        (1, -1), (-1, 1)
    ]
    return [(i + di, j + dj) for di, dj in directions]

def get_possible_moves(tabla):
    potezi = []
    for koord, podaci in tabla.items():
        if podaci['status'] == 'free':
            potezi.append(koord)
    return potezi

def play_move(tabla, koordinate, igrac):
    if koordinate not in tabla:
        return False
    
    if tabla[koordinate]['status'] != 'free':
        return False
        
    if igrac == "crveni":
        tabla[koordinate]['status'] = "crveni kamen"
    elif igrac == "zeleni":
        tabla[koordinate]['status'] = "zeleni kamen"
    
    return True

def postavi_kamencic(tabla, koordinate, igrac):
    polje = tabla.get(koordinate)
    if not polje:
        raise Exception("Polje ne postoji!")
    
    if polje['status'] != 'free':
        oznaka = polje.get('oznaka', str(koordinate))
        raise Exception(f"Polje {oznaka} je zauzeto!")
        
    play_move(tabla, koordinate, igrac)
    return True

def get_connected_group(tabla, start_node, target_status_list):
    queue = deque([start_node])
    visited = {start_node}
    group = {start_node}
    
    while queue:
        curr = queue.popleft()
        neighbors = get_neighbors(curr[0], curr[1])
        
        for nb in neighbors:
            if nb in tabla and nb not in visited:
                stat = tabla[nb]['status']
                if stat in target_status_list:
                    visited.add(nb)
                    group.add(nb)
                    queue.append(nb)
    return group

def check_win(tabla, current_player):

    if current_player == "crveni":
        my_stone = "crveni kamen"
        my_island = "crveno ostrvo"
    else:
        my_stone = "zeleni kamen"
        my_island = "zeleno ostrvo"

    player_stones = [k for k, v in tabla.items() if v['status'] == my_stone]
    
    if not player_stones:
        return False

    visited_stones = set()
    
    for stone in player_stones:
        if stone in visited_stones:
            continue
        group = get_connected_group(tabla, stone, [my_stone, my_island])
        
        for g_node in group:
            if tabla[g_node]['status'] == my_stone:
                visited_stones.add(g_node)

        connected_islands_ids = []
        for g_node in group:
            if tabla[g_node]['status'] == my_island:
                i_id = tabla[g_node]['island_id']
                if i_id is not None:
                    connected_islands_ids.append(i_id)   
        ids = sorted(list(set(connected_islands_ids)))
        
        if len(ids) < 2:
            continue

        TOTAL_ISLANDS = 12
        WIN_THRESHOLD = 7
        
        nasao_pobedu = False
        
        for start_node in ids:
            counter = 0

            max_dist_right = 0
            for x in ids:
                if x == start_node: continue
                
                diff = abs(start_node - x)
                
                if diff == 2 or diff == 10:
                    continue

                dist_r = x - start_node
                if dist_r > max_dist_right:
                    max_dist_right = dist_r
            
            if (max_dist_right + 1) >= WIN_THRESHOLD:
                counter += 1

            max_dist_left = 0
            for x in ids:
                if x == start_node: continue 
                
                diff = abs(start_node - x)
                if diff == 2 or diff == 10:
                    continue

                dist_l = start_node + TOTAL_ISLANDS - x
                if dist_l > max_dist_left:
                    max_dist_left = dist_l
                    
            if (max_dist_left + 1) >= WIN_THRESHOLD:
                counter += 1

            if counter == 2:
                nasao_pobedu = True
                break
        
        if nasao_pobedu:
            return True

    return False

def draw_board(canvas, tabla_recnik, radius):
    canvas.delete("all")
    all_x = []
    labels_cols = {}
    labels_rows = {}

    for koordinate, podaci in tabla_recnik.items():
        i, j = koordinate
        x, y = mats.hex_to_pixel(i, j, radius)
        all_x.append(x)

        slovo = podaci.get('slovo')
        if slovo: labels_cols[slovo] = x

        broj = podaci.get('broj')
        if broj:
            if broj not in labels_rows:
                labels_rows[broj] = {'min_x': x, 'left_y': y, 'max_x': x, 'right_y': y}
            else:
                if x < labels_rows[broj]['min_x']:
                    labels_rows[broj]['min_x'] = x
                    labels_rows[broj]['left_y'] = y
                if x > labels_rows[broj]['max_x']:
                    labels_rows[broj]['max_x'] = x
                    labels_rows[broj]['right_y'] = y

        status = podaci['status']
        color = "white"; outline = "#cccccc"; width=2

        if status == "zeleno ostrvo":
            color = "#7cb342"; outline = "#5b5b5b"
        elif status == "crveno ostrvo":
            color = "#f44336"; outline = "#5b5b5b"
        elif status == "crveni kamen":
            color = "#f44336"; outline = "black"
        elif status == "zeleni kamen":
            color = "#7cb342"; outline = "black"
        elif status == "free":
            color = "#e0e0e0"; outline = "#5b5b5b"

        canvas.create_oval(
            x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
            x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
            fill=color, outline=outline, width=width
        )

    all_y_coords = [mats.hex_to_pixel(k[0], k[1], radius)[1] for k in tabla_recnik.keys()]
    if not all_y_coords: return
    
    min_global_y = min(all_y_coords)
    max_global_y = max(all_y_coords)
    min_board_x = min(all_x)
    max_board_x = max(all_x)
    OFFSET_TEXT = 50

    for slovo, x_pos in sorted(labels_cols.items()):
        canvas.create_text(x_pos, min_global_y - OFFSET_TEXT, text=slovo, font=("Arial", 12, "bold"), fill="#333")
        canvas.create_text(x_pos, max_global_y + OFFSET_TEXT, text=slovo, font=("Arial", 12, "bold"), fill="#333")

    brojevi_ints = sorted([int(b) for b in labels_rows.keys()])
    if brojevi_ints:
        FIXED_STEP_Y = math.sqrt(3) * mats.HEX_SIZE
        min_br = min(brojevi_ints)
        max_br = max(brojevi_ints)
        sredina = (min_br + max_br) // 2
        
        start_y_left = labels_rows[str(min_br)]['left_y'] + 17
        start_y_right = labels_rows[str(sredina)]['right_y'] - 40

        for i, broj_int in enumerate(brojevi_ints):
            broj_str = str(broj_int)
            if broj_int <= sredina:
                ideal_y = start_y_left + (i * FIXED_STEP_Y)
                canvas.create_text(min_board_x - OFFSET_TEXT, ideal_y, text=broj_str, font=("Arial", 12, "bold"), fill="#333")
            if broj_int >= sredina:
                index_from_mid = broj_int - sredina
                ideal_y = start_y_right + (index_from_mid * FIXED_STEP_Y)
                canvas.create_text(max_board_x + OFFSET_TEXT, ideal_y, text=broj_str, font=("Arial", 12, "bold"), fill="#333")
