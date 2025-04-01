import pandas as pd
import os


class PasswordManager:
    _instances = {}

    def __new__(cls, account):
        if account not in cls._instances:
            cls._instances[account] = super(PasswordManager, cls).__new__(cls)
            cls._instances[account]._initialized = False
        return cls._instances[account]

    def __init__(self, account):
        if not self._initialized:
            self.account = account
            self.password = self._load_password()
            self._initialized = True

    def _load_password(self):
        if not os.path.exists('passwords.xlsx'):
            return None

        try:
            df = pd.read_excel('passwords.xlsx')
            account_row = df[df['Account'] == self.account]
            if not account_row.empty:
                return account_row['Password'].values[0]
            return None
        except Exception as e:
            print(f"Ошибка при загрузке пароля: {e}")
            return None

    def set_password(self, password):
        self.password = password
        self._save_password()
        print(f"\nПароль для аккаунта '{self.account}' успешно сохранён!")

    def get_password(self):
        return self.password

    def _save_password(self):
        data = {'Account': [], 'Password': []}

        if os.path.exists('passwords.xlsx'):
            try:
                existing_df = pd.read_excel('passwords.xlsx')
                data['Account'] = existing_df['Account'].tolist()
                data['Password'] = existing_df['Password'].tolist()
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")

        if self.account in data['Account']:
            index = data['Account'].index(self.account)
            data['Password'][index] = self.password
        else:
            data['Account'].append(self.account)
            data['Password'].append(self.password)

        df = pd.DataFrame(data)
        try:
            df.to_excel('passwords.xlsx', index=False)
        except Exception as e:
            print(f"Ошибка при сохранении пароля: {e}")

    @classmethod
    def get_all_accounts(cls):
        if not os.path.exists('passwords.xlsx'):
            return []

        try:
            df = pd.read_excel('passwords.xlsx')
            return df['Account'].tolist()
        except Exception as e:
            print(f"Ошибка при чтении списка аккаунтов: {e}")
            return []


def display_menu():
    print("\n" + "=" * 40)
    print("МЕНЕДЖЕР ПАРОЛЕЙ".center(40))
    print("=" * 40)
    print("1. Посмотреть все аккаунты")
    print("2. Добавить/изменить пароль")
    print("3. Посмотреть пароль")
    print("4. Выход")
    print("=" * 40)


def main():
    while True:
        display_menu()
        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            accounts = PasswordManager.get_all_accounts()
            if accounts:
                print("\nСписок аккаунтов:")
                for i, account in enumerate(accounts, 1):
                    print(f"{i}. {account}")
            else:
                print("\nАккаунты не найдены.")

        elif choice == "2":
            account = input("\nВведите имя аккаунта: ").strip()
            if not account:
                print("Имя аккаунта не может быть пустым!")
                continue

            password = input("Введите пароль: ").strip()
            if not password:
                print("Пароль не может быть пустым!")
                continue

            pm = PasswordManager(account)
            pm.set_password(password)

        elif choice == "3":
            account = input("\nВведите имя аккаунта: ").strip()
            if not account:
                print("Имя аккаунта не может быть пустым!")
                continue

            pm = PasswordManager(account)
            password = pm.get_password()

            if password:
                print(f"\nПароль для аккаунта '{account}': {password}")
            else:
                print(f"\nПароль для аккаунта '{account}' не найден.")

        elif choice == "4":
            print("\nРабота программы завершена.")
            break

        else:
            print("\nНеверный выбор. Пожалуйста, введите число от 1 до 4.")

        input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    if not os.path.exists('passwords.xlsx'):
        pd.DataFrame(columns=['Account', 'Password']).to_excel('passwords.xlsx', index=False)

    main()