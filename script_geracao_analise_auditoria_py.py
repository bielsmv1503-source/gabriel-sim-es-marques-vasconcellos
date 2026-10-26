import pandas as pd
import numpy as np
import sys

def gerar_e_analisar_base():
    print("=== INICIANDO EXECUÇÃO DE GERADORES E TESTES DE AUDITORIA ===")
    
    # 1. PARÂMETROS E PREMISSAS
    TOTAL_LINHAS = 500000
    VALOR_TOTAL_TARGET = 57908000000.00  # R$ 57,908 Bilhões (Notas Explicativas DFs 2025)
    MATERIALIDADE_EXECUCAO = 204750000.00 # R$ 204.75 Mi
    
    np.random.seed(2025)
    
    # 2. GERAÇÃO PROCEDURAL DA BASE DE DADOS (500.000 LINHAS)
    print(f"\n[1/3] Gerando base sintética de {TOTAL_LINHAS:,} registros...")
    
    empresas = ['Coelba', 'Pernambuco', 'Cosern', 'Elektro', 'Brasília', 'Transmissora Sul', 'Transmissora Norte']
    pesos_empresas = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
    
    tipos_ativo = [1, 2, 3] # 1: Ativo Fin. NC, 2: Ativo Contratual NC, 3: Ativo Contratual Circ.
    pesos_tipos = [0.5697, 0.4055, 0.0248]
    
    status_op = ['A', 'D', 'P'] # A: Aprovado, D: Divergência, P: Pendente de Unitização
    pesos_status = [0.975, 0.020, 0.005]
    
    ids = np.arange(1, TOTAL_LINHAS + 1)
    empresa_col = np.random.choice(empresas, TOTAL_LINHAS, p=pesos_empresas)
    tipo_col = np.random.choice(tipos_ativo, TOTAL_LINHAS, p=pesos_tipos)
    status_col = np.random.choice(status_op, TOTAL_LINHAS, p=pesos_status)
    taxa_col = np.round(np.random.uniform(0.08, 0.11, TOTAL_LINHAS), 4)
    
    # Geração de valores exponenciais ajustados ao teto financeiro
    val_raw = np.random.exponential(scale=100000, size=TOTAL_LINHAS) + 1000
    val_normalizado = (val_raw / val_raw.sum()) * VALOR_TOTAL_TARGET
    val_col = np.round(val_normalizado, 2)
    
    df = pd.DataFrame({
        'id_registro': ids,
        'empresa_segmento': empresa_col,
        'tipo_ativo': tipo_col,
        'valor_nominal': val_col,
        'taxa_desconto_implicita': taxa_col,
        'status_auditoria': status_col
    })
    
    print("✓ Base gerada com sucesso.")
    
    # 3. TESTES DE CONCILIAÇÃO CONTÁBIL E REVISÃO ANALÍTICA
    print("\n[2/3] Executando testes de conciliação e integridade...")
    soma_geral = df['valor_nominal'].sum()
    print(f"-> Saldo Contábil Target:  R$ {VALOR_TOTAL_TARGET:,.2f}")
    print(f"-> Saldo Conciliado Base: R$ {soma_geral:,.2f}")
    print(f"-> Diferença de Arredondamento: R$ {abs(VALOR_TOTAL_TARGET - soma_geral):,.2f}")
    
    # 4. EXECUÇÃO DE AMOSTRAGEM MONETÁRIA (NBC TA 530 - PPS)
    print("\n[3/3] Aplicando Amostragem de Unidade Monetária (PPS)...")
    intervalo_amostragem = MATERIALIDADE_EXECUCAO / 3.0
    df['probabilidade'] = df['valor_nominal'] / soma_geral
    
    tamanho_amostra = 1250
    amostra_indices = np.random.choice(
        df['id_registro'], 
        size=tamanho_amostra, 
        replace=False, 
        p=df['probabilidade']
    )
    
    df_amostra = df[df['id_registro'].isin(amostra_indices)]
    
    divergencias_encontradas = df_amostra[df_amostra['status_auditoria'] == 'D']
    pendentes_encontrados = df_amostra[df_amostra['status_auditoria'] == 'P']
    
    print(f"✓ Amostra de {len(df_amostra)} itens selecionada com sucesso.")
    print(f"-> Itens Aprovados sem ressalva: {len(df_amostra) - len(divergencias_encontradas) - len(pendentes_encontrados)}")
    print(f"-> Exceções de Divergência Calculada (D): {len(divergencias_encontradas)}")
    print(f"-> Obras Pendentes de Unitização (P): {len(pendentes_encontrados)}")
    print("\n=== EXECUÇÃO E TESTES DE AUDITORIA CONCLUÍDOS COM SUCESSO ===")

if __name__ == "__main__":
    gerar_e_analisar_base()