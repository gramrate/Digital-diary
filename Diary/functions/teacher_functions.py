def Teacher(func):
    def wrapper(*args, **kwargs):
        # Проверка на учителя
        func(*args, **kwargs) # Если да

    return wrapper

