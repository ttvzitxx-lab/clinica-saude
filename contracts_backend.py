"""Backend para gerenciamento de contratos."""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import Workbook

CONTRACTS_FILE = "contratos.xlsx"
CONTRACTS_DIR = "contratos_uploads"

COLUNAS = [
    "ID", "Nome", "Tipo", "Parte_A", "Parte_B", "Descricao",
    "Arquivo", "Hash_Arquivo", "Tamanho_KB", "Status",
    "Adicionado_em", "Lido_em", "Lido_por", "Prioridade", "Tags", "Observacoes"
]

STATUS_OPTIONS = ["Pendente", "Em Revisão", "Lido", "Arquivado"]
TIPO_OPTIONS = ["Prestação de Serviços", "Sigilo (NDA)", "Parceria", "Locação", "Trabalhista", "Fornecimento", "Outro"]
PRIORIDADE_OPTIONS = ["Alta", "Média", "Baixa"]


def _init_storage():
    Path(CONTRACTS_DIR).mkdir(exist_ok=True)
    if not os.path.exists(CONTRACTS_FILE):
        df = pd.DataFrame(columns=COLUNAS)
        df.to_excel(CONTRACTS_FILE, index=False)


def _carregar() -> pd.DataFrame:
    _init_storage()
    df = pd.read_excel(CONTRACTS_FILE)
    for col in COLUNAS:
        if col not in df.columns:
            df[col] = ""
    return df


def _salvar(df: pd.DataFrame):
    df.to_excel(CONTRACTS_FILE, index=False)


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


# ── CRUD ────────────────────────────────────────────────────────────────────

def adicionar_contrato(nome: str, tipo: str, parte_a: str, parte_b: str,
                       descricao: str, prioridade: str, tags: str,
                       arquivo_bytes: bytes | None, arquivo_nome: str | None) -> int:
    df = _carregar()
    novo_id = int(df["ID"].max()) + 1 if not df.empty and not pd.isna(df["ID"].max()) else 1

    arquivo_salvo = ""
    hash_arq = ""
    tamanho_kb = 0

    if arquivo_bytes and arquivo_nome:
        ext = Path(arquivo_nome).suffix
        nome_salvo = f"contrato_{novo_id:04d}{ext}"
        caminho = os.path.join(CONTRACTS_DIR, nome_salvo)
        with open(caminho, "wb") as f:
            f.write(arquivo_bytes)
        arquivo_salvo = nome_salvo
        hash_arq = _hash_bytes(arquivo_bytes)
        tamanho_kb = round(len(arquivo_bytes) / 1024, 1)

    novo = {
        "ID": novo_id,
        "Nome": nome,
        "Tipo": tipo,
        "Parte_A": parte_a,
        "Parte_B": parte_b,
        "Descricao": descricao,
        "Arquivo": arquivo_salvo,
        "Hash_Arquivo": hash_arq,
        "Tamanho_KB": tamanho_kb,
        "Status": "Pendente",
        "Adicionado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Lido_em": "",
        "Lido_por": "",
        "Prioridade": prioridade,
        "Tags": tags,
        "Observacoes": "",
    }
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    _salvar(df)
    return novo_id


def marcar_como_lido(contrato_id: int, lido_por: str):
    df = _carregar()
    mask = df["ID"] == contrato_id
    if mask.any():
        df.loc[mask, "Status"] = "Lido"
        df.loc[mask, "Lido_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        df.loc[mask, "Lido_por"] = lido_por
        _salvar(df)
        return True
    return False


def atualizar_status(contrato_id: int, novo_status: str):
    df = _carregar()
    mask = df["ID"] == contrato_id
    if mask.any():
        df.loc[mask, "Status"] = novo_status
        if novo_status != "Lido":
            df.loc[mask, "Lido_em"] = ""
            df.loc[mask, "Lido_por"] = ""
        _salvar(df)
        return True
    return False


def atualizar_observacoes(contrato_id: int, obs: str):
    df = _carregar()
    mask = df["ID"] == contrato_id
    if mask.any():
        df.loc[mask, "Observacoes"] = obs
        _salvar(df)
        return True
    return False


def excluir_contrato(contrato_id: int):
    df = _carregar()
    row = df[df["ID"] == contrato_id]
    if not row.empty:
        arq = str(row.iloc[0]["Arquivo"])
        if arq:
            caminho = os.path.join(CONTRACTS_DIR, arq)
            if os.path.exists(caminho):
                os.remove(caminho)
        df = df[df["ID"] != contrato_id]
        _salvar(df)
        return True
    return False


def obter_arquivo(contrato_id: int) -> tuple[bytes | None, str]:
    df = _carregar()
    row = df[df["ID"] == contrato_id]
    if row.empty:
        return None, ""
    arq = str(row.iloc[0]["Arquivo"])
    if not arq:
        return None, ""
    caminho = os.path.join(CONTRACTS_DIR, arq)
    if not os.path.exists(caminho):
        return None, ""
    with open(caminho, "rb") as f:
        return f.read(), arq


# ── CONSULTAS ───────────────────────────────────────────────────────────────

def listar_todos() -> pd.DataFrame:
    return _carregar()


def listar_por_status(status: str) -> pd.DataFrame:
    df = _carregar()
    return df[df["Status"] == status].copy()


def stats() -> dict:
    df = _carregar()
    total = len(df)
    por_status = df["Status"].value_counts().to_dict() if total > 0 else {}
    por_tipo = df["Tipo"].value_counts().to_dict() if total > 0 else {}
    por_prioridade = df["Prioridade"].value_counts().to_dict() if total > 0 else {}

    pendentes_alta = len(df[(df["Status"] == "Pendente") & (df["Prioridade"] == "Alta")]) if total > 0 else 0

    return {
        "total": total,
        "pendentes": por_status.get("Pendente", 0),
        "em_revisao": por_status.get("Em Revisão", 0),
        "lidos": por_status.get("Lido", 0),
        "arquivados": por_status.get("Arquivado", 0),
        "por_tipo": por_tipo,
        "por_prioridade": por_prioridade,
        "pendentes_alta_prioridade": pendentes_alta,
    }
