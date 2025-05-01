import random
import time
from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("Maze Solver")
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close())
        self.widget = Canvas(bg="white")
        self.widget.pack()
        self.running = False


    def draw_line(self, line, color):
        line.draw(self.widget, color)

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, color):
        canvas.create_line(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y,
            fill=color,
            width=2
        )


class Cell:
    def __init__(self, left, top, right, bottom, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = left
        self._x2 = right
        self._y1 = top
        self._y2 = bottom
        self._win = window
        self.visited = False

    def draw(self):
        if self.has_left_wall:
            self._win.widget.create_line(
                self._x1,
                self._y1,
                self._x1,
                self._y2,
                fill="black",
                width=2
            )
        if self.has_top_wall:
            self._win.widget.create_line(
                self._x1,
                self._y1,
                self._x2,
                self._y1,
                fill="black",
                width=2,
                tag="top_wall"
            )
        if self.has_right_wall:
            self._win.widget.create_line(
                self._x2,
                self._y1,
                self._x2,
                self._y2,
                fill="black",
                width=2
            )
        if self.has_bottom_wall:
            self._win.widget.create_line(
                self._x1,
                self._y2,
                self._x2,
                self._y2,
                fill="black",
                width=2
            )

    def draw_move(self, to_cell, undo=False):
        self._win.widget.create_line(
            self._x1 + ((self._x2 - self._x1) / 2),
            self._y1 + ((self._y2 - self._y1) / 2),
            to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2),
            to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2),
            fill="gray" if undo else "red",
            width=2
        )


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = random.seed(0) if seed is None else random.seed(seed)
        self._create_cells()
        self._break_walls_r(int(self.num_cols / 2), int(self.num_rows / 2))

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            self._cells.append([])
            for j in range(self.num_rows):
                self._cells[i].append(Cell(
                    self.x1 + (self.cell_size_x * i),
                    self.y1 + (self.cell_size_y * j),
                    self.x1 + self.cell_size_x + (self.cell_size_x * i),
                    self.y1 + self.cell_size_y + (self.cell_size_y * j),
                    self.win
                ))
                if i == 0 and j == 0:
                    self._cells[i][j].has_top_wall = False
                if i == self.num_cols - 1 and j == self.num_rows - 1:
                    self._cells[i][j].has_bottom_wall = False
                self._draw_cell(i, j)

    def _draw_cells(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].draw()
        self._animate()

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while not self._cells[0][0].visited or not self._cells[self.num_cols - 1][self.num_rows - 1].visited:
            to_visit = []
            if i - 1 >= 0 and not self._cells[i - 1][j].visited:
                to_visit.append([i - 1, j])
            if i + 1 < self.num_cols and not self._cells[i + 1][j].visited:
                to_visit.append([i + 1, j])
            if j - 1 >= 0 and not self._cells[i][j - 1].visited:
                to_visit.append([i, j - 1])
            if j + 1 < self.num_rows and not self._cells[i][j + 1].visited:
                to_visit.append([i, j + 1])
            if not to_visit:
                return
            next_indices = to_visit[random.randrange(len(to_visit))]
            if next_indices[0] == i:
                if next_indices[1] < j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_indices[0]][next_indices[1]].has_bottom_wall = False
                else:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_indices[0]][next_indices[1]].has_top_wall = False
            else:
                if next_indices[0] < i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_indices[0]][next_indices[1]].has_right_wall = False
                else:
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_indices[0]][next_indices[1]].has_left_wall = False
            self.win.widget.delete("all")
            self._draw_cells()
            self._break_walls_r(next_indices[0], next_indices[1])

def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 10, 10, 10, 10, win, random.randrange(10))
    win.wait_for_close()


main()