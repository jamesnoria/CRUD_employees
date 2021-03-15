from database_config import EmployeeDataBase


crud_ui = """
**********************************************
                    C R U D
**********************************************
[01] Crear un nuevo usuario
[02] Ver usuarios
[03] Modificar usuarios
[04] Borrar usuario
[05] Salir
**********************************************
"""

print(crud_ui)
while True:
    crud = EmployeeDataBase()
    try:
        choice = int(input('[1-5] '))
        if choice == 1:
            crud.create_employee()
            crud.continue_choice(crud_ui)
        elif choice == 2:
            crud.see_employees()
            crud.continue_choice(crud_ui)
        elif choice == 3:
            crud.see_employees()
            crud.update_employee()
            crud.continue_choice(crud_ui)
        elif choice == 4:
            crud.see_employees()
            crud.delete_employee()
            crud.continue_choice(crud_ui)
        elif choice == 5:
            print('\n*** GRACIAS POR USAR ESTE PROGRAMA | Twitter: @jamesnoria ***\n')
            break
    except ValueError:
        print('\nSolo números entre 1 y 5\n')
