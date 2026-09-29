import os
import pickle
import tkinter as tk
from tkinter import ttk, messagebox

NOME_ARQUIVO = "inventario.dat"


#CLASSE DE DADOS (3 CAMPOS)

class Equipamento:
    def __init__(self, codigo: str, nome: str, estado: str):
        self.codigo = codigo  
        self.nome = nome      
        self.estado = estado  



#PERSISTÊNCIA EM ARQUIVO BINÁRIO (PICKLE)

def carregar_dados() -> list[Equipamento]:
    if not os.path.exists(NOME_ARQUIVO):
        return []
    try:
        with open(NOME_ARQUIVO, "rb") as f:
            return pickle.load(f)
    except Exception:
        return []


def salvar_dados(equipamentos: list[Equipamento]):
    with open(NOME_ARQUIVO, "wb") as f:
        pickle.dump(equipamentos, f)



#INTERFACE GRÁFICA CLEAN (TKINTER)

class TechInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechInventory")
        self.root.geometry("740x580")
        self.root.configure(bg="#f8f9fa")

        self.equipamentos = carregar_dados()
        self.item_selecionado_index = None

        self.configurar_estilos()
        self.criar_interface()
        self.atualizar_tabela()

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(".", background="#f8f9fa", font=("Segoe UI", 10))
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10), background="#ffffff", fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e9ecef", foreground="#212529")
        self.style.map("Treeview", background=[("selected", "#0d6efd")], foreground=[("selected", "#ffffff")])

    def criar_interface(self):
        #Título
        header = tk.Frame(self.root, bg="#f8f9fa")
        header.pack(fill="x", padx=20, pady=(15, 5), side="top")
        
        lbl_titulo = tk.Label(header, text="Gestão de Inventário de TI", font=("Segoe UI", 14, "bold"), bg="#f8f9fa", fg="#212529")
        lbl_titulo.pack(side="left")

        #Formulário (3 Campos em linha)
        form_frame = tk.LabelFrame(self.root, text=" Cadastro / Edição ", font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#495057", padx=15, pady=15)
        form_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(form_frame, text="Código do Item:", bg="#f8f9fa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_codigo = tk.Entry(form_frame, width=15, font=("Segoe UI", 10))
        self.txt_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Equipamento:", bg="#f8f9fa").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_nome = tk.Entry(form_frame, width=25, font=("Segoe UI", 10))
        self.txt_nome.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Estado:", bg="#f8f9fa").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.cb_estado = ttk.Combobox(form_frame, values=["Disponível", "Em Uso", "Em Manutenção"], width=15, state="readonly")
        self.cb_estado.current(0)
        self.cb_estado.grid(row=0, column=5, padx=5, pady=5)

        #Botões
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(fill="x", padx=20, pady=5)

        self.btn_salvar = tk.Button(btn_frame, text="Salvar Item", command=self.salvar_item, bg="#0d6efd", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, pady=5)
        self.btn_salvar.pack(side="left", padx=(0, 5))

        btn_limpar = tk.Button(btn_frame, text="Limpar Campos", command=self.limpar_formulario, bg="#6c757d", fg="white", font=("Segoe UI", 9), relief="flat", padx=10, pady=5)
        btn_limpar.pack(side="left", padx=5)

        btn_deletar = tk.Button(btn_frame, text="Excluir Selecionado", command=self.deletar_item, bg="#dc3545", fg="white", font=("Segoe UI", 9), relief="flat", padx=10, pady=5)
        btn_deletar.pack(side="right")

        #Barra de Pesquisa 
        search_frame = tk.Frame(self.root, bg="#f8f9fa")
        search_frame.pack(fill="x", padx=20, pady=(10, 0))

        tk.Label(search_frame, text="🔍 Pesquisar:", font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#495057").pack(side="left", padx=(0, 5))
        self.txt_pesquisa = tk.Entry(search_frame, font=("Segoe UI", 10))
        self.txt_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.txt_pesquisa.bind("<KeyRelease>", self.filtrar_tabela)  # Pesquisa em tempo real ao digitar

        btn_limpar_pesquisa = tk.Button(search_frame, text="X", command=self.limpar_pesquisa, bg="#e9ecef", fg="#495057", font=("Segoe UI", 8, "bold"), relief="flat", padx=8)
        btn_limpar_pesquisa.pack(side="left")

        #Tabela 
        table_frame = tk.Frame(self.root, bg="#f8f9fa")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        colunas = ("codigo", "nome", "estado")
        self.tabela = ttk.Treeview(table_frame, columns=colunas, show="headings", selectmode="browse")
        
        self.tabela.heading("codigo", text="CÓDIGO DO ITEM")
        self.tabela.heading("nome", text="NOME DO EQUIPAMENTO")
        self.tabela.heading("estado", text="ESTADO")

        self.tabela.column("codigo", width=140, anchor="center")
        self.tabela.column("nome", width=360, anchor="w")
        self.tabela.column("estado", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabela.bind("<<TreeviewSelect>>", self.carregar_item_selecionado)

    
    #REGRAS DE NEGÓCIO E CRUD
    
    def atualizar_tabela(self, lista_para_exibir=None):
        for row in self.tabela.get_children():
            self.tabela.delete(row)
        
        itens = lista_para_exibir if lista_para_exibir is not None else self.equipamentos
        for eq in itens:
            self.tabela.insert("", "end", values=(eq.codigo, eq.nome, eq.estado))

    def filtrar_tabela(self, event=None):
        termo = self.txt_pesquisa.get().strip().lower()
        if not termo:
            self.atualizar_tabela()
            return

        filtrados = [
            eq for eq in self.equipamentos
            if termo in eq.codigo.lower() or termo in eq.nome.lower() or termo in eq.estado.lower()
        ]
        self.atualizar_tabela(filtrados)

    def limpar_pesquisa(self):
        self.txt_pesquisa.delete(0, tk.END)
        self.atualizar_tabela()

    def limpar_formulario(self):
        self.txt_codigo.delete(0, tk.END)
        self.txt_nome.delete(0, tk.END)
        self.cb_estado.current(0)
        self.txt_codigo.config(state="normal")
        self.item_selecionado_index = None

    def carregar_item_selecionado(self, event):
        selecao = self.tabela.selection()
        if not selecao:
            return
        
        valores = self.tabela.item(selecao[0], "values")
        codigo_item = valores[0]

        #Localiza o índice real na lista principal de equipamentos
        for idx, eq in enumerate(self.equipamentos):
            if eq.codigo == codigo_item:
                self.item_selecionado_index = idx
                break

        eq = self.equipamentos[self.item_selecionado_index]

        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, eq.codigo)
        self.txt_codigo.config(state="disabled")

        self.txt_nome.delete(0, tk.END)
        self.txt_nome.insert(0, eq.nome)
        
        self.cb_estado.set(eq.estado)

    def salvar_item(self):
        codigo = self.txt_codigo.get().strip().upper()
        nome = self.txt_nome.get().strip()
        estado = self.cb_estado.get()

        if not codigo or not nome:
            messagebox.showwarning("Atenção", "Preencha o Código do Item e o Nome do equipamento.")
            return

        #Modo UPDATE
        if self.item_selecionado_index is not None:
            self.equipamentos[self.item_selecionado_index].nome = nome
            self.equipamentos[self.item_selecionado_index].estado = estado
            messagebox.showinfo("Sucesso", "Equipamento atualizado!")
        
        #Modo CREATE
        else:
            for eq in self.equipamentos:
                if eq.codigo == codigo:
                    messagebox.showerror("Erro", f"Já existe um item cadastrado com o código '{codigo}'.")
                    return

            novo_eq = Equipamento(codigo, nome, estado)
            self.equipamentos.append(novo_eq)
            messagebox.showinfo("Sucesso", "Equipamento cadastrado!")

        salvar_dados(self.equipamentos)
        self.limpar_pesquisa()
        self.limpar_formulario()

    def deletar_item(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione um equipamento na tabela para excluir.")
            return

        valores = self.tabela.item(selecao[0], "values")
        codigo_item = valores[0]

        #Busca o item correto na lista
        for idx, eq in enumerate(self.equipamentos):
            if eq.codigo == codigo_item:
                if messagebox.askyesno("Confirmar Exclusão", f"Deseja remover '{eq.nome}' ({eq.codigo})?"):
                    self.equipamentos.pop(idx)
                    salvar_dados(self.equipamentos)
                    self.limpar_pesquisa()
                    self.limpar_formulario()
                    messagebox.showinfo("Sucesso", "Equipamento removido!")
                return


if __name__ == "__main__":
    root = tk.Tk()
    app = TechInventoryApp(root)
    root.mainloop()