from dataclasses import dataclass
from typing import Callable


def has_lowercase(password: str) -> bool:
	return any(character.islower() for character in password)


def has_uppercase(password: str) -> bool:
	return any(character.isupper() for character in password)


def has_digit(password: str) -> bool:
	return any(character.isdigit() for character in password)


def has_special_character(password: str) -> bool:
	return any(not character.isalnum() and not character.isspace() for character in password)


def has_no_spaces(password: str) -> bool:
	return not any(character.isspace() for character in password)


@dataclass(frozen=True)
class ValidationResult:
	level: str
	message: str


class WeakPasswordValidator:
	def validate(self, password: str) -> bool:
		return len(password) >= 6


class MediumPasswordValidator:
	def validate(self, password: str) -> bool:
		checks: tuple[Callable[[str], bool], ...] = (
			lambda value: len(value) >= 8,
			has_lowercase,
			has_uppercase,
			has_digit,
		)
		return all(check(password) for check in checks)


class StrongPasswordValidator:
	def validate(self, password: str) -> bool:
		checks: tuple[Callable[[str], bool], ...] = (
			lambda value: len(value) >= 12,
			has_lowercase,
			has_uppercase,
			has_digit,
			has_special_character,
			has_no_spaces,
		)
		return all(check(password) for check in checks)


class PasswordValidator:
	def __init__(self) -> None:
		self.strong_validator = StrongPasswordValidator()
		self.medium_validator = MediumPasswordValidator()
		self.weak_validator = WeakPasswordValidator()

	def validate(self, password: str) -> ValidationResult:
		if self.strong_validator.validate(password):
			return ValidationResult("высокий", "Пароль очень надёжный")
		if self.medium_validator.validate(password):
			return ValidationResult("средний", "Пароль достаточно надёжный")
		if self.weak_validator.validate(password):
			return ValidationResult("слабый", "Пароль нужно усилить")
		return ValidationResult("слабый", "Пароль слишком короткий")


def main() -> None:
	password = input("Введите пароль: ")
	result = PasswordValidator().validate(password)
	print(f"Уровень: {result.level}")
	print(result.message)


if __name__ == "__main__":
	main()
