from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("Maze Solver")
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close())
        self.widget = Canvas()
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
    def __init__(self, left, top, right, bottom, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = left
        self.x2 = right
        self.y1 = top
        self.y2 = bottom
        self.win = window

    def draw(self):
        if self.has_left_wall:
            self.win.widget.create_line(
                self.x1,
                self.y1,
                self.x1,
                self.y2,
                fill="black",
                width=2
            )
        if self.has_top_wall:
            self.win.widget.create_line(
                self.x1,
                self.y1,
                self.x2,
                self.y1,
                fill="black",
                width=2
            )
        if self.has_right_wall:
            self.win.widget.create_line(
                self.x2,
                self.y1,
                self.x2,
                self.y2,
                fill="black",
                width=2
            )
        if self.has_bottom_wall:
            self.win.widget.create_line(
                self.x1,
                self.y2,
                self.x2,
                self.y2,
                fill="black",
                width=2
            )

def main():
    win = Window(800, 600)
    cell = Cell(10, 10, 30, 30, win)
    cell.draw()
    win.wait_for_close()


main()