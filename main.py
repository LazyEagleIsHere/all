import pygame
import sys
import time
import random
from text import *
from BouncingBall import *
from lander import login
from yazy import player_init
from ShootingGame import shooting_game

pygame.init()

display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
fps = 100
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

screen = pygame.display.set_mode((width ,height))

def draw(text, font_size, y_position):
  font = pygame.font.Font(None, font_size)
  text_render = font.render(text, True, gray)
  text_rect = text_render.get_rect(center=(width // 2, y_position))
  screen.blit(text_render, text_rect)

scrollbar_bg = (200, 200, 200)
scrollbar_slider = (100, 100, 100)
item_bg = black
item_selected = gray
item_text = white
item_hover = (100, 100, 100)
border = (180, 180, 180)

font = pygame.font.SysFont(None, 50)

items = ["Bouncing Ball", 
          "Lander", 
          "Yazy", 
          "Shooting Game"]

item_height = 50
visible_items_cnt = 3

content_area_width = 350
content_area_height = item_height * visible_items_cnt
content_area_x = (width - (content_area_width + 20)) // 2
content_area_y = (height - content_area_height) // 2

content_rect = pygame.Rect(content_area_x, content_area_y, content_area_width, content_area_height)

scrollbar_width = 20
scrollbar_height = content_rect.height
scrollbar_x = content_rect.right
scrollbar_y = content_rect.top

slider_height = max(scrollbar_height * visible_items_cnt / len(items), 20)

slider_rect = pygame.Rect(scrollbar_x, 
                          scrollbar_y, 
                          scrollbar_width, 
                          slider_height
                        )

slider_min_y = scrollbar_y
slider_max_y = scrollbar_y + scrollbar_height - slider_rect.height

dragging = False
drag_offset_y = 0

scroll_offset = 0.0

selected_index = None

def clamp(n, minn, maxn):
  return max(min(maxn, n), minn)


def get_visible_items(scroll_offset):
  start_index = int(scroll_offset)
  end_index = min(start_index + visible_items_cnt, len(items))
  return items[start_index:end_index], start_index

def draw_items(surface, items, start_index, mouse_pos):
  global selected_index
  for i, item in enumerate(items):
    item_rect = pygame.Rect(
      content_rect.left, 
      content_rect.top + i * item_height, 
      content_rect.width, 
      item_height - 2
    )
    
    if item_rect.bottom > content_rect.top and item_rect.top < content_rect.bottom:
      hovered = item_rect.collidepoint(mouse_pos)
      
      if selected_index == start_index + i:
        bg_colour = item_selected
      elif hovered:
        bg_colour = item_hover
      else:
        bg_colour = item_bg
      
      pygame.draw.rect(surface, bg_colour, item_rect)
      
      text_surf = font.render(item, True, item_text)
      text_rect = text_surf.get_rect(midleft = (item_rect.left + 5, item_rect.centery))
      surface.blit(text_surf, text_rect)
    
def update_scroll_offset_from_slider():
  max_scroll = len(items) - visible_items_cnt
  if max_scroll <= 0:
    return 0
  relative_pos = slider_rect.top - scrollbar_y
  scroll_range = scrollbar_height - slider_rect.height
  
  if scroll_range <= 0:
    return 0.0
  
  scroll_ratio = relative_pos / scroll_range
  return scroll_ratio * max_scroll

def update_slider_position_from_scroll():
  max_scroll = len(items) - visible_items_cnt
  if max_scroll <= 0:
    slider_rect.top = scrollbar_y
    return
  
  scorll_ratio = scroll_offset / max_scroll
  slider_rect.top = scrollbar_y + scorll_ratio * (scrollbar_height - slider_rect.height)

def main():
  global dragging, drag_offset_y, scroll_offset, selected_index
  
  screen.fill(black)
  
  running = True
  while running:
    screen.fill(black)
    mouse_pos = pygame.mouse.get_pos()
    
    draw("Games", 100, height // 4)
    
    pygame.draw.rect(screen, border, content_rect, 2, border_radius = 5)
    visible_items, start_index = get_visible_items(scroll_offset)
    draw_items(screen, visible_items, start_index, mouse_pos)
    
    scrollbar_bg_rect = pygame.Rect(
      scrollbar_x, 
      scrollbar_y, 
      scrollbar_width, 
      scrollbar_height
    )
    pygame.draw.rect(screen, scrollbar_bg, scrollbar_bg_rect, border_radius = 5)
    
    pygame.draw.rect(screen, scrollbar_slider, slider_rect, border_radius = 5)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if slider_rect.collidepoint(event.pos):
            dragging = True
            drag_offset_y = event.pos[1] - slider_rect.top
          elif content_rect.collidepoint(event.pos):
            visible_items, start_index = get_visible_items(scroll_offset)
            for i, item in enumerate(visible_items):
              item_rect = pygame.Rect(
                content_rect.left, 
                content_rect.top + i * item_height, 
                content_rect.width, 
                item_height - 2
              )
              
              if item_rect.collidepoint(event.pos):
                selected_index = start_index + i
                if selected_index == 0:
                  bounce()
                elif selected_index == 1:
                  login()
                elif selected_index == 2:
                  player_init()
                elif selected_index == 3:
                  shooting_game()
                break
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          dragging = False
      elif event.type == pygame.MOUSEMOTION:
        if dragging:
          new_top = event.pos[1] - drag_offset_y
          new_top = clamp(new_top, slider_min_y, slider_max_y)
          slider_rect.top = new_top
          scroll_offset = update_scroll_offset_from_slider()
      elif event.type == pygame.MOUSEWHEEL:
        if content_rect.collidepoint(mouse_pos) or slider_rect.collidepoint(mouse_pos):
          max_scroll = len(items) - visible_items_cnt
          scroll_offset -= event.y
          scroll_offset = clamp(scroll_offset, 0, max_scroll)
          update_slider_position_from_scroll()
    
    pygame.display.flip()
    clock.tick(fps)

main()