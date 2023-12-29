import pygame
import math
from pginput import InputBox

# constant based on lidar resolution
LIDAR_RESOLUTION = 360
# Constant screen width
SCREEN_WIDTH = 800
# Selected positions in a frame (result of the Sklearn SelectKBest function)
DECISIVE_FRAME_POSITIONS = [24, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 46, 50, 51, 150, 156, 202, 206,
                            212, 213, 324, 330, 333, 335, 337, 359]


def get_data_from_arduino(line):
    d_list = line.split(",")
    return d_list


def run():
    pygame.init()
    clock = pygame.time.Clock()
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_WIDTH])
    # Set up the font
    font = pygame.font.Font(None, 32)
    # FONT = pygame.font.Font(None, 32)

    input_box1 = InputBox(350, 650, 140, 32, font)
    input_box2 = InputBox(350, 700, 140, 32, font)
    input_boxes = [input_box1, input_box2]

    file1 = open('./data/run2/out.txt', 'r')

    lines = file1.readlines()
    running = True
    counter = 0
    paused = False
    inspect_mode = False

    while counter < len(lines):
        line = lines[counter]
        if inspect_mode:
            paused = True
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    # print('PAUSE STATUS: {}'.format(paused))
                elif event.key == pygame.K_i:
                    """
                    Press 'i' keyboard will turn on inspection mode,
                    which run frame by frame
                    """
                    inspect_mode = not inspect_mode
                    # print('INSPECT MODE: {}'.format(inspect_mode))
                elif event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.QUIT:
                # Press 'X' button on window will close the program
                running = False

            # handle input box event
            for box in input_boxes:
                box.handle_event(event)

        if not running:
            break
        # elif paused:
        #     continue

        distances = get_data_from_arduino(line)
        # print(len(distances))
        if len(distances) == LIDAR_RESOLUTION + 1:
            # Fill the background with white
            screen.fill((250, 250, 250))

            for x in range(LIDAR_RESOLUTION):
                # depend on the average distance, divide distance with a constant for better view
                a = float(distances[x]) / 3
                if x in DECISIVE_FRAME_POSITIONS:
                    # Draw the important point with RED color
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (math.cos(x / 180 * math.pi) * a + SCREEN_WIDTH / 2,
                                        math.sin(x / 180 * math.pi) * a + SCREEN_WIDTH / 2),
                                       3)
                else:
                    # Draw the ordinary point with BLACK color
                    pygame.draw.circle(screen, (0, 0, 0),
                                       (math.cos(x / 180 * math.pi) * a + SCREEN_WIDTH / 2,
                                        math.sin(x / 180 * math.pi) * a + SCREEN_WIDTH / 2),
                                       2)
                    # print('Position x:{}, y:{}'
                    #       .format(line_positions[x][0] * a + 400, line_positions[x][1] * a + 400))

            # draw input boxes on screen
            if not input_box1.active:
                input_box1.set_text(distances[360])
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(screen)

            # Render the text
            text = font.render("line: {}, turn: {:.2f}".format(counter, float(distances[360])), True, (0, 255, 255))
            # Blit the text to the screen
            screen.blit(text, (350, 600))

            # draw the car
            pygame.draw.circle(screen, (252, 132, 3), (SCREEN_WIDTH/2, SCREEN_WIDTH/2), 12)
            pygame.draw.line(screen, (0, 0, 255), (SCREEN_WIDTH/2, SCREEN_WIDTH/2),
                             (SCREEN_WIDTH/2 + 40, SCREEN_WIDTH/2), 3)
            x = math.cos(float(distances[360]) * math.pi / 4) * 40
            y = math.sin(float(distances[360]) * math.pi / 4) * 40
            pygame.draw.line(screen, (0, 255, 0), (SCREEN_WIDTH / 2, SCREEN_WIDTH / 2),
                             (SCREEN_WIDTH/2 + x, SCREEN_WIDTH/2 + y), 3)
            # Flip the display
            pygame.display.flip()
            clock.tick(10)

            if not paused:
                counter += 1

    pygame.quit()


if __name__ == '__main__':
    run()
