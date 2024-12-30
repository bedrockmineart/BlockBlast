import pygame

class Cell:
    def __init__( self, color, block_size ):
        self.color = color
        self.block_size = block_size

    def render( self, screen, x, y ):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect( x, y, self.block_size, self.block_size )
        )
