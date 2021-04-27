from ursina import *
from helper import *
from config import *
import numpy as np

GAME_STATE = np.zeros((4, 4, 4), dtype=np.int16)


class Board:
    def __init__(self):
        self.floor = Entity(
            model="cube",
            name="board",
            collider="box",
            texture=TEXTURE_BOARD,
            scale=Vec3(X, Y, Z)
        )

        self.text = Text(
            text="Your Turn",
            y=.45,
            x=-.85,
            background=True
        )

        self.walls = list()
        for sides in range(4):
            self.walls.append(Entity(
                model='cube',
                collider="box",
                name="board_wall",
                parent=self.floor,
                texture=TEXTURE_BOARD
            ))
        self.walls[0].scale = Vec3(0.2 / X, 1, 1)
        self.walls[0].world_position = Vec3(3.8, 0.2, 0)
        self.walls[1].scale = Vec3(0.2 / X, 1, 1)
        self.walls[1].world_position = Vec3(-3.8, 0.2, 0)
        self.walls[2].scale = Vec3(1, 1, 0.2 / Z)
        self.walls[2].world_position = Vec3(0, 0.2, 3.8)
        self.walls[3].scale = Vec3(1, 1, 0.2 / Z)
        self.walls[3].world_position = Vec3(0, 0.2, -3.8)

        # Creation of the boards sticks
        self.sticks = list()
        for i in range(4):
            for j in range(4):
                self.sticks.append(Entity(
                    parent=self.floor,
                    name=str(i) + str(j),
                    model="cube",
                    collider="box",
                    on_click=logic,
                    texture=TEXTURE_STICKS,
                    scale=Vec3(0.2 / X, 3.5 * (1 / Y), 0.2 / Z),
                    world_position=Vec3(i - (3 - i), 1.75, j - (3 - j))
                ))

        # Creation of a golden marker which is hidden at first but will soon indicate where the last action took place
        self.marker = Entity(
            parent=self.floor,
            model="cube",
            collider="box",
            color=color.gold,
            scale=Vec3(0.21 / X, 0.1 / Y, 0.21 / Z),
            world_position=Vec3(10, 10, 10)
        )

    def add_sphere(self, player, row, column, height):
        self.spheres.append(Entity(
            parent=self.floor,
            model="sphere",
            name="ball",
            collider="sphere",
            texture=TEXTURE_C if player == C else TEXTURE_H,
            scale=Vec3((1 / X) * 4 / 5, (1 / Y) * 4 / 5, (1 / Z) * 4 / 5),
            world_position=Vec3(row - (3 - row), height * 0.77 + 0.5, column - (3 - column))
        ))


app = Ursina()

# Creating the interface
window.title = "3D4Wins"
window.borderless = False
EditorCamera()
camera.world_y += 1
camera.world_z -= 2

board = Board()


def logic():
    player = fetch_player(GAME_STATE)

    if player == H:
        row = int(mouse.hovered_entity.name[0])
        column = int(mouse.hovered_entity.name[1])
        height = 4 - GAME_STATE[row][column].count(E)
        if height == 4:
            return

    elif player == C:
        best_action = minimax(GAME_STATE)
        row = best_action[0]
        column = best_action[1]
        height = best_action[2]

    # Add sphere
    board.add_sphere(player, row, column, height)
    # Set marker over used pole
    board.marker.world_position = Vec3(row - (3 - row), 3.75 * 0.77 + 0.5, column - (3 - column))
    # Update game_state
    GAME_STATE[row][column][height] = player

    # Check if terminal, if yes end game and sent winner message and set RUNNING to False
    status = terminal(GAME_STATE)
    if status is not None:
        running = False
        if status == -1:
            corner_text.text = "The mere mortal claimed victory."
        elif status == 1:
            corner_text.text = "Computer won."
        else:
            corner_text.text = "It's a draw."
    else:
        if player == H:
            corner_text.text = "Computer thinking..."
        else:
            corner_text.text = "Your turn!"
    corner_text.background = True


app.run()