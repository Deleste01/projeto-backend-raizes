import os
import sqlite3

db_path = 'instance/raizes.db'
print(f"--- Verificando banco de dados em: {db_path} ---")

if not os.path.exists(db_path):
    print("[AVISO] O arquivo do banco de dados NÃO existe na pasta 'instance/'. O banco precisa ser inicializado!")
else:
    print("[OK] Arquivo do banco encontrado.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    if not tables:
        print("[AVISO] O banco existe, mas está vazio (sem tabelas criadas).")
    else:
        print(f"Tabelas encontradas: {tables}\n")
        for t in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {t}")
                count = cursor.fetchone()[0]
                print(f"  -> Tabela '{t}': {count} registros")
                
                # mostrar conteúdo se houver poucos registros
                if count > 0 and count <= 10:
                    cursor.execute(f"SELECT * FROM {t}")
                    rows = cursor.fetchall()
                    for r in rows:
                        print(f"     Registro: {r}")
            except Exception as e:
                print(f"  -> Tabela '{t}': Erro ao ler ({e})")
    conn.close()
