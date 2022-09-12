from src.data.data import Fields
from faker import Faker

faker_ru = Faker('ru_RU')
Faker.seed()


def generated_data_for_fill_fields():
    yield Fields(
        title=faker_ru.email(),
        description=faker_ru.address()
    )
