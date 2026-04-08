import random

class Crab:
    def __init__(self, x, y, health=None, sight=None, speed=None, lifespan=None):
        self.x = x
        self.y = y
        self.is_newborn = True
        self.age = 0

        #For starting crabs that don't inherit health parameter
        #Roll for random starting health
        if health is None:
            health_options = [28, 29, 30, 31, 32, 33, 34, 35]
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
        
        if lifespan is None:
            lifespan_options = [100, 110, 120, 130, 140, 150]
            lifespan_weights = [20, 30, 20, 15, 10, 5]
            self.lifespan = random.choices(lifespan_options, weights=lifespan_weights, k=1)[0]
        else:
            self.lifespan = lifespan
    


    def move(self, grid_size, foods, crabs):
        target = None
        closest_dist = self.sight + self.speed

        if self.wants_to_mate and self.health > (self.max_health * .8):#set target to other crabs 
            closest_dist = self.sight + self.speed
            for other in crabs:
                if other == self or not other.wants_to_mate: continue
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

                if self.x == target.x and self.y == target.y:
                    break

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
        baby_sight = random.randint(low_s, high_s)
        if random.random() <= 0.25: # 10% chance to mutate sight
            baby_sight += random.choice([-1, 1])
            baby_sight = max(1, baby_sight) #No blind babies

        #Inherit health
        low_h = min(self.max_health, partner.max_health)
        high_h = max(self.max_health, partner.max_health)
        baby_health = random.randint(low_h, high_h)
        if random.random() <= .25:
            baby_health += random.choice([-1,1])
            baby_health = max(1, baby_health) #No stillborn babies

        #Inherit speed
        low_sp = min(self.speed, partner.speed)
        high_sp = max(self.speed, partner.speed)
        baby_sp = random.randint(low_sp, high_sp)
        if random.random() <= .25:
            baby_sp += random.choice([-1, 1])
        baby_sp = max(1, baby_sp)

        #Inherit lifespan
        low_ls = min(self.lifespan, partner.lifespan)
        high_ls = max(self.lifespan, partner.lifespan)
        baby_ls = random.randint(low_ls, high_ls)
        if random.random() <= .25:
            baby_ls += random.choice([-10, 10])
        baby_ls = max(50, baby_ls)

        baby = Crab(self.x, self.y, health=baby_health, sight=baby_sight, speed=baby_sp, lifespan = baby_ls)

        self.mating_cooldown = 15
        partner.mating_cooldown = 15
        self.wants_to_mate = False
        partner.wants_to_mate = False
        

        return baby


class Food:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 


