def validate_wish(name, price):
    if not name or name.strip() == '':
        return 'Название не может быть пустым'
    try:
        p = float(price)
        if p < 0:
            return 'Цена не может быть отрицательной'
    except ValueError:
        return 'Цена должна быть числом'
    return None
