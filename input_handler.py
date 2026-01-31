import pygame
from dataclasses import dataclass
from typing import List, Union

@dataclass
class ClickCommand:
    x: int
    y: int

@dataclass
class RestartCommand:
    pass

@dataclass
class QuitCommand:
    pass

class InputHandler:
    def process_events(self) -> List[Union[ClickCommand, RestartCommand, QuitCommand]]:
        """
        Convert pygame events to game commands
        """
        commands: List[Union[ClickCommand, RestartCommand, QuitCommand]] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                commands.append(QuitCommand())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    commands.append(RestartCommand())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x: int
                y: int
                x, y = event.pos
                commands.append(ClickCommand(x, y))
        return commands