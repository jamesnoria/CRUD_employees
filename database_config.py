import sqlite3
import pandas as pd
import sys
import time
import re

from typing import (
    Any,
    List,
)

# Regular Expression
FORMAT_EMAIL = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'

# Errors:
EMAIL_WITHOUT_FORMAT = "Error email without format: El email {} no posee el formato correcto"


class Error():
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class EmployeeDataBase():

    def __init__(self):
        # Data base connection
        self.db = sqlite3.connect('employees.db')
        self.sql = self.db.cursor()

    def _check_email(self, email):
        return bool(re.match(FORMAT_EMAIL, email))

    def continue_choice(self, menu):
        """ A simple question to continue the crud or program """
        option = input('\n¿Desea continuar? (si/no): ')
        if option in ['si', 'SI']:
            print(menu)
        else:
            print('\n*** GRACIAS POR USAR ESTE PROGRAMA | Twitter: @jamesnoria ***\n')
            sys.exit()

    def create_employee(self):
        """ Create a new employee info """
        first_name = input('\nNombre: ')
        last_name = input('Apellido: ')
        position = input('Cargo: ')
        phone = input('Telefono: ')
        address = input('Dirección: ')
        email = input('Email: ')

        if not self._check_email(email):
            print(self._new_error(EMAIL_WITHOUT_FORMAT, [email]))
            return

        self.sql.execute(f"""
        INSERT INTO employees (first_name, last_name, position, phone, address, email)
        VALUES ('{first_name.title()}', '{last_name.title()}', '{position.title()}', '{phone}', '{address.title()}', '{email}');
        """)
        self.db.commit()

    def _new_error(self, message: str, contents: List[Any]):
        return Error(message.format(*contents))

    def see_employees(self):
        """ Fuction that allows to see all data base """
        df = pd.read_sql_query("""
        SELECT first_name AS NOMBRE,
        last_name AS APELLIDO,
        position AS CARGO,
        phone AS TELEFONO,
        address AS DIRECCION,
        email AS EMAIL
        FROM employees;""", self.db)

        df.index += 1
        print('\n', df)

    def update_employee(self):
        """ Alter an employee info """
        while True:
            print('\n¿Que usuario desearía modificar? (Introduzca Nombre y Apellido): ')
            user_name_mod = input('\nNombre: ')
            last_name_mod = input('Apellido: ')

            df = pd.read_sql_query(f"""
            SELECT first_name AS NOMBRE,
            last_name AS APELLIDO,
            position AS CARGO,
            phone AS TELEFONO,
            address AS DIRECCION,
            email AS EMAIL
            FROM employees
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """, self.db)

            if df.empty:
                print('\nResultados no encontrados. Introduzcalos nuevamente')
            else:
                print('\n', df)
                break

        print(
            '\n¿Que valor deseas modificar?\n[01] Nombre\n[02] Apellido\n[03] Cargo\n[04] Telefono\n[05] Dirección\n[06] Email')
        modifications_option = int(input('\n[1-6] '))
        if modifications_option == 1:
            new_name = input('\nInserte el nuevo nombre: ')
            self.sql.execute(f"""
            UPDATE employees
            SET first_name = '{new_name.title()}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        elif modifications_option == 2:
            new_lname = input('\nInserte el nuevo apellido: ')
            self.sql.execute(f"""
            UPDATE employees
            SET last_name = '{new_lname.title()}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        elif modifications_option == 3:
            new_position = input('\nInserte el nuevo cargo: ')
            self.sql.execute(f"""
            UPDATE employees
            SET position = '{new_position.title()}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        elif modifications_option == 4:
            new_phone = input('\nInserte el nuevo telefono: ')
            self.sql.execute(f"""
            UPDATE employees
            SET phone = '{new_phone}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        elif modifications_option == 5:
            new_address = input('\nInserte la nueva dirección: ')
            self.sql.execute(f"""
            UPDATE employees
            SET address = '{new_address.title()}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        elif modifications_option == 6:
            new_email = input('\nInserte el nuevo email: ')
            self.sql.execute(f"""
            UPDATE employees
            SET email = '{new_email}'
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """)
            self.db.commit()
        else:
            print('\nOpción NO VALIDA')

    def delete_employee(self):
        """ Delete a user or employee (by row) """
        while True:
            print('\n¿Que usuario desearía eliminar? (Introduzca Nombre y Apellido): ')
            user_name_mod = input('Nombre: ')
            last_name_mod = input('Apellido: ')

            df = pd.read_sql_query(f"""
            SELECT first_name AS NOMBRE,
            last_name AS APELLIDO,
            position AS CARGO,
            phone AS TELEFONO,
            address AS DIRECCION,
            email AS EMAIL
            FROM employees
            WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
            """, self.db)

            if df.empty:
                print('\nResultados no encontrados. Introduzcalos nuevamente')
            else:
                print(
                    f'\n¿Esta seguro de eliminar a {user_name_mod.title()} {last_name_mod.title()}?')
                delete_option = input('[si/no]: ')
                if delete_option in ['si', 'SI']:
                    self.sql.execute(f"""
                    DELETE FROM employees
                    WHERE first_name = '{user_name_mod.title()}' AND last_name = '{last_name_mod.title()}';
                    """)
                    self.db.commit()
                    break
                else:
                    break
