import enum
import random
import numpy as np


class Piece(enum.Enum):
    Red = 'r'
    Green = 'g'
    Orange = 'o'
    Blue = 'b'
    Yellow = 'y'
    White = 'w'


class Face(enum.Enum):
    Red = 'R'
    Green = 'G'
    Orange = 'O'
    Blue = 'B'
    Yellow = 'Y'
    White = 'W'


class Side(enum.Enum):
    Front = 0
    Right = 1
    Back = 2
    Left = 3
    Top = 4
    Bottom = 5


class Cube:
    def __init__(self, faces=None):
        if faces is None:
            self.faces = {
                Face.Red: [[Piece.Red for _ in range(3)] for _ in range(3)],
                Face.Green: [[Piece.Green for _ in range(3)] for _ in range(3)],
                Face.Orange: [[Piece.Orange for _ in range(3)] for _ in range(3)],
                Face.Blue: [[Piece.Blue for _ in range(3)] for _ in range(3)],
                Face.Yellow: [[Piece.Yellow for _ in range(3)] for _ in range(3)],
                Face.White: [[Piece.White for _ in range(3)] for _ in range(3)],
            }

        self.sides = {
            Side.Front: Face.Red,
            Side.Right: Face.Green,
            Side.Back: Face.Orange,
            Side.Left: Face.Blue,
            Side.Top: Face.Yellow,
            Side.Bottom: Face.White,
        }

        self.instruction_set = {
            "U": [self.U, ["U2", "U"]],
            "x": [self.x, ["x2", "x"]],
            "y": [self.y, ["y2", "y"]],
            "z": [self.z, ["z2", "z"]],

            'D': [['x2', 'U', 'x2'], ['x2', "U'", 'x2']],
            'R': [["z'", 'U', 'z'], ["z'", "U'", 'z']],
            'L': [['z', 'U', "z'"], ['z', "U'", "z'"]],
            'F': [['x', 'U', "x'"], ['x', "U'", "x'"]],
            'B': [["x'", 'U', 'x'], ["x'", 'U', 'x']],
            'M': [["L'", 'R', "x'"], ['L', "R'", 'x']],
            'u': [['D', 'y'], ["D'", "y'"]],
            'd': [['U', "y'"], ["U'", 'y']],
            'r': [['L', 'x'], ["L'", "x'"]],
            'l': [['R', 'x'], ["R'", "x'"]],
        }

    def print(self):
        for side in self.sides.values():
            for row in self.faces[side]:
                print('  |  '.join([piece.value for piece in row]))
                print('—  ┼  —  ┼  —')
            print()

    def execute(self, instructions):
        if len(instructions) == 0:
            return

        instruction_index = 1 if (instruction := instructions.pop(0))[-1] == "'" else 0

        if instruction[-1] == "2":
            instructions.insert(0, instruction[0])

        if type(decoded_instruction := self.instruction_set[instruction[0]][instruction_index]) is list:
            instructions = decoded_instruction + instructions
        else:
            decoded_instruction()

        return self.execute(instructions)

    def scramble(self):
        scramble = []
        for _ in range(40):
            scramble.append(random.choice(list(self.instruction_set.keys())))
        print(' '.join(scramble))
        self.execute(scramble)

    def rotate_clockwise_90(self, side_name, k=1):
        self.faces[self.sides[side_name]] = np.rot90(self.faces[self.sides[side_name]], 4-k)

    def cycle_sides(self, sides):
        buffer = self.sides[sides[0]]
        self.sides[sides[0]] = self.sides[sides[1]]
        self.sides[sides[1]] = self.sides[sides[2]]
        self.sides[sides[2]] = self.sides[sides[3]]
        self.sides[sides[3]] = buffer

    def U(self):
        """
        This move method effectively only makes a U move. Other moves can be produced later by performing cube
        rotations that will change which faces this move method will affect.
        :return: None
        """

        buffer = self.faces[self.sides[Side.Front]][0].copy()  # Save the front in a buffer as it will be lost otherwise

        # Row rotations
        self.faces[self.sides[Side.Front]][0] = self.faces[self.sides[Side.Right]][0].copy()
        self.faces[self.sides[Side.Right]][0] = self.faces[self.sides[Side.Back]][0].copy()
        self.faces[self.sides[Side.Back]][0] = self.faces[self.sides[Side.Left]][0].copy()
        self.faces[self.sides[Side.Left]][0] = buffer

        # Top face Rotation
        self.rotate_clockwise_90(Side.Top, 1)

    def x(self):

        # Side Rotations
        cycles = [Side.Front, Side.Bottom, Side.Back, Side.Top]
        self.cycle_sides(cycles)

        # Face Rotations
        rotations = [[Side.Right, 1], [Side.Back, 2], [Side.Left, 3], [Side.Bottom, 2]]
        for side, rotations in rotations:
            self.rotate_clockwise_90(side, rotations)

    def y(self):

        # Side Rotations
        cycles = [Side.Front, Side.Right, Side.Back, Side.Left]
        self.cycle_sides(cycles)

        # Face Rotations
        rotations = [[Side.Top, 1], [Side.Bottom, 3]]
        for side, rotations in rotations:
            self.rotate_clockwise_90(side, rotations)

    def z(self):

        # Side Cycles
        cycles = [Side.Right, Side.Top, Side.Left, Side.Bottom]
        self.cycle_sides(cycles)

        # Face Rotations
        rotations = [[Side.Front, 1], [Side.Right, 1], [Side.Back, 3], [Side.Left, 1], [Side.Top, 1], [Side.Bottom, 1]]
        for side, rotations in rotations:
            self.rotate_clockwise_90(side, rotations)


class CustomCube(Cube):
    def __init__(self):
        # function that allows user to input their own maybe?
        self.faces = {
            Face.Red: [[Piece[input()] for _ in range(3)] for _ in range(3)],
            Face.Green: [[Piece[input()] for _ in range(3)] for _ in range(3)],
            Face.Orange: [[Piece[input()] for _ in range(3)] for _ in range(3)],
            Face.Blue: [[Piece[input()] for _ in range(3)] for _ in range(3)],
            Face.Yellow: [[Piece[input()] for _ in range(3)] for _ in range(3)],
            Face.White: [[Piece[input()] for _ in range(3)] for _ in range(3)],
        }
        super().__init__(faces)


if __name__ == '__main__':
    cube = Cube()
    cube.execute("y' x2 L D2 U B U R F B2 L' D2 L F2 D' F' R' F D2 L' D L2".split(' '))
    cube.print()
    cube.execute("F' U' F D' R' B L U2 R F2 U R2 B D L2 F2 U' D2 L2 F2".split(' '))
    cube.print()
