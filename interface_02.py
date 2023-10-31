import tkinter as tk
from tkinter import ttk
import sqlite3

def buscar_data():
    caminho_do_banco = 'C:\\Users\\Denner_Manoel_Bruno\\OneDrive\\Area_de_Trabalho\\FACULDADE\\Trabalho\\main.db'
    conn = sqlite3.connect(caminho_do_banco)
    c = conn.cursor()

    nome = entry_search.get()
    cidade = entry_cidade.get()
    estado = combo_estado.get()
    expectativa_salario = combo_expectativa_salario.get()

    query = """SELECT p.nome, p.idade, p.cidade, p.estado, p.ddd, p.telefone, p.email, e.expectativa_salario
               FROM perfis AS p
               JOIN empregabilidade AS e ON p.id = e.perfil_id
               WHERE p.nome LIKE ?"""

    params = [f"%{nome}%"]

    if cidade:
        query += " AND p.cidade LIKE ?"
        params.append(f"%{cidade}%")

    if estado != 'Selecione':
        query += " AND p.estado = ?"
        params.append(estado)

    if expectativa_salario != 'Selecione':
        query += " AND e.expectativa_salario = ?"
        params.append(expectativa_salario)

    c.execute(query, tuple(params))
    records = c.fetchall()

    for row in tree.get_children():
        tree.delete(row)

    for record in records:
        tree.insert("", "end", values=record)

    conn.close()

app = tk.Tk()
app.title("Recrutador - Consulta de Candidatos")

label_search = ttk.Label(app, text="Buscar por nome:")
label_search.pack(padx=10, pady=5)
entry_search = ttk.Entry(app, width=50)
entry_search.pack(padx=10, pady=5)

label_expectativa_salario = ttk.Label(app, text="Expectativa salarial:")
label_expectativa_salario.pack(padx=10, pady=5)
expectativas = ['Selecione', 'Até R$ 1.900', 'De R$ 1.900 a R$ 3.300', 'De R$ 3.300 a R$ 5.500', 'Acima de R$ 5.500']
combo_expectativa_salario = ttk.Combobox(app, values=expectativas, state="readonly")
combo_expectativa_salario.current(0)
combo_expectativa_salario.pack(padx=10, pady=5)

label_cidade = ttk.Label(app, text="Buscar por cidade:")
label_cidade.pack(padx=10, pady=5)
entry_cidade = ttk.Entry(app, width=50)
entry_cidade.pack(padx=10, pady=5)

label_estado = ttk.Label(app, text="Buscar por estado:")
label_estado.pack(padx=10, pady=5)
estados = ['Selecione', 'AC', 'AP',  'CE', 'DF', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'SP', 'SE', 'TO']
combo_estado = ttk.Combobox(app, values=estados, state="readonly")
combo_estado.current(0)
combo_estado.pack(padx=10, pady=5)

btn_search = ttk.Button(app, text="Buscar", command=buscar_data)
btn_search.pack(padx=10, pady=10)

columns = ("Nome", "Idade", "Cidade", "Estado", "DDD", "Telefone", "E-mail", "Expectativa Salarial")
tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, stretch=tk.NO)
tree.pack(padx=10, pady=20, fill="both", expand=True)

app.mainloop()