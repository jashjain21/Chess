import pygame
from pieces import Queen, Rook, Pawn, King, Bishop, Knight

pygame.init()


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.selected = None
        self.king = self.board.kings[self.color]
        self.opponent = None
        self.legal_moves = {}
        self.promoting_pawn = None

        self.set_legal_moves()
        self.get_legal_moves(None)

    def set_opponent(self, other):
        """
        Sets the opponent of the player
        """
        self.opponent = other

    def get_status(self, check, current_turn):
        """
        Determines whether the game should continue or end.
        Called ONLY from GameState.
        """
        flag = True
        insufficient = False
        self.get_legal_moves(check)

        if len(self.legal_moves) == 1:
            if len(self.opponent.legal_moves) == 1:
                insufficient = True
            elif len(self.opponent.legal_moves) == 2:
                insufficient = True
                for piece in self.opponent.legal_moves:
                    if isinstance(piece, (Queen, Rook, Pawn)):
                        insufficient = False

        elif len(self.legal_moves) == 2:
            insufficient = True
            remaining = None
            for piece in self.legal_moves:
                if isinstance(piece, (Queen, Rook, Pawn)):
                    insufficient = False
                elif not isinstance(piece, King):
                    remaining = piece

            if insufficient:
                if len(self.opponent.legal_moves) == 2:
                    opponent_remaining = None
                    for piece in self.opponent.legal_moves:
                        if isinstance(piece, (Queen, Rook, Pawn)):
                            insufficient = False
                        elif not isinstance(piece, King):
                            opponent_remaining = piece

                    if isinstance(remaining, Bishop) and isinstance(opponent_remaining, Bishop):
                        if remaining.square.color != opponent_remaining.square.color:
                            insufficient = False
                    else:
                        insufficient = False
                elif len(self.opponent.legal_moves) > 2:
                    insufficient = False

        for piece in self.legal_moves:
            if len(self.legal_moves[piece]) != 0:
                flag = False

        if check is not None:
            if flag:
                return 'Checkmate'
            elif insufficient:
                return 'Draw by insufficient material'
            else:
                return 'Continue'
        elif flag:
            return 'Stalemate'
        elif insufficient:
            return 'Draw by insufficient material'
        else:
            return 'Continue'

    def set_legal_moves(self):
        """
        Initializes pieces at object creation
        """
        limit = (1, 3) if self.color == 'White' else (7, 9)
        for i in range(limit[0], limit[1]):
            for j in range(1, 9):
                self.legal_moves[self.board.get_square(i, j).piece] = []

    def get_legal_moves(self, check):
        """
        Calculates legal moves for all pieces
        """
        if check is not None and check.double_check():
            self.legal_moves[self.king] = self.king.possible_moves(check)
            return

        captured = []
        for piece in self.legal_moves:
            if piece.square is None:
                captured.append(piece)
                continue
            self.legal_moves[piece] = piece.possible_moves(check)

        for piece in captured:
            del self.legal_moves[piece]

    def clear_legal_moves(self):
        """
        Clears all previous legal moves
        """
        for piece in self.legal_moves:
            self.legal_moves[piece] = []
            if isinstance(piece, Pawn):
                piece.en_passant = 0

    def highlight_legal_moves(self, piece):
        """
        Highlights legal moves for selected piece
        """
        for move in self.legal_moves[piece]:
            move.highlighted = not move.highlighted

    def select(self, piece):
        """
        Selects a piece
        """
        self.selected = piece
        if self.selected is not None and self.selected.color != self.color:
            self.selected = None

        if self.selected is not None:
            self.highlight_legal_moves(self.selected)
            piece.square.selected_highlighted = True

    def unselect(self):
        """
        Unselects current piece
        """
        self.selected.square.selected_highlighted = False
        self.highlight_legal_moves(self.selected)
        self.selected = None

    def end_turn(self):
        """
        Clears selection and move highlights at end of turn.
        """
        self.selected = None
        self.clear_legal_moves()

    def promotion(self, sq):
        """
        Handles pawn promotion
        """
        if sq.column != self.promoting_pawn.square.column:
            return 'Continue'

        if self.color == 'White':
            mapping = {8: Queen, 7: Rook, 6: Bishop, 5: Knight}
        else:
            mapping = {1: Queen, 2: Rook, 3: Bishop, 4: Knight}

        piece_cls = mapping.get(sq.row)
        if piece_cls is None:
            return 'Continue'

        promoted_piece = self.promoting_pawn.promote(piece_cls)
        if promoted_piece is not None:
            del self.legal_moves[self.promoting_pawn]
            self.legal_moves[promoted_piece] = []
            self.promoting_pawn = None
            self.board.promoting_pawn = None
            self.end_turn()
            return 'Continue'

        return 'Continue'

    def play(self, x, y):
        """
        Handles a player click
        """
        sq = self.board.get_clicked_square(x, y)
        if sq is None:
            return 'Continue'

        if self.promoting_pawn is not None:
            return self.promotion(sq)

        if self.selected is not None:
            if sq in self.legal_moves[self.selected]:
                if self.king.square.check_highlighted:
                    self.king.square.check_highlighted = False

                self.selected.square.selected_highlighted = False
                self.promoting_pawn = self.selected.move(sq)

                self.unselect()
                self.clear_legal_moves()

                if self.promoting_pawn is not None:
                    self.board.promoting_pawn = self.promoting_pawn

                return 'Continue'

            elif sq.piece is not None:
                if sq.piece == self.selected:
                    self.unselect()
                elif sq.piece.color == self.color:
                    self.unselect()
                    self.select(sq.piece)
                else:
                    self.unselect()
            else:
                self.unselect()
        else:
            self.select(sq.piece)

        return 'Continue'