import pickle


def log_user(user: dict):
    """
    Logs a new user's info if not already exists.
    
    Args:
        user (dict): Contains user's info which consists of (username) as key, and (id, first name, last name) as dict value.
    
    Returns:
        None.
    """
    users: dict = {}
    key: str = list(user.keys())[0]
    
    try:
        with open('data/users.pkl', 'rb') as file:
            users = pickle.load(file)
    
    except FileNotFoundError:
        pass
    
    if len(users) == 0 or key not in list(users.keys()):
        users[key] = user[key]
        with open('data/users.pkl', 'wb') as file:
            pickle.dump(users, file)
        with open('data/users.txt', 'a+') as file:
            user_info: str = f"username: {key}, name: {user[key]['first_name']} {user[key]['last_name']}\n"
            file.write(user_info)


def calculate_factorial(number: int) -> int:
    """
    Calculates the factorial of a given number recursively.
    
    Args:
        number (int): The number to calculate factorial for.
        
    Returns:
        int: The result of the calculation.
    """
    if number == 1:
        return 1
    else:
        return number * calculate_factorial(number-1)