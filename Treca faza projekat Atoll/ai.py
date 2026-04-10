from collections import deque
import tabla
import itertools

WIN_SCORE = 100000
LOSE_SCORE = -100000
NEAR_WIN_BONUS = 5000
BLOCK_PRIORITY = 10000
DEPTH = 2
TOTAL_ISLANDS = 12

def get_bfs_distance_to_connect(board_state, player_color, radius):
    my_island_type = "crveno ostrvo" if player_color == "crveni" else "zeleno ostrvo"
    my_stone_type = "crveni kamen" if player_color == "crveni" else "zeleni kamen"
    
    op_island_type = "zeleno ostrvo" if player_color == "crveni" else "crveno ostrvo"
    op_stone_type = "zeleni kamen" if player_color == "crveni" else "crveni kamen"

    my_islands = {} 
    
    for coord, data in board_state.items():
        if data['status'] == my_island_type:
            i_id = data['island_id']
            if i_id not in my_islands:
                my_islands[i_id] = []
            my_islands[i_id].append(coord)
            
    island_ids = list(my_islands.keys())
    if len(island_ids) < 2:
        return float('inf') 

    min_total_dist = float('inf')

    for id1, id2 in itertools.combinations(island_ids, 2):
        diff = abs(id1 - id2)
        dist_on_circle = min(diff, TOTAL_ISLANDS - diff)
        
        threshold = TOTAL_ISLANDS // 2 - 1
        if dist_on_circle < threshold:
            continue

        queue = deque()
        visited = set()
        
        for start_node in my_islands[id1]:
            queue.append((start_node, 0))
            visited.add(start_node)
            
        found_dist = float('inf')
        
        while queue:
            curr_node, dist = queue.popleft()
            
            if dist >= min_total_dist:
                continue

            curr_val = board_state[curr_node]
            if curr_val['status'] == my_island_type and curr_val['island_id'] == id2:
                found_dist = dist
                break
            
            neighbors = tabla.get_neighbors(curr_node[0], curr_node[1])
            for nb in neighbors:
                if nb not in board_state: continue
                if nb in visited: continue
                
                status = board_state[nb]['status']
                
                if status == op_stone_type or status == op_island_type:
                    continue
                
                cost = 1
                if status == my_stone_type or status == my_island_type: 
                    cost = 0 

                if cost == 0:
                    visited.add(nb)
                    queue.appendleft((nb, dist))
                else:
                    visited.add(nb)
                    queue.append((nb, dist + 1))
        
        if found_dist < min_total_dist:
            min_total_dist = found_dist

    return min_total_dist

def heuristic(board_state, radius, max_player, min_player):
    
    dist_ai = get_bfs_distance_to_connect(board_state, max_player, radius)
    dist_human = get_bfs_distance_to_connect(board_state, min_player, radius)
    
    score = 0
    
    if dist_ai != float('inf'):
        score += (30 - dist_ai) * 100
        if dist_ai <= 1:
            score += NEAR_WIN_BONUS

    if dist_human != float('inf'):
        score -= (30 - dist_human) * 120 
        
        if dist_human <= 1:
            score -= BLOCK_PRIORITY
            
    return score

def get_relevant_moves(board_state):
    relevant = set()
    occupied = False
    
    for coord, data in board_state.items():
        if data['status'] != 'free':
            occupied = True
            neighbors = tabla.get_neighbors(coord[0], coord[1])
            for nb in neighbors:
                if nb in board_state and board_state[nb]['status'] == 'free':
                    relevant.add(nb)

    if not occupied:
        return tabla.get_possible_moves(board_state)
        
    return list(relevant)

def minimax(board_state, depth, alpha, beta, maximizing_player, radius, ai_color, human_color):

    if tabla.check_win(board_state, ai_color):
        return WIN_SCORE, None
    if tabla.check_win(board_state, human_color):
        return LOSE_SCORE, None

    if depth == 0:
        return heuristic(board_state, radius, ai_color, human_color), None

    possible_moves = get_relevant_moves(board_state)
    
    if not possible_moves:
        return heuristic(board_state, radius, ai_color, human_color), None

    best_move = None

    if maximizing_player:
        max_eval = -float('inf')
        for move in possible_moves:
            
            tabla.play_move(board_state, move, ai_color)
            
            eval_val, _ = minimax(board_state, depth - 1, alpha, beta, False, radius, ai_color, human_color)
            
            tabla.undo_move(board_state, move)
            
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
            
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break 
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        for move in possible_moves:
            
            tabla.play_move(board_state, move, human_color)
            
            eval_val, _ = minimax(board_state, depth - 1, alpha, beta, True, radius, ai_color, human_color)
            
            tabla.undo_move(board_state, move)
            
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
            
            beta = min(beta, eval_val)
            if beta <= alpha:
                break 
        return min_eval, best_move

def get_best_move(board_state, radius, ai_color):

    human_color = "zeleni" if ai_color == "crveni" else "crveni"
    
    print(f"AI ({ai_color}) razmislja... Dubina: {DEPTH}")

    score, move = minimax(board_state, DEPTH, -float('inf'), float('inf'), True, radius, ai_color, human_color)
            
    print(f"AI odlucio: Potez {move} sa procenom {score}")
    return move