from game_state import GameState
from renderer import ChessRenderer
from input_handler import InputHandler, ClickCommand, RestartCommand, QuitCommand
from constants import BG_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

pygame.init()

bg_color: tuple = BG_COLOR
screen_width: int = SCREEN_WIDTH
screen_height: int = SCREEN_HEIGHT
size: tuple = (screen_width, screen_height)

screen: pygame.Surface = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_state: GameState = GameState()
renderer: ChessRenderer = ChessRenderer(screen)
input_handler: InputHandler = InputHandler()


def redraw(game_state: GameState) -> None:
    renderer.draw_board(game_state.board)
    if game_state.result != 'Continue':
        game_state.ended = True
        renderer.draw_game_end(game_state.result, game_state.current_turn)

    renderer.update()


run = True
while run:
    commands = input_handler.process_events()
    for command in commands:
        if isinstance(command, QuitCommand):
            run = False
            break
        elif isinstance(command, RestartCommand):
            if game_state.ended:
                game_state.reset()
        elif isinstance(command, ClickCommand):
            if not game_state.ended:
                result = game_state.current_player().play(command.x, command.y)
                player = game_state.current_player()
                if player.selected is None and game_state.board.promoting_pawn is None:
                    game_state.current_turn ^= 1
                    opponent = game_state.current_player()
                    check = opponent.king.in_check(opponent.king.square)
                    if check is not None:
                        opponent.king.square.check_highlighted = True
                    game_state.result = opponent.get_status(check, game_state.current_turn)
                else:
                    game_state.result = 'Continue'

    redraw(game_state)

pygame.quit()
