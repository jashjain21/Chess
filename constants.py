from typing import Dict, Tuple

# Display constants
SCREEN_WIDTH: int = 480
SCREEN_HEIGHT: int = 480
TILE_SIZE: int = 60  # SCREEN_WIDTH // 8
BOARD_SIZE: int = 8

# Color constants
BG_COLOR: Tuple[int, int, int] = (0, 0, 0)
TEXT_SIZE: int = 30
END_SCREEN_COLOR: Tuple[int, int, int] = (142, 164, 210)
END_SCREEN_WIDTH: int = 300
END_SCREEN_HEIGHT: int = 150

# Board colors
COLOR_BOARD_LIGHT: Tuple[int, int, int] = (250, 215, 180)
COLOR_BOARD_DARK: Tuple[int, int, int] = (105, 58, 12)
COLOR_HIGHLIGHT: Tuple[int, int, int] = (120, 223, 245)
COLOR_CHECK_HIGHLIGHT: Tuple[int, int, int] = (255, 0, 0)

# Asset constants
IMAGE_PATHS: Dict[str, str] = {
    'Pawn': 'chess_pieces/{color}_pawn.png',
    'Rook': 'chess_pieces/{color}_rook.png',
    'Knight': 'chess_pieces/{color}_knight.png',
    'Bishop': 'chess_pieces/{color}_bishop.png',
    'Queen': 'chess_pieces/{color}_queen.png',
    'King': 'chess_pieces/{color}_king.png'
}

# Piece constants
PIECE_COLORS: Dict[str, int] = {'Black': 0, 'White': 1}