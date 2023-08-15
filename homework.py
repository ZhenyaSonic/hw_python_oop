from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    """LEN_STEP: длина шага."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

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
    CMSM: int = 18   # CALORIES_MEAN_SPEED_MULTIPLIER: CMSM
    CMSS: float = 1.79  # CALORIES_MEAN_SPEED_SHIFT: CMSS
    TYPE: str = 'RUN'

    def get_spent_calories(self) -> float:
        calories_1 = self.CMSM * self.get_mean_speed() + self.CMSS
        calories_2 = self.weight / self.M_IN_KM * self.duration * super().MIN
        calories = calories_1 * calories_2
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: float = 0.035  # коэффициент для расчета скорости ходьбы
    COEFF_2: int = 2  # коэффициент для расчета шагов на метр при ходьбе
    COEFF_3: float = 0.029  # коэффициент для расчета скорости бега
    TYPE: str = 'WLK'  # тип активности (ходьба)
    KMH_IN_MSEC: float = 0.278  # коэффициент перевода км/ч в м/с
    CM_IN_M: int = 100  # коэффициент перевода сантиметров в метры

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
    LEN_STEP: float = 1.38  # LEN_STEP : Длина гребка
    COEFF_SWIM_1: float = 1.1  # коэффициент для расчета скорости плавания
    TYPE: str = 'SWM'  # тип активности (плавание)
    COEFF_SWIM_2: int = 2  # коэф расчета количества движений рук и ног на метр

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


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[type(str, Training)] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in training_dict:
        raise ValueError(f"Unknown workout type: {workout_type}")
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
