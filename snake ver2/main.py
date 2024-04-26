import math
import pygame, sys
from button import Button
from pygame.math import Vector2
from snake import MAIN

pygame.init()
FPS=60
cell_size = 40
cell_number = 30

SCREEN_WIDTH=cell_number *cell_size
SCREEN_HEIGHT=cell_number*8//13 *cell_size

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load('assets/logogame.png').convert())


BG = pygame.image.load("assets/bg.png")
bg_width = BG.get_width()
bg_rect = BG.get_rect()

#SKIN_IMAGES = [pygame.image.load("assets/skin1.png"), pygame.image.load("assets/skin2.png"), pygame.image.load("assets/skin3.png")]
skin_global = 0
# def scroll_bg():
#     scroll = 0  # Khởi tạo giá trị scroll
#     num_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1  # Số lượng ô vuông để vẽ background
#     buffer_width = num_tiles * bg_width - SCREEN_WIDTH  # Tính buffer width

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         SCREEN.fill((175, 215, 70))  # Tô màu nền
#         screen_rect = SCREEN.get_rect()
#         screen_rect.center = (SCREEN.get_width() // 2, SCREEN.get_height() // 2)


#         # Vẽ background
#         for i in range(num_tiles):
#             # Tính toán vị trí x dựa trên scroll và rect của SCREEN
#             x_position = i * bg_width + scroll
#             SCREEN.blit(BG.convert_alpha(), (x_position, 0))

#         pygame.display.update()

#         # Cập nhật giá trị scroll để tạo hiệu ứng cuộn
#         scroll -= 1

#         if scroll <= -buffer_width:
#             scroll = 0

#         pygame.time.delay(10)  # Đợi một chút để tạo hiệu ứng cuộn

        


def get_font(size):
    return pygame.font.Font("Font/PoetsenOne-Regular.ttf", size)

def play(snake_speed,mode,skin):
    main_game = MAIN(mode,skin)
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
                if(main_game.reverse_mushroom==True):
                    main_game.reverse_time+=1
                if(main_game.reverse_time>=50):
                    main_game.reverse_mushroom=False
                    main_game.reverse_time=0
            if main_game.reverse_mushroom==True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                            main_game.start=True
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)
                            main_game.start=True
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
                            main_game.start=True
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)
                            main_game.start=True
                    if event.key == pygame.K_p:  # Bắt pause khi phím 'p' được nhấn
                        if not paused:  # Nếu trò chơi không bị tạm dừng
                            main_game.snake.save_direction = main_game.snake.direction  # Lưu hướng hiện tại của rắn
                        paused = not paused  # Chuyển trạng thái của biến paused                
            elif main_game.reverse_mushroom == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
                            main_game.start=True
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)
                            main_game.start=True
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                            main_game.start=True
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)
                            main_game.start=True
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
                main_game.fruit.random=True
                main_game.reset()  # Reset trò chơi
                paused = False  # Đặt trạng thái paused về False để tiếp tục chơi theo hướng đang di chuyển
            elif action == True:  # Nếu người dùng chọn tiếp tục
                paused = False  # Đặt trạng thái paused về False để tiếp tục chơi
            elif action == "QUIT":  # Nếu người dùng chọn thoát
                return  # Thoát khỏi hàm, quay lại màn hình chính của trò chơi
        if main_game.end:
            action = draw_end_screen(SCREEN, main_game,main_game.save_score)
            if action == "RESET":  # Nếu người chơi chọn "New Game"
                main_game.fruit.random=True
                main_game.end=False
                main_game.reset()  # Reset trò chơi

            elif action == "QUIT":  # Nếu người chơi chọn "Quit"
                return  # Thoát game
        
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
                    main_game.fruit.random=True
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


def draw_end_screen(SCREEN, main_game,score):    
    main_game = MAIN()
    # Vẽ các nút reset và thoát
    RESET_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 420), 
                            text_input="New game", font=get_font(60), base_color="#69330f", hovering_color="#af613a")
    QUIT_BOTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 540), 
                            text_input="Quit", font=get_font(60), base_color="#69330f", hovering_color="#af613a")     
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESET_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_game.fruit.random=True
                    main_game.reset()  # Gọi phương thức reset của đối tượng snake trong main_game
                    return "RESET"  # Trả về giá trị "RESET" khi người dùng chọn reset
                elif QUIT_BOTTON.checkForInput(pygame.mouse.get_pos()):
                    return "QUIT"  # Trả về giá trị "QUIT" khi người dùng chọn thoát
        #SCREEN.fill((0,0,0))
        #main_game.draw_elements()
        SCORE_FONT = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 100)
        # print("hello",score)
        SCORE_TEXT = SCORE_FONT.render("Score: "+format(score),True,(255,255,255),None)
        SCORE_RECT = SCORE_TEXT.get_rect(center=(600,200))
        # new_game_text = SCORE_FONT.render("New Game (N)", True, (255, 255, 255))
        # new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        # quit_text = SCORE_FONT.render("Quit (Q)", True, (255, 255, 255))
        # quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        SCREEN.blit(SCORE_TEXT, SCORE_RECT)
        # SCREEN.blit(new_game_text, new_game_rect)
        # SCREEN.blit(quit_text, quit_rect)
    # Cập nhật trạng thái của các nút và vẽ lại chúng trên màn hình
        RESET_BUTTON.changeColor(pygame.mouse.get_pos())
        QUIT_BOTTON.changeColor(pygame.mouse.get_pos())
        
        RESET_BUTTON.update(SCREEN)
        QUIT_BOTTON.update(SCREEN)

        pygame.display.flip() 
        
def options(main_game,skin_global):
    selected_difficulty = None
    mode=0
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

        #print("skin global: ",skin_global)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Kiểm tra người dùng chọn mức độ nào
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed()
                    mode=0
                    play(snake_speed,mode,skin_global)        
                elif NORMAL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 2
                    mode=1
                    play(snake_speed,mode,skin_global)        
                elif HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 3
                    mode=2
                    play(snake_speed,mode,skin_global)        
                elif SUPER_HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    snake_speed = main_game.snake.get_snake_speed() * 4
                    mode=3
                    play(snake_speed,mode,skin_global)       
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(skin_global) 
                #if selected_difficulty:
                #    return selected_difficulty #chuyển sang play với mức độ được chọn

        pygame.display.update()
def skins(main_game):
    skin=0
    exited = False  # Biến để theo dõi trạng thái thoát khỏi menu Skins
    #Giao diện
    #frame_image = pygame.image.load("assets/Options Rect.png").convert_alpha()
    #frame_positions = [(400, 200), (400, 320), (400, 440), (400, 560)]
    #frame_height = frame_image.get_height()

    while not exited:  # Vòng lặp sẽ chạy cho đến khi người dùng thoát khỏi menu Skins
        SKINS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))  # Thêm hình nền 2

        SKINS_TEXT = get_font(45).render("Choose the skin.", True, "#f5d189")
        SKINS_RECT = SKINS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 30))
        SCREEN.blit(SKINS_TEXT, SKINS_RECT)

        SKIN0_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(200, 120),
                            skin_image=pygame.image.load("Graphics/snake_skin_preview.png"),
                            text_input="Snake", font=get_font(55), base_color="#69330f",
                            hovering_color="#af613a")
        SKIN1_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 120),
                            skin_image=pygame.image.load("Graphics/dragon_skin_preview.png"),
                            text_input="Dragon", font=get_font(55), base_color="#69330f",
                            hovering_color="#af613a")
        SKIN2_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(1000, 120),
                            skin_image=pygame.image.load("Graphics/ant_skin_preview.png"),
                            text_input="Ant", font=get_font(55), base_color="#69330f",
                            hovering_color="#af613a")

        SKINS_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 640),
                            text_input="Back", font=get_font(55), base_color="#69330f", hovering_color="#af613a")


        # SKIN0_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 120),
        #                       text_input="Choose", font=get_font(55), base_color="#69330f",
        #                       hovering_color="#af613a")
        # SKIN1_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 250),
        #                       text_input="Choose", font=get_font(55), base_color="#69330f",
        #                       hovering_color="#af613a")
        # SKIN2_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 380),
        #                       text_input="Choose", font=get_font(55), base_color="#69330f",
        #                       hovering_color="#af613a")

        # SKINS_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(600, 640),
        #                     text_input="Back", font=get_font(55), base_color="#69330f", hovering_color="#af613a")

        SKIN0_BUTTON.changeColor(SKINS_MOUSE_POS)
        SKIN1_BUTTON.changeColor(SKINS_MOUSE_POS)
        SKIN2_BUTTON.changeColor(SKINS_MOUSE_POS)
        SKINS_BACK.changeColor(SKINS_MOUSE_POS)

        SKIN0_BUTTON.update(SCREEN)
        SKIN1_BUTTON.update(SCREEN)
        SKIN2_BUTTON.update(SCREEN)
        SKINS_BACK.update(SCREEN)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SKIN0_BUTTON.checkForInput(SKINS_MOUSE_POS):
                    skin = 0
                    exited = True  # Đặt biến exited thành True để thoát khỏi vòng lặp
                elif SKIN1_BUTTON.checkForInput(SKINS_MOUSE_POS):
                    skin = 1
                    exited = True
                elif SKIN2_BUTTON.checkForInput(SKINS_MOUSE_POS):
                    skin = 2
                    exited = True
                if SKINS_BACK.checkForInput(SKINS_MOUSE_POS):
                    exited = True
            pygame.display.update()
        skin_global=skin
    # Sau khi thoát khỏi vòng lặp, trở lại menu chính
    main_menu(skin_global)
def main_menu(skin_global):
    print("skin: ",skin_global)
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
        SKINS_BUTTON = Button(image=pygame.image.load("assets/button3.png"), pos =(600,530),
                            text_input="SKINS", font=get_font(65), base_color="#69330f", hovering_color="af613a")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button2.png"), pos=(600, 670), 
                            text_input="QUIT", font=get_font(65), base_color="#69330f", hovering_color="#af613a")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SKINS_BUTTON, QUIT_BUTTON]:
            #button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        main_game = MAIN() #Khởi tạo đối tượng main_game từ class MAIN

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                   snake_speed = main_game.snake.get_snake_speed()
                   play(snake_speed,0,skin_global)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_difficulty = options(main_game,skin_global) # Nhận giá trị snake_speed từ hàm options()
                    mode=options(main_game,skin_global)
                    if selected_difficulty and mode:
                        play(selected_difficulty,mode,skin_global)  # Truyền giá trị snake_speed vào hàm play() khi chọn chế độ
                if SKINS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    skin_global=skins(main_game)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    
#scroll_bg()
main_menu(0)
