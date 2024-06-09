'''
Backtracking es una técnica para resolver problemas de manera recursiva.
Se utiliza principalmente para encontrar todas las soluciones posibles a un problema dado mediante la construcción
de soluciones paso a paso y descartando aquellas soluciones que no satisfacen las restricciones del problema.

Cómo Funciona
Construcción de Soluciones Parciales: Se construye una solución paso a paso.
Verificación de Restricciones: En cada paso, se verifica si la solución parcial cumple con las restricciones del problema.
Retroceso (Backtrack): Si una solución parcial no cumple con las restricciones, se retrocede al paso anterior y se intenta
con una solución diferente.
Exploración Completa: Este proceso continúa hasta que todas las soluciones posibles han sido exploradas.
'''

def is_safe(board, row, col, num):
    # Verificar si el número ya está en la fila
    for x in range(9):
        if board[row][x] == num:
            return False

    # Verificar si el número ya está en la columna
    for x in range(9):
        if board[x][col] == num:
            return False

    # Verificar si el número ya está en la subcuadrícula 3x3
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def solve_sudoku(board):
    #print_board(board)
    empty = find_empty_location(board)
    if not empty:
        return True  # No hay más ubicaciones vacías, se resolvió el Sudoku
    row, col = empty

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Deshacer el cambio (backtrack)

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))

def main():
    # Ejemplo de un Sudoku parcialmente completado
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    if solve_sudoku(board):
        print_board(board)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()
