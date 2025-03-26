# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) 
# и методы (`make_sound()`, `eat()`) для всех животных.
# 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`. 
# Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
# 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных 
# и вызывает метод `make_sound()` для каждого животного.
# 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках. 
# Должны быть методы для добавления животных и сотрудников в зоопарк.
# 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические методы 
# (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).
# Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл 
# и возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.
from errno import ENAMETOOLONG


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        return "Издает животный звук"

    def eat(self):
        return f"{self.name} поедает."


class Bird(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def make_sound(self):
        return "Чик-чирик!"


class Mammal(Animal):
    def __init__(self, name, age, weight):
        super().__init__(name, age)
        self.weight = weight

    def make_sound(self):
        return "Ррррррррыыык-бля-ик!"


class Reptile(Animal):
    def __init__(self, name, age, length):
        super().__init__(name, age)
        self.length = length

    def make_sound(self):
        return "Шшшшшшсссссссуууккк!"


class Worker:
    def __init__(self, name):
        self.name = name

    def work(self):
        return f"{self.name} работник зоопарка."


class ZooKeeper(Worker):
    def feed_animal(self, animal):
        return f"{self.name} кормит {animal.name}."


class Veterinarian(Worker):
    def heal_animal(self, animal):
        return f"{self.name} лечит {animal.name}."


class Zoo:
    def __init__(self):
        self.animals = []
        self.workers = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def add_worker(self, worker):
        self.workers.append(worker)

    def save_to_file(self, filename="zoo.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Животные:\n")
            file.write("{:<15} {:<10} {:<15}\n".format("Вид", "Имя", "Возраст"))
            file.write("-" * 40 + "\n")
            for animal in self.animals:
                extra_attr = ""
                if isinstance(animal, Bird):
                    extra_attr = f"Цвет: {animal.color}"
                elif isinstance(animal, Mammal):
                    extra_attr = f"Вес: {animal.weight} кг"
                elif isinstance(animal, Reptile):
                    extra_attr = f"Длина: {animal.length} м"
                file.write(
                    "{:<15} {:<10} {:<15} {}\n".format(animal.__class__.__name__, animal.name, animal.age, extra_attr))

            file.write("\nСотрудники:\n")
            file.write("{:<15} {:<10}\n".format("Должность", "Имя"))
            file.write("-" * 30 + "\n")
            for worker in self.workers:
                file.write("{:<15} {:<10}\n".format(worker.__class__.__name__, worker.name))

    def load_from_file(self, filename="zoo.txt"):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        self.animals.clear()
        self.workers.clear()

        is_animal_section = False
        is_worker_section = False

        for line in lines:
            line = line.strip()
            if not line or "----" in line:
                continue  # Пропускаем пустые строки и разделители

            if "Животные:" in line:
                is_animal_section = True
                is_worker_section = False
                continue
            elif "Сотрудники:" in line:
                is_animal_section = False
                is_worker_section = True
                continue

            parts = line.split()
            if is_animal_section and len(parts) >= 3:
                animal_type = parts[0]
                name = parts[1]
                try:
                    age = int(parts[2])
                except ValueError:
                    continue  # Если возраст не число, пропускаем строку

                extra_attr = " ".join(parts[3:])

                if animal_type == "Bird":
                    color = extra_attr.replace("Цвет: ", "").strip()
                    self.animals.append(Bird(name, age, color))
                elif animal_type == "Mammal":
                    try:
                        weight = int(extra_attr.replace("Вес: ", "").replace(" кг", "").strip())
                        self.animals.append(Mammal(name, age, weight))
                    except ValueError:
                        continue  # Пропускаем ошибочные строки
                elif animal_type == "Reptile":
                    try:
                        length = int(extra_attr.replace("Длина: ", "").replace(" м", "").strip())
                        self.animals.append(Reptile(name, age, length))
                    except ValueError:
                        continue

            elif is_worker_section and len(parts) >= 2:
                worker_type, name = parts[:2]
                if worker_type == "ZooKeeper":
                    self.workers.append(ZooKeeper(name))
                elif worker_type == "Veterinarian":
                    self.workers.append(Veterinarian(name))


zoo = Zoo()
zoo.add_animal(Bird("Воробей", 2, "Коричневый"))
zoo.add_animal(Mammal("Лев", 5, 190))
zoo.add_animal(Reptile("Змей", 3, 2))

keeper1 = ZooKeeper("Вано")
keeper2 = ZooKeeper("Педро")
veterinarian = Veterinarian("Гюзель Мухтаровна")
zoo.add_worker(keeper1)
zoo.add_worker(keeper2)
zoo.add_worker(veterinarian)

zoo.save_to_file()
zoo.load_from_file()

for animal in zoo.animals:
    print(animal.make_sound())