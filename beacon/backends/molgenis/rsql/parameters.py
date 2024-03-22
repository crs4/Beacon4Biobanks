class Parameter:
    def __init__(self, attribute, operator, values: list):
        self.attribute = attribute
        self.operator = operator
        self.values = values

    def get_values(self):
        return self.values

    def set_values(self, values):
        self.values = values

    def get_rsql(self):
        if self.attribute == '':
            return ''
        if self.operator == 'in':
            return f'{self.attribute}=in=({",".join(self.values)})'
        else:  # contains operator
            return ' or '.join(f'{self.attribute}=like="{v}"' for v in self.values)
