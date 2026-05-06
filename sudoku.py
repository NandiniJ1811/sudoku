from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
class Board:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        board_str = ''
        for row in self.board:
            row_str = [str(i) if i else '*' for i in row]
            board_str += ' '.join(row_str)
            board_str += '\n'
        return board_str

    def find_empty_cell(self):
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(9))

    def valid_in_square(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num):
        row, col = empty
        valid_in_row = self.valid_in_row(row, num)
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])

    def solver(self):
        if (next_empty := self.find_empty_cell()) is None:
            return True
        for guess in range(1, 10):
            if self.is_valid(next_empty, guess):
                row, col = next_empty
                self.board[row][col] = guess
                if self.solver():
                    return True
                self.board[row][col] = 0
        return False

@app.route('/')
def index():
    return render_template('sudindex.html')
 
@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    board_input = data.get('board')
 
    # Basic validation
    if not board_input or len(board_input) != 9:
        return jsonify({'solved': False, 'error': 'Invalid board shape.'})
    for row in board_input:
        if len(row) != 9:
            return jsonify({'solved': False, 'error': 'Invalid board shape.'})
 
    # Deep-copy so the original isn't mutated across requests
    import copy
    board_copy = copy.deepcopy(board_input)
 
    gameboard = Board(board_copy)
    if gameboard.solver():
        return jsonify({'solved': True, 'board': gameboard.board})
    return jsonify({'solved': False, 'error': 'This puzzle is unsolvable.'})
 
if __name__ == '__main__':
    app.run(debug=True)