from turtle import*
from random import randint
import pygame
 
#initialisation de l'ecran 
ecran = Screen()
ecran.register_shape("resources/bird_up.gif")
ecran.register_shape("resources/bird_down.gif")
ecran.register_shape("resources/tuyau_up.gif")
ecran.register_shape("resources/tuyau_down.gif")
ecran.register_shape("resources/background.gif")
ecran.register_shape("resources/sol.gif")
ecran.register_shape("resources/foreground_white.gif")
ecran.bgpic("resources/background.gif")
ecran.setup (800,800)
ecran.title("Legendary bird")

#initialisation de notre personnage(bird)
bird = Turtle(shape="resources/bird_up.gif")
bird.penup()
bird.speed(0)
bird.setpos(-130,0)
bird_hauteur = 35 #pixel
bird_largeur = 41 #pixel

#initialisation d'animation
listAnim = ["resources/bird_down.gif", "resources/bird_up.gif"]
delay = 1.5    
index_img = 0
compteur = 0

#initialisation de score
afficheur_de_Score = Turtle(visible= False)
afficheur_de_Score.color("white")
afficheur_de_Score.penup()
afficheur_de_Score.speed(0)
afficheur_de_Score.setpos(0,170)
score = 0
afficheur_de_Score.write(str(score),align="center", font=("Arial", 40,"bold"))

#initialisation des tuyaux
listTuyaux = [Turtle() for t in range(4)]
for tuyau in listTuyaux:
    tuyau.speed(0)
    tuyau.penup()
    
    #les caracteristiques
tuyau_largeur = 26
tuyau_hauteur = 400
ecart_Minimum = bird_hauteur

    #l'images et la position 
for i in range(0,4 ,2):
    listTuyaux[i].shape("resources/tuyau_up.gif")
    listTuyaux[i+1].shape("resources/tuyau_down.gif")
    listTuyaux[i].setpos(listTuyaux[i-1].xcor() + 400,randint(-400,-150))  
    listTuyaux[i+1].setpos(listTuyaux[i].xcor(),listTuyaux[i].ycor() + tuyau_hauteur + ecart_Minimum + randint(60,150))
    #listTuyaux[i-1].xcor() vaut 0 car y a ca n'existe pas je crois
    
#initialisation du sol
sol = Turtle(shape="resources/sol.gif")
sol.penup()
sol.speed(0)
sol.setpos(0,-240)

#initialisation du premier plan
foreground = Turtle(shape="resources/foreground_white.gif")

#initialisation du son
pygame.mixer.init()
point_sound = pygame.mixer.Sound("resources/sound/point.wav")
hit_sound = pygame.mixer.Sound("resources/sound/hit.wav")
point_sound = pygame.mixer.Sound("resources/sound/point.wav")
point_sound = pygame.mixer.Sound("resources/sound/point.wav")

#initialisation de la musique de fond
pygame.mixer.music.load("resources/sound/bg_music.mp3")
pygame.mixer.music.play()

def sauter(x,y):
    bird.goto(bird.xcor(),bird.ycor() + 60)
    
def bird_animation():
    global compteur
    global index_img
    if compteur > delay:
        compteur = 0
        bird.shape(listAnim[index_img])
        index_img += 1 #on passe à l'image suivante
        index_img %= len(listAnim) #rebouclage 
    else:
        compteur += 1

def deplacement_tuyaux():
    for i in range(0,4 ,2):
        listTuyaux[i].goto(listTuyaux[i].xcor() - 12,listTuyaux[i].ycor())
        listTuyaux[i+1].goto(listTuyaux[i+1].xcor() - 12,listTuyaux[i+1].ycor())
 
        #les tuyaux sont en dehors l'écran?
        if listTuyaux[i].xcor() <= -200:
            gestion_Score()
            listTuyaux[i].goto(listTuyaux[i-1].xcor() + 400,randint(-400,-150))
            listTuyaux[i+1].setpos(listTuyaux[i].xcor(),listTuyaux[i].ycor() + tuyau_hauteur + ecart_Minimum + randint(60,150) )
    
def deplacement_sol():
    sol.goto(sol.xcor() - 12,sol.ycor())
    if sol.xcor() < -70:
        sol.setx(0)

def gestion_Collision():
    for tuyau in listTuyaux:#tester avec tous les tuyaux de la liste en meme temp
        if bird.xcor() - (bird_largeur/2) >= tuyau.xcor() + (tuyau_largeur/2) or bird.xcor() + (bird_largeur/2) <= tuyau.xcor() - (tuyau_largeur/2) or bird.ycor() - (bird_hauteur/2) >= tuyau.ycor() + (tuyau_hauteur/2) or bird.ycor() +  (bird_hauteur/2) <= tuyau.ycor() - (tuyau_hauteur/2):
        #droite gauche haut bas
            continue 
        else:
            hit_sound.play()#jouer le son lorsque l'oiseau touche le tuyau 
            return True
            
        
def gestion_Score():
    global score #pour pouvoir modifier la variable score
    point_sound.play()#jouer le son
    score += 1
    afficheur_de_Score.clear()#on efface ce qu'il y a écrit avant
    afficheur_de_Score.write(str(score),align="center", font=("Arial", 40,"bold"))
    
def exitEcran():
    if bird.ycor() >= (500/2) or bird.ycor() <= -(500/2):
        return True 

def gameOver():
    for turtles in ecran.turtles():#on cache tous les turtles qui sont presents dans l'ecran 
        turtles.hideturtle()
    foreground.showturtle()#on affiche l'image du premier plan
    pygame.mixer.music.stop()#on arrete la musique de fond
    ecran.onclick(None)#on empeche le joueur de cliquer 

    #affichage de score
    afficheur_de_Score.setpos(0,0)#le texte s'affiche au centre de l'écran
    afficheur_de_Score.clear()#on efface le texte score 
    afficheur_de_Score.write("GAME OVER\n SCORE: " + str(score) ,align="center", font=("Arial", 20,"bold"))
   
def principale():
    # si l'une des conditions est fausse alors on quitte la boucle
    while gestion_Collision() != True and exitEcran() != True :
        bird.goto(bird.xcor(),bird.ycor() - 10)
        bird_animation()
        deplacement_tuyaux()
        deplacement_sol()            
        
#gestion_clavier
ecran.onclick(sauter)

principale()

gameOver()
