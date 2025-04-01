from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class ICharacterBuilder(ABC):
    @abstractmethod
    def set_name(self, name: str) -> 'ICharacterBuilder':
        pass

    @abstractmethod
    def set_race(self, race: str) -> 'ICharacterBuilder':
        pass

    @abstractmethod
    def set_class(self, char_class: str) -> 'ICharacterBuilder':
        pass

    @abstractmethod
    def set_weapon(self, weapon: str) -> 'ICharacterBuilder':
        pass

    @abstractmethod
    def set_magic(self, magic: str) -> 'ICharacterBuilder':
        pass

    @abstractmethod
    def build(self) -> Dict[str, str]:
        pass

class Character:
    def __init__(self):
        self._attributes: Dict[str, Optional[str]] = {
            'name': None,
            'race': None,
            'class': None,
            'weapon': None,
            'magic': None
        }

    def set_attribute(self, key: str, value: str) -> None:
        self._attributes[key] = value

    def get_attributes(self) -> Dict[str, Optional[str]]:
        return self._attributes


class CharacterValidator:
    @staticmethod
    def validate_race(race: str, valid_races: List[str]) -> bool:
        return race.lower() in valid_races

    @staticmethod
    def validate_class(char_class: str, valid_classes: List[str]) -> bool:
        return char_class.lower() in valid_classes

    @staticmethod
    def validate_not_empty(value: str) -> bool:
        return bool(value.strip())


class CharacterBuilder(ICharacterBuilder):
    def __init__(self):
        self._character = Character()
        self._validator = CharacterValidator()
        self._valid_races = ['человек', 'эльф', 'гном', 'орк', 'дварф']
        self._valid_classes = ['воин', 'маг', 'лучник', 'жрец', 'разбойник']

    def set_name(self, name: str) -> 'CharacterBuilder':
        if self._validator.validate_not_empty(name):
            self._character.set_attribute('name', name)
        else:
            raise ValueError("Имя не может быть пустым")
        return self

    def set_race(self, race: str) -> 'CharacterBuilder':
        if self._validator.validate_race(race, self._valid_races):
            self._character.set_attribute('race', race.lower())
        else:
            raise ValueError(f"Недопустимая раса. Допустимые расы: {', '.join(self._valid_races)}")
        return self

    def set_class(self, char_class: str) -> 'CharacterBuilder':
        if self._validator.validate_class(char_class, self._valid_classes):
            self._character.set_attribute('class', char_class.lower())
        else:
            raise ValueError(f"Недопустимый класс. Допустимые классы: {', '.join(self._valid_classes)}")
        return self

    def set_weapon(self, weapon: str) -> 'CharacterBuilder':
        if self._validator.validate_not_empty(weapon):
            self._character.set_attribute('weapon', weapon)
        else:
            raise ValueError("Оружие не может быть пустым")
        return self

    def set_magic(self, magic: str) -> 'CharacterBuilder':
        self._character.set_attribute('magic', magic)
        return self

    def build(self) -> Dict[str, Optional[str]]:
        attributes = self._character.get_attributes()
        if not all([attributes['name'], attributes['race'], attributes['class']]):
            raise ValueError("Не заполнены обязательные поля: имя, раса и класс")
        return attributes


class ICharacterDisplayer(ABC):
    @abstractmethod
    def display(self, character: Dict[str, Optional[str]]) -> None:
        pass


class ConsoleCharacterDisplayer(ICharacterDisplayer):
    def display(self, character: Dict[str, Optional[str]]) -> None:
        print("\nСоздан персонаж:")
        for key, value in character.items():
            print(f"{key}: {value}")


class CharacterDirector:
    @staticmethod
    def create_character(builder: ICharacterBuilder, displayer: ICharacterDisplayer) -> Dict[str, Optional[str]]:
        try:
            character = (builder
                         .set_name(input("Введите имя персонажа: "))
                         .set_race(input("Введите расу персонажа: "))
                         .set_class(input("Введите класс персонажа: "))
                         .set_weapon(input("Введите оружие персонажа: "))
                         .set_magic(input("Введите магию персонажа (или оставьте пустым): "))
                         .build())
            displayer.display(character)
            return character
        except ValueError as e:
            print(f"Ошибка: {e}")
            return {}


def main():
    print("=== Создание персонажа ===")
    builder = CharacterBuilder()
    displayer = ConsoleCharacterDisplayer()
    CharacterDirector.create_character(builder, displayer)


if __name__ == "__main__":
    main()