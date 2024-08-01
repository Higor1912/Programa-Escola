import flet as ft
import json

# Função para carregar os estudantes do arquivo JSON
def get_students():
    try:
        with open('students.json', 'r') as f:
            students = json.load(f)
        return students
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return []

# Função para salvar os estudantes no arquivo JSON
def save_students(students):
    with open('students.json', 'w') as f:
        json.dump(students, f, indent=4)

# Função para exibir a tabela de estudantes
def show_students(students):
    student_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('Nome')),
            ft.DataColumn(ft.Text('Idade')),
            ft.DataColumn(ft.Text('Turma')),
            ft.DataColumn(ft.Text('Nota'))
        ],
        rows=[ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(student['id']))),
                ft.DataCell(ft.Text(student['nome'])),
                ft.DataCell(ft.Text(str(student['idade']))),
                ft.DataCell(ft.Text(student['turma'])),
                ft.DataCell(ft.Text(str(student['nota'])))
            ]) for student in students]
    )

    return student_table

# Função para ordenar os estudantes
def sort_students(students, criteria, ascending=True):
    def convert_value(value):
        # Converte para inteiro se possível, caso contrário mantém como string
        try:
            return int(value)
        except ValueError:
            return value

    return sorted(students, key=lambda x: convert_value(x[criteria]), reverse=not ascending)

# Função principal para o formulário
def main(page: ft.Page):
    page.title = "Escola"
    page.window.width = 500
    page.window.height = 500

    students = get_students()

    def adicionar_aluno(e):
        new_student = {
            "id": entrada_id.value,
            "nome": entrada_nome.value,
            "idade": entrada_idade.value,
            "turma": entrada_turma.value,
            "nota": entrada_nota.value
        }
        students.append(new_student)
        save_students(students)
        entrada_id.value = ""
        entrada_nome.value = ""
        entrada_idade.value = ""
        entrada_turma.value = ""
        entrada_nota.value = ""
        page.update()

    def remover_aluno(e):
        id_to_remove = entrada_id.value
        for student in students:
            if student['id'] == id_to_remove:
                students.remove(student)
                break
        save_students(students)
        entrada_id.value = ""
        page.update()

    def abrir_lista(e):
        criteria = dropdown.value
        ascending = toggle_button.value
        sorted_students = sort_students(students, criteria, ascending)
        student_table = show_students(sorted_students)

        content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("Fechar", on_click=lambda e: close_dialog(e, dialog), icon=ft.icons.CLOSE),
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Row(
                    controls=[student_table],
                ),
            ]
        )

        dialog = ft.AlertDialog(
            title=ft.Text('Lista de Estudantes'),
            content=content,
            actions=[]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(e, dialog):
        dialog.open = False
        page.update()

    entrada_id = ft.TextField(label="ID")
    entrada_nome = ft.TextField(label="Nome")
    entrada_idade = ft.TextField(label="Idade")
    entrada_turma = ft.TextField(label="Turma")
    entrada_nota = ft.TextField(label="Nota")

    dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option("id", "ID"),
            ft.dropdown.Option("nome", "Nome"),
            ft.dropdown.Option("idade", "Idade"),
            ft.dropdown.Option("turma", "Turma"),
            ft.dropdown.Option("nota", "Nota")
        ],
        value="id"
    )

    toggle_button = ft.Switch(label="Ascendente", value=True)

    botao_add = ft.ElevatedButton(text="Adicionar", on_click=adicionar_aluno)
    botao_remover = ft.ElevatedButton(text="Remover", on_click=remover_aluno)
    botao_lista = ft.ElevatedButton(text="Lista de Estudantes", on_click=abrir_lista)

    page.add(
        entrada_id,
        entrada_nome,
        entrada_idade,
        entrada_turma,
        entrada_nota,
        dropdown,
        toggle_button,
        botao_add,
        botao_remover,
        botao_lista
    )

ft.app(target=main, view=ft.WEB_BROWSER)
