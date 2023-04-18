from random import randint
import time

# Класс куда пользователь будет ходить.

class Coordinate: # Класс координаты.
    def __init__(self, x, y): # Инициализирую точки.
        self.x = x
        self.y = y

    def __eq__(self, other):# Метод, который сравнивает 2 объекта.
        return self.x == other.x and self.y == other.y

    def __repr__(self): # Этот метод будет выводить более информативное строковое значение.
        return f'Coordinate({self.x}, {self.y})'

# Класс корабля

class Ship:
    def __init__(self, bow, long, orient): # В конструкторе класса объявлю поля: нос, длинна, ориентация корабля.
        self.bow = bow
        self.long = long
        self.orient = orient
        self.lives = long

    @property
    def points(self): # Создаю метод точки корабля.
        ship_points = [] # В этом списке будут храниться все точки у коробля.
        for i in range(self.long): # Прохожусь циклом.
            cor_x = self.bow.x
            cor_y = self.bow.y

            if self.orient == 0: # Если орентация корабля = 0, значит он вертикали.
                cor_x += i

            elif self.orient == 1: # Если орментация корабля = 1, значит он горизонтали.
                cor_y += i

            ship_points.append(Coordinate(cor_x, cor_y)) # Добавляю и получаю список точек.

        return ship_points

    def hit(self, hit): # Создаю метод попадание.
        return hit in self.points # Делаю проверку на попадание.

# Класс исключений.

class ClassException(Exception): # Класс исключений
    pass

class Placement(ClassException): # Класс размещения кораблей.
    pass

class CoordinateUsed(ClassException): # Класс наличия места.
    def __str__(self):
        return "Координата уже была использована."

class CoordinateException(ClassException): # Класс поля видимости.
    def __str__(self):
        return "Координаты вне поля видимости."

# Класс игровое поле.

class GameField:
    def __init__(self, size=6, hide=False): # Создаю поле размера и нужно ли его скрывать.
        self.size = size
        self.hide = hide
        self.stricken = 0 # Атрибут счетчик, который будет счить кол-во пораженных кораблей.
        self.field = [["0"] * size for n in range(size)] # Данный атрибут хранит состояние клетки.
        self.busy = [] # Список, куда уже стреляли.
        self.ships = [] # Список кораблей.

    def __str__(self): # Определяю __str__, чтобы не создавать отдельный метод.
        board = "" # Переменная в котрую будет записа вся доска.
        board += "  | 1 | 2 | 3 | 4 | 5 | 6 |"

        for i, row in enumerate(self.field): # Прохожусь в цикле по строком доски.
            board += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            board = board.replace("■", "0")
        return board

    def abroad(self, a): # Делаю проверку на то, что точка не выходит за поле.
        return not ((0 <= a.x < self.size) and (0 <= a.y < self.size))

    def contour(self, ship, verb = False): # Метод добавления корабля на доску.
        near = [ # Объявляю координаты, которые на находятся вокруг корабля.
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, -1),
            (1, -1), (1, 0), (1, 1)
        ]

        for i in ship.points: # При помощи данной конструкции прохожусь по всем координатам вокруг корабля.
            for ix, iy in near:
                cor = Coordinate(i.x + ix, i.y + iy)
                if not(self.abroad(cor)) and cor not in self.busy: # Если точка не занята и находится на игровом поле.
                    if verb: # Нужно ли будет расставлять точки.
                        self.field[cor.x][cor.y] = "."
                    self.busy.append(cor)

    def add_ship(self, ship): # Метод для размещения корабля.

        for i in ship.points: # Проверяю, чтобы указаные коордиенаты были не заняты и не выходили за пределы игрового поля.
            if self.abroad(i) or i in self.busy:
                raise Placement() # Иначе будет выходить искючение.

        for i in ship.points: # Прохожусь по точкам корабля.
            self.field[i.x][i.y] = "■" # Эти точки будут иметь значение "■"
            self.busy.append(i) # И эти точки будут добавлены в список занятых точек.

        self.ships.append(ship) # Добавляю в список кораблей.
        self.contour(ship) # Обвожу корабль по контуру.

    def shot(self, d): # Метод при пощи которого пользователь будет делать выстрел.
        if self.abroad(d): # Проверяю выходит ли координата за границы игрового поля.
            raise CoordinateException() # Если выходит выбрасывается исключение.

        if d in self.busy: # Проверяю занята ли координата.
            raise CoordinateUsed() # Если занята, выбрасывается исключение.
        self.busy.append(d) # Если не была занята, то добавляем её в список.

        for ship in self.ships: # Прохожусь циклом по кораблям.
            if ship.hit(d): # Если по кораблю попали.
                ship.lives -= 1 # Уменьшается кол-во жизней на одну.
                self.field[d.x][d.y] = "X" # И ставится крестик на место попадания.
                if ship.lives == 0: # Если у корабля кончились жизни.
                    self.stricken += 1 # Добавляю еденицу в счетчик пораженнх.
                    self.contour(ship, verb = True) # Контур корабля обозначется точками, если он был поражен.
                    print("Цель поражена!") # И выводится сообщение о паражении.
                    return False # Возвращаю False, чтобы понимать, что дальше ход делать не нужно.
                else: # Если корабль у корабля есть ещё жизни.
                    print("Есть пробитие!") # Выводится сообщение.
                    return True # Возвращаю True, чтобы понимать, дальше нужно сдеть ещё один ход.

        self.field[d.x][d.y] = "T" # Если небыло попаданий по корабля мставится точка.
        print("Мимо!") # Выодится сообщение о промахе.
        return False # Возвращаю False, чтобы понимать, что дальше ход делать не нужно.

    def begin(self): # При помощи данного метода обнуляю счетчик.
        self.busy = []

    def defeat(self): # Метод проверки пораженных кораблей и имеющихся на игровм поле.
        return self.stricken == len(self.ships)

# Класс "Игрок"

class Player:
    def __init__(self, board, rival): # В качестве аргументов атрибуту пердеются два игровых поля, самого игрока и соперника.
        self.board = board
        self.rival = rival

    def ask(self): # Этот метод создан для дочерних классов.
        raise NotImplementedError()

    def move(self):
        while True: # Создаю бесконечный цикл.
            try:
                target = self.ask() # прошу одного из игроков указать координаты выстрела.
                repeat = self.rival.shot(target) # Осуществление самого выстрела.
                return repeat # Если все прошло гладко, повторяем вопрос, но уже у другого игрока.
            except ClassException as e: # Если выстрел был сдела не верно, то вылетает исключение и повторяем цикл заново.
                print(e)

# Класс "Игрок-компьютер"

class AI(Player):
    def ask(self):
        print("Я думаю ...")
        time.sleep(3) # Делаю симуляцию раздумывания.
        a = Coordinate(randint(0, 5), randint(0, 5)) # Случайно генерирует 2 точки в диапазоне от 0, до 5.
        print(f"Ходит компьютер: {a.x + 1} {a.y + 1}")
        return a

# Класс Пользователя.

class User(Player):
    def ask(self):
        while True: # Созаю бесконечный цикл.
            cords = input("Введите координаты куда хотели бы сходить: ").split()

            if len(cords) != 2: # Проверяю, чтобы было введено именно 2 координаты.
                print("Необходимо ввести 2 координаты!")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()): # Проверка на то, чтобы все символы были числами.
                print("Необходимо ввести числа! ")
                continue

            x, y = int(x), int(y)

            return Coordinate(x - 1, y - 1)

# Класс Игра

class Game:

    def __init__(self, size = 6): # Задаю размер игрового поля.
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        player = self.random_board() # Создается рандомное поля для игрока.
        comp = self.random_board() # Создается рандомное поля для компьютера.
        comp.hide = True # Для компьютера скрываются корабли.

        # Создаются игроки и передаются им доски.

        self.ai = AI(comp, player)
        self.user = User(player, comp)

    def board_generation(self): # Метрод, который будет создавать доску.
        board = GameField(size = self.size) # Создание доски.
        attempts = 0 # Переменная счетчик, которая будет считать кол-во попыток расстановки кораблей.
        for n in self.lens: # Для каждой клинны корбаля будем пытаться его поставить.
            while True: # Для этого создается бесконечный цикл.
                attempts += 1 # Каждый раз счетчик будет увеличиваться на 1.
                if attempts > 2000: # Если кол-во попыток больше 2000.
                    return None # Вернется пустое игровое поле.
                ship = Ship(Coordinate(randint(0, self.size), randint(0, self.size)), n, randint(0, 1))
                try:
                    board.add_ship(ship) # Происходит добавление корабля.
                    break # Если все получилось, тогда этот цикл заканчивается.
                except Placement: # Если выбрасывает исключение, то цикл начинает снова.
                    pass
        board.begin() # Обнуляю игровое поле.
        return board

    def random_board(self): # Метод генерирующий случайную доску.
        board = None # Сперва доска пустая.
        while board is None:
            board = self.board_generation() # В бесконечном цикле игровое поле создается и когда оно сформируется.
            return board # Возвращается игровое поле.

    def greetings(self):  # Метод "приветствие".
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~Добро пожаловать в игру!~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~Sea Battle~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~Первое значение - № строки~~")
        print("~~Второе значение - № столбца~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('')

    def print_board(self):
        print("~" * 27)
        print("Поле боя User")
        print(self.user.board)
        print("~" * 27)
        print("Поле боя компьютера")
        print(self.ai.board)
        print("~" * 27)

    def game_loop(self): # Метод иговой цикл.
        num = 0 # Переменная номер хода.
        while True:
            self.print_board()
            if num % 2 == 0: # Если номер хода четный, ходит пользователь.
                print("Ходит User!")
                repeat = self.user.move() # Сюда записывается результат хода.
            else: # Иначе ходит компьютер.
                print("Ходит компьютер!")
                repeat = self.ai.move() # Сюда записывается результат хода.

            if repeat: # Если нужно повторить ход, то переменная уменьшается на 1, чтобы ход остался того же игрока.
                num -= 1

            if self.ai.board.defeat(): # Если все корабли компьютера уничтожены, выиграл пользователь.
                self.print_board()
                print("~" * 20)
                print("User выиграл!")
                break

            if self.user.board.defeat(): # Если все корабли пользователя уничтожены, выиграл компьютер.
                self.print_board()
                print("~" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self): # Метод начала игры.
        self.greetings()
        self.game_loop()

g = Game()
g.start()