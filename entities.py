import random

class Crab:
    def __init__(self, x, y, health=None, sight=None, speed=None):
        self.x = x
        self.y = y
        self.is_newborn = True
        #For starting crabs that don't inherit health parameter
        #Roll for random starting health
        if health is None:
            health_options = [18, 19, 20, 21, 22, 23, 24, 25]
            health_weights = [4.5, 8, 12.5, 25, 25, 12.5, 8, 4.5]
            self.max_health = random.choices(health_options, weights=health_weights, k=1)[0]
            self.health = self.max_health
        else:
            self.health = health
            self.max_health = health
        #Doing the same for sight
        if sight is None:
            sight_options = [0,1,2,3,4,5,6,7,8]
            sight_weights = [1.5,4,10,17,35,17,10,4,1.5]
            self.sight = random.choices(sight_options, weights=sight_weights, k=1)[0]
        else: 
            self.sight = sight
        self.mating_cooldown = 30
        self.wants_to_mate = False
        if speed is None:
            speed_options = [1,2,3]
            speed_weights = [80, 15, 5]
            self.speed = random.choices(speed_options, weights=speed_weights, k=1)[0]
        else:
            self.speed = speed
    


    def move(self, grid_size, foods, crabs):
        target = None
        closest_dist = self.sight + self.speed

        if self.wants_to_mate:#set target to other crabs 
            for other in crabs:
                if other == self: continue
                dist = abs(other.x - self.x) + abs(other.y - self.y)
                if dist < closest_dist:
                    closest_dist = dist
                    target = other

        if target == None:
            closest_dist = self.sight + self.speed
        for food in foods:
            #Calculate distance to nearest food
            dist = abs(food.x - self.x) + abs(food.y - self.y)

            if dist <= self.sight and dist<closest_dist:
                closest_dist = dist
                target = food
        #Decide how to move
        for speed in range(self.speed):
            if target:
                #Move toward food
                if target.x > self.x: self.x +=  1
                elif target.x < self.x: self.x -= 1
                elif target.y > self.y: self.y += 1
                elif target.y < self.y: self.y -=  1
            else:
                #Crab doesn't see food, moves randomly
                axis = random.choice(['x', 'y']) #Chooses to move up/down or left/right
                step = random.choice([-1* self.speed, self.speed]) #Chooses which way to move on chosen axis

                if axis == 'x':
                    self.x += step
                else:
                    self.y += step

        #Keep them inside the boundaries
        self.x = max(0, min(self.x, grid_size - 1))
        self.y = max(0, min(self.y, grid_size - 1))

    
    def reproduce(self, partner):
        #Inherit sight from parents
        low_s = min(self.sight, partner.sight)
        high_s = max(self.sight, partner.sight)
        baby_sight = random.randint((low_s * 3) // 4, (high_s * 3) // 2)
        if random.random() <= 0.25: # 10% chance to mutate sight
            baby_sight += random.choice([-1, 1])
            baby_sight = max(1, baby_sight) #No blind babies

        #Inherit health
        low_h = min(self.health, partner.health)
        high_h = max(self.health, partner.health)
        baby_health = random.randint((low_h * 3)//4, (high_h * 3)//2)
        if random.random() <= .25:
            baby_health += random.choice([-1,1])
            baby_health = max(1, baby_health) #No stillborn babies

        #Inherit speed
        low_sp = min(self.speed, partner.speed)
        high_sp = max(self.speed, partner.speed)
        baby_sp = random.randint((low_sp*3)//4, (high_sp * 3)//2)
        if random.random() <= .25:
            baby_sp += random.choice([-1, 1])
        baby_sp = max(1, baby_sp)

        baby = Crab(self.x, self.y, health=baby_health, sight=baby_sight, speed=baby_sp)

        self.health -= 3
        partner.health -= 3
        self.mating_cooldown = 30
        partner.mating_cooldown = 30
        self.wants_to_mate = False
        partner.wants_to_mate = False
        

        return baby


class Food:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.fresh = random.randint(15, 20)
        self.is_rotten = False

    def update(self):
        self.fresh -= 1
        if self.fresh <= 0:
            self.is_rotten = True