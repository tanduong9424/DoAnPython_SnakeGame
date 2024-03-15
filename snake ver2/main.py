import pygame, sys
from button import Button
from pygame.math import Vector2
from snake import MAIN

pygame.init()
cell_size = 40
cell_number = 20

SCREEN = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load('C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/logogame.png').convert_alpha())


BG = pygame.image.load("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/bg.png")

def get_font(size):
    return pygame.font.Font("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/Font/PoetsenOne-Regular.ttf", size)

def play(snake_speed):
    main_game = MAIN()
    
    SCREEN_UPDATE = pygame.USEREVENT
    screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
    clock = pygame.time.Clock()
    
    #Cập nhật phản ứng màn hình
    def set_screen_update_time(snake_speed):
        return int(1000 / (snake_speed * 2))
    
    pygame.time.set_timer(SCREEN_UPDATE,set_screen_update_time(main_game.snake.snake_speed))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def options(main_game):
    selected_difficulty = None
    #Giao diện
    frame_image = pygame.image.load("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/Options Rect.png").convert_alpha()
    frame_positions = [(400, 200), (400, 320), (400, 440), (400, 560)]
    frame_height = frame_image.get_height()

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))  # Thêm hình nền

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 400))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        #OPTIONS_BACK = Button(image=None, pos=(400, 460), 
        #                    text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green") 
        #Hiển thị chế độ
        EASY_BUTTON = Button(image=None, pos=(400, 200),
                             text_input="Easy", font=get_font(75), base_color="Black", hovering_color="Green")
        NORMAL_BUTTON = Button(image=None, pos=(400, 320),
                             text_input="Normal", font=get_font(75), base_color="Black", hovering_color="Green")
        HARD_BUTTON = Button(image=None, pos=(400, 440),
                             text_input="Hard", font=get_font(75), base_color="Black", hovering_color="Green")
        SUPER_HARD_BUTTON = Button(image=None, pos=(400, 560),
                             text_input="Super Hard", font=get_font(75), base_color="Black", hovering_color="Green")
        
        #OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        #OPTIONS_BACK.update(SCREEN)
        #Giao diện
        frame_rects = [pygame.Rect((pos[0] - frame_image.get_width() / 2, pos[1] - frame_height / 2), (frame_image.get_width(), frame_height)) for pos in frame_positions]
        for rect in frame_rects:
            SCREEN.blit(frame_image, rect.topleft)
        
        EASY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        NORMAL_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        SUPER_HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        
        EASY_BUTTON.update(SCREEN)
        NORMAL_BUTTON.update(SCREEN)
        HARD_BUTTON.update(SCREEN)
        SUPER_HARD_BUTTON.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
            #    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            #       main_menu()
                #Kiểm tra người dùng chọn mức độ nào
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed()
                    play(snake_speed)        
                elif NORMAL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 2
                    play(snake_speed)        
                elif HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 3
                    play(snake_speed)        
                elif SUPER_HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 4
                    play(snake_speed)        
                #if selected_difficulty:
                #    return selected_difficulty #chuyển sang play với mức độ được chọn

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Snake Game", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/Options Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("C:/Users/ADMIN/Downloads/snakegame-main (1)/snakegame-main/snake ver2/assets/Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        main_game = MAIN() #Khởi tạo đối tượng main_game từ class MAIN

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                   snake_speed = main_game.snake.get_snake_speed()
                   play(snake_speed)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_difficulty = options(main_game) # Nhận giá trị snake_speed từ hàm options()
                    if selected_difficulty:
                        play(selected_difficulty)  # Truyền giá trị snake_speed vào hàm play() khi chọn chế độ
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main_menu()