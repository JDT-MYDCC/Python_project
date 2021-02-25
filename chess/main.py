import pygame
from constants import *
from board import *


def draw_window(win, board, valid_moves, turn):
    board.draw(win)
    board.draw_valid_moves(win, valid_moves, board.board, turn)
    for i in range(8):
        for j in range(8):
            if board.board[i][j] != 0:
                if turn != board.board[i][j].color:
                    board.board[i][j].draw(win)

    for i in range(8):
        for j in range(8):
            if board.board[i][j] != 0:
                if turn == board.board[i][j].color:
                    board.board[i][j].draw(win)

    pygame.display.update()

def get_pos(m_x, m_y):
    for i in range(8):
        for j in range(8):
            if m_x >= j * W and m_x <= j * W + W and m_y >= i * W and m_y <= i * W + W:
                return j, i

def change_turn(turn):
    if turn == BLACK:
        turn = WHITE
    else:
        turn = BLACK
    return turn


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChessL")
    board = Board()
    clock = pygame.time.Clock()
    selected_pos = ()
    valid_moves = []
    played_moves = []
    returned_moves = []
    seleceted = False
    turn = WHITE
    run = True
    while run:
        clock.tick(60)
        draw_window(win, board, valid_moves, turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if played_moves:
                        zug = played_moves.pop()
                        end, start = zug[0], zug[1]
                        returned_moves.append(zug)
                        board.move(start, end)
                        # board.print_board()
                        turn = change_turn(turn)

                if event.key == pygame.K_RIGHT:
                    if returned_moves:
                     zug = returned_moves.pop()
                     end, start = zug[0], zug[1]
                     played_moves.append(zug)
                     print(start, end)
                     # board.print_board()
                     board.move(start, end)
                     turn = change_turn(turn)


            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    seleceted = True
                    for j in range(8):
                        for i in range(8):
                            if board.board[i][j] != 0:
                                x, y = pygame.mouse.get_pos()
                                if board.board[i][j].onclick(x, y):
                                    board.board[i][j].selected = True
                                    selected_pos = (i, j)
                                    if board.board[selected_pos[0]][selected_pos[1]].color == turn:
                                        for move in board.board[i][j].get_valid_moves(board.board):
                                            if board.is_legal_move(turn, (selected_pos[0], selected_pos[1]), move):
                                                valid_moves.append(move)


            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                x, y = get_pos(m_x, m_y)    
                selected = False
                if selected_pos:
                    # check who's turn
                    if turn == board.board[selected_pos[0]][selected_pos[1]].color:
                        if (x, y) != selected_pos:
                            if (x, y) in valid_moves:
                                if board.board[x][y] == 0 or board.board[x][y].color != board.board[selected_pos[0]][selected_pos[1]].color:
                                    move_text = board.move(selected_pos, (x, y))
                                    if returned_moves:
                                        if selected_pos != returned_moves[-1]:
                                            returned_moves = []

                                    played_moves.append([selected_pos, (x, y)])
                                    if isinstance(board.board[x][y], Rook):
                                        board.board[x][y].castled = True

                                    if isinstance(board.board[x][y], King):
                                        if turn == WHITE:
                                            if not board.board[x][y].castled:
                                                # o-o
                                                if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O:
                                                    if board.board[7][7] != 0:
                                                        if not board.board[7][7].castled:
                                                            board.move((7, 7), (5, 7))
                                                            board.board[x][y].castled = True
                                                            board.board[5][7].castled = True
                                                # o-o-o
                                                elif board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O_O:
                                                    if board.board[0][7] != 0:
                                                        if not board.board[0][7].castled:
                                                            board.move((0, 7), (3, 7))
                                                            board.board[x][y].castled = True
                                                            board.board[3][7].castled = True


                                        else:
                                            if not board.board[x][y].castled:
                                                # o-o
                                                if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O:
                                                    if board.board[7][0] != 0:
                                                        if not board.board[7][0].castled:
                                                            board.move((7, 0), (5, 0))
                                                            board.board[x][y].castled = True
                                                            board.board[5][0].castled = True
                                                # o-o-o
                                                elif board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O_O:
                                                    if board.board[0][0] != 0:
                                                        if not board.board[0][0].castled:
                                                            board.move((0, 0), (3, 0))
                                                            board.board[x][y].castled = True
                                                            board.board[3][0].castled = True

                                    if isinstance(board.board[x][y], Pawn):
                                        board.board[x][y].first = False
                                    turn = change_turn(turn)
                                    if board.check(BLACK):
                                        print("black checks!")
                                    if board.check(WHITE):
                                        print("white checks!")
                                    if board.checkmate(BLACK):
                                        print("black checkmate!")
                                        main()
                                    if board.checkmate(WHITE):
                                        print("white checkmate!")
                                        main()
                                    print()
                                    board.print_board()
                                    print(move_text)
                                    
                                elif board.board[x][y].color == board.board[selected_pos[0]][selected_pos[1]].color:
                                    board.board[selected_pos[0]][selected_pos[1]].col = selected_pos[0]
                                    board.board[selected_pos[0]][selected_pos[1]].row = selected_pos[1]
                            else:
                                board.board[selected_pos[0]][selected_pos[1]].col = selected_pos[0]
                                board.board[selected_pos[0]][selected_pos[1]].row = selected_pos[1]

                    else:
                        board.board[selected_pos[0]][selected_pos[1]].col = selected_pos[0]
                        board.board[selected_pos[0]][selected_pos[1]].row = selected_pos[1]
                    board.set_every_pos()
                    # board.set_every_coord()
                    board.unselectall()
                valid_moves = []
                selected_pos = ()
            
            if event.type == pygame.MOUSEMOTION:
                if seleceted:
                    x, y = event.pos
                    img_x = x - W / 2
                    img_y = y - W / 2
                    for j in range(8):
                        for i in range(8):
                            if board.board[i][j] != 0:
                                if board.board[i][j].selected:
                                    board.board[i][j].x = img_x
                                    board.board[i][j].y = img_y

main()