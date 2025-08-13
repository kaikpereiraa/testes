import sqlite3

BANCO='schema.sql'

conexao = sqlite3.connect('banco.db')

with open(BANCO) as f:
    conexao.executescript(f.read())

conexao.commit()
conexao.close()