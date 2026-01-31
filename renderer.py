import pygame
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from board import Board
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TEXT_SIZE,
    END_SCREEN_COLOR,
    END_SCREEN_WIDTH,
    END_SCREEN_HEIGHT
)
from pieces import Piece

class ChessRenderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen: pygame.Surface = screen

    def draw_square(self, square) -> None:
        """
        Draw a single square with appropriate color and highlighting
        """
        if square.highlighted:
            if square.piece is not None:
                pygame.draw.rect(self.screen, square.highlight, (square.x, square.y, square.length, square.length))
            else:
                pygame.draw.circle(self.screen, square.highlight, (square.x + square.length // 2, square.y + square.length // 2),
                                   square.length // 6)
        elif square.check_highlighted:
            pygame.draw.rect(self.screen, square.check_highlight, (square.x, square.y, square.length, square.length))
        elif square.selected_highlighted:
            pygame.draw.rect(self.screen, square.highlight, (square.x, square.y, square.length, square.length))
        else:
            pygame.draw.rect(self.screen, square.color, (square.x, square.y, square.length, square.length))

        if square.piece is not None:
            self.draw_piece(square.piece, square.x, square.y)

    def draw_piece(self, piece: Piece, x: int, y: int) -> None:
        """
        Draw a piece image at the given position
        """
        if piece.img is not None:
            self.screen.blit(piece.img, (x, y))

    def draw_board(self, board: 'Board') -> None:
        """
        Draw the entire board including all squares and pieces
        """
        for row in board.squares:
            for square in row:
                self.draw_square(square)

        if board.promoting_pawn is not None:
            self.draw_promotion_dialogue(board)

    def draw_promotion_dialogue(self, board: 'Board') -> None:
        """
        Draw the pawn promotion selection overlay
        """
        if board.promoting_pawn is None:
            return
        length: int = board.square_length
        x: int = board.promoting_pawn.square.x
        y: int = board.promoting_pawn.square.y
        asset_manager = board.asset_manager
        if board.promoting_pawn.color == 'White':
            pygame.draw.rect(self.screen, (73, 81, 111), (x, y, length, 4 * length))
            self.screen.blit(asset_manager.get_image('Queen', 'White'), (x, y))
            self.screen.blit(asset_manager.get_image('Rook', 'White'), (x, y + length))
            self.screen.blit(asset_manager.get_image('Bishop', 'White'), (x, y + 2 * length))
            self.screen.blit(asset_manager.get_image('Knight', 'White'), (x, y + 3 * length))

        else:
            pygame.draw.rect(self.screen, (98, 121, 184), (x, y - 3 * length, length, 4 * length))
            self.screen.blit(asset_manager.get_image('Queen', 'Black'), (x, y))
            self.screen.blit(asset_manager.get_image('Rook', 'Black'), (x, y - length))
            self.screen.blit(asset_manager.get_image('Bishop', 'Black'), (x, y - 2 * length))
            self.screen.blit(asset_manager.get_image('Knight', 'Black'), (x, y - 3 * length))

    def draw_game_end(self, res: str, player_turn: int) -> None:
        """
        Draw the game end screen
        """
        text_size: int = TEXT_SIZE
        font = pygame.font.SysFont('SansSerif', text_size)
        winner: Optional[str] = f"{'White' if player_turn == 1 else 'Black'} wins!!" if res == 'Checkmate' else None
        restart: str = 'Press Space to restart'

        end_screen_color = END_SCREEN_COLOR
        end_screen_width = END_SCREEN_WIDTH
        end_screen_height = END_SCREEN_HEIGHT
        end_screen_x: int = SCREEN_WIDTH // 2 - end_screen_width // 2
        end_screen_y: int = SCREEN_HEIGHT // 2 - end_screen_height // 2
        pygame.draw.rect(self.screen, end_screen_color, (end_screen_x, end_screen_y, end_screen_width, end_screen_height))

        pos = (end_screen_x + end_screen_width // 2, end_screen_y + end_screen_height // 2)

        message = font.render(res, True, (0, 0, 0))
        rect = message.get_rect()
        rect.center = (pos[0], pos[1] - text_size)
        self.screen.blit(message, rect)

        if winner is not None:
            message = font.render(winner, True, (0, 0, 0))
            rect = message.get_rect()
            rect.center = pos
            self.screen.blit(message, rect)

        message = font.render(restart, True, (0, 0, 0))
        rect = message.get_rect()
        rect.center = (pos[0], pos[1] + text_size)
        self.screen.blit(message, rect)

    def update(self) -> None:
        """
        Update the display
        """
        pygame.display.update()