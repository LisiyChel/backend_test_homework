class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type:str, duration:float, distance:float, speed:float, calories:float)-> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed=speed
        self.calories=calories

    def get_message(self)->str:
        return (f'Тип тренировки: {self.training_type}; '
        f'Длительность: {self.duration:.3f} ч.; '
        f'Дистанция: {self.distance:.3f} км; '
        f'Ср. скорость: {self.speed:.3f} км/ч; '
        f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
   
    LEN_STEP:float = 0.65
    M_IN_KM:int = 1000
    MIN_IN_HOUR: int = 60

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration        

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
   
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())        


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
         super().__init__(action, duration, weight)  
   
    def get_spent_calories(self) -> float:
        kcal_coeff_1:int = 18
        kcal_coeff_2:int = 20
        return ((kcal_coeff_1 * Training.get_mean_speed(self) - kcal_coeff_2) * 
                 self.weight / Training.M_IN_KM * (self.duration*Training.MIN_IN_HOUR))

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    
    def __init__(self, action, duration, weight, height:float):
        super().__init__(action, duration, weight)
        self.height = height
   
    def get_spent_calories(self) -> float:
        kcal_coeff_1 = 0.035
        kcal_coeff_2 = 0.029
        return ((kcal_coeff_1 * self.weight + (Training.get_mean_speed(self)**2 // self.weight) *
                 kcal_coeff_2 * self.height) * (self.duration * Training.MIN_IN_HOUR))        


class Swimming(Training):
    """Тренировка: плавание."""
    
    LEN_STEP : float = 1.38

    def __init__(self, action, duration, weight, length_pool:int, count_pool:int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
       mean_speed = self.length_pool * self.count_pool / Training.M_IN_KM / self.duration
       return mean_speed

    def get_spent_calories(self) -> float:
        kcal_coeff_1 = 1.1
        kcal_coeff_2 = 2
        return (self.get_mean_speed() + kcal_coeff_1) * kcal_coeff_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    get_information  = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return get_information[workout_type](*data)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
