class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
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
    TYPE = ''
    MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)
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
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    """CALORIES_MEAN_SPEED_MULTIPLIER = CMSM"""
    """CALORIES_MEAN_SPEED_SHIFT = CMSS"""
    CMSM: int = 18
    CMSS: float = 1.79
    TYPE = 'RUN'

    def get_spent_calories(self) -> float:
        calories_1 = self.CMSM * self.get_mean_speed() + self.CMSS
        calories_2 = self.weight / self.M_IN_KM * self.duration * super().MIN
        calories = calories_1 * calories_2
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: float = 0.035
    COEFF_2: int = 2
    COEFF_3: float = 0.029
    TYPE = 'WLK'
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_1 * self.weight
                    + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                       ** self.COEFF_2 / self.height
                     * self.CM_IN_M)
                    * self.COEFF_3 * self.weight) * self.duration
                    * super().MIN)
        calories_1 = self.COEFF_1 * self.weight
        calories_2 = self.get_mean_speed() * self.KMH_IN_MSEC
        calories_3 = calories_2 ** self.COEFF_2 / self.height * self.CM_IN_M
        calories_4 = calories_3 * self.COEFF_3 * self.weight
        calories = (calories_1 + calories_4) * self.duration * super().MIN
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    """LEN_STEP : Длина гребка"""
    LEN_STEP: float = 1.38
    COEFF_SWIM_1 = 1.1
    TYPE = 'SWM'
    COEFF_SWIM_2 = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / super().M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.COEFF_SWIM_1
        calories = calories_1 * self.COEFF_SWIM_2 * self.weight * self.duration
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
