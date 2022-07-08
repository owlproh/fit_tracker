class InfoMessage:    # кончено
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.__class__.get_distance(self),
                           self.__class__.get_mean_speed(self),
                           self.__class__.get_spent_calories(self))


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())    # тут типа проблема


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trains = {'SWM': Swimming,
              'RUN': Running,
              'WLK': SportsWalking}
    return trains[workout_type](*data)


class Running(Training):    # кончено
    """Тренировка: бег."""
    coef_1r = 18
    coef_2r = 20

    def get_spent_calories(self) -> float:
        cal_r = ((self.coef_1r * self.get_mean_speed()
                 - self.coef_2r) * self.weight
                 / self.M_IN_KM * self.duration * 60)
        return cal_r


class SportsWalking(Training):    # кончено
    """Тренировка: спортивная ходьба."""
    coef_1sw = 0.035
    coef_2sw = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.duration = duration

    def get_spent_calories(self) -> float:
        cal_sw = ((self.coef_1sw * self.weight
                  + (self.get_mean_speed() ** 2 // self.height)
                  * self.coef_2sw * self.weight)
                  * self.duration * 60)
        return cal_sw


class Swimming(Training):    # кончено
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coef_1s = 1.1

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        sw_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                    / self.duration)
        return sw_speed

    def get_spent_calories(self) -> float:
        cal_s = ((self.get_mean_speed() + self.coef_1s)
                 * 2 * self.weight)
        return cal_s


if __name__ == '__main__':    # вроде норм
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),  # 1206, 16, 6
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
