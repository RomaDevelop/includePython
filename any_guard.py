class AnyGuard:
    def __init__(self, var, enter_value=True, exit_value=False):
        self.var = var
        self.enter_value = enter_value
        self.exit_value = exit_value

    def __enter__(self):
        self.var = self.enter_value   # Устанавливаем новое значение
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.var = self.exit_value     # Устанавливаем значение при выходе