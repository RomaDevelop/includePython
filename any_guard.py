class AnyGuard:
    def __init__(self, setter_func, enter_value, exit_value):
        self.setter_func = setter_func
        self.enter_value = enter_value
        self.exit_value = exit_value

    def __enter__(self):
        self.setter_func(self.enter_value)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.setter_func(self.exit_value)

# в питоне нельзя передать в функцию bool по ссылке, поэтому только setter_func
# нельзя вот так (с переменной): def __init__(self, var, enter_value, exit_value)  ...  self.var = self.enter_value

# можно сделать ещё класс, который вместо вызова функции с начальным и конечным значением вызывает две разные функции