from board import Board
from player import Player
from assets import AssetManager
from rules_engine import MoveValidator
from constants import IMAGE_PATHS

class GameState:
    def __init__(self) -> None:
        self.asset_manager: AssetManager = AssetManager(IMAGE_PATHS)
        self.move_validator: MoveValidator = MoveValidator()
        self.board: Board = Board(self.asset_manager, self.move_validator)
        self.white_player: Player = Player(self.board, 'White')
        self.black_player: Player = Player(self.board, 'Black')
        self.white_player.set_opponent(self.black_player)
        self.black_player.set_opponent(self.white_player)
        self.current_turn: int = 0  # 0 for white, 1 for black
        self.result: str = 'Continue'
        self.ended: bool = False

    def current_player(self) -> Player:
        return self.white_player if self.current_turn == 0 else self.black_player

    def reset(self) -> None:
        self.board = Board(self.asset_manager, self.move_validator)
        self.white_player = Player(self.board, 'White')
        self.black_player = Player(self.board, 'Black')
        self.white_player.set_opponent(self.black_player)
        self.black_player.set_opponent(self.white_player)
        self.current_turn = 0
        self.result = 'Continue'
        self.ended = False