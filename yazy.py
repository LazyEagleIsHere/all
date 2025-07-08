import pygame
import random
import time
import sys
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from pygame.math import Vector2
from text import *
from quantum import *

pygame.init()

display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
# width, height = 1500, 1000
fps = 60
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (200, 200, 200)
orange = (255, 165, 0)
yellow = (155, 155, 0)
light_blue = (173, 116, 233)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Yazy')
font = pygame.font.Font(None, 36)

def draw(text, font_size, y_position):
  font = pygame.font.Font(None, font_size)
  text_render = font.render(text, True, gray)
  text_rect = text_render.get_rect(center=(width // 2, y_position))
  screen.blit(text_render, text_rect)

def player_init():
  global player
  player = ""
  init = True
  
  while init:
    screen.fill(black)
    draw("YAZY!", 100, height // 4)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        elif event.key == pygame.K_RETURN:
          if player != "":
            if player == "0":
              draw("?????", 750, height // 2)
              pygame.display.flip()
              time.sleep(1)
              player = ""
            elif player > "9":
              draw("TOO MANY PEOPLE", 200, height // 2)
              pygame.display.flip()
              time.sleep(1)
              player = ""
            else:
              init = False
          else:
            draw("USE KEYBOARD TO TYPE NUMBER OF PLAYERS", 100, height // 2)
            pygame.display.flip()
            time.sleep(2)
        elif event.key == pygame.K_BACKSPACE:
          player = player[:-1]
        else:
          if '0' <= event.unicode <= '9':
            player += event.unicode
    
    player_surface = font.render(player, True, white)
    player_rect = player_surface.get_rect()
    player_rect.center = (width // 2, height // 2)
    screen.blit(player_surface, player_rect)
    
    text_surface = font.render("Number of players:", True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 - 80)
    screen.blit(text_surface, text_rect)
    
    pygame.display.update()
  
  start()

def start():
  screen.fill(black)
  
  global die, lock, locka, roll, score, row_3, row_4, b25, b40, b50
  
  base = [625, 100]
  basee = [base[0] + 10, base[1] + 10]
  round = 0
  die = [0 for _ in range(6)]
  lock = [0 for _ in range(6)]
  locka = [[0 for _ in range(12)] for _ in range(int(player))]
  roll = 0
  score = [[0 for _ in range(12)] for _ in range(int(player))]
  row_3 = 7
  row_4 = 8
  b25 = 9
  b40 = 10
  b50 = 11
  cnt_round = 0
    
  running = True
  while running:
    screen.fill(black)
    player_text = f"Player {round + 1}"
    player_text_rect = pygame.Rect(width // 2 - 50, 10, 100, 100)
    write(screen, player_text_rect, player_text, 65, "white", "black", 10)
    
    roll_text = f"Roll remaining: {3 - roll}"
    roll_text_rect = pygame.Rect(width // 2 + 500, height - 250, 100, 100)
    write(screen, roll_text_rect, roll_text, 65, "white", "black", 10)
    
    for i in range(int(player)):
      tot = 0
      for j in range(12):
        if locka[i][j]:
          tot += score[i][j]
      lead_rect = pygame.Rect(100, 100 + (100 * i), 100, 100)
      write(screen, lead_rect, f"Player {i + 1}: {tot}", 65, "white", "black", 10)
    b1 = [Vector2(base[0], base[1]), 
          Vector2(width - base[0], base[1]), 
          Vector2(width - base[0], height - base[1]), 
          Vector2(base[0], height - base[1]), 
          Vector2(base[0], base[1])
        ]
    pygame.draw.polygon(screen, white, [(p.x, p.y) for p in b1])
    
    b2 = [Vector2(basee[0], basee[1]), 
          Vector2(width - basee[0] , basee[1]), 
          Vector2(width - basee[0], height - basee[1]), 
          Vector2(basee[0], height - basee[1]), 
          # Vector2(basee[0], basee[1])
        ]
    pygame.draw.polygon(screen, gray, [(p.x, p.y) for p in b2])
    
    mouse_pos = pygame.mouse.get_pos()
    
    roll_size = [600, 100]
    roll_button = pygame.Rect(width // 2 - 300, height - basee[1] * 2, roll_size[0], roll_size[1])
    
    if roll_button.collidepoint(mouse_pos) and roll != 3:
      write(screen, roll_button, "Roll", 65, "black", "gray69", 10)
    else:
      if roll == 3:
        write(screen, roll_button, "Roll", 65, "black", "red", 10)
      else:
        write(screen, roll_button, "Roll", 65, "black", "white", 10)
      
    b3 = [Vector2(width // 2 - 300, height - basee[1] * 2 - 100), 
          Vector2(width // 2 - 300 + roll_size[0], height - basee[1] * 2 - 100), 
          Vector2(width // 2 - 300 + roll_size[0], height - basee[1] * 2 - 100 + 90), 
          Vector2(width // 2 - 300, height - basee[1] * 2 - 100 + 90)
        ]
    pygame.draw.polygon(screen, orange, [(p.x, p.y) for p in b3])
    
    space = 37.5
    
    dice1 = pygame.Rect(width // 2 - 300, height - basee[1] * 2 - 100, 90, 90)
    if lock[1] or roll == 3:
      write(screen, dice1, str(die[1]), 65, "black", "gray69", 10)
    else:
      write(screen, dice1, str(die[1]), 65, "black", "white", 10)
    
    dice2 = pygame.Rect(width // 2 - 300 + 90 + space, height - basee[1] * 2 - 100, 90, 90)
    if lock[2] or roll == 3:
      write(screen, dice2, str(die[2]), 65, "black", "gray69", 10)
    else:
      write(screen, dice2, str(die[2]), 65, "black", "white", 10)
        
    dice3 = pygame.Rect(width // 2 - 300 + 90 * 2 + space * 2, height - basee[1] * 2 - 100, 90, 90)
    if lock[3] or roll == 3:
      write(screen, dice3, str(die[3]), 65, "black", "gray69", 10)
    else:
      write(screen, dice3, str(die[3]), 65, "black", "white", 10)
    
    dice4 = pygame.Rect(width // 2 - 300 + 90 * 3 + space * 3, height - basee[1] * 2 - 100, 90, 90)
    if lock[4] or roll == 3:
      write(screen, dice4, str(die[4]), 65, "black", "gray69", 10)
    else:
      write(screen, dice4, str(die[4]), 65, "black", "white", 10)
    
    dice5 = pygame.Rect(width // 2 - 300 + 90 * 4 + space * 4, height - basee[1] * 2 - 100, 90, 90)
    if lock[5] or roll == 3:
      write(screen, dice5, str(die[5]), 65, "black", "gray69", 10)
    else:
      write(screen, dice5, str(die[5]), 65, "black", "white", 10)
    
    cnt_pos = [basee[0] + 10, basee[1] + 10]
    cnt_size = [width - cnt_pos[0] - width // 2 - 5, 50]
    space_y = 8
    
    cnt_1_text = pygame.Rect(cnt_pos[0], cnt_pos[1], cnt_size[0], cnt_size[1])
    write(screen, cnt_1_text, "1", 55, "black", "yellow", 10)
    
    if not(locka[round][1]):
      score[round][1] = 0
      for i in range(1, 6):
        if int(die[i]) == 1:
          score[round][1] += 1
    cnt_1 = pygame.Rect(width // 2 + 5, cnt_pos[1], cnt_size[0], cnt_size[1])
    if cnt_1.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_1, str(score[round][1]), 55, "black", "gray69", 10)
    else:
      if locka[round][1]:
        write(screen, cnt_1, str(score[round][1]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_1, str(score[round][1]), 55, "black", "white", 10)
    
    cnt_2_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + cnt_size[1] + space_y, cnt_size[0], cnt_size[1])
    write(screen, cnt_2_text, "2", 55, "black", "yellow", 10)
    
    if not(locka[round][2]):
      score[round][2] = 0
      for i in range(1, 6):
        if int(die[i]) == 2:
          score[round][2] += 2
    cnt_2 = pygame.Rect(width // 2 + 5, cnt_pos[1] + cnt_size[1] + space_y, cnt_size[0], cnt_size[1])
    if cnt_2.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_2, str(score[round][2]), 55, "black", "gray69", 10)
    else:
      if locka[round][2]:
        write(screen, cnt_2, str(score[round][2]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_2, str(score[round][2]), 55, "black", "white", 10)
    
    cnt_3_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 2, cnt_size[0], cnt_size[1])
    write(screen, cnt_3_text, "3", 55, "black", "yellow", 10)
    
    if not(locka[round][3]):
      score[round][3] = 0
      for i in range(1, 6):
        if int(die[i]) == 3:
          score[round][3] += 3
    cnt_3 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 2, cnt_size[0], cnt_size[1])
    if cnt_3.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_3, str(score[round][3]), 55, "black", "gray69", 10)
    else:
      if locka[round][3]:
        write(screen, cnt_3, str(score[round][3]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_3, str(score[round][3]), 55, "black", "white", 10)

    cnt_4_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 3, cnt_size[0], cnt_size[1])
    write(screen, cnt_4_text, "4", 55, "black", "yellow", 10)
    
    if not(locka[round][4]):
      score[round][4] = 0
      for i in range(1, 6):
        if int(die[i]) == 4:
          score[round][4] += 4
    cnt_4 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 3, cnt_size[0], cnt_size[1])
    if cnt_4.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_4, str(score[round][4]), 55, "black", "gray69", 10)
    else:
      if locka[round][4]:
        write(screen, cnt_4, str(score[round][4]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_4, str(score[round][4]), 55, "black", "white", 10)
    
    cnt_5_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 4, cnt_size[0], cnt_size[1])
    write(screen, cnt_5_text, "5", 55, "black", "yellow", 10)
    
    if not(locka[round][5]):
      score[round][5] = 0
      for i in range(1, 6):
        if int(die[i]) == 5:
          score[round][5] += 5
    cnt_5 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 4, cnt_size[0], cnt_size[1])
    if cnt_5.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_5, str(score[round][5]), 55, "black", "gray69", 10)
    else:
      if locka[round][5]:
        write(screen, cnt_5, str(score[round][5]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_5, str(score[round][5]), 55, "black", "white", 10)
    
    cnt_6_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 5, cnt_size[0], cnt_size[1])
    write(screen, cnt_6_text, "6", 55, "black", "yellow", 10)
    
    if not(locka[round][6]):
      score[round][6] = 0
      for i in range(1, 6):
        if int(die[i]) == 6:
          score[round][6] += 6
    cnt_6 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 5, cnt_size[0], cnt_size[1])
    if cnt_6.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_6, str(score[round][6]), 55, "black", "gray69", 10)
    else:
      if locka[round][6]:
        write(screen, cnt_6, str(score[round][6]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_6, str(score[round][6]), 55, "black", "white", 10)
    
    cnt_row_3_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 6, cnt_size[0], cnt_size[1])
    write(screen, cnt_row_3_text, "***", 55, "black", "yellow", 10)
    
    if not(locka[round][row_3]):
      score[round][row_3] = 0
      amount = [0 for _ in range(6)]
      for i in range(1, 6):
        for j in range(1, 6):
          if die[j] == i:
            amount[i] += 1
        if amount[i] >= 3:
          for j in range(1, 6):
            score[round][row_3] += die[j]
          break
    cnt_row_3 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 6, cnt_size[0], cnt_size[1])
    if cnt_row_3.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_row_3, str(score[round][row_3]), 55, "black", "gray69", 10)
    else:
      if locka[round][row_3]:
        write(screen, cnt_row_3, str(score[round][row_3]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_row_3, str(score[round][row_3]), 55, "black", "white", 10)
    
    cnt_row_4_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 7, cnt_size[0], cnt_size[1])
    write(screen, cnt_row_4_text, "****", 55, "black", "yellow", 10)
    
    if not(locka[round][row_4]):
      score[round][row_4] = 0
      amount = [0 for _ in range(6)]
      for i in range(1, 6):
        for j in range(1, 6):
          if die[j] == i:
            amount[i] += 1
        if amount[i] >= 4:
          for j in range(1, 6):
            score[round][row_4] += die[j]
          break
    cnt_row_4 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 7, cnt_size[0], cnt_size[1])
    if cnt_row_4.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_row_4, str(score[round][row_4]), 55, "black", "gray69", 10)
    else:
      if locka[round][row_4]:
        write(screen, cnt_row_4, str(score[round][row_4]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_row_4, str(score[round][row_4]), 55, "black", "white", 10)
    
    cnt_b25_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 8, cnt_size[0], cnt_size[1])
    write(screen, cnt_b25_text, "****##", 55, "black", "yellow", 10)
    
    if not(locka[round][b25]):
      score[round][b25] = 0
      amount = [0 for _ in range(7)]
      two = 0
      three = 0
      for i in range(1, 7):
        for j in range(1, 6):
          if die[j] == i:
            amount[i] += 1
        if amount[i] == 2:
          two += 1
        elif amount[i] == 3:
          three += 1
      if two == 1 and three == 1:
        score[round][b25] = 25
    cnt_b25 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 8, cnt_size[0], cnt_size[1])
    if cnt_b25.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_b25, str(score[round][b25]), 55, "black", "gray69", 10)
    else:
      if locka[round][b25]:
        write(screen, cnt_b25, str(score[round][b25]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_b25, str(score[round][b25]), 55, "black", "white", 10)
    
    cnt_b40_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 9, cnt_size[0], cnt_size[1])
    write(screen, cnt_b40_text, "!@#$%", 55, "black", "yellow", 10)
    
    if not(locka[round][b40]):
      score[round][b40] = 0
      amount = [0 for _ in range(6)]
      sorted_die = sorted(die)
      consectutive = True
      for i in range(2, 6):
        if sorted_die[i] != sorted_die[i - 1] + 1:
          consectutive = False
      if consectutive:
        score[round][b40] = 40
    cnt_b40 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 9, cnt_size[0], cnt_size[1])
    if cnt_b40.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_b40, str(score[round][b40]), 55, "black", "gray69", 10)
    else:
      if locka[round][b40]:
        write(screen, cnt_b40, str(score[round][b40]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_b40, str(score[round][b40]), 55, "black", "white", 10)
    
    cnt_b50_text = pygame.Rect(cnt_pos[0], cnt_pos[1] + (cnt_size[1] + space_y) * 10, cnt_size[0], cnt_size[1])
    write(screen, cnt_b50_text, "*****", 55, "black", "yellow", 10)
    
    if not(locka[round][b50]) and roll != 0:
      score[round][b50] = 0
      if die[1] == die[2] == die[3] == die[4] == die[5]:
        score[round][b50] = 50
    cnt_b50 = pygame.Rect(width // 2 + 5, cnt_pos[1] + (cnt_size[1] + space_y) * 10, cnt_size[0], cnt_size[1])
    if cnt_b50.collidepoint(mouse_pos) and roll != 0:
      write(screen, cnt_b50, str(score[round][b50]), 55, "black", "gray69", 10)
    else:
      if locka[round][b50]:
        write(screen, cnt_b50, str(score[round][b50]), 55, "black", "gray69", 10)
      else:
        write(screen, cnt_b50, str(score[round][b50]), 55, "black", "white", 10)

    if cnt_round == int(player) * 11:
      print("Yes")
      running = False
      win()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        elif event.key == pygame.K_RSHIFT:
          running = False
          start()
        elif event.key == pygame.K_r:
          running = False
          player_init()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if roll_button.collidepoint(mouse_pos) and roll != 3:
          cnt = 0
          for i in range(1, 6):
            cnt += lock[i]
          if cnt != 5:
            roll += 1
            for i in range(1, 6):
              if not(lock[i]):
                die[i] = roll_quantum_dice(6, 1)
        elif dice1.collidepoint(mouse_pos) and roll != 3 and roll != 0:
          if lock[1]:
            lock[1] = 0
          else:
            lock[1] = 1
        elif dice2.collidepoint(mouse_pos) and roll != 3 and roll != 0:
          if lock[2]:
            lock[2] = 0
          else:
            lock[2] = 1
        elif dice3.collidepoint(mouse_pos) and roll != 3 and roll != 0:
          if lock[3]:
            lock[3] = 0
          else:
            lock[3] = 1
        elif dice4.collidepoint(mouse_pos) and roll != 3 and roll != 0:
          if lock[4]:
            lock[4] = 0
          else:
            lock[4] = 1
        elif dice5.collidepoint(mouse_pos) and roll != 3 and roll != 0:
          if lock[5]:
            lock[5] = 0
          else:
            lock[5] = 1
        elif cnt_1.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][1]):
            locka[round][1] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_2.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][2]):
            locka[round][2] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_3.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][3]):
            locka[round][3] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_4.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][4]):
            locka[round][4] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_5.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][5]):
            locka[round][5] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_6.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][6]):
            locka[round][6] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_row_3.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][row_3]):
            locka[round][row_3] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_row_4.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][row_4]):
            locka[round][row_4] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_b25.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][b25]):
            locka[round][b25] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_b40.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][b40]):
            locka[round][b40] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
        elif cnt_b50.collidepoint(mouse_pos) and roll != 0:
          if not(locka[round][b50]):
            locka[round][b50] = 1
            round = (round + 1) % int(player)
            roll = 0
            die = [0 for _ in range(6)]
            lock = [0 for _ in range(6)]
            cnt_round += 1
  
    pygame.display.flip()
  pygame.display.flip()

def win():
  screen.fill(black)
  running = True
  while running:
    screen.fill(black)
    winner = []
    for i in range(int(player)):
      tot = 0
      for j in range(12):
        tot += score[i][j]
      winner.append((i + 1, tot))
    winner.sort(key = lambda x : x[1], reverse = True)
    max_score = 300
    i = 0
    num_i = 1
    for a, b in winner:
      if max_score != b:
        max_score = b
        i += 1
      draw(f"{i}: Player {a} | Score: {b}", 75, 100 * num_i)
      num_i += 1
    
    mouse_pos = pygame.mouse.get_pos()
    
    home_size = [200, 100]
    home_pos = [100, height // 2]
    home = pygame.Rect(home_pos[0], home_pos[1], home_size[0], home_size[1])
    if home.collidepoint(mouse_pos):
      write(screen, home, "Home", 65, "black", "gray69", 10)
    else:
      write(screen, home, "Home", 65, "black", "white", 10)

    again_size = home_size
    again_pos = [100, home_pos[1] + 150]
    again = pygame.Rect(again_pos[0], again_pos[1], again_size[0], again_size[1])
    if again.collidepoint(mouse_pos):
      write(screen, again, "Again", 65, "black", "gray69", 10)
    else:
      write(screen, again, "Again", 65, "black", "white", 10)
        
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if home.collidepoint(mouse_pos):
          running = False
          player_init()
        elif again.collidepoint(mouse_pos):
          running = False
          start()
    pygame.display.flip()
  pygame.display.flip()
        
# player_init()

pygame.display.flip()