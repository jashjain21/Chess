from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from constants import (
    COLOR_BOARD_LIGHT,
    COLOR_BOARD_DARK,
    COLOR_HIGHLIGHT,
    COLOR_CHECK_HIGHLIGHT,
    SCREEN_WIDTH,
    TILE_SIZE
)
from typing import TYPE_CHECKING, Optional, List
if TYPE_CHECKING:
    from assets import AssetManager
import pygame

pygame.init()


class Square:
    white = COLOR_BOARD_LIGHT
    black = COLOR_BOARD_DARK
    highlight = COLOR_HIGHLIGHT
    check_highlight = COLOR_CHECK_HIGHLIGHT
    home_piece = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    # home_piece = [None, Knight, Bishop, None, King, None, None, None]

    def __init__(self, board, row: int, column: int, color, x: int, y: int, length: int) -> None:
        self.board = board
        self.column: int = column
        self.row: int = row
        self.color = color
        self.x: int = x
        self.y: int = y
        self.length: int = length
        self.piece: Optional[Piece] = self.get_home_piece()
        self.highlighted: bool = False
        self.selected_highlighted: bool = False
        self.check_highlighted: bool = False

    def __repr__(self) -> str:
        return f'{self.get_name()} -> {self.piece}'

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.column == other.column

    def get_name(self) -> str:
        return f"{chr(ord('a') + self.column - 1)}{self.row}"

    def get_home_piece(self) -> Optional[Piece]:
        asset_manager = self.board.asset_manager
        if self.row == 1:
            return self.home_piece[self.column - 1](self.board, 'White', self, asset_manager)
        elif self.row == 8:
            return self.home_piece[self.column - 1](self.board, 'Black', self, asset_manager)
        elif self.row == 2:
            return Pawn(self.board, 'White', self, asset_manager)
        elif self.row == 7:
            return Pawn(self.board, 'Black', self, asset_manager)
        return None




class Board:
    def __init__(self, asset_manager: 'AssetManager', move_validator: 'MoveValidator') -> None:
        self.asset_manager: 'AssetManager' = asset_manager
        self.move_validator: 'MoveValidator' = move_validator
        self.length: int = SCREEN_WIDTH
        self.x: int = 0
        self.y: int = 0
        self.square_length: int = TILE_SIZE
        self.squares: List[List[Square]] = self.make_squares()
        white_king_square = self.get_square(1, 5)
        black_king_square = self.get_square(8, 5)
        assert white_king_square is not None and white_king_square.piece is not None
        assert black_king_square is not None and black_king_square.piece is not None
        self.kings: dict = {'White': white_king_square.piece,
                      'Black': black_king_square.piece}
        self.promoting_pawn: Optional[Piece] = None

    def get_square(self, row: int, column: int) -> Optional[Square]:
        """
        This method finds the square given a row and a column
        :param row: Row of the square
        :param column: Column of the square
        :return: A Square Object
        """
        if row <= 0 or column <= 0 or row > 8 or column > 8:
            return None
        return self.squares[8 - row][column - 1]

    def make_squares(self) -> List[List[Square]]:
        """
        This method creates the board representation matrix
        :return:  8*8 matrix of "Square" objects
        """
        squares = []
        x, y = self.x, self.y

        for j in range(8, 0, -1):
            color = Square.white if j % 2 == 0 else Square.black
            row = []
            for i in range(8):
                if i != 0:
                    color = Square.white if color == Square.black else Square.black
                square = Square(self, j, i + 1, color, x, y, self.square_length)
                row.append(square)
                x += self.square_length
            squares.append(row)
            x = self.x
            y += self.square_length

        return squares



    def get_clicked_square(self, x, y):
        """
        This method will take the coordinates and return what square the coordinate is on
        :param x: x-coordinate
        :param y: y-coordinate
        :return: "Square" object
        """
        if x < self.x or y < self.y or x >= self.x + self.length or y >= self.y + self.length:
            return None
        i = (x - self.x) // self.square_length
        j = (y - self.y) // self.square_length
        return self.squares[j][i]
