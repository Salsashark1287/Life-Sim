import pygame
import sys
from entities import *
import random

crabs =[]
foods = []
# ---Configuration___
FIELD_SIZE = 900
UI_WIDTH = 300
GRID_SIZE = 20
CELL_SIZE = FIELD_SIZE // GRID_SIZE
SCREEN_WIDTH = FIELD_SIZE + UI_WIDTH
SCREEN_HEIGHT = FIELD_SIZE


#Colors(R, G, B)
COLOR_BG = (225, 198, 153)
COLOR_GRID = (225, 198, 153)
COLOR_FOOD = (120, 255, 70)
COLOR_UI_BG = (40, 40, 45)
COLOR_TEXT = (255, 255, 255)

def main():



    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Life Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)
    header_font = pygame.font.SysFont('Arial', 32, bold=True)
    
    def draw_text(text, x, y, current_font = font):
        img = current_font.render(text, True, COLOR_TEXT)
        screen.blit(img, (x,y))

    def is_location_valid(x,y, existing_foods):
        neighbor_count = 0
        for food in existing_foods:
            if abs(food.x - x) <= 1 and abs(food.y - y) <= 1:
                neighbor_count += 1
        return neighbor_count <= 2

    for i in range (10):
        #Spawn crabs at random locations to start
        start_x = random.randint(0, GRID_SIZE - 1)
        start_y = random.randint(0, GRID_SIZE - 1)
        new_crab = Crab(start_x, start_y,)
        new_crab.is_newborn = False
        crabs.append(new_crab)

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
        for i in range(1 + len(foods)//5):
            new_x = random.randint(0, GRID_SIZE - 1)
            new_y = random.randint(0, GRID_SIZE - 1)

            if is_location_valid(new_x, new_y, foods):
                foods.append(Food(new_x, new_y))

        for i, crab in enumerate (crabs[:]):
            crab.health -= 1
            if crab.health <= 0:
                crabs.remove(crab)
            if crab.health > 8 and crab.mating_cooldown == 0:
                crab.wants_to_mate = True
            crab.move(GRID_SIZE, foods, crabs)
            for food in foods[:]:
                if crab.x == food.x and crab.y == food.y:
                    crab.health += 6
                    foods.remove(food)
            for partner in crabs[i+1:]:
                if crab.x == partner.x and crab.y == partner.y and crab.health >= 5 and partner.health >= 5:
                    if crab.mating_cooldown == 0 and partner.mating_cooldown == 0:
                        baby = crab.reproduce(partner)
                        crabs.append(baby)
            if crab.mating_cooldown > 0:
                crab.mating_cooldown -= 1 
            if crab.is_newborn == True and crab.mating_cooldown <= 0:
                crab.is_newborn = False
            crab.health -= 1
        for food in foods:
            food.update()
            if food.is_rotten == True:
                foods.remove(food)
            

        #3. Draw
        screen.fill(COLOR_BG)
        ui_rect = pygame.Rect(FIELD_SIZE, 0, UI_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, COLOR_UI_BG, ui_rect)#DRAW INFORMATION WINDOW
        pygame.draw.line(screen, (0,0,0), (FIELD_SIZE, 0), (FIELD_SIZE, SCREEN_HEIGHT), 3) #DRAW BORDER
        total_crabs_count = len(crabs)
        newborn_count = len([c for c in crabs if c.is_newborn])
        adult_count = total_crabs_count - newborn_count
        avg_sight = 0
        avg_max_health = 0
        if total_crabs_count > 0:
            avg_sight = sum(c.sight for c in crabs) // total_crabs_count
            avg_max_health = sum(c.max_health for c in crabs) // total_crabs_count

        for food in foods:
            rect = (food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_FOOD, rect)

        for crab in crabs:
            if crab.is_newborn:
                dynamic_color = (255, 165, 0)
            else:
                #Dynamic crab color based on health
                health_factor = max(0, min(20, crab.health))
                tint = 200 - (health_factor * 10)
                dynamic_color = (255, tint, tint)
            #Multiply grid position by CELL_SIZE to get pixel position
            padding = 2#Keeps crabs from touching sides of grid
            w = CELL_SIZE -(padding * 2) #sets the width of crabs
            h = int(w*.7) #sets height of crabs
            off_y =(CELL_SIZE - h) // 2 #Centers crabs vertically in cell
            oval_rect = (crab.x * CELL_SIZE + padding, crab.y * CELL_SIZE + off_y, w, h)
            pygame.draw.ellipse(screen, dynamic_color, oval_rect)
            pygame.draw.ellipse(screen, "black", oval_rect, 2)

        #Draw the grid lines
        for x in range(0, FIELD_SIZE, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (x,0), (x, FIELD_SIZE))
        for y in range(0, FIELD_SIZE, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (0,y), (FIELD_SIZE, y))

        draw_text("Ecosystem Stats", FIELD_SIZE + 20, 20, header_font)
        draw_text(f"Total Crabs: {total_crabs_count}", FIELD_SIZE + 20, 80)
        draw_text(f"Adults: {adult_count}", FIELD_SIZE + 40, 120)
        draw_text(f"Newborns: {newborn_count}", FIELD_SIZE + 40, 155)
        draw_text(f"Avg Sight: {avg_sight:}", FIELD_SIZE + 20, 200)
        draw_text(f"Avg Max Health: {avg_max_health:}", FIELD_SIZE + 20, 240)
        draw_text(f"Food Count: {len(foods)}", FIELD_SIZE + 20, 280)
        
        pygame.display.flip()
        clock.tick(5) #Sets fps
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()