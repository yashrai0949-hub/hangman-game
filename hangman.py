import pygame, random, sys
pygame.init()

W,H=800,550
win=pygame.display.set_mode((W,H))
pygame.display.set_caption("Advanced Hangman - Short Code")

FONT=pygame.font.SysFont("Arial",40)
SMALL=pygame.font.SysFont("Arial",25)
WHITE=(255,255,255);BLACK=(0,0,0);RED=(230,40,40);GREEN=(40,200,90)

WORDS={
"ANIMALS":["TIGER","LION","ZEBRA","MONKEY","EAGLE","PANDA"],
"FRUITS":["APPLE","MANGO","ORANGE","BANANA","GRAPES","PAPAYA"],
"COUNTRIES":["INDIA","NEPAL","CANADA","GERMANY","BRAZIL","FRANCE"]
}

def draw_hang(win,m):
    x,y=150,420
    pygame.draw.line(win,BLACK,(x,y),(x+250,y),8)
    pygame.draw.line(win,BLACK,(x+60,y),(x+60,y-300),8)
    pygame.draw.line(win,BLACK,(x+60,y-300),(x+160,y-300),8)
    pygame.draw.line(win,BLACK,(x+160,y-300),(x+160,y-260),8)
    if m>0:pygame.draw.circle(win,BLACK,(x+160,y-230),30,6)
    if m>1:pygame.draw.line(win,BLACK,(x+160,y-200),(x+160,y-130),6)
    if m>2:pygame.draw.line(win,BLACK,(x+160,y-185),(x+120,y-145),6)
    if m>3:pygame.draw.line(win,BLACK,(x+160,y-185),(x+200,y-145),6)
    if m>4:pygame.draw.line(win,BLACK,(x+160,y-130),(x+130,y-90),6)
    if m>5:pygame.draw.line(win,BLACK,(x+160,y-130),(x+190,y-90),6)

def pick_word():
    cat=random.choice(list(WORDS.keys()))
    return cat, random.choice(WORDS[cat])

def text_center(t,f,c,y):
    r=f.render(t,True,c); win.blit(r,((W-r.get_width())//2,y))

def make_buttons():
    btns=[];x,y=420,250;w,h=45,45;gap=8
    row1="QWERTYUIOP"; row2="ASDFGHJKL"; row3="ZXCVBNM"
    rows=[row1,row2,row3]
    for r in rows:
        x=420+(350-len(r)*(w+gap))//2
        for ch in r:
            btns.append([pygame.Rect(x,y,w,h),ch,True])
            x+=w+gap
        y+=h+gap
    return btns

def game():
    cat,word=pick_word()
    guessed=set(); mistakes=0; btns=make_buttons()
    fade=0;clock=pygame.time.Clock()

    while True:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                for b in btns:
                    if b[0].collidepoint(e.pos) and b[2]:
                        b[2]=False; g=b[1]
                        guessed.add(g); mistakes+=(g not in word)
            if e.type==pygame.KEYDOWN:
                if e.unicode.isalpha():
                    g=e.unicode.upper()
                    if g not in guessed:
                        guessed.add(g); mistakes+=(g not in word)

        win.fill(WHITE)
        text_center(f"Category: {cat}",SMALL,BLACK,20)
        draw_hang(win,mistakes)

        # word display with fade animation
        disp=" ".join([c if c in guessed else "_" for c in word])
        fade=min(255,fade+8)
        txt=FONT.render(disp,True,(fade,0,0))
        win.blit(txt,((W-txt.get_width())//2,460))

        # draw buttons
        for r,ch,en in btns:
            pygame.draw.rect(win,(0,150,200) if en else (180,180,180),r,border_radius=5)
            t=SMALL.render(ch,True,WHITE if en else (90,90,90))
            win.blit(t,(r.x+12,r.y+5))

        # win / lose
        if all(c in guessed for c in word):
            text_center("YOU WIN!",FONT,GREEN,180)
            text_center("Press R to Restart",SMALL,BLACK,250)
        if mistakes>=6:
            text_center(f"YOU LOST! Word: {word}",FONT,RED,180)
            text_center("Press R to Restart",SMALL,BLACK,250)

        if mistakes>=6 or all(c in guessed for c in word):
            keys=pygame.key.get_pressed()
            if keys[pygame.K_r]: return game()

        pygame.display.update()

game()

