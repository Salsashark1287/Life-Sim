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



    def reset():
        crabs.clear()
        foods.clear()
        for i in range (10):
            #Spawn crabs at random locations to start
            start_x = random.randint(0, GRID_SIZE - 1)
            start_y = random.randint(0, GRID_SIZE - 1)
            new_crab = Crab(start_x, start_y,)
            new_crab.is_newborn = False
            crabs.append(new_crab)

        while len(foods) < 25:
            f_x = random.randint(0, GRID_SIZE - 1)
            f_y = random.randint(0, GRID_SIZE - 1)
            if is_location_valid(f_x, f_y, foods):
                foods.append(Food(f_x, f_y))

    def draw_text(text, x, y, current_font = font):
        img = current_font.render(text, True, COLOR_TEXT)
        screen.blit(img, (x,y))

    def is_location_valid(x,y, existing_foods):
        neighbor_count = 0
        for food in existing_foods:
            if abs(food.x - x) <= 1 and abs(food.y - y) <= 1:
                neighbor_count += 1
        return neighbor_count <= 2

    reset()
    is_paused = False #pause flag
    selected_crab = None #tracks which crab has been clicked on 
    wave_y = -1#Current row wave is on (-1 = no wave)
    wave_timer = 0#Controls speed of wave
    WAVE_SPEED= 2 #How many ticks before wave advances 1 row
    running = True


    

    while running:
        # 1. Input/Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused = not is_paused #Toggle
                if event.key == pygame.K_r:
                    reset()
                    is_paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    mouse_x, mouse_y = event.pos

                    #Check if the click is inside FIELD_SIZE
                    if mouse_x < FIELD_SIZE:
                        #Convert pixels to grid coords
                        grid_x = mouse_x // CELL_SIZE
                        grid_y = mouse_y // CELL_SIZE

                        #Check if crab is at that location
                        found_selection = False
                        for crab in crabs:
                            if crab.x == grid_x and crab.y == grid_y:
                                selected_crab = crab
                                found_selection = True
                                break

                        #if no crab at coords, deselect
                        if not found_selection:
                            selected_crab =  None
                

        #2. Update 
        if not is_paused:
            #Food spawns
            for i in range(5 + len(foods)//4):
                new_x = random.randint(0, GRID_SIZE - 1)
                new_y = random.randint(0, GRID_SIZE - 1)
                 if is_location_valid(new_x, new_y, foods):
                    foods.append(Food(new_x, new_y))

            #Waves come in and take crabs out to sea
            if wave_y == -1 and random.random() < 0.01:
                wave_y = GRID_SIZE - 1 #wave starts at bottom of grid
                wave_timer = 0
            if wave_y != -1:
                wave_timer += 1
                if wave_timer >= WAVE_SPEED:
                    for crab in crabs[:]:
                        if crab.y == wave_y:
                            if selected_crab == crab:
                                selected_crab = None
                            crabs.remove(crab)
                    wave_y -= 1 #move wave up 1 row
                    wave_timer = 0
                    if wave_y < GRID_SIZE // 2:
                        wave_y = -1

            #Crabs move toward food, or other crabs to mate
            if len(crabs) == 0:
                is_paused = True
            for i, crab in enumerate (crabs[:]):
                crab.health -= 1
                crab.age += 1
                if crab.health <= 0 or crab.age >= crab.lifespan:
                    crabs.remove(crab)
                    continue
                if crab.health > (crab.max_health * .5) and crab.mating_cooldown == 0:
                    crab.wants_to_mate = True
                crab.move(GRID_SIZE, foods, crabs)
                for food in foods[:]:
                    if crab.x == food.x and crab.y == food.y:
                        if crab.health + 12 < crab.max_health:
                            crab.health += 12
                        else:
                            crab.health = crab.max_health
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
                

        #3. Draw
        screen.fill(COLOR_BG)
        if wave_y != -1:
            water_height = (GRID_SIZE - wave_y) * CELL_SIZE #Calculate the pixel height of the water
            water_rect = pygame.Rect(0, wave_y* CELL_SIZE, FIELD_SIZE, water_height)
            surf = pygame.Surface((FIELD_SIZE, water_height), pygame.SRCALPHA) #Create semi-transparent water
            surf.fill((0, 105, 148, 150))#Blue with 150 Alpha
            screen.blit(surf, (0, wave_y * CELL_SIZE))
            pygame.draw.line(screen, (255, 255, 255), (0, wave_y * CELL_SIZE), (FIELD_SIZE, wave_y * CELL_SIZE), 3)

        ui_rect = pygame.Rect(FIELD_SIZE, 0, UI_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, (30, 30, 35), ui_rect)#DRAW INFORMATION WINDOW
        header_bg_height = 60
        header_bg_rect = pygame.Rect(FIELD_SIZE, 0, UI_WIDTH, header_bg_height)
        pygame.draw.rect(screen, (60, 60, 70), header_bg_rect)
        pygame.draw.line(screen, (0,0,0), (FIELD_SIZE, header_bg_height), (FIELD_SIZE + UI_WIDTH, header_bg_height), 2)
        pygame.draw.line(screen, (0,0,0), (FIELD_SIZE, 0), (FIELD_SIZE, SCREEN_HEIGHT), 3) #DRAW BORDER
        total_crabs_count = len(crabs)
        newborn_count = len([c for c in crabs if c.is_newborn])
        adult_count = total_crabs_count - newborn_count
        avg_sight = 0
        avg_max_health = 0
        if total_crabs_count > 0:
            avg_sight = sum(c.sight for c in crabs) // total_crabs_count
            avg_max_health = sum(c.max_health for c in crabs) // total_crabs_count
            avg_speed =sum(c.speed for c in crabs)// total_crabs_count

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

        #Draw Paused/Running Status
        status_text = "PAUSED" if is_paused else "RUNNING"
        status_color = (255, 100, 100) if is_paused else (100, 255, 100)
        status_img = font.render(f"Status : {status_text}", True, status_color)
        screen.blit(status_img, (FIELD_SIZE + 20, 750))

        #Draw information box
        draw_text("Ecosystem Stats", FIELD_SIZE + 20, 20, header_font)
        draw_text(f"Total Crabs: {total_crabs_count}", FIELD_SIZE + 20, 80)
        draw_text(f"Adults: {adult_count}", FIELD_SIZE + 20, 120)
        draw_text(f"Newborns: {newborn_count}", FIELD_SIZE + 20, 155)
        draw_text(f"Avg Sight: {avg_sight:}", FIELD_SIZE + 20, 200)
        draw_text(f"Avg Max Health: {avg_max_health:}", FIELD_SIZE + 20, 240)
        draw_text(f"Avg Speed: {avg_speed:}", FIELD_SIZE + 20, 280)
        draw_text(f"Food Count: {len(foods)}", FIELD_SIZE + 20, 320)
        draw_text(f"Pause : Space | R : Reset", FIELD_SIZE + 20, 800)
        
        if selected_crab and selected_crab in crabs: #Makes sure selcted crab is still alive
            current_y = 400
            draw_text(f"Health: {selected_crab.health}/{selected_crab.max_health}", FIELD_SIZE + 40, current_y)
            draw_text(f"Lifespan: {selected_crab.age}/{selected_crab.lifespan}", FIELD_SIZE + 40, current_y + 35)
            draw_text(f"Sight: {selected_crab.sight}", FIELD_SIZE + 40, current_y + 70)
            draw_text(f"Speed: {selected_crab.speed}", FIELD_SIZE + 40, current_y +105)
        elif selected_crab:
            #if selected crab is dead
            selected_crab = None

        pygame.display.flip()
        clock.tick(5) #Sets fps
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()