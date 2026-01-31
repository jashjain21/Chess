from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board
    from pieces import Piece, King

from pieces import Dummy, Knight, Bishop, Rook, Queen, Pawn

class MoveValidator:
    def is_in_check(self, board: 'Board', color: str) -> Optional['Check']:
        """
        Check if the king of the given color is in check.
        """
        king: 'King' = board.kings[color]
        checking_pieces = []
        for piece_class in [Knight, Bishop, Rook, Queen]:
            checking_piece = self.is_attacked_by(board, king.square, piece_class, color)
            if checking_piece is not None:
                checking_pieces.append(checking_piece)

        # Check for pawn attacks
        row_inc = 1 if color == 'White' else -1
        right = board.get_square(king.square.row + row_inc, king.square.column + 1)
        left = board.get_square(king.square.row + row_inc, king.square.column - 1)
        for sq in [right, left]:
            if sq and isinstance(sq.piece, Pawn) and sq.piece.color != color:
                checking_pieces.append(sq.piece)

        from pieces import Check
        return None if len(checking_pieces) == 0 else Check(king, checking_pieces)

    def is_attacked_by(self, board: 'Board', square, piece_class, color) -> Optional['Piece']:
        """
        Check if the square is attacked by the given piece type from the opponent.
        """
        dummy = Dummy(board, color, square, piece_class, board.kings[color], board.asset_manager)
        moves = dummy.possible_moves(None)
        for move in moves:
            if isinstance(move.piece, piece_class) and move.piece.color != color:
                return move.piece
        return None