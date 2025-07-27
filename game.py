import pyxel
import random

class Game:
    def __init__(self):
        self.level = 1
        self.total_score = 0
        self.game_over = False
        self.win = False
        self.ball_x = 10
        self.ball_y = 100
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.gravity = 0.3
        self.friction = 0.5
        self.is_jumping = False
        self.particles = []
        self.coins = []
        self.platforms = [] # Initialize empty, will be filled by _generate_level
        self.enemies = []   # Initialize empty, will be filled by _generate_level
        self.finish = (0,0,0,0) # Placeholder, will be set by _generate_level

    def reset_ball_position(self):
        # Resets ball position and speed for current level
        self.ball_x = 10
        self.ball_y = 100
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.is_jumping = False

    def update(self, skin):
        if self.game_over or self.win:
            if pyxel.btnp(pyxel.KEY_R):
                # If game over or win, reset game completely (new game)
                self.level = 1
                self.total_score = 0
                self.game_over = False
                self.win = False
                self._generate_level() # Generate first level
                self.reset_ball_position() # Reset ball for new level
            elif pyxel.btnp(pyxel.KEY_M):
                return "menu"
            elif pyxel.btnp(pyxel.KEY_L):
                return "leaderboard"
            return None

        # ==== Update Game State ====
        self.ball_speed_y += self.gravity
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Kontrol bola dan gesekan horizontal
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ball_speed_x = -2
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.ball_speed_x = 2
        else:
            if self.ball_speed_x > 0:
                self.ball_speed_x = max(0, self.ball_speed_x - self.friction)
            elif self.ball_speed_x < 0:
                self.ball_speed_x = min(0, self.ball_speed_x + self.friction)

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.ball_speed_y = -5
            self.is_jumping = True
            for _ in range(5):
                self.particles.append([self.ball_x, self.ball_y + 4, random.uniform(-1, 1), random.uniform(-1, -3), 4]) # warna kuning

        # Batas layar
        if self.ball_x < 0:
            self.ball_x = 0
            self.ball_speed_x = 0
        if self.ball_x > pyxel.width - 4:
            self.ball_x = pyxel.width - 4
            self.ball_speed_x = 0
        if self.ball_y < 0:
            self.ball_y = 0
            self.ball_speed_y = 0

        # Update Platform Bergerak
        for platform in self.platforms:
            if platform[4] == "moving_h":
                platform[0] += platform[5]
                # Ensure platform stays within screen bounds (or its defined range)
                if platform[0] <= platform[6] or platform[0] + platform[2] >= platform[7]:
                    platform[5] *= -1

            elif platform[4] == "moving_v":
                platform[1] += platform[5]
                # Ensure platform stays within screen bounds (or its defined range)
                if platform[1] <= platform[6] or platform[1] + platform[3] >= platform[7]:
                    platform[5] *= -1

        # Cek tabrakan dengan platform
        on_platform = False
        for platform in self.platforms:
            if (
                self.ball_x + 4 >= platform[0]
                and self.ball_x - 4 <= platform[0] + platform[2]
                and self.ball_y + 4 >= platform[1]
                and self.ball_y + 4 <= platform[1] + platform[3] + 1
                and self.ball_speed_y >= 0
            ):
                if platform[4] in ["moving_h", "moving_v"]:
                    self.ball_x += platform[5]

                self.ball_y = platform[1] - 4
                self.ball_speed_y = 0
                self.is_jumping = False
                on_platform = True
                break

        if not on_platform and self.ball_speed_y >= 0:
            self.is_jumping = True

        # Update Musuh Bergerak
        for enemy in self.enemies:
            enemy_type = enemy[4]
            if enemy_type == "horizontal":
                enemy[0] += enemy[5]
                if enemy[0] <= enemy[6] or enemy[0] + enemy[2] >= enemy[7]:
                    enemy[5] *= -1
            elif enemy_type == "chase":
                if abs(self.ball_x - (enemy[0] + enemy[2]/2)) < 50: # Hanya mengejar jika dekat
                    if self.ball_x < enemy[0]:
                        enemy[0] -= enemy[5] # speed
                    elif self.ball_x > enemy[0]:
                        enemy[0] += enemy[5] # speed
                
                # Batasi musuh agar tidak keluar layar
                if enemy[0] < 0: enemy[0] = 0
                if enemy[0] + enemy[2] > pyxel.width: enemy[0] = pyxel.width - enemy[2]

        # Cek tabrakan dengan musuh
        for enemy in self.enemies:
            if (
                self.ball_x + 4 >= enemy[0]
                and self.ball_x - 4 <= enemy[0] + enemy[2]
                and self.ball_y + 4 >= enemy[1]
                and self.ball_y - 4 <= enemy[1] + enemy[3]
            ):
                self.game_over = True
                return "lose_life"

        # Cek tabrakan dengan koin
        coins_to_remove = []
        for i, coin in enumerate(self.coins):
            if (
                self.ball_x + 4 >= coin[0]
                and self.ball_x - 4 <= coin[0] + coin[2]
                and self.ball_y + 4 >= coin[1]
                and self.ball_y - 4 <= coin[1] + coin[3]
            ):
                self.total_score += 10 # Skor dari koin
                coins_to_remove.append(i)
                for _ in range(3):
                    self.particles.append([coin[0] + coin[2]/2, coin[1] + coin[3]/2, random.uniform(-1, 1), random.uniform(-2, -4), 11]) # warna kuning

        for i in reversed(coins_to_remove):
            del self.coins[i]

        # Update partikel
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.2
            p[4] -= 0.05
            if p[4] <= 0:
                self.particles.remove(p)

        # Cek tabrakan dengan finish
        if (
            self.ball_x + 4 >= self.finish[0]
            and self.ball_x - 4 <= self.finish[0] + self.finish[2]
            and self.ball_y + 4 >= self.finish[1]
            and self.ball_y - 4 <= self.finish[1] + self.finish[3]
        ):
            self.win = True
            self.total_score += 100 * self.level
            self.level += 1
            if self.level > 5: # Misalnya, ada 5 level total
                return "game_complete"
            else:
                self._generate_level() # Generate new level
                self.reset_ball_position() # Reset ball for new level
                self.win = False # Reset win state for next level

        # Batas bawah layar (jika jatuh)
        if self.ball_y > pyxel.height - 4:
            self.game_over = True
            return "lose_life"

        return None

    def draw(self, skin):
        pyxel.cls(0)

        for platform in self.platforms:
            pyxel.rect(platform[0], platform[1], platform[2], platform[3], 3)
        
        for enemy in self.enemies:
            pyxel.circ(enemy[0] + enemy[2] // 2, enemy[1] + enemy[3] // 2, enemy[2] // 2, 8)
        
        for coin in self.coins:
            pyxel.circ(coin[0] + coin[2]/2, coin[1] + coin[3]/2, coin[2]/2, 11)

        pyxel.rect(self.finish[0], self.finish[1], self.finish[2], self.finish[3], 10)
        
        pyxel.circ(self.ball_x, self.ball_y, 4, skin)

        for p in self.particles:
            if p[4] > 0:
                pyxel.pset(p[0], p[1], int(p[4]))

        if self.game_over:
            pyxel.text(50, 50, "GAME OVER", 8)
            pyxel.text(50, 60, "R: Ulang", 7)
            pyxel.text(50, 70, "M: Menu", 7)
            pyxel.text(50, 80, "L: Leaderboard", 7)
        if self.win:
            pyxel.text(50, 50, "YOU WIN!", 11)
            pyxel.text(50, 60, f"Skor: {self.total_score}", 7)
            pyxel.text(50, 70, "R: Ulang", 7)
            pyxel.text(50, 80, "M: Menu", 7)
            pyxel.text(50, 90, "L: Leaderboard", 7)

    def _generate_level(self):
        self.platforms = []
        self.enemies = []
        self.coins = []
        
        # Platform awal (tanah)
        self.platforms.append([0, pyxel.height - 10, pyxel.width, 10, "static"])

        # Define jump capabilities for ball to ensure reachability
        # These values are estimates based on ball physics
        max_jump_height = 40 # Max vertical distance ball can jump
        max_horizontal_jump_distance = 60 # Max horizontal distance ball can cover in one jump

        # Start from the initial ground platform
        last_platform_x = 0
        last_platform_y = pyxel.height - 10
        last_platform_width = pyxel.width

        # Generate platforms iteratively
        num_platforms = random.randint(3, 6) + self.level
        
        for i in range(num_platforms):
            min_platform_width = 30
            max_platform_width = 80
            width = random.randint(min_platform_width, max_platform_width)

            # Calculate potential x range for the new platform
            # It should be reachable from the previous platform
            # Ensure the new platform's start or end is within jump distance of the last platform's start or end
            min_x_from_prev = max(0, last_platform_x - max_horizontal_jump_distance)
            max_x_from_prev = min(pyxel.width - width, last_platform_x + last_platform_width + max_horizontal_jump_distance - width)
            
            # Ensure there's a valid range, if not, adjust
            if min_x_from_prev > max_x_from_prev:
                # Fallback: if calculated range is invalid, try to place it within screen bounds
                min_x_from_prev = 0
                max_x_from_prev = pyxel.width - width
                # If still invalid, it means the screen is too small or jump distance is too large
                # For now, we'll just use the forced range, but in a real game, this might need more sophisticated handling
                if min_x_from_prev > max_x_from_prev:
                    min_x_from_prev = 0
                    max_x_from_prev = pyxel.width - width # Should always be valid if width > 0

            x = random.randint(min_x_from_prev, max_x_from_prev)

            # Calculate potential y range for the new platform
            # It should be within jumping distance (up) or falling distance (down)
            min_y_reachable = max(20, last_platform_y - max_jump_height) # Cannot go higher than max jump
            max_y_reachable = min(pyxel.height - 20, last_platform_y + 10) # Cannot go too low, or too much below prev platform

            # Ensure min_y_reachable is not greater than max_y_reachable
            if min_y_reachable > max_y_reachable:
                # This can happen if last_platform_y is already very high or low
                # Adjust to ensure a valid range for random.randint
                min_y_reachable = max(20, pyxel.height - 50) # Force a reasonable lower bound
                max_y_reachable = min(pyxel.height - 20, pyxel.height - 30) # Force a reasonable upper bound
                if min_y_reachable > max_y_reachable: # Still invalid, use a default
                    min_y_reachable = 50
                    max_y_reachable = pyxel.height - 50


            y = random.randint(min_y_reachable, max_y_reachable)

            platform_height = 10
            platform_type_choices = ["static"] * 5 # More static platforms
            if self.level >= 2:
                platform_type_choices.extend(["moving_h"] * 2)
            if self.level >= 3:
                platform_type_choices.extend(["moving_v"] * 2)
            platform_type = random.choice(platform_type_choices)

            if platform_type == "static":
                self.platforms.append([x, y, width, platform_height, "static"])
            elif platform_type == "moving_h":
                move_speed = random.choice([-1, 1]) * (1 + self.level * 0.2)
                # Define movement range based on platform's width and screen bounds
                move_range_min = max(0, x - random.randint(10, 30))
                move_range_max = min(pyxel.width - width, x + width + random.randint(10, 30))
                self.platforms.append([x, y, width, platform_height, "moving_h", move_speed, move_range_min, move_range_max])
            elif platform_type == "moving_v":
                move_speed = random.choice([-1, 1]) * (1 + self.level * 0.2)
                # Define movement range based on platform's height and screen bounds
                move_range_min = max(20, y - random.randint(10, 20))
                move_range_max = min(pyxel.height - 20, y + platform_height + random.randint(10, 20))
                self.platforms.append([x, y, width, platform_height, "moving_v", move_speed, move_range_min, move_range_max])

            last_platform_x = x
            last_platform_y = y
            last_platform_width = width

            # Generate musuh di atas platform
            if random.random() < (0.3 + self.level * 0.1) :
                enemy_width = 10
                enemy_height = 10
                enemy_x = x + random.randint(0, width - enemy_width)
                enemy_y = y - enemy_height
                
                enemy_type_choices = ["static"] * 5
                if self.level >= 2:
                    enemy_type_choices.extend(["horizontal"] * 2)
                if self.level >= 3:
                    enemy_type_choices.extend(["chase"] * 1) # Chase enemies are rarer
                enemy_type = random.choice(enemy_type_choices)

                if enemy_type == "static":
                    self.enemies.append([enemy_x, enemy_y, enemy_width, enemy_height, "static"])
                elif enemy_type == "horizontal":
                    move_speed = random.choice([-0.5, 0.5]) * (1 + self.level * 0.1)
                    move_range_min = max(0, enemy_x - random.randint(10, 20))
                    move_range_max = min(pyxel.width - enemy_width, enemy_x + enemy_width + random.randint(10, 20))
                    self.enemies.append([enemy_x, enemy_y, enemy_width, enemy_height, "horizontal", move_speed, move_range_min, move_range_max])
                elif enemy_type == "chase":
                    chase_speed = (0.5 + self.level * 0.1)
                    self.enemies.append([enemy_x, enemy_y, enemy_width, enemy_height, "chase", chase_speed])

            # Generate koin di atas platform
            if random.random() < (0.5 + self.level * 0.1):
                coin_size = 6
                coin_x = x + random.randint(0, width - coin_size)
                coin_y = y - coin_size - 5
                self.coins.append([coin_x, coin_y, coin_size, coin_size])

        # Place finish line on a platform that is relatively high and towards the right
        # Find a suitable platform for the finish line
        # Prioritize platforms that are higher and further right
        suitable_platforms = [p for p in self.platforms if p[1] < pyxel.height / 2 and p[0] > pyxel.width / 2]
        if not suitable_platforms: # If no high-right platforms, pick the highest one
            suitable_platforms = [min(self.platforms, key=lambda p: p[1])]
        
        finish_platform = random.choice(suitable_platforms)
        self.finish = (random.randint(finish_platform[0], finish_platform[0] + finish_platform[2] - 10), 
                       finish_platform[1] - 20, 10, 10) # Place slightly above the chosen platform

        # Ensure finish is not too low and within screen bounds
        if self.finish[1] > pyxel.height / 2 or self.finish[1] < 0:
            self.finish = (self.finish[0], random.randint(30, int(pyxel.height / 2) - 20), 10, 10)
        
        # Ensure finish is within horizontal bounds
        if self.finish[0] < 0: self.finish = (0, self.finish[1], self.finish[2], self.finish[3])
        if self.finish[0] + self.finish[2] > pyxel.width: self.finish = (pyxel.width - self.finish[2], self.finish[1], self.finish[2], self.finish[3])
