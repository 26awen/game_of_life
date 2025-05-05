import os
import sys
import random
import time

import pygame


# Game environment

CELL_WIDTH = 3
CELL_HEIGHT = 3
CELL_AMOUNT_X = 300
CELL_AMOUNT_Y = 180
SCREEN_WIDTH = CELL_WIDTH * CELL_AMOUNT_X + (CELL_AMOUNT_X - 1)
SCREEN_HEIGHT = CELL_HEIGHT * CELL_AMOUNT_Y + (CELL_AMOUNT_Y - 1)

GIRD_COLOR = "white"

V_GIRD_LINES = tuple(
    (((CELL_WIDTH + 1) * i, 0), ((CELL_WIDTH + 1) * i, SCREEN_HEIGHT))
    for i in range(1, CELL_AMOUNT_X)
)

H_GIRD_LINES = tuple(
    ((0, (CELL_HEIGHT + 1) * i), (SCREEN_WIDTH, (CELL_HEIGHT + 1) * i))
    for i in range(1, CELL_AMOUNT_Y)
)


class Cell:
    def __init__(self, index: int, alive: bool) -> None:
        self.index: int = index
        self.alive: bool = alive
        self.neighbourhood_1: int | None
        self.neighbourhood_2: int | None
        self.neighbourhood_3: int | None
        self.neighbourhood_4: int | None
        self.neighbourhood_5: int | None
        self.neighbourhood_6: int | None
        self.neighbourhood_7: int | None
        self.neighbourhood_8: int | None
        self.line_num: int
        self.x_pos: int
        self.line_num, self.x_pos = divmod(self.index, CELL_AMOUNT_X)

        # Four coners
        # Left Top
        # None                  None                            None
        # None                  self                            self + 1
        # None                  self+line                       self +line + 1
        if self.line_num == 0 and self.x_pos == 0:
            # print("here-1")
            self.neighbourhood_1 = None
            self.neighbourhood_2 = None
            self.neighbourhood_3 = None
            self.neighbourhood_4 = None
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = None
            self.neighbourhood_7 = CELL_AMOUNT_X + self.index
            self.neighbourhood_8 = CELL_AMOUNT_X + self.index + 1
        # Right Top
        # None                  None                            None
        # self - 1              self                            None
        # self + line -1        self+line                       None
        elif self.line_num == 0 and self.x_pos == CELL_AMOUNT_X - 1:
            # print("here-2")
            self.neighbourhood_1 = None
            self.neighbourhood_2 = None
            self.neighbourhood_3 = None
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = None
            self.neighbourhood_6 = CELL_AMOUNT_X + self.index - 1
            self.neighbourhood_7 = CELL_AMOUNT_X + self.index
            self.neighbourhood_8 = None
        # Left Bottom
        # None                  self - line                     self - line + 1
        # None                  self                            self + 1
        # None                  None                            None
        elif self.line_num == CELL_AMOUNT_Y - 1 and self.x_pos == 0:
            # print("here-3")
            self.neighbourhood_1 = None
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = self.index - CELL_AMOUNT_X + 1
            self.neighbourhood_4 = None
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = None
            self.neighbourhood_7 = None
            self.neighbourhood_8 = None
        # Right Bottom
        # self - line -1        self - line                     None
        # self - 1              self                            None
        # None                  None                            None
        elif self.line_num == CELL_AMOUNT_Y - 1 and self.x_pos == CELL_AMOUNT_X - 1:
            self.neighbourhood_1 = self.index - CELL_AMOUNT_X - 1
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = None
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = None
            self.neighbourhood_6 = None
            self.neighbourhood_7 = None
            self.neighbourhood_8 = None
        # Four borders
        # Top
        # None                  None                            None
        # self - 1              self                            self + 1
        # self + line - 1       self+line                       self + line + 1
        elif self.line_num == 0 and (self.x_pos > 0 and self.x_pos < CELL_AMOUNT_X - 1):
            self.neighbourhood_1 = None
            self.neighbourhood_2 = None
            self.neighbourhood_3 = None
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = self.index + CELL_AMOUNT_X - 1
            self.neighbourhood_7 = CELL_AMOUNT_X + self.index
            self.neighbourhood_8 = CELL_AMOUNT_X + self.index + 1
        # Right
        # self - line -1        self - line                     None
        # self - 1              self                            None
        # self + line - 1       self+line                       None
        elif (
            self.line_num > 0 and self.line_num < CELL_AMOUNT_Y - 1
        ) and self.x_pos == CELL_AMOUNT_X - 1:
            self.neighbourhood_1 = self.index - CELL_AMOUNT_X - 1
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = None
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = None
            self.neighbourhood_6 = self.index + CELL_AMOUNT_X - 1
            self.neighbourhood_7 = CELL_AMOUNT_X + self.index
            self.neighbourhood_8 = None
        # Bottom
        # self - line -1        self - line                     self - line + 1
        # self - 1              self                            self + 1
        # None                  None                            None
        elif self.line_num == CELL_AMOUNT_Y - 1 and (
            self.x_pos > 0 and self.x_pos < CELL_AMOUNT_X - 1
        ):
            self.neighbourhood_1 = self.index - CELL_AMOUNT_X - 1
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = self.index - CELL_AMOUNT_X + 1
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = None
            self.neighbourhood_7 = None
            self.neighbourhood_8 = None
        # Left
        # None                  self - line                     self - line + 1
        # None                  self                            self + 1
        # None                  self + line                     self + line + 1
        elif (self.line_num > 0 and self.line_num < CELL_AMOUNT_Y - 1) and (
            self.x_pos == 0
        ):
            self.neighbourhood_1 = None
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = self.index - CELL_AMOUNT_X + 1
            self.neighbourhood_4 = None
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = None
            self.neighbourhood_7 = self.index + CELL_AMOUNT_X
            self.neighbourhood_8 = self.index + CELL_AMOUNT_X + 1
        else:
            self.neighbourhood_1 = self.index - CELL_AMOUNT_X - 1
            self.neighbourhood_2 = self.index - CELL_AMOUNT_X
            self.neighbourhood_3 = self.index - CELL_AMOUNT_X + 1
            self.neighbourhood_4 = self.index - 1
            self.neighbourhood_5 = self.index + 1
            self.neighbourhood_6 = self.index + CELL_AMOUNT_X - 1
            self.neighbourhood_7 = self.index + CELL_AMOUNT_X
            self.neighbourhood_8 = self.index + CELL_AMOUNT_X + 1

        self.neighbourhoods: tuple[int | None, ...] = (
            self.neighbourhood_1,
            self.neighbourhood_2,
            self.neighbourhood_3,
            self.neighbourhood_4,
            self.neighbourhood_5,
            self.neighbourhood_6,
            self.neighbourhood_7,
            self.neighbourhood_8,
        )

    @property
    def rect_pos(self):
        # line_num, x_pos = divmod(self.index, CELL_AMOUNT_X)
        left = self.x_pos * (CELL_WIDTH + 1) + 1
        top = self.line_num * (CELL_HEIGHT + 1) + 1
        width = CELL_WIDTH
        height = CELL_HEIGHT
        return (left, top, width, height)

    def fill(self, surface: pygame.Surface, color="black"):
        if self.alive:
            _ = pygame.draw.rect(surface=surface, color=color, rect=self.rect_pos)

    def clone(self):
        return Cell(self.index, self.alive)


def main():
    print("Hello from game-of-life!")


# c_0 = Cell(101, True)
# c_many = [Cell(random.randint(5, 500), True) for _ in range(50)]
# Set up all cells
c_all = [
    Cell(i, bool(random.randint(0, 1))) for i in range(CELL_AMOUNT_X * CELL_AMOUNT_Y)
]

current_frame = c_all.copy()
next_frame: list[Cell]
begin = False
restart = False
if __name__ == "__main__":
    # pygame setup
    _ = pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    test_index = CELL_AMOUNT_X * CELL_AMOUNT_Y - 120
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    begin = True
                elif event.key == pygame.K_r:
                    current_frame = [
                        Cell(i, bool(random.randint(0, 1)))
                        for i in range(CELL_AMOUNT_X * CELL_AMOUNT_Y)
                    ]

        # fill the screen with a color to wipe away anything from last frame
        _ = screen.fill((201, 201, 201))

        # RENDER YOUR GAME HERE
        for h_line in H_GIRD_LINES:
            # print(h_line)
            _ = pygame.draw.line(
                screen,
                GIRD_COLOR,
                h_line[0],
                h_line[1],
            )
        for v_line in V_GIRD_LINES:
            # print(h_line)
            _ = pygame.draw.line(
                screen,
                GIRD_COLOR,
                v_line[0],
                v_line[1],
            )

        if not begin:
            continue

        for c in current_frame:
            if c.alive:
                c.fill(screen)
        # time.sleep(0.5)

        next_frame = [c.clone() for c in current_frame]
        for i in range(len(current_frame)):
            neighbourhood_alive_count = 0
            for n in current_frame[i].neighbourhoods:
                if n:
                    if current_frame[n].alive:
                        neighbourhood_alive_count += 1
            if current_frame[i].alive:
                if neighbourhood_alive_count < 2:
                    next_frame[i].alive = False
                elif neighbourhood_alive_count >= 2 and neighbourhood_alive_count <= 3:
                    pass
                elif neighbourhood_alive_count > 3:
                    next_frame[i].alive = False
            else:
                if neighbourhood_alive_count == 3:
                    next_frame[i].alive = True

        current_frame = next_frame
        # Test running scnning
        # for n in c_all[test_index].neighbourhoods:
        #     print(c_all[test_index].neighbourhoods)
        #     if n:
        #         c_all[n].alive = True
        #         c_all[n].fill(screen)
        # test_index += 1
        # time.sleep(0.1)

        # Test 2
        # for c in c_all:
        #     c.alive = random.randint(0, 1) == 1
        #
        # for c in c_all:
        #     c.fill(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        _ = clock.tick(60)  # limits FPS to 60

    pygame.quit()
