import pytest
from game_state import GameState

def get_click_coords(square):
    # Return the center coordinates of the square for clicking
    return square.x + 30, square.y + 30

def get_piece_symbol(piece):
    if piece is None:
        return '.'
    name = piece.__class__.__name__
    color = piece.color
    symbol = {
        'Pawn': 'p',
        'Rook': 'r',
        'Knight': 'n',
        'Bishop': 'b',
        'Queen': 'q',
        'King': 'k'
    }[name]
    return symbol.upper() if color == 'White' else symbol

def get_board_ascii(board):
    lines = []
    for row in range(8, 0, -1):
        line = ''
        for col in range(1, 9):
            sq = board.get_square(row, col)
            line += get_piece_symbol(sq.piece)
        lines.append(line)
    return '\n'.join(lines)

def simulate_scholars_mate():
    # Create game state
    game_state = GameState()

    # Scholar's Mate moves: e4 e5 Bc4 Nc6 Qh5 Nf6 Qxf7#
    # Each move is (select_square, target_square)
    moves = [
        # 1. e4
        ((2, 5), (4, 5)),  # e2 to e4
        # 1. ... e5
        ((7, 5), (5, 5)),  # e7 to e5
        # 2. Bc4
        ((1, 6), (4, 3)),  # f1 to c4 (Bc4)
        # 2. ... Nc6
        ((8, 2), (6, 3)),  # b8 to c6 (Nc6)
        # 3. Qh5
        ((1, 4), (5, 8)),  # d1 to h5 (Qh5)
        # 3. ... Nf6
        ((8, 7), (6, 6)),  # g8 to f6 (Nf6)
        # 4. Qxf7#
        ((5, 8), (7, 6)),  # h5 to f7 (Qxf7#)
    ]

    for select_coords, target_coords in moves:
        select_sq = game_state.board.get_square(*select_coords)
        target_sq = game_state.board.get_square(*target_coords)

        # First click: select piece
        x, y = get_click_coords(select_sq)
        result = game_state.current_player().play(x, y)
        assert result == 'Continue'

        # Second click: move to target
        result = game_state.current_player().play(x, y)

        # Simulate end turn
        player = game_state.current_player()
        if player.selected is None and game_state.board.promoting_pawn is None:
            game_state.current_turn ^= 1
            opponent = game_state.current_player()
            check = opponent.king.in_check()
            if check is not None:
                opponent.king.square.check_highlighted = True
            game_state.result = opponent.get_status(check, game_state.current_turn)
            # Update legal moves for the new current player
            game_state.current_player().get_legal_moves(None)
        else:
            game_state.result = 'Continue'

    # After last move, result should be 'Continue'
    assert game_state.result == 'Continue'

    # Get final board ascii
    ascii_board = get_board_ascii(game_state.board)
    return ascii_board

def test_golden_master():
    # Run simulation
    actual_output = simulate_scholars_mate()

    # Read expected output
    with open('tests/expected_output.txt', 'r') as f:
        expected_output = f.read().strip()

    # Assert they match
    assert actual_output == expected_output