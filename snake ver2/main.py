import math
import pygame, sys
from button import Button
from pygame.math import Vector2
from snake import MAIN

pygame.init()
FPS=60
cell_size = 40
cell_number = 30

SCREEN_WIDTH=cell_number*cell_size
SCREEN_HEIGHT=cell_number*8//13*cell_size

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load('assets/logogame.png').convert())


BG = pygame.image.load("assets/bg.png")
bg_width = BG.get_width()
bg_rect = BG.get_rect()


def scroll_bg():
    scroll = 0  # Khởi tạo giá trị scroll
    num_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1  # Số lượng ô vuông để vẽ background
    buffer_width = num_tiles * bg_width - SCREEN_WIDTH  # Tính buffer width

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((175, 215, 70))  # Tô màu nền
        screen_rect = SCREEN.get_rect()
        screen_rect.center = (SCREEN.get_width() // 2, SCREEN.get_height() // 2)


        # Vẽ background
        for i in range(num_tiles):
            # Tính toán vị trí x dựa trên scroll và rect của SCREEN
            x_position = i * bg_width + scroll
            SCREEN.blit(BG.convert_alpha(), (x_position, 0))

        pygame.display.update()

        # Cập nhật giá trị scroll để tạo hiệu ứng cuộn
        scroll -= 1

        if scroll <= -buffer_width:
            scroll = 0

        pygame.time.delay(10)  # Đợi một chút để tạo hiệu ứng cuộn

        


def get_font(size):
    return pygame.font.Font("Font/PoetsenOne-Regular.ttf", size)

def play(snake_speed):
    main_game = MAIN()
    
    #paused
    paused = False
    
    PAUSE_BUTTON = Button(image=None, pos=(1130, 20),
                          text_input="PAUSE(P)", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
    
    
    SCREEN_UPDATE = pygame.USEREVENT
    
    clock = pygame.time.Clock()
    
    #Cập nhật phản ứng màn hình
    pygame.time.set_timer(SCREEN_UPDATE, int(1000 / (snake_speed * 2)))
    
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
                if event.key == pygame.K_p:  # Bắt pause khi phím 'p' được nhấn
                    if not paused:  # Nếu trò chơi không bị tạm dừng
                        main_game.snake.save_direction = main_game.snake.direction  # Lưu hướng hiện tại của rắn
                    paused = not paused  # Chuyển trạng thái của biến paused
                    

        SCREEN.fill((175,215,70))
        main_game.draw_elements()
        
        # Vẽ button pause
        PAUSE_BUTTON.update(SCREEN)
        PAUSE_BUTTON.changeColor(pygame.mouse.get_pos())
        
        if paused:
        # Hiển thị màn hình pause
            action = draw_pause_screen(SCREEN, main_game)
            if action == "RESET":  # Nếu người dùng chọn reset
                main_game.reset()  # Reset trò chơi
                paused = False  # Đặt trạng thái paused về False để tiếp tục chơi theo hướng đang di chuyển
            elif action == True:  # Nếu người dùng chọn tiếp tục
                paused = False  # Đặt trạng thái paused về False để tiếp tục chơi
            elif action == "QUIT":  # Nếu người dùng chọn thoát
                return  # Thoát khỏi hàm, quay lại màn hình chính của trò chơi
        
        
        pygame.display.update()
        clock.tick(FPS)
    
    # Vẽ màn hình pause
def draw_pause_screen(SCREEN, main_game):
    main_game = MAIN()
    # Vẽ các nút tiếp tục, reset và thoát
    CONTINUE_BUTTON = Button(image=pygame.image.load("assets/button3.png"), pos=(600, 300), 
                            text_input="Continue", font=get_font(60), base_color="#69330f", hovering_color="#af613a")
    RESET_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 420), 
                            text_input="Reset", font=get_font(60), base_color="#69330f", hovering_color="#af613a")
    QUIT_BOTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 540), 
                            text_input="Quit", font=get_font(60), base_color="#69330f", hovering_color="#af613a")
    
    # Xử lý sự kiện khi click chuột
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_game.snake.direction = main_game.snake.save_direction  # Thiết lập hướng trở lại như cũ khi tiếp tục
                    return True  # Quay lại trò chơi
                elif RESET_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_game.reset()  # Gọi phương thức reset của đối tượng snake trong main_game
                    return "RESET"  # Trả về giá trị "RESET" khi người dùng chọn reset
                elif QUIT_BOTTON.checkForInput(pygame.mouse.get_pos()):
                    return "QUIT"  # Trả về giá trị "QUIT" khi người dùng chọn thoát

        SCREEN.fill((175,215,70))
        main_game.draw_elements()  # Vẽ các phần khác của trò chơi
        
        PAUSED_FONT = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 100)
        PAUSED_TEXT = PAUSED_FONT.render("Paused", True, (255, 255, 255))
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 200))
        SCREEN.blit(PAUSED_TEXT, PAUSED_RECT)
        
        # Cập nhật trạng thái của các nút và vẽ lại chúng trên màn hình
        CONTINUE_BUTTON.changeColor(pygame.mouse.get_pos())
        RESET_BUTTON.changeColor(pygame.mouse.get_pos())
        QUIT_BOTTON.changeColor(pygame.mouse.get_pos())
        
        
        CONTINUE_BUTTON.update(SCREEN)
        RESET_BUTTON.update(SCREEN)
        QUIT_BOTTON.update(SCREEN)
        
        pygame.display.update()

    
def options(main_game):
    selected_difficulty = None
    #Giao diện
    #frame_image = pygame.image.load("assets/Options Rect.png").convert_alpha()
    #frame_positions = [(400, 200), (400, 320), (400, 440), (400, 560)]
    #frame_height = frame_image.get_height()

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))  # Thêm hình nền 2

        OPTIONS_TEXT = get_font(45).render("Choose the game mode.", True, "#f5d189")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 30))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        #Hiển thị chế độ
        EASY_BUTTON = Button(image=pygame.image.load("assets/button3.png"), pos=(600, 120),
                             text_input="Easy", font=get_font(55), base_color="#69330f", hovering_color="#af613a")
        NORMAL_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 250),
                             text_input="Normal", font=get_font(55), base_color="#69330f", hovering_color="#af613a")
        HARD_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 380),
                             text_input="Hard", font=get_font(55), base_color="#69330f", hovering_color="#af613a")
        SUPER_HARD_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 510),
                             text_input="Super Hard", font=get_font(55), base_color="#69330f", hovering_color="#af613a")
        
        OPTIONS_BACK=Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 640),
                             text_input="Back", font=get_font(55), base_color="#69330f", hovering_color="#af613a")
        #Giao diện
        #frame_rects = [pygame.Rect((pos[0] - frame_image.get_width() / 2, pos[1] - frame_height / 2), (frame_image.get_width(), frame_height)) for pos in frame_positions]
        #for rect in frame_rects:
           # SCREEN.blit(frame_image, rect.topleft)
        
        EASY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        NORMAL_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        SUPER_HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        
        EASY_BUTTON.update(SCREEN)
        NORMAL_BUTTON.update(SCREEN)
        HARD_BUTTON.update(SCREEN)
        SUPER_HARD_BUTTON.update(SCREEN)
        OPTIONS_BACK.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu() 
                #if selected_difficulty:
                #    return selected_difficulty #chuyển sang play với mức độ được chọn

        pygame.display.update()

def main_menu():
    while True:
        # Vẽ hình nền fullscreen
        SCREEN.blit(pygame.transform.scale(BG, SCREEN.get_size()), (0, 0))
                
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Snake Game", True, "#f5d189")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 250), 
                            text_input="PLAY", font=get_font(65), base_color="#69330f", hovering_color="#af613a")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button3.png"), pos=(600, 390), 
                            text_input="OPTIONS", font=get_font(65), base_color="#69330f", hovering_color="#af613a")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 530), 
                            text_input="QUIT", font=get_font(65), base_color="#69330f", hovering_color="#af613a")

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
    
#scroll_bg()
main_menu()
