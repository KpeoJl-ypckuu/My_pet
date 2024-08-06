import pygame as pg
import random
import json

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80
PADDING = 5
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
DOG_WIDNT = PADDING + 400
DOG_HEIGHT = PADDING + 250
MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130
FOOD_SIZE = 100
TOY_SIZE = 100
FPS = 60


font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)

def load_image(file, widht, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (widht, height))
    return image


def text_render(text):
    return font.render(str(text), True, 'black')

class Item:
    def __init__(self, name_item, price, file, is_put_on=False, is_bought=False):
        self.name = name_item
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on
        self.file = file
        self.image = load_image(file, DOG_WIDNT // 1.7, DOG_HEIGHT)
        self.full_image = load_image(file, ICON_SIZE + 200, ICON_SIZE + 300)

class Food:
    def __init__(self, name, price, file, satiety, medicine_power = 0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_power = medicine_power
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image ("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image ("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    
        self.items = [Food("Мясо", 10, "Images/food/meat.png", 10), Food("Корм", 50, "images/food/dog food.png", 15), Food("Элитный корм", 50, "images/food/dog food elite.png", 25, medicine_power = 2), Food("Лекарство", 50, "images/food/medicine.png", 0, medicine_power = 200)]
    
        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button('Вперёд', SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)
        self.prev_button = Button('Назад', MENU_NAV_XPAD, SCREEN_HEIGHT - MENU_NAV_YPAD, width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_prev)
        self.buy_button = Button('Съесть', SCREEN_WIDTH // 2 - int (BUTTON_WIDTH // 1.5) // 2, SCREEN_HEIGHT // 2 + 95, width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5), func=self.buy)

        

        

        

    

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1 

    def to_prev(self):
        if self.current_item > 0:
            self.current_item -= 1

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100


    def update(self):
        self.next_button.update()
        self.prev_button.update()
       
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clecked(event)
        self.prev_button.is_clecked(event)
        self.buy_button.is_clecked(event)


    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        
            
        self.next_button.draw(screen)
        self.prev_button.draw(screen)
        self.buy_button.draw(screen)

        
class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image ("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image ("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
    
        self.items = []
        for item in data:
            self.items.append(Item(*item.values()))
    
        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button('Вперёд', SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)
        self.prev_button = Button('Назад', MENU_NAV_XPAD, SCREEN_HEIGHT - MENU_NAV_YPAD, width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_prev)
        self.put_on_button = Button('Надеть', SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD - 60, width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.use_item)
        self.buy_button = Button('Купить', SCREEN_WIDTH // 2 - int (BUTTON_WIDTH // 1.5) // 2, SCREEN_HEIGHT // 2 + 95, width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5), func=self.buy)

        self.text_font = font 
        self.text_is_put_on = self.text_font.render(str('Надето'), True, 'Black')
        self.text_rect = self.text_is_put_on.get_rect()
        self.text_rect.center = (700, 120)

        self.text_not_put_on = self.text_font.render(str('не надето'), True, 'Black')
        self.text_rect = self.text_not_put_on.get_rect()
        self.text_rect.center = (700, 120)

        self.use_text = text_render ( "Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH - 150, 130)

        self.buy_text = text_render ("Куплено")
        self.buy_text_rect = self. buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH - 140,200)


        

    def use_item(self):
        self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1 

    def to_prev(self):
        if self.current_item > 0:
            self.current_item -= 1

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True


    def update(self):
        self.next_button.update()
        self.prev_button.update()
        self.put_on_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clecked(event)
        self.prev_button.is_clecked(event)
        self.put_on_button.is_clecked(event)
        self.buy_button.is_clecked(event)


    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
            screen.blit(self.buy_text, self.buy_text_rect)
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_put_on:
            screen.blit(self.bottom_label_on, (0, -80))
            screen.blit(self.text_is_put_on, self.text_rect)
        else:
            screen.blit(self.bottom_label_off, (0, -80))
            screen.blit(self.text_not_put_on, self.text_rect)

        self.next_button.draw(screen)
        self.prev_button.draw(screen)
        self.put_on_button.draw(screen)
        self.buy_button.draw(screen)



class Toy(pg.sprite.Sprite):
    def __init__(self):
        toys_images = [load_image('images/toys/ball.png', TOY_SIZE, TOY_SIZE), load_image('images/toys/blue bone.png', TOY_SIZE, TOY_SIZE), load_image('images/toys/red bone.png', TOY_SIZE, TOY_SIZE)]
        pg.sprite.Sprite.__init__(self)
        number_toy = random.randint(0,2)
        x = random.randint(PADDING, SCREEN_WIDTH - PADDING)
        self.image = toys_images[number_toy]
        self.rect = self.image.get_rect(center = (x, 0))
        
    def update(self):
        self.rect.y += 5
    
    


    

class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('images/dog.png', DOG_WIDNT // 2, DOG_HEIGHT // 2)
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2))
        self.speed = 5

    def update(self):
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] == True and self.rect.left > 0:
            self.rect.x = self.rect.x - self.speed
        if keys[pg.K_RIGHT] == True and self.rect.right < 1510:
            self.rect.x = self.rect.x + self.speed

class MiniGame:
    def __init__(self, game):
        self.game = game
        self.background = load_image('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5


    def new_game(self):
        self.background = load_image('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 60

    def update(self):
        
        self.dog.update()
        self.toys.update()
        if random.randint(0, 100) == 0:
            self.toys.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happines += int(self.score // 2)
            self.game.mode = "Main"


    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.dog.image, self.dog.rect)
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))
        self.toys.draw(screen)




class Button:
    def __init__ (self, text, x, y, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text_font = font, func = None):
        self.func = func
        self.idle_image = load_image("images/button.png", width, height)
        self.pressed_image = load_image("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.is_pressed = False
        
        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, 'Black')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clecked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False



class Game:
    def __init__(self):
        with open('save.json', encoding='UTF-8') as f:
            data = json.load(f)
        self.coins_per_second = data['coins_per_second']
        self.costs_of_upgrade = {}
        for key, value in data['costs_of_upgrade'].items():
            self.costs_of_upgrade[int(key)] = value
        self.clock = pg.time.Clock()
        self.start = True
        


        self.mode = 'Main'
        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.happines = data['happines']
        self.satiety = data['satiety']
        self.health = data['health']
        self.money = data['money']

        self.background = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happiness_image = load_image('images/happiness.png', ICON_SIZE, ICON_SIZE)
        self.satiety_image = load_image('images/satiety.png', ICON_SIZE, ICON_SIZE)
        self.health_image = load_image('images/health.png', ICON_SIZE, ICON_SIZE)
        self.money_image = load_image('images/money.png', ICON_SIZE, ICON_SIZE)
        self.pet_image = load_image('images/dog.png', ICON_SIZE + 200, ICON_SIZE + 300)
        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING
        self.eat_button = Button('еда',button_x, PADDING + ICON_SIZE, func=self.food_menu_on)
        self.clothes_button = Button('одежда',button_x, PADDING + ICON_SIZE * 2, func=self.clothes_menu_on)
        self.mini_game_button = Button('мини игры', button_x, PADDING + ICON_SIZE * 3, func = self.game_on)
        
        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0, width = BUTTON_WIDTH // 3, height = BUTTON_HEIGHT // 3, text_font = mini_font, func = self.increase_money)

        self.buttons = [self.eat_button, self.clothes_button, self.mini_game_button, self.upgrade_button]
        
        self.clothes_menu = ClothesMenu(self, data["clothes"])

        self.DECREASE = pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE, 10000)
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        
        self.food_menu = FoodMenu(self)

        self.mini_game = MiniGame(self)

        self.run()
    

    def clothes_menu_on(self):
        self.mode = 'Clothes menu'

    def food_menu_on(self):
        self.mode = 'Food menu'

    def game_on(self):
        self.mode = 'Mini game'
        self.mini_game.new_game()
        

    def increase_money(self):
        for key in self.costs_of_upgrade:
            if self.costs_of_upgrade[key] == False and self.money >= key:
                self.money = self.money - key
                self.coins_per_second = self.coins_per_second + 1
                self.costs_of_upgrade[key] = True
                break

     

                




    def run(self):
        
        while self.start:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == 'Game over':
                    {
                    "happines" : 100,
                    "satiety" : 100,
                    "health" : 100,
                    "money" : 0,
                    "coins_per_second" : 1,
                    "costs_of_upgrade" : {
                        "100": False,
                        "1000": False,
                        "5000": False,
                        "10000": False
                        },

                        "clothes": [

                                        {

                                        "name" : "синяя футболка",
                                        "price" : 10,
                                        "image" : "images/items/blue t-shirt.png",

                                        "is_put_on": False,
                                        "is_bought": False
                                        },
                                        {
                                        "name" : "Ботинки",
                                        "price" : 50,
                                        "image" : "images/items/boots.png",
                                        "is_put_on": False,
                                        "is_bought": False
                                        },
                                        {
                                        "name" : "Шляпа",
                                        "price" : 50,
                                        "image" : "images/items/hat.png",
                                        "is_put_on": False,
                                        "is_bought": False
                                        }
                                    ]

                    }

                else:
                    data = {
                    "happines" : 100,
                    "satiety" : 100,
                    "health" : 100,
                    "money" : 0,
                    "coins_per_second" : 1,
                    "costs_of_upgrade" : {
                        "100": False,
                        "1000": False,
                        "5000": False,
                        "10000": False
                    },
                    "clothes": []
                }
                    
                for item in self.clothes_menu.items:
                    data["clothes"].append({"name": item.name,
                                            "price": item.price,
                                            "image": item.file,
                                            "is_put_on": item.is_put_on,
                                            "is_bought": item.is_bought})
                
                with open('save.json', 'w', encoding='UTF-8') as f:
                    json.dump(data, f, ensure_ascii=False)

                self.start = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = 'Main'

            
            
            

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happines -= 1
                else:
                    self.health -= 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money = self.money + self.coins_per_second
            
            

            if self.mode == 'Main':
                for button in self.buttons:
                    button.is_clecked(event)

            elif self.mode != 'Main':
                self.clothes_menu.is_clicked(event)
                self.food_menu.is_clicked(event)



            
              
            

    def update(self):
        if self.mode == 'Clothes menu':
            self.clothes_menu.update()
        elif self.mode == 'Food menu':
            self.food_menu.update()
        elif self.mode == 'Mini game':
            self.mini_game.update()
        else:
            self.eat_button.update()
            self.clothes_button.update()
            self.mini_game_button.update()
            self.upgrade_button.update()
        if self.happines <= 0 or self.satiety <= 0 or self.health <= 0:
            self.mode = 'Game over'
        

    def draw(self):
        # отрисовка иконок стат
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiety_image, (PADDING, PADDING + 80))
        self.screen.blit(self.health_image, (PADDING, PADDING + 160))
        self.screen.blit(self.money_image, (PADDING + 815, PADDING))
        self.screen.blit(self.pet_image, (450 - (DOG_WIDNT // 2), 225 - (DOG_HEIGHT // 2)))

        # отрисовка значений стат
        self.screen.blit(text_render(self.happines), (PADDING + ICON_SIZE, PADDING * 6))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 22))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 38))
        self.screen.blit(text_render(self.money), (PADDING + 800, PADDING * 6))
        # отрисовка кнопок
        self.eat_button.draw(self.screen)
        self.clothes_button.draw(self.screen)
        self.mini_game_button.draw(self.screen)
        self.upgrade_button.draw(self.screen)
        # отрисовка меню
        if self.mode == 'Clothes menu':
            self.clothes_menu.draw(self.screen)
        
        if self.mode == 'Food menu':
            self.food_menu.draw(self.screen)

        if self.mode == 'Mini game':
            self.mini_game.draw(self.screen)
        
        if self.mode == 'Game over':
            text = font_maxi.render('ПРОИГРЫШ, ВЫ НЕ УСЛЕДИЛИ ЗА СОСТОЯНИЕМ', True, 'red')
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
        # отрисовка одежды на собаке

        for item in self.clothes_menu.items:
            if item.is_put_on and self.mode == 'Main':
               self.screen.blit(item.full_image, (450 - (DOG_WIDNT // 2), 225 - (DOG_HEIGHT // 2)))
            
        pg.display.flip()



if __name__ == "__main__":
    Game()