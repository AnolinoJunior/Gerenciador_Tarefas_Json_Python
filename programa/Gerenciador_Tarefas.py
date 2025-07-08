import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

TASKS_FILE = "tasks.json"

# --------------------------
# FUNÇÕES DE ARQUIVO JSON
# --------------------------

def load_tasks():
    try:
        if not os.path.exists(TASKS_FILE) or os.path.getsize(TASKS_FILE) == 0:
            with open(TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []

        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)

        if not isinstance(tasks, list):
            print("⚠️ Estrutura inválida no arquivo. Recriando...")
            with open(TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []

        return tasks

    except Exception as e:
        print(f"⚠️ Erro ao carregar tarefas: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Erro ao salvar tarefas: {e}")

def add_task(description, date_str, time_str):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "description": description,
        "date": date_str,
        "time": time_str,
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)

# --------------------------
# FUNÇÕES DE INTERFACE
# --------------------------

def atualizar_lista():
    lista_tarefas.delete(0, tk.END)
    tasks = load_tasks()
    for task in tasks:
        status = "✅" if task["done"] else "🕒"
        texto = f'{task["id"]}. [{status}] {task["description"]} - {task["date"]} às {task["time"]}'
        lista_tarefas.insert(tk.END, texto)

def adicionar_tarefa():
    desc = entry_descricao.get()
    data = entry_data.get()
    hora = entry_hora.get()

    if not desc or not data or not hora:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    try:
        datetime.strptime(data, "%Y-%m-%d")
        datetime.strptime(hora, "%H:%M")
    except ValueError:
        messagebox.showerror("Formato inválido", "Data ou hora inválida.")
        return

    add_task(desc, data, hora)
    entry_descricao.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_hora.delete(0, tk.END)
    atualizar_lista()

def marcar_como_concluida():
    selecionado = lista_tarefas.curselection()
    if not selecionado:
        messagebox.showinfo("Selecionar", "Selecione uma tarefa para marcar como concluída.")
        return

    index = selecionado[0]
    tasks = load_tasks()
    task = tasks[index]
    task["done"] = True
    save_tasks(tasks)
    atualizar_lista()

def remover_tarefa():
    selecionado = lista_tarefas.curselection()
    if not selecionado:
        messagebox.showinfo("Selecionar", "Selecione uma tarefa para remover.")
        return

    index = selecionado[0]
    tasks = load_tasks()
    tarefa = tasks[index]

    confirmar = messagebox.askyesno("Remover", f"Tem certeza que deseja remover:\n\n{tarefa['description']}?")
    if confirmar:
        del tasks[index]
        save_tasks(tasks)
        atualizar_lista()

# --------------------------
# INTERFACE GRÁFICA
# --------------------------

janela = tk.Tk()
janela.title("📚 Planejador de Estudos")
janela.geometry("650x450")

# --- Campos de entrada ---
frame_inputs = tk.Frame(janela)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Tarefa:").grid(row=0, column=0, padx=5)
entry_descricao = tk.Entry(frame_inputs, width=30)
entry_descricao.grid(row=0, column=1)

tk.Label(frame_inputs, text="Data (AAAA-MM-DD):").grid(row=1, column=0, padx=5)
entry_data = tk.Entry(frame_inputs)
entry_data.grid(row=1, column=1)

tk.Label(frame_inputs, text="Hora (HH:MM):").grid(row=2, column=0, padx=5)
entry_hora = tk.Entry(frame_inputs)
entry_hora.grid(row=2, column=1)

# --- Botão adicionar ---
btn_adicionar = tk.Button(janela, text="➕ Adicionar Tarefa", command=adicionar_tarefa)
btn_adicionar.pack(pady=10)

# --- Botões de ação ---
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

btn_concluir = tk.Button(frame_botoes, text="✅ Marcar como Concluída", command=marcar_como_concluida)
btn_concluir.grid(row=0, column=0, padx=10)

btn_remover = tk.Button(frame_botoes, text="🗑️ Remover Tarefa", command=remover_tarefa)
btn_remover.grid(row=0, column=1, padx=10)

# --- Lista de tarefas ---
lista_tarefas = tk.Listbox(janela, width=80)
lista_tarefas.pack(pady=10)

# --- Iniciar com a lista atual ---
atualizar_lista()

# --- Rodar a janela ---
janela.mainloop()
 