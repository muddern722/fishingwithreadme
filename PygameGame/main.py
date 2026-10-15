import pygame
import sys
import random

pygame.init()

# ------------------------------

width = 1440
height = 1440
screen = pygame.display.set_mode((width, height))

#------------------------------

player = {"x": 200, "y": 80, "width": 50, "height": 50}

#-----------------------------

running = True
fishing = False
idle = True

#-----------------------------

idle_state = pygame.image.load("/home/Mochi/PygameGame/Art/Idle.png")  # Load the idle image
fishing_state = pygame.image.load("/home/Mochi/PygameGame/Art/Fishing.png")  # Load the fishing image
env = pygame.image.load("/home/Mochi/PygameGame/Art/Env.png")  # Load the environment image
salmon = pygame.image.load("/home/Mochi/PygameGame/Art/Salmon.png")  # Load the salmon image
caughtfish = pygame.image.load("/home/Mochi/PygameGame/Art/CaughtFish.png")  # Load the caught fish image

#-----------------------------

idle_state = pygame.transform.scale(idle_state, (540, 540))
fishing_state = pygame.transform.scale(fishing_state, (540, 540))
caughtfish = pygame.transform.scale(caughtfish, (540, 540))
env = pygame.transform.scale(env, (1440, 1440))
salmon = pygame.transform.scale(salmon, (900, 900))

#-----------------------------
# FIXED NAME MIX-UPS HERE
bite_timer = 0
catch_window = 0
fish_display_timer = 0

clock = pygame.time.Clock()









while running:

    clock.tick(60)  # Limit the frame rate to 60 FPS

    # --- TIMERS SEPARATED AND FIXED ---
    if bite_timer > 0:
        bite_timer -= 16
        if bite_timer <= 0:
            bite_timer = 0       # <--- FIX: Force to 0 so it's not negative
            catch_window = 2000  
            print("FISH ON THE LINE!")

    if catch_window > 0:
        catch_window -= 16
        if catch_window <= 0:
            catch_window = 0     # <--- FIX: Force to 0 so it's not negative
            fishing = False
            idle = True
            print("The fish got away...")

    if fish_display_timer > 0:
        fish_display_timer -= 16
        if fish_display_timer <= 0:
            fish_display_timer = 0  # <--- FIX: Force to 0 so it's not negative

    # --- EVENT INPUTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                # If doing nothing, start fishing & start the 3-10 sec bite timer
                if not fishing and catch_window == 0 and fish_display_timer == 0:
                    fishing = True
                    bite_timer = random.randint(3000, 10000)
                    print("Casting line...")
                    
                # If a fish is on the hook, catch it!
                elif catch_window > 0:
                    catch_window = 0
                    fishing = False
                    fish_display_timer = 5000  # Show salmon for 5 seconds
                    print("CAUGHT IT!")
                    
                # If they reel in too early while waiting
                elif bite_timer > 0:
                    bite_timer = 0
                    fishing = False
                    print("Reeled in too early!")

    # --- RENDERING IMAGES ---
    screen.fill((0, 0, 139))  
    screen.blit(env, (0, 0))  

    if catch_window > 0:
        screen.blit(caughtfish, (player["x"], player["y"]))  # Show alert sprite
    elif fishing:
        screen.blit(fishing_state, (player["x"], player["y"]))  # Show standard fishing sprite
    else:
        screen.blit(idle_state, (player["x"], player["y"]))  # Show idle sprite

    # Draw the Salmon in the middle of the screen if the display timer is active
    if fish_display_timer > 0:
        screen.blit(salmon, (150, 150))  

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
