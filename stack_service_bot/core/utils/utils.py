import random
import string

def generate_password(length):
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов")
    
    # Определяем наборы символов
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    # Объединяем все символы
    all_chars = lowercase + uppercase + digits + special_chars
    
    # Гарантируем, что пароль содержит хотя бы один символ из каждой категории
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Заполняем оставшуюся часть пароля случайными символами из всех категорий
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    
    # Перемешиваем символы, чтобы порядок не был предсказуемым
    random.shuffle(password)
    
    # Преобразуем список в строку
    return ''.join(password)

