def validate_settings(length, letters, digits, symbols):
    if length < 4:
        raise ValueError("Минимальная длина пароля - 4 символа.")

    if length > 64:
        raise ValueError("Максимальная длина пароля - 64 символа.")

    if not any([letters, digits, symbols]):
        raise ValueError("Выберите хотя бы один тип символов.")