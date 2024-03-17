import pygame

class Piece:
    def __init__(self,screen,color,piece_type,position):
        self.screen = screen
        self.color = color
        self.piece_type = piece_type
        self.position = position
        self.selected = False
        self.image = pygame.image.load(f"assets/{self.color}/{self.piece_type}.png")
        self.image = pygame.transform.scale(self.image, (75, 75))  # Resize image to fit 75x75 square
        self.isMoved = False
    def draw(self):
        # calculate position on screen based on board position
        x = self.position[0] * 75
        y = self.position[1] * 75
        self.screen.blit(self.image, (x, y))
    
    def move(self, new_position,board):
        isValid = self.ValidateMove(self.position,new_position,board.pieces_position,board)
        if isValid:
            self.isMoved = True
            # Remove the piece from its old position
            del board.pieces_position[self.position]
            board.pieces.remove(self)
            
            # as there is no chace the validate Move return true
            existing_piece = board.pieces_position.get(new_position)
            if existing_piece is not None:
                # as move is valid and there is a existing piece in that new_position 
                # then that means this pawn is capturing that piece
                # remove that piece board and place this pawn in that position
                board.pieces.remove(existing_piece)
                
            if self.piece_type == "pawn" and new_position[1] == 0 or new_position[1] == 7:
                #promote pawn to queen
                QueenPiece = Piece(self.screen, self.color, "queen", new_position)
                #replace pawn with queen in pieces list and pieces_position dict
                board.pieces.remove(self)
                board.pieces.append(QueenPiece)
                #update pieces_position dict
                board.pieces_position[new_position] = QueenPiece
                board.pieces_position.pop(self.position, None)
            else:
                #if there is a piece we are capturing we removed it
                #if there is a promotion to queen we done it
                # all that left is directly movement               
                self.position = new_position
                board.pieces.append(self)
                board.pieces_position[new_position] = self
            
            #check if this piece in its new position is giving check to opponentking
            Opponentking = board.black_king if self.color == "white" else board.white_king
            #check if the king is under attack
            if self.ValidateMove(self.position,new_position,board.pieces_position,board):
                board.king_under_attack = Opponentking
            
            board.draw()
            #pygame.display.flip()
            
            
    def ValidateMove(self,old_position,new_position,pieces_position,board):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position
        # Check if the new position is outside the board boundaries
        if not (0 <= new_x < 8 and 0 <= new_y < 8):
            return False
        isValid = False
        if self.piece_type == "pawn":
            isValid = self.ValidatePawnMove(old_position,new_position,pieces_position)
        elif self.piece_type == "rook":
            isValid = self.ValidateRookMove(old_position,new_position,pieces_position)
        elif self.piece_type == "bishop":
            isValid = self.ValidateBishopMove(old_position,new_position,pieces_position)
        elif self.piece_type == "knight":
            isValid = self.ValidateKnightMove(old_position,new_position,pieces_position)
        elif self.piece_type == "queen":
            isValid = self.ValidateQueenMove(old_position,new_position,pieces_position)
        elif self.piece_type == "king":
            isValid = self.ValidateKingMove(old_position,new_position,pieces_position,board)
        
        return isValid
    
    def ValidatePawnMove(self, old_position, new_position, pieces_position):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position
        
        direction = 1 if self.color == "white" else -1
        
        # check if its really possible to move to new position
        diff_col = new_x - old_x
        diff_row = new_y - old_y
        
        if not ((direction > 0 and diff_row > 0) or (direction < 0 and diff_row < 0 )):
            # Pawn can only move forward, not backwards
            return False
        
        if diff_col > 1 or diff_row > 2:
            # the square to which pawn is moving is not accessable to pawn
            return False
        if diff_col == 0:
            #pawn is moving forward
            if abs(diff_row) == 2:
                #checking if pawn is moving two positions forward
                #check if the pawn is in its starting position
                #check if there are no pieces in the squares it is moving
                if self.color == "white" and old_y != 1:
                    return False
                if self.color == "black" and old_y != 6:
                    return False
                piece = pieces_position.get((old_x, old_y + direction), None) or pieces_position.get((old_x, old_y + 2*direction), None)
                if piece is None:
                    return True
            elif abs(diff_row) == 1:
                #we only need to check that there are no pieces in that position
                piece = pieces_position.get((old_x, old_y + direction), None)
                if piece is None:
                    return True
        else:
            #if difference in column is greater than one then it is trying to capture a oppenet piece
            #check if there is a piece in the position, if there is check its color
            piece = pieces_position.get((new_x, new_y), None)
            if piece and piece.color != self.color:
                return True

        return False  
    
    def ValidateRookMove(self, old_position, new_position, pieces_position):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position

        # check if its really possible to move to new position
        diff_col = new_x - old_x
        diff_row = new_y - old_y
        
        if (diff_col!= 0 and diff_row !=0) or diff_row==diff_col:
            # Rook can only move horizontally or vertically
            return False
        #if the movement is in the same row or column then it is possible to move
        #check if there are any pieces in between the old position and new position
        if diff_col == 0:
            # Rook is traveling in columns
            if old_y < new_y:
                for i in range(old_y + 1, new_y):
                    piece = pieces_position.get((old_x, i), None)
                    if piece:
                        return False
            else:
                for i in range(new_y + 1, old_y):
                    piece = pieces_position.get((old_x, i), None)
                    if piece:
                        return False
            if old_x < new_x:
                for i in range(old_x + 1, new_x):
                    piece = pieces_position.get((i, old_y), None)
                    if piece:
                        return False
            else:
                for i in range(new_x + 1, old_x):
                    piece = pieces_position.get((i, old_y), None)
                    if piece:
                        return False
        elif diff_row == 0:
            # Rook is traveling in rows
            if old_x < new_x:
                for i in range(old_x + 1, new_x):
                    piece = pieces_position.get((i, old_y), None)
                    if piece:
                        return False
            else:
                for i in range(new_x + 1, old_x):
                    piece = pieces_position.get((i, old_y), None)
                    if piece:
                        return False
        # we have checked for pieces in between but piece on new position
        piece = pieces_position.get((new_x, new_y), None)
        if piece and piece.color == self.color:
            return False
        
        # as it came to this line and statisified all the conditions upto here then we can assume
        # that the move is valid
        return True
    
    def ValidateBishopMove(self,old_position,new_position,pieces_position):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position

        # check if its really possible to move to new position
        diff_col = new_x - old_x
        diff_row = new_y - old_y
        
        #bishop travells diagonally so diff_col and diff_row should be equal
        if abs(diff_col)!= abs(diff_row):
            return False
        #if the movement is in the same row or column then it is possible to move
        #check if there are any pieces in between the old position and new position
        direction_col = 1 if new_x > old_x else -1
        direction_row = 1 if new_y > old_y else -1
        for i in range(1,abs(diff_col)):
            piece = pieces_position.get((old_x + i*direction_col, old_y + i*direction_row), None)
            if piece:
                return False
        # we have checked for pieces in between but piece on new position
        piece = pieces_position.get((new_x, new_y), None)
        if piece and piece.color == self.color:
            return False
        # as there are no pieces in the way then it means that the move is valid
        return True
    
    def ValidateKnightMove(self,old_position,new_position,pieces_position):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position

        # Knights can move in L shapes - 2 squares in one direction, 1 square perpendicular
        diff_x = abs(new_x - old_x) 
        diff_y = abs(new_y - old_y)

        if (diff_x == 2 and diff_y == 1) or (diff_x == 1 and diff_y == 2):
            # Check if knight is trying to capture piece of same color
            piece = pieces_position.get(new_position)
            if piece is not None and piece.color == self.color:
                return False
            
            # If no same color piece on new pos, move is valid
            return True

        # Not a valid L shaped knight move
        return False
    
    def ValidateQueenMove(self,old_position,new_position,pieces_position):
        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position

        # Queens can move horizontally, vertically and diagonally
        # Check horizontal/vertical movement
        if old_x == new_x or old_y == new_y:
            # Movement is in same row or column
            return self.ValidateRookMove(old_position, new_position, pieces_position)
        
        # Check diagonal movement
        elif abs(old_x - new_x) == abs(old_y - new_y):
            return self.ValidateBishopMove(old_position, new_position, pieces_position)

        # Not a valid horizontal, vertical or diagonal movement
        return False
    def ValidateKingMove(self, old_position, new_position, pieces_position, board):
        # Kings can move 1 square in any direction

        # Extract old and new coordinates
        old_x, old_y = old_position
        new_x, new_y = new_position

        # Check that new position is only 1 square away 
        diff_x = abs(new_x - old_x)
        diff_y = abs(new_y - old_y)
        if diff_x > 1 or diff_y > 1:
            return False

        # Check if landing on square of same color
        piece = pieces_position.get(new_position)
        if piece is not None and piece.color == self.color:
            return False

        # Check if king is castling
        if self.is_castling_move(old_position, new_position):
            return self.validate_castling(old_position, new_position, pieces_position, board)

        # If checks passed, valid move
        return True
    def is_castling_move(self, old_pos, new_pos):
        # Castling can only happen horizontally
        if old_pos[1] != new_pos[1]:
            return False

        # Get king's starting column
        if self.color == "white":
            king_start_col = 4 
        else:
            king_start_col = 3
        
        # Check if king is moving two squares
        if abs(old_pos[0] - new_pos[0]) == 2:
            if old_pos[0] < new_pos[0]:
                # Kingside castling
                return new_pos[0] == king_start_col + 2
            else:
                # Queenside castling
                return new_pos[0] == king_start_col - 2
        
        return False
    def validate_castling(self, old_pos, new_pos, pieces_position,board):
        # we need to sure our king is not under attack
        # we need to be sure that rook and king are not moved
        # we need to make sure there are no pieces between king and rook
        # we need to be sure that there is no opposite player pieces which are attacking
        # the squares between king and the rook which is getting castled
        # Check if king is in check
        if board.king_under_attack == self:
            return False

        # Get rook based on castling direction
        if new_pos[0] < old_pos[0]: # Queenside
            rook = board.get_queenside_rook(self.color)
        else: # Kingside
            rook = board.get_kingside_rook(self.color)

        # Make sure rook hasn't moved
        if rook is None or rook.has_moved:
            return False

        # Make sure no pieces between rook and king
        for col in range(old_pos[0] + 1, new_pos[0]):
            if pieces_position.get((col, old_pos[1]),None) is not None:
                return False

        # Make sure no opponent piece attacks empty squares
        for piece in board.get_opponent_pieces(self.color):
            if piece.color == self.color:
                continue
            # Check if piece is attacking empty squares
            for col in range(old_pos[0] + 1, new_pos[0]):
                if piece.ValidateMove(piece.position,(col, old_pos[1]), board.pieces_position,board):
                    return False
        
        return True  