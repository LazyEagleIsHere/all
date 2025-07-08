import pygame
import sys

pygame.init()

# --- Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000 # Increased screen size for better visibility
FPS = 60

# Colors
COLOR_BG = (240, 240, 240)
COLOR_SCROLLBAR_BG = (200, 200, 200)
COLOR_SCROLLBAR_SLIDER = (100, 100, 250)
COLOR_ITEM_BG = (255, 255, 255)
COLOR_ITEM_SELECTED = (150, 200, 255)
COLOR_ITEM_TEXT = (0, 0, 0)
COLOR_ITEM_HOVER = (220, 220, 255)
COLOR_BORDER = (180, 180, 180) # New color for the content area border

# Font
FONT = pygame.font.SysFont(None, 24)

# Item list and item height
ITEMS = [f"Item {i+1}" for i in range(50)]
ITEM_HEIGHT = 30
VISIBLE_ITEMS_COUNT = 7 # Number of items visible at once

# --- Central Content Area Definition ---
# This rect defines the area where items will be displayed,
# and the scrollbar will be attached to its right side.
CONTENT_AREA_WIDTH = 250 # Width of the area displaying items
CONTENT_AREA_HEIGHT = ITEM_HEIGHT * VISIBLE_ITEMS_COUNT
CONTENT_AREA_X = (SCREEN_WIDTH - (CONTENT_AREA_WIDTH + 20)) // 2 # Center the content area + scrollbar
CONTENT_AREA_Y = (SCREEN_HEIGHT - CONTENT_AREA_HEIGHT) // 2

CONTENT_RECT = pygame.Rect(CONTENT_AREA_X, CONTENT_AREA_Y, CONTENT_AREA_WIDTH, CONTENT_AREA_HEIGHT)

# Scrollbar dimensions (relative to CONTENT_RECT)
SCROLLBAR_WIDTH = 20
SCROLLBAR_X = CONTENT_RECT.right # Scrollbar is positioned to the right of content area
SCROLLBAR_Y = CONTENT_RECT.top
SCROLLBAR_HEIGHT = CONTENT_RECT.height

# Calculate slider height proportional to visible items
# Ensure slider has a minimum height
slider_height = max(SCROLLBAR_HEIGHT * VISIBLE_ITEMS_COUNT / len(ITEMS), 20)

# Initialize slider rect
slider_rect = pygame.Rect(
    SCROLLBAR_X,
    SCROLLBAR_Y,
    SCROLLBAR_WIDTH,
    slider_height
)

# Scrollbar slider min/max Y positions
SLIDER_MIN_Y = SCROLLBAR_Y
SLIDER_MAX_Y = SCROLLBAR_Y + SCROLLBAR_HEIGHT - slider_rect.height


# --- Initialize screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Scrollbar Item Selector (Centered UI)")

clock = pygame.time.Clock()

# --- Scrollbar state ---
dragging = False
drag_offset_y = 0

# Scroll offset in items (float, to allow smooth scroll)
scroll_offset = 0.0

# Selected item index (relative to ITEMS list)
selected_index = None

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def get_visible_items(scroll_offset):
    # Return the slice of items currently visible based on scroll offset
    start_index = int(scroll_offset)
    end_index = min(start_index + VISIBLE_ITEMS_COUNT, len(ITEMS))
    return ITEMS[start_index:end_index], start_index

def draw_items(surface, items, start_index, mouse_pos):
    global selected_index
    for i, item in enumerate(items):
        item_rect = pygame.Rect(
            CONTENT_RECT.left,              # Item starts at content area's left
            CONTENT_RECT.top + i * ITEM_HEIGHT, # Positioned within content area
            CONTENT_RECT.width,             # Item width is content area's width
            ITEM_HEIGHT - 2                 # Height with a small padding
        )
        
        # Ensure item is only drawn if it's within the content rect's vertical bounds
        # This is particularly important for partial items at the top/bottom if not perfectly aligned
        if item_rect.bottom > CONTENT_RECT.top and item_rect.top < CONTENT_RECT.bottom:
            # Check if hovered
            hovered = item_rect.collidepoint(mouse_pos)
            
            # Background color
            if selected_index == start_index + i:
                bg_color = COLOR_ITEM_SELECTED
            elif hovered:
                bg_color = COLOR_ITEM_HOVER
            else:
                bg_color = COLOR_ITEM_BG
            
            # Draw item background
            pygame.draw.rect(surface, bg_color, item_rect)
            
            # Draw text
            text_surf = FONT.render(item, True, COLOR_ITEM_TEXT)
            text_rect = text_surf.get_rect(midleft=(item_rect.left + 5, item_rect.centery))
            surface.blit(text_surf, text_rect)

def update_scroll_offset_from_slider():
    # Map slider y-position to scroll offset
    max_scroll = len(ITEMS) - VISIBLE_ITEMS_COUNT
    if max_scroll <= 0:
        return 0.0 # No scrolling needed if all items fit
    
    relative_pos = slider_rect.top - SCROLLBAR_Y
    scroll_range = SCROLLBAR_HEIGHT - slider_rect.height
    
    if scroll_range <= 0: # Avoid division by zero if slider fills scrollbar
        return 0.0
        
    scroll_ratio = relative_pos / scroll_range
    return scroll_ratio * max_scroll

def update_slider_position_from_scroll():
    # Map scroll offset to slider y-position
    max_scroll = len(ITEMS) - VISIBLE_ITEMS_COUNT
    if max_scroll <= 0:
        slider_rect.top = SCROLLBAR_Y
        return
        
    scroll_ratio = scroll_offset / max_scroll
    slider_rect.top = SCROLLBAR_Y + scroll_ratio * (SCROLLBAR_HEIGHT - slider_rect.height)

def main():
    global dragging, drag_offset_y, scroll_offset, selected_index
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if slider_rect.collidepoint(event.pos):
                        dragging = True
                        drag_offset_y = event.pos[1] - slider_rect.top
                    elif CONTENT_RECT.collidepoint(event.pos): # Check if click is within the content area
                        # Check if clicked on any visible item
                        visible_items, start_index = get_visible_items(scroll_offset)
                        for i, item in enumerate(visible_items):
                            item_rect = pygame.Rect(
                                CONTENT_RECT.left,
                                CONTENT_RECT.top + i * ITEM_HEIGHT,
                                CONTENT_RECT.width,
                                ITEM_HEIGHT - 2
                            )
                            if item_rect.collidepoint(event.pos):
                                selected_index = start_index + i
                                print(f"Selected: {ITEMS[selected_index]}")
                                break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Move slider within bounds
                    new_top = event.pos[1] - drag_offset_y
                    new_top = clamp(new_top, SLIDER_MIN_Y, SLIDER_MAX_Y)
                    slider_rect.top = new_top
                    scroll_offset = update_scroll_offset_from_slider()
        
            elif event.type == pygame.MOUSEWHEEL:
                # Scroll items with mouse wheel if mouse is over the content or scrollbar
                if CONTENT_RECT.collidepoint(mouse_pos) or slider_rect.collidepoint(mouse_pos):
                    max_scroll = len(ITEMS) - VISIBLE_ITEMS_COUNT
                    scroll_offset -= event.y  # y is 1 for up, -1 for down
                    scroll_offset = clamp(scroll_offset, 0, max_scroll)
                    update_slider_position_from_scroll()
        
        # --- Drawing ---
        screen.fill(COLOR_BG)
        
        # Draw the main content area border
        pygame.draw.rect(screen, COLOR_BORDER, CONTENT_RECT, 2, border_radius=5)
        
        # Draw items within the content area
        # Use a sub-surface or clip for more precise drawing, especially for partial items.
        # For simplicity here, we rely on the item_rect logic in draw_items.
        visible_items, start_index = get_visible_items(scroll_offset)
        draw_items(screen, visible_items, start_index, mouse_pos)
        
        # Draw scrollbar background
        scrollbar_bg_rect = pygame.Rect(SCROLLBAR_X, SCROLLBAR_Y, SCROLLBAR_WIDTH, SCROLLBAR_HEIGHT)
        pygame.draw.rect(screen, COLOR_SCROLLBAR_BG, scrollbar_bg_rect, border_radius=5)
        
        # Draw slider
        pygame.draw.rect(screen, COLOR_SCROLLBAR_SLIDER, slider_rect, border_radius=5)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
