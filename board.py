import pygame
from piece import Piece
class Board:
    def __init__(self,screen):
        self.screen = screen
        self.square_size = 75
        self.board_size = self.square_size * 8
        self.white_king = None
        self.black_king = None   
        self.pieces = self.initialize_pieces()
        self.pieces_position = {piece.position:piece for piece in self.pieces}
        self.piece_selected = None
        self.king_under_attack = None
        
    def initialize_pieces(self):
        pieces = []
        # Add white pieces
        #column and row
        pieces.append(Piece(self.screen, "white", "rook", (0, 0)))
        pieces.append(Piece(self.screen, "white", "knight", (1, 0)))
        pieces.append(Piece(self.screen, "white", "bishop", (2, 0)))
        pieces.append(Piece(self.screen, "white", "queen", (3, 0)))
        pieces.append(Piece(self.screen, "white", "bishop", (5, 0)))
        pieces.append(Piece(self.screen, "white", "knight", (6, 0)))
        pieces.append(Piece(self.screen, "white", "rook", (7, 0)))
        self.white_king = Piece(self.screen, "white", "king", (4, 0))
        pieces.append(self.white_king)
        for i in range(8):
            pieces.append(Piece(self.screen, "white", "pawn", (i, 1)))

        # Add black pieces
        pieces.append(Piece(self.screen, "black", "rook", (0, 7)))
        pieces.append(Piece(self.screen, "black", "knight", (1, 7)))
        pieces.append(Piece(self.screen, "black", "bishop", (2, 7)))
        pieces.append(Piece(self.screen, "black", "queen", (3, 7)))
        pieces.append(Piece(self.screen, "black", "bishop", (5, 7)))
        pieces.append(Piece(self.screen, "black", "knight", (6, 7)))
        pieces.append(Piece(self.screen, "black", "rook", (7, 7)))
        self.black_king = Piece(self.screen, "black", "king", (4, 7))
        pieces.append(self.black_king)
        for i in range(8):
            pieces.append(Piece(self.screen, "black", "pawn", (i, 6)))

        return pieces
        
    def draw_board(self):
        colors = [(210, 180, 140), (255, 222, 173)]  # Brown and Beige colors
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen,color,(col*self.square_size,row*self.square_size,self.square_size,self.square_size))
    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw()
            
    def draw(self):
        self.draw_board()
        self.draw_pieces()
    
    def handle_click(self,mouse_position):
        #calculate which square was clicked
        x,y = mouse_position
        row = y // self.square_size
        col = x // self.square_size
        #get the piece at that position
        piece = self.pieces_position.get((col,row))
        if self.piece_selected is None and piece is not None:
            self.piece_selected = piece
            self.piece_selected.selected = True
            return
        elif self.piece_selected is not None and self.piece_selected == piece:
            self.piece_selected.selected = False
            self.piece_selected = None
            return
        elif self.piece_selected is not None:
            self.piece_selected.move((col,row),self)
            self.piece_selected = None
            return
        
    def get_queenside_rook(self,color):
        Piece = None
        if color == "white":
            Piece = self.pieces_position.get((0,0),None)
        elif color == "black":
            Piece = self.pieces_position.get((0,7),None)
        if Piece is not None and Piece.piece_type == "rook":
            return Piece
        else:
            return None
    def get_kingside_rook(self,color):
        Piece = None
        if color == "white":
            Piece = self.pieces_position.get((7,0),None)
        elif color == "black":
            Piece = self.pieces_position.get((7,7),None)
        if Piece is not None and Piece.piece_type == "rook":
            return Piece
        else:
            return None
            