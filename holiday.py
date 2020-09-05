class Holiday:
    def __init__(self, date, name, type, type_code):
        self.date = date
        self.name = name
        self.type = type
        self.type_code = type_code

    def __str__(self):
        return f'Data: {self.date}\tNome: {self.name}\tTipo: {self.type}'
