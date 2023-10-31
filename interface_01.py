import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox


   
def limpar():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    combo_estado.set('Selecione')
    entry_ddd.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_expectativa_salario.delete(0, tk.END)
    for exp in experiencias[:]:
        if exp['empresa'].winfo_exists():
            exp['empresa'].delete(0, tk.END)
        else:
            experiencias.remove(exp)
    for exp in experiencias:
        exp['frame'].destroy()
    experiencias.clear()
    

experiencias = []

for exp in experiencias:
        exp['empresa'].delete(0, tk.END)
        exp['cargo'].delete(0, tk.END)
        exp['periodo'].delete(0, tk.END)
        exp['soft_skills'].delete(0, tk.END)
        exp['hard_skills'].delete(0, tk.END)
        exp['linkedin'].delete(0, tk.END)
    

def submit():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cidade = entry_cidade.get()
    estado = combo_estado.get()
    dd = entry_ddd.get()
    telefone = entry_telefone.get()
    email = entry_email.get()

    if not nome or not idade or not cidade or estado == 'Selecione' or not dd or not telefone or not email:
        messagebox.showerror('Erro', 'Todos os campos são obrigatórios!')
        return

    if not dd.isdigit() or not telefone.isdigit():
        messagebox.showerror('Erro', 'Erro: DDD e telefone devem conter apenas números!')
        return

    if len(dd) != 2 or len(telefone) != 9:
        messagebox.showerror('Erro', 'Erro: DDD deve ter 2 dígitos e telefone deve ter 9 dígitos!')
        return

    caminho_do_banco = 'C:\\Users\\Denner_Manoel_Bruno\\OneDrive\\Area_de_Trabalho\\FACULDADE\\Trabalho\\main.db'
    conn = sqlite3.connect(caminho_do_banco)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS perfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            cidade TEXT,
            estado TEXT,
            dd INTEGER,
            telefone INTEGER,
            email TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS empregabilidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_emprego TEXT,
            expectativa_salario TEXT,
            outras_info TEXT,
            perfil_id INTEGER,
            FOREIGN KEY (perfil_id) REFERENCES perfis (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS experiencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT,
            cargo TEXT,
            periodo TEXT,
            soft_skills TEXT,
            hard_skills TEXT,
            linkedin TEXT,
            perfil_id INTEGER,
            FOREIGN KEY (perfil_id) REFERENCES perfis (id)
        )
    ''')


    c.execute('PRAGMA table_info(empregabilidade)')
    columns = c.fetchall()
    column_names = [column[1] for column in columns]

    if 'status_emprego' not in column_names:
        c.execute('ALTER TABLE empregabilidade ADD COLUMN status_emprego TEXT')
    if 'expectativa_salario' not in column_names:
        c.execute('ALTER TABLE empregabilidade ADD COLUMN expectativa_salario TEXT')
    if 'outras_info' not in column_names:
        c.execute('ALTER TABLE empregabilidade ADD COLUMN outras_info TEXT')

    c.execute('''
        INSERT INTO perfis (nome, idade, cidade, estado, dd, telefone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, idade, cidade, estado, dd, telefone, email))

    perfil_id = c.lastrowid

    for exp in experiencias:
        c.execute('''
            INSERT INTO experiencias (empresa, cargo, periodo, soft_skills, hard_skills, linkedin, perfil_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            exp['empresa'].get(),
            exp['cargo'].get(),
            exp['periodo'].get(),
            exp['soft_skills'].get(),
            exp['hard_skills'].get(),
            exp['linkedin'].get(),
            perfil_id
        ))

    c.execute('''
        INSERT INTO empregabilidade (status_emprego, expectativa_salario, outras_info, perfil_id)
        VALUES (?, ?, ?, ?)
    ''', (status_emprego_var.get(), entry_expectativa_salario.get(), entry_outras_info.get(), perfil_id))

    result_label.config(text='Perfil enviado com sucesso!')
    
    limpar()

    conn.commit()
    conn.close()


root = tk.Tk()
root.title('Startup')

frame = ttk.Frame(root, padding='12')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text='Nome completo:').grid(row=0, column=0, sticky=tk.W)
entry_nome = ttk.Entry(frame, width=35)
entry_nome.grid(row=0, column=1, sticky=tk.W)

ttk.Label(frame, text='Idade:').grid(row=1, column=0, sticky=tk.W)
entry_idade = ttk.Entry(frame, width=7, validate='key', validatecommand=(root.register(lambda s: s.isdigit()), '%S'))
entry_idade.grid(row=1, column=1, sticky=tk.W)

ttk.Label(frame, text='DDD + Telefone:').grid(row=4, column=0, sticky=tk.W)
entry_ddd = ttk.Entry(frame, width=5)
entry_ddd.grid(row=4, column=1, sticky=tk.W)
entry_telefone = ttk.Entry(frame, width=10)
entry_telefone.grid(row=4, column=3, sticky=tk.W)

ttk.Label(frame, text='Cidade:').grid(row=2, column=0, sticky=tk.W)
entry_cidade = ttk.Entry(frame, width=35)
entry_cidade.grid(row=2, column=1, sticky=tk.W)

ttk.Label(frame, text='Estado:').grid(row=3, column=0, sticky=tk.W)
estados = ['Selecione', 'AC', 'AP',  'CE', 'DF', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'SP', 'SE', 'TO']
combo_estado = ttk.Combobox(frame, values=estados, state='readonly')
combo_estado.grid(row=3, column=1, sticky=tk.W)
combo_estado.set('Selecione') 

ttk.Label(frame, text='E-mail:').grid(row=6, column=0, sticky=tk.W)
entry_email = ttk.Entry(frame, width=35)
entry_email.grid(row=6, column=1, sticky=tk.W)

def adicionar_exp():
    frame_experiencia = ttk.Frame(frame, padding='7')
    frame_experiencia.grid(row=13 + len(experiencias), column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))

    ttk.Label(frame_experiencia, text='Empresa:').grid(row=0, column=0, sticky=tk.W)
    entry_empresa = ttk.Entry(frame_experiencia, width=25)
    entry_empresa.grid(row=0, column=1, sticky=tk.W)

    ttk.Label(frame_experiencia, text='Cargo:').grid(row=1, column=0, sticky=tk.W)
    entry_cargo = ttk.Entry(frame_experiencia, width=25)
    entry_cargo.grid(row=1, column=1, sticky=tk.W)

    ttk.Label(frame_experiencia, text='Período:').grid(row=2, column=0, sticky=tk.W)
    entry_periodo = ttk.Entry(frame_experiencia, width=25)
    entry_periodo.grid(row=2, column=1, sticky=tk.W)

    ttk.Label(frame_experiencia, text='Principais Soft Skills:').grid(row=3, column=0, sticky=tk.W)
    entry_soft_skills = ttk.Entry(frame_experiencia, width=25)
    entry_soft_skills.grid(row=3, column=1, sticky=tk.W)

    ttk.Label(frame_experiencia, text='Principais Hard Skills:').grid(row=4, column=0, sticky=tk.W)
    entry_hard_skills = ttk.Entry(frame_experiencia, width=25)
    entry_hard_skills.grid(row=4, column=1, sticky=tk.W)

    ttk.Label(frame_experiencia, text='LinkedIn:').grid(row=5, column=0, sticky=tk.W)
    entry_linkedin = ttk.Entry(frame_experiencia, width=25)
    entry_linkedin.grid(row=5, column=1, sticky=tk.W)

    experiencias.append({
        'frame': frame_experiencia,  
        'empresa': entry_empresa,
        'cargo': entry_cargo,
        'periodo': entry_periodo,
        'soft_skills': entry_soft_skills,
        'hard_skills': entry_hard_skills,
        'linkedin': entry_linkedin
    })


ttk.Label(frame, text='Status atual de emprego:').grid(row=8, column=0, sticky=tk.W)
status_emprego_var = tk.StringVar()
desempregado_button = ttk.Radiobutton(frame, text='Desempregado', variable=status_emprego_var, value='Desempregado')
desempregado_button.grid(row=8, column=1, sticky=tk.W)
empregado_button = ttk.Radiobutton(frame, text='Empregado', variable=status_emprego_var, value='Empregado')
empregado_button.grid(row=8, column=2, sticky=tk.W)

label_expectativa_salario = ttk.Label(frame, text='Expectativa Salarial:')
label_expectativa_salario.grid(row=9, column=0, sticky=tk.W)
entry_expectativa_salario = ttk.Entry(frame, width=25)
entry_expectativa_salario.grid(row=9, column=1, sticky=tk.W)

label_outras_info = ttk.Label(frame, text='Outras informações:')
label_outras_info.grid(row=10, column=0, sticky=tk.W)
entry_outras_info = ttk.Entry(frame, width=25)
entry_outras_info.grid(row=10, column=1, sticky=tk.W)

ttk.Separator(frame, orient='horizontal').grid(row=11, column=0, columnspan=4, pady=10, sticky="ew")

add_experiencia_button = ttk.Button(frame, text='Adicionar Experiência', command=adicionar_exp)
add_experiencia_button.grid(row=12, column=0, columnspan=2, pady=10)

submit_button = ttk.Button(frame, text='Enviar', command=submit)
submit_button.grid(row=12, column=2, columnspan=2, pady=10)

result_label = ttk.Label(frame, text='')
result_label.grid(row=11, column=0, columnspan=4)

root.mainloop()