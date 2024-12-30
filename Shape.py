import random
import pygame

class Shape:
    def __init__( self, shape, block_size ):
        self.shape = shape
        self.block_size = block_size
        self.color = self.random_color(  )
        self.x = 0
        self.y = 0
        self.frameX = 0
        self.frameY = 0
        self.sizeX, self.sizeY = self.findSize( shape )

    def findSize( self, shape ):
        sizeY = len( shape )
        sizeX = 0
        for row in shape:
            s = len( row )
            sizeX = max( sizeX, s )

        return sizeX, sizeY

    def random_color( self ):
        return random.choice([ 
            ( 255, 0, 0 ),    # Red
            ( 0, 255, 0 ),    # Green
            ( 0, 0, 255 ),    # Blue
            ( 255, 255, 0 ),  # Yellow
            ( 255, 165, 0 ),  # Orange
            ( 128, 0, 128 )   # Purple 
            ])

    def get_blocks( self ):
        blocks = [  ]
        for row_idx, row in enumerate( self.shape ):
            for col_idx, cell in enumerate( row ):
                if cell:
                    blocks.append(( row_idx, col_idx ))
        return blocks

    def render( self, surface, x, y ):
        for row_idx, row in enumerate( self.shape ):
            for col_idx, cell in enumerate( row ):
                if cell:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        pygame.Rect( 
                            x + col_idx * self.block_size,
                            y + row_idx * self.block_size,
                            self.block_size,
                            self.block_size 
                        )
                    )