from django.db import models

# Create your models here.
class Ingredient(models.Model):
    UNIT_TYPES = [
        ("count", "By Item"),
        ("weight", "By Weight")
    ]
    UNITS = [
        ("kg", "kilograms"),
        ("lb", "pounds"),
        ("g", "grams"),
        ("oz", "ounces"),
        ("l", "liters"),
        ("ml", "milliliters"),
        ("fl oz", "fluid ounces")
    ]

    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=10, choices=UNIT_TYPES)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNITS)

    def __str__(self):
        return self.name