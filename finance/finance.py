from datetime import datetime, date

class FinanceRecord:
    def __init__(self, id, type, amount, category, date, description):
        self.id = id
        self.type = type
        self.amount = amount
        self.category = category
        try:
            self.date = datetime.strptime(date, "%d-%m-%Y").date()
        except (TypeError, ValueError):
            self.date = date
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%d-%m-%Y").date()
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%d-%m-%Y"),
            "description": self.description
        }
