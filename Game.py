import pygame
import sys
import random

# Initialize Pygame
pygame.init(  )

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colors
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
from Grid import Grid
from Shape import Shape

BLOCK_SIZE = 50
SHAPE_DISTANCE = 50

shapes = [ 
    # I shape
    [ [ 1, 1, 1, 1 ] ],
    [ [ 1 ], [ 1 ], [ 1 ], [ 1 ] ],

    # O shape
    [ [ 1, 1 ],
     [ 1, 1 ] ],

    # T shape
    [ [ 1, 1, 1 ],
     [ 0, 1, 0 ] ],
    [ [ 0, 1 ],
     [ 1, 1 ],
     [ 0, 1 ] ],
    [ [ 0, 1, 0 ],
     [ 1, 1, 1 ] ],
    [ [ 1, 0 ],
     [ 1, 1 ],
     [ 1, 0 ] ],

    # L shape
    [ [ 1, 0 ],
     [ 1, 0 ],
     [ 1, 1 ] ],
    [ [ 1, 1, 1 ],
     [ 1, 0, 0 ] ],
    [ [ 1, 1 ],
     [ 0, 1 ],
     [ 0, 1 ] ],
    [ [ 0, 0, 1 ],
     [ 1, 1, 1 ] ],

    # Mirrored L shape
    [ [ 0, 1 ],
     [ 0, 1 ],
     [ 1, 1 ] ],
    [ [ 1, 1, 1 ],
     [ 0, 0, 1 ] ],
    [ [ 1, 1 ],
     [ 1, 0 ],
     [ 1, 0 ] ],
    [ [ 1, 0, 0 ],
     [ 1, 1, 1 ] ],

    # Z shape
    [ [ 1, 1, 0 ],
     [ 0, 1, 1 ] ],
    [ [ 0, 1 ],
     [ 1, 1 ],
     [ 1, 0 ] ],

    # Mirrored Z shape
    [ [ 0, 1, 1 ],
     [ 1, 1, 0 ] ],
    [ [ 1, 0 ],
     [ 1, 1 ],
     [ 0, 1 ] ],

    # Small L shape
    [ [ 1, 0 ],
     [ 1, 1 ] ],
    [ [ 1, 1 ],
     [ 0, 1 ] ],

    # Small mirrored L shape
    [ [ 0, 1 ],
     [ 1, 1 ] ],
    [ [ 1, 1 ],
     [ 1, 0 ] ],

    # Plus shape
    [ [ 0, 1, 0 ],
     [ 1, 1, 1 ],
     [ 0, 1, 0 ] ],

    # Big L shape
    [ [ 1, 0, 0 ],
     [ 1, 1, 1 ] ],
    [ [ 1, 1 ],
     [ 1, 0 ],
     [ 1, 0 ] ],
    [ [ 1, 1, 1 ],
     [ 0, 0, 1 ] ],
    [ [ 0, 1 ],
     [ 0, 1 ],
     [ 1, 1 ] ],

    # Mirrored big L shape
    [ [ 0, 0, 1 ],
     [ 1, 1, 1 ] ],
    [ [ 1, 1 ],
     [ 0, 1 ],
     [ 0, 1 ] ],
    [ [ 1, 1, 1 ],
     [ 1, 0, 0 ] ],
    [ [ 1, 0 ],
     [ 1, 0 ],
     [ 1, 1 ] ],

    # Big T shape
    [ [ 1, 1, 1 ],
     [ 0, 1, 0 ],
     [ 0, 1, 0 ] ],
    [ [ 0, 1 ],
     [ 1, 1 ],
     [ 0, 1 ],
     [ 0, 1 ] ],
    [ [ 0, 1, 0 ],
     [ 0, 1, 0 ],
     [ 1, 1, 1 ] ],
    [ [ 1, 0 ],
     [ 1, 0 ],
     [ 1, 1 ],
     [ 0, 1 ] ]
 ]


class Game:
    def __init__( self ):
        self.screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
        pygame.display.set_caption( "Block Blast made in 30 minutes" )
        self.clock = pygame.time.Clock(  )
        self.running = True
        self.grid = Grid( BLOCK_SIZE )
        self.availableShapes = [  ]
        self.populate_shapes(  )
        self.dragging_shape = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.score = 0
        self.font = pygame.font.SysFont( None, 36 )

    def populate_shapes( self ):
        self.availableShapes.append( Shape( shapes[ random.randint( 0, len( shapes ) - 1 ) ], BLOCK_SIZE ) )
        self.availableShapes.append( Shape( shapes[ random.randint( 0, len( shapes ) - 1 ) ], BLOCK_SIZE ) )
        self.availableShapes.append( Shape( shapes[ random.randint( 0, len( shapes ) - 1 ) ], BLOCK_SIZE ) )
        self.setPosition(  )

    def populate_shapes( self ):
        self.availableShapes = [  ]
        shapesCopy = shapes[ : ]
        random.shuffle( shapesCopy )

        while len( self.availableShapes ) < 3:
            if len( shapesCopy ) == 0:
                pygame.quit()
                sys.exit()
            new_shape = Shape( shapesCopy[ 0 ], BLOCK_SIZE )
            shapesCopy.pop( 0 )
            if self.can_place_anywhere( new_shape ):
                self.availableShapes.append( new_shape )
        self.setPosition(  )

    def setPosition( self ):
        for shapeIndex, shape in enumerate( self.availableShapes ):
            shape.x = 50 + shapeIndex * ( 3 * BLOCK_SIZE + SHAPE_DISTANCE )
            shape.y = 450
            shape.frameX = shape.x
            shape.frameY = shape.y

    def handle_mouse_event( self, event ):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for shape in self.availableShapes:
                shape_rect = pygame.Rect( 
                    shape.x, shape.y,
                    len( shape.shape[ 0 ] ) * shape.block_size,
                    len( shape.shape ) * shape.block_size
                )
                if shape_rect.collidepoint( event.pos ):
                    self.dragging_shape = shape
                    self.drag_offset_x = shape.x - event.pos[ 0 ]
                    self.drag_offset_y = shape.y - event.pos[ 1 ]
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_shape:
                dragShape = self.dragging_shape
                grid_x = ( event.pos[ 0 ] + self.drag_offset_x ) / self.grid.block_size
                grid_y = ( event.pos[ 1 ] + self.drag_offset_y ) / self.grid.block_size
                grid_x = round( grid_x )
                grid_y = round( grid_y ) 
                if grid_x + dragShape.sizeX >= 9 or grid_y + dragShape.sizeY >= 9 or grid_x < 0 or grid_y < 0 or not self.can_place( dragShape, grid_x, grid_y ):
                    dragShape.x = dragShape.frameX
                    dragShape.y = dragShape.frameY
                    self.dragging_shape = None
                    return
                self.place_shape( dragShape, grid_x, grid_y )
                # kill the shape
                self.availableShapes.remove( dragShape )
                self.dragging_shape = None
                if len( self.availableShapes ) == 0:
                    self.populate_shapes(  )

                lines_cleared = self.grid.checkForLines(  )
                self.update_score( lines_cleared )
                self.checkForLoss(  )

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_shape:
                self.dragging_shape.x = event.pos[ 0 ] + self.drag_offset_x
                self.dragging_shape.y = event.pos[ 1 ] + self.drag_offset_y

    def can_place_anywhere( self, shape ):
        for row_index in range( len( self.grid.grid ) ):
            for col_index in range( len( self.grid.grid[ row_index ] ) ):
                if ( row_index + shape.sizeY <= len( self.grid.grid ) and 
                    col_index + shape.sizeX <= len( self.grid.grid[ row_index ] ) and 
                    self.can_place( shape, col_index, row_index ) ):
                    return True
        return False

    def checkForLoss( self ):
        Lost = True
        for shape in self.availableShapes:
            if self.can_place_anywhere( shape ):
                Lost = False
                break
        if Lost:
            pygame.quit(  )
            sys.exit(  )
            
    def can_place( self, shape, grid_x, grid_y ):
        for row_idx, col_idx in shape.get_blocks(  ):
            if not self.grid.can_place( col_idx + grid_x, row_idx + grid_y ):
                return False
        return True

    def place_shape( self, shape, grid_x, grid_y ):
        for row_idx, col_idx in shape.get_blocks(  ):
            self.grid.place_cell( grid_x + col_idx, grid_y + row_idx, shape.color, shape.block_size )

    def renderShapes( self ):
        for shape in self.availableShapes:
            shape.render( self.screen, shape.x, shape.y )

    def render( self ):
        self.screen.fill( WHITE )
        self.grid.render( self.screen )
        self.renderShapes(  )
        self.render_score(  )
        pygame.display.flip(  )

    def update_score( self, lines_cleared ):
        self.score += lines_cleared * 100

    def render_score( self ):
        score_text = self.font.render( f"Score: {self.score}", True, BLACK )
        self.screen.blit( score_text, ( 10, 10 ) )

    def run( self ):
        while self.running:
            for event in pygame.event.get(  ):
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type in ( pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION ):
                    self.handle_mouse_event( event )

            self.render(  )
            self.clock.tick( 60 )

        pygame.quit(  )
        sys.exit(  )

if __name__ == "__main__":
    game = Game(  )
    game.run(  )