import pygame
import sys
from entities import *
import random

# ---Configuration___
SCREEN_SIZE = 900
GRID_SIZE = 20
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

#Colors(R, G, B)
COLOR_BG = (30, 30, 30)
COLOR_GRID = (50, 50, 50)
COLOR_CRAB =(255, 100, 100)
COLOR_FOOD =(100, 255, 100)

def main():

    def is_location_valid(x,y, existing_foods):
        neighbor_count = 0
        for food in existing_foods:
            if abs(food.x - x) <= 1 and abs(food.y - y) <= 1:
                neighbor_count += 1
        return neighbor_count <= 2

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Life Sim")
    clock = pygame.time.Clock()
    crabs = []
    for i in range (10):
        #Spawn five crabs at random locations to start
        start_x = random.randint(0, GRID_SIZE - 1)
        start_y = random.randint(0, GRID_SIZE - 1)
        crabs.append(Crab(start_x, start_y))
    foods = []
    while len(foods) < 15:
        f_x = random.randint(0, GRID_SIZE - 1)
        f_y = random.randint(0, GRID_SIZE - 1)
        if is_location_valid(f_x, f_y, foods):
            foods.append(Food(f_x, f_y))
    running = True


    

    while running:
        # 1. Input/Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #2. Update 
        for i in range(1 + len(foods)//4):
            new_x = random.randint(0, GRID_SIZE - 1)
            new_y = random.randint(0, GRID_SIZE - 1)

            if is_location_valid(new_x, new_y, foods):
                foods.append(Food(new_x, new_y))

        for i, crab in enumerate (crabs[:]):
            if crab.is_alive == False:
                crabs.remove(crab)
            if crab.health > 8 and crab.mating_cooldown == 0:
                crab.wants_to_mate = True
            crab.move(GRID_SIZE, foods, crabs)
            for food in foods[:]:
                if crab.x == food.x and crab.y == food.y:
                    crab.health += 8
                    foods.remove(food)
            for partner in crabs[i+1:]:
                if crab.x == partner.x and crab.y == partner.y and crab.health >= 5 and partner.health >= 5:
                    if crab.mating_cooldown == 0 and partner.mating_cooldown == 0:
                        baby = crab.reproduce(partner)
                        crabs.append(baby)
            if crab.mating_cooldown > 0:
                crab.mating_cooldown -= 1 
            crab.health -= 1
        for food in foods:
            food.update()
            if food.is_rotten == True:
                foods.remove(food)
            

        #3. Draw
        screen.fill(COLOR_BG)
        for food in foods:
            rect = (food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_FOOD, rect)

        for crab in crabs:
            #Multiply grid position by CELL_SIZE to get pixel position
            rect = (crab.x * CELL_SIZE, crab.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_CRAB, rect)

        #Draw the grid lines
        for x in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (x,0), (x, SCREEN_SIZE))
        for y in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (0,y), (SCREEN_SIZE, y))
        
        pygame.display.flip()
        clock.tick(2) #Sets fps
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()