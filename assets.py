import pygame
from typing import Dict

class AssetManager:
    def __init__(self, image_paths: Dict[str, str]) -> None:
        self.images: Dict[str, Dict[str, pygame.Surface]] = {}
        for piece, path_template in image_paths.items():
            self.images[piece] = {}
            for color in ['Black', 'White']:
                full_path: str = path_template.replace('{color}', color.lower())
                self.images[piece][color] = pygame.image.load(full_path)

    def get_image(self, piece: str, color: str) -> pygame.Surface:
        return self.images[piece][color]