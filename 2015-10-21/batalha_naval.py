#!/usr/bin/env python

import itertools
import unittest
import random


class BattleShipTest(unittest.TestCase):
    def test_board_size(self):
        game = BattleShip()
        assert game.get_size() == 100

    def test_ships_qt(self):
        game = BattleShip()
        assert len(game.get_all_ships()) == 10

    def test_create_board(self):
        board = Board(10, 10)
        assert board.cols == 10
        assert board.rows == 10

    def test_create_board_small(self):
        board = Board(2, 3)
        matrix = [[0, 0],
                  [0, 0],
                  [0, 0]]
        assert board.matrix == matrix

    def test_create_matrix(self):
        matrix = [[0 for i in range(10)] for j in range(10)]
        board = Board(10, 10)
        assert board.matrix == matrix

    def test_ship_init_count(self):
        board = Board(10, 10)
        flat_board = list(itertools.chain(*board.matrix))
        assert flat_board.count(0) == 100

    def test_ship_count_with_ships(self):
        board = Board(10, 10)
        board.add_ships(_random=False)
        flat_board = list(itertools.chain(*board.matrix))
        for key, value in Board.ships.items():
            self.assertEqual(value, flat_board.count(key))

    def test_validatepos(self):
        board = Board(10, 10)
        self.assertTrue(board.validate_pos(0, 0))
        board.matrix[2][3] = 1
        self.assertFalse(board.validate_pos(2, 3))

    def test_constants(self):
        self.assertEqual(Board.CARRIER, 1)
        self.assertEqual(Board.BATTLESHIP, 2)
        self.assertEqual(Board.DESTROYER, 3)
        self.assertEqual(Board.SUBMARINE, 4)
        self.assertEqual(Board.PATROL_BOAT, 5)

    def test_miss_attack(self):
        board = Board(10, 10)
        self.assertEqual(board.receive_attack(0, 0), False)

    def test_hit_attack(self):
        board = Board(10, 10)
        board.add_ships()
        self.assertEqual(board.receive_attack(0, 0), True)

    def test_empty_attack_list(self):
        board = Board(10, 10)
        self.assertEqual(len(board.attacks), 0)

    def test_insert_attack_list_empty_board(self):
        board = Board(10, 10)
        board.receive_attack(0, 0)
        self.assertEqual(board.attacks[0], (0, 0, False))

    def test_insert_attack_list_full_board(self):
        board = Board(10, 10)
        board.add_ships()
        board.receive_attack(0, 0)
        self.assertEqual(board.attacks[0], (0, 0, True))

    def test_gameover_false(self):
        board = Board(10, 10)
        board.add_ships()
        self.assertFalse(board.game_over())

    def test_plot_board(self):
        board = Board(10, 10)
        board_str = """------------
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
|~~~~~~~~~~|
------------"""

class Board(object):

    CARRIER = 1
    BATTLESHIP = 2
    DESTROYER = 3
    SUBMARINE = 4
    PATROL_BOAT = 5

    ships = {
        CARRIER: 5,   # porta-avioes
        BATTLESHIP: 4,   # encouracado
        DESTROYER: 3,   # destroier
        SUBMARINE: 3,   # submarino
        PATROL_BOAT: 2    # barco de patrulha
    }

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.create_matrix()
        self.attacks = []

    def add_ships(self, _random=False):
        if _random:
            pass
            # fazer coisas bonitinhas
        else:
            i = 0
            for key, value in self.ships.items():
                for idx in range(value):
                    self.matrix[idx][i] = key
                i += 1


    def validate_pos(self, x, y):
        return self.matrix[x][y] == 0

    def create_matrix(self):
        self.matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]

    def receive_attack(self, col, row):
        value = self.matrix[col][row]
        self.attacks.append((col, row, bool(value)))
        return bool(value)

    def game_over(self):
        shipcount = sum(self.ships.values())
        hitcount = len(filter(lambda x: x[2], set(self.attacks)))
        return hitcount == shipcount

class BattleShip(object):
    size = [10, 10]
    boards = ()

    def get_size(self):
        return self.size[0] * self.size[1]

    def get_all_ships(self):
        return range(10)

    def create_board(self):
        return [self.size[0], self.size[1]]


if __name__ == '__main__':
    unittest.main()
