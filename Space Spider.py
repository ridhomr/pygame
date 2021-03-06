##RIDHO##
	# 1 - Import Library
import pygame
from pygame.locals import *
import math
from random import randint
	# 2 - Inisialisasi Game
pygame.init()
width, height = 640, 480 # Ukuran Layar game
screen = pygame.display.set_mode((width, height))
	# Key 
keys = {
    "left": False, 
    "right": False,
}
running = True
Pesawatpos = [140, 240] # Posisi Pesawat
	# Menang Kalah
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1
score = 0 
health_point = 194 # health poin Planet
countdown_timer = 60000 # Waktu main
Pelurunya = [] # Peluru
enemy_timer = 100 # waktu kemunculan
enemies = [[width, 100]] # Koordinat musuh
	# 3 - Aset Game
	# Images
Pesawat = pygame.image.load("resources/images/Pesawat2.png")
Bintang = pygame.image.load("resources/images/back.png")
Planet = pygame.image.load("resources/images/planet3.png")
Peluru = pygame.image.load("resources/images/sht.png")
Musuh = pygame.image.load("resources/images/Musuh2.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
	# Efek Suara
pygame.mixer.init()
Tertembak = pygame.mixer.Sound("resources/audio/explode.wav")
MusuhMenyerang = pygame.mixer.Sound("resources/audio/enemy.wav")
SuaraPeluru = pygame.mixer.Sound("resources/audio/shoot.wav")
Tertembak.set_volume(0.05)
MusuhMenyerang.set_volume(0.05)
SuaraPeluru.set_volume(0.05)
	# Music
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)



##AYUDYA##
## 4 - Game Loop
while(running):
        # Clear screen
    screen.fill(0)
        # Player Game
    	# Tampilan background
    for x in range(int(width/Bintang.get_width()+1)):
        for y in range(int(height/Bintang.get_height()+1)):
            screen.blit(Bintang, (x*100, y*100))
		# Menampilkan Planet dalam koordinat
    screen.blit(Planet, (3, 40))
    screen.blit(Planet, (3, 145))
    screen.blit(Planet, (3, 250))
    screen.blit(Planet, (3, 355))
	    # gerakan Pesawat tertuju pada mouse
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (Pesawatpos[1]), mouse_position[0] - (Pesawatpos[0]))
    Pesawat_rotation = pygame.transform.rotate(Pesawat, 360 - angle * 57.29)
    new_Pesawatpos = (Pesawatpos[0] - Pesawat_rotation.get_rect().width / 2, Pesawatpos[1] - Pesawat_rotation.get_rect().height / 2)
    screen.blit(Pesawat_rotation, new_Pesawatpos)
	    # posisi muncul Pelurunya
    for bullet in Pelurunya:
        Peluru_index = 0
        velx=math.cos(bullet[0])*20
        vely=math.sin(bullet[0])*20
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            Pelurunya.pop(Peluru_index)
        Peluru_index += 1
        	# Menampilkan Peluru
        for projectile in Pelurunya:
            new_Peluru = pygame.transform.rotate(Peluru, 360-projectile[0]*57.29)
            screen.blit(new_Peluru, (projectile[1], projectile[2]))



##YUSRIYAH##
    # Buat Musuh
    # Waktu saat musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        # Buat musuh baru
        enemies.append([width, randint(25, height-32)])
        # waktu kemuculan
        enemy_timer = randint(1, 100)

    index = 5
    for enemy in enemies:
        	# Musuh bergerak dengan kecepatan 1.5 pixel ke kiri
        enemy[0] -= 0.5
        	# hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -64:
            enemies.pop(index)
			# Benturan antara musuh dengan planet
        enemy_rect = pygame.Rect(Musuh.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y (tinggi)
        enemy_rect.left = enemy[0] # ambil titik x (lebar)
        # benturan musuh dengan planet
        if enemy_rect.left < 64:
            enemies.pop(index_Peluru)
            health_point -= randint(5,20) # mengurangi hp secara acak dengan nilai antara 5 - 20
            Tertembak.play()
            print("Awas! Musuh datang!")
        	# Benturan musuh dengan pelurunya
        index_Peluru = 0
        for bullet in Pelurunya:
            bullet_rect = pygame.Rect(Peluru.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            	# benturan peluru dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index_Peluru)
                Pelurunya.pop(index_Peluru)
                MusuhMenyerang.play()
                print("Wuahahaha! Mati kau!!")
                print("Score: {}".format(score))
            index_Peluru += 1
        index += 1
	    # Menampilkan musuh
    for enemy in enemies:
        screen.blit(Musuh, enemy)
	


##JENNY##
	    # Menampilkan health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))
	    # Menampilkan timer
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)    
    	# memperbarui screen
    pygame.display.flip()
	    # Perulangan
    for event in pygame.event.get():
        # tombol exit di klik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            # Suara Menembak
        if event.type == pygame.MOUSEBUTTONDOWN:
            Pelurunya.append([angle, new_Pesawatpos[0]+32, new_Pesawatpos[1]+32])
            SuaraPeluru.play()
            # tombol untuk menggerakkan pesawat
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["left"] = True
            elif event.key == K_s:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["left"] = False
            elif event.key == K_s:
                keys["right"] = False
    	# Akhir Perulangan
    	# Gerakan pesawat
    if keys["left"]:
        Pesawatpos[0] -= 5 # kurangi nilai y
    elif keys["right"]:
        Pesawatpos[0] += 5 # tambah nilai y
        # keadaan jika waktu habis
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER
# - End of Game Loop



##IQBAL##
	# 5 - Tampilan menang dan kalah
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))
	# Tampilkan score
text = font.render("Total Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 400
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()