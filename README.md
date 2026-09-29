# TechInventory - Gestor de Inventário de TI

O **TechInventory** é uma aplicação desktop com interface gráfica moderna e minimalista criada em Python para o controle de equipamentos e periféricos de TI em laboratórios ou ambientes corporativos.

---

## Funcionalidades (CRUD + Pesquisa)

O sistema implementa o ciclo completo do **CRUD** e inclui consulta em tempo real:

- **[C]reate (Criar):** Cadastro de novos equipamentos (Código do Item, Nome e Estado).
- **[R]ead (Ler / Pesquisar):** Listagem em tabela organizada e campo de pesquisa instantânea por código, nome ou estado.
- **[U]pdate (Atualizar):** Edição rápida do nome e estado de conservação ao selecionar um item na tabela.
- **[D]elete (Remover):** Exclusão de equipamentos com confirmação de segurança.

---

## Três Campos de Entrada

Cada equipamento cadastrado possui exatamente 3 atributos:
1. **Código do Item:** Identificador exclusivo (ex: `COD-001`).
2. **Equipamento:** Descrição ou nome do item (ex: `Monitor Dell 24"`).
3. **Estado:** Situação de uso (`Disponível`, `Em Uso`, `Em Manutenção`).

---

## Persistência de Dados em Arquivo Binário

O sistema atende ao requisito do desafio utilizando o módulo nativo `pickle` da linguagem Python. 

Os dados do inventário são serializados e armazenados localmente em formato binário no ficheiro `inventario.dat`. Toda operação realizada atualiza o ficheiro automaticamente, garantindo a permanência dos dados ao fechar e abrir a aplicação.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica (GUI):** `tkinter` e `tkinter.ttk` (bibliotecas nativas)
- **Persistência de Dados:** `pickle` (serialização em arquivo binário) e `os`

---

## Como Executar

### Pré-requisito
Ter o **Python 3** instalado na máquina.

### Passo a Passo

1. Clone o repositório:

```bash
git clone https://github.com/DeiseEllen/tech-inventory.git
```

