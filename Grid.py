from EmptyCell import EmptyCell
from Cell import Cell
import pygame

class Grid(  ):
    def __init__( self, block_size ):
        self.block_size = block_size
        self.grid = [ [ EmptyCell(  ) for x in range( 8 ) ] for y in range( 8 ) ]
    
    def render( self, screen ):
        for y in range( 8 ):
            for x in range( 8 ):
                self.grid[ y ][ x ].render( screen, x * self.block_size, y * self.block_size )
                pygame.draw.rect(
                    screen,
                    ( 0, 0, 0 ),  # Black color for the outline
                    pygame.Rect( x * self.block_size, y * self.block_size, self.block_size, self.block_size ),
                    1  # Width of the outline
                )

    def checkForLines( self ):
        rowsToClear = [ x for x in range( 8 ) ]
        columnsToClear = [ x for x in range( 8 ) ]

        for rowIndex, row in enumerate( self.grid ):
            for columnIndex, cell in enumerate( row ):
                if cell.__class__ == EmptyCell:
                    if rowIndex in rowsToClear:
                        rowsToClear.remove( rowIndex )
                    if columnIndex in columnsToClear:
                        columnsToClear.remove( columnIndex )

        for row in rowsToClear:
            self.grid[ row ] = [ EmptyCell(  ) for x in range( 8 ) ]
        for row in self.grid:
            for column in columnsToClear:
                row[ column ] = EmptyCell(  )

        return len( rowsToClear ) + len( columnsToClear )

    def place_cell( self, x, y, color, block_size ):
        self.grid[ y ][ x ] = Cell( color, block_size )

    def can_place( self, x, y ):
        return self.grid[ y ][ x ].__class__ == EmptyCell