import random

class Crab:
    def __init__(self, x, y, health=None, sight=None):
        self.x = x
        self.y = y
        self.is_alive = True

        #For starting crabs that don't inherit health parameter
        #Roll for random starting health
        if health is None:
            health_options = [16, 17, 18, 19, 20, 21, 22, 23]
            health_weights = [4.5, 8, 12.5, 25, 25, 12.5, 8, 4.5]
            self.health = random.choices(health_options, weights=health_weights, k=1)[0]
        else:
            self.health = health
        #Doing the same for sight
        if sight is None:
            sight_options = [0,1,2,3,4,5,6,7,8]
            sight_weights = [1.5,4,10,17,35,17,10,4,1.5]
            self.sight = random.choices(sight_options, weights=sight_weights, k=1)[0]
        self.mating_cooldown = 30
        self.wants_to_mate = False


    def move(self, grid_size, foods, crabs):
        target = None
        
        if self.wants_to_mate:#set target to other crabs 
            closest_dist = self.sight + 1
            for other in crabs:
                if other == self: continue
                dist = abs(other.x - self.x) + abs(other.y - self.y)
                if dist < closest_dist:
                    closest_dist = dist
                    target =(other.x, other.y)

        for food in foods:
            #Calculate distance to nearest food
            closest_dist = self.sight + 1
            dist = abs(food.x - self.x) + abs(food.y - self.y)

            if dist <= self.sight and dist<closest_dist:
                closest_dist = dist
                target = food
        #Decide how to move
        if target:
            #Move toward food
            if target.x > self.x: self.x += 1
            elif target.x < self.x: self.x -= 1
            elif target.y > self.y: self.y += 1
            elif target.y < self.y: self.y -= 1
        else:
            #Crab doesn't see food, moves randomly
            axis = random.choice(['x', 'y']) #Chooses to move up/down or left/right
            step = random.choice([-1, 1]) #Chooses which way to move on chosen axis

            if axis == 'x':
                self.x += step
            else:
                self.y += step

        #Keep them inside the boundaries
        self.x = max(0, min(self.x, grid_size - 1))
        self.y = max(0, min(self.y, grid_size - 1))

        #Crabs lose health when moving
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False
    
    def reproduce(self, partner):
        #Inherit sight from parents
        low_s = min(self.sight, partner.sight)
        high_s = max(self.sight, partner.sight)
        baby_sight = random.randint(low_s, high_s)
        if random.random() < 0.1: # 10% chance to mutate sight
            baby_sight += random.choice([-1, 1])
            baby_sight = max(1, baby_sight) #No blind babies

        #Inherit health
        low_h = min(self.health, partner.health)
        high_h = max(self.health, partner.health)
        baby_health = random.randint(low_h, high_h)
        if random.random() < .1:
            baby_health += random.choice([-1,1])
            baby_health = max(1, baby_health) #No stillborn babies

        baby = Crab(self.x, self.y, health=baby_health, sight=baby_sight)

        self.health -= 5
        partner.health -= 5
        self.mating_cooldown = 30
        partner.mating_cooldown = 30
        

        return baby


class Food:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.fresh = random.randint(4, 8)
        self.is_rotten = False

    def update(self):
        self.fresh -= 1
        if self.fresh <= 0:
            self.is_rotten = True