# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║              JEFFÃO BOT — HIGHRISE  •  VERSÃO LIMPA (sem rádio)            ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  Python 3.10+  │  SDK: highrise-bot-sdk  │  Dep: aiohttp                  ║
# ║  Editores: VS Code · PyCharm · Thonny · IDLE · qualquer editor de texto   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  INSTALAÇÃO RÁPIDA                                                          │
# └─────────────────────────────────────────────────────────────────────────────┘
#
#   1. Instale Python 3.11  →  https://www.python.org/downloads/
#      (Windows: marque "Add Python to PATH" no instalador)
#
#   2. No terminal/CMD, instale as dependências:
#        pip install highrise-bot-sdk aiohttp
#
#   3. (Opcional) IA mais rápida via Groq — sem chave usa Pollinations grátis:
#        Windows CMD :  set GROQ_API_KEY=sua_chave
#        Windows PS  :  $env:GROQ_API_KEY="sua_chave"
#        Linux/macOS :  export GROQ_API_KEY=sua_chave
#
#   4. Preencha room_id e bot_token no final deste arquivo (classe RunBot).
#
#   5. Execute:
#        python main.py    ou    py main.py    (Windows)
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  ARQUIVOS DO PROJETO                                                        │
# └─────────────────────────────────────────────────────────────────────────────┘
#
#   main.py            ← este arquivo (lógica principal do bot)
#   emotes.py          ← lista de emotes com IDs e durações (OBRIGATÓRIO)
#   aliases.json       ← apelidos de usuários (criado automaticamente)
#   emote_aliases.json ← atalhos de emotes criados pelos ADMs (auto)
#   platforms.json     ← posições salvas na sala (auto)
#   placar.json        ← ranking do jokenpô (auto)
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  O QUE MUDAR E ONDE                                                        │
# └─────────────────────────────────────────────────────────────────────────────┘
#
#  ── POSIÇÃO INICIAL DO BOT (spawn) ──────────────────────────────────────────
#   Procure: SPAWN_POSITION
#   Troque os valores de x / y / z pela posição que quiser na sala.
#   "facing" define a direção: "FrontLeft", "FrontRight", "BackLeft", "BackRight"
#
#  ── DONO DO BOT (acesso total) ───────────────────────────────────────────────
#   Procure: BOT_OWNER_USERNAME
#   Troque "Fenix_inthe_HR" pelo seu username exato do Highrise.
#
#  ── ADMs EXTRAS (além dos designers/moderadores da sala) ────────────────────
#   Procure: EXTRA_ADMINS
#   Adicione usernames separados por vírgula:
#     EXTRA_ADMINS = {"Amigo1", "Amigo2"}
#
#  ── VIP1 (local exclusivo de ADMs) ──────────────────────────────────────────
#   Procure: VIP_LOCATIONS, chave "vip1"
#   Troque os valores de x / y / z pela posição do VIP1 na sua sala.
#
#  ── PERSONALIDADE DA IA ──────────────────────────────────────────────────────
#   Procure: SYSTEM_PROMPT
#   Edite o texto entre as aspas triplas para mudar como o Jeffão fala,
#   seu humor, conhecimentos ou estilo de resposta.
#
#  ── EMOTES DE EMOÇÃO (gestos automáticos do bot) ────────────────────────────
#   Procure: EMOTION_EMOTES
#   Cada chave é um "humor" e o valor é o ID do emote que o bot faz.
#   Troque os IDs para mudar os gestos. IDs disponíveis estão em emotes.py.
#
#  ── DENOMINAÇÕES DE GOLD (reembolso) ─────────────────────────────────────────
#   Procure: GOLD_DENOMINATIONS
#   Lista com os valores de tips disponíveis no Highrise (ordem decrescente).
#   Só altere se o Highrise adicionar ou remover alguma denominação.
#
#  ── TOKEN E SALA ─────────────────────────────────────────────────────────────
#   Procure: class RunBot  (final do arquivo)
#   room_id   → ID da sala (URL do Highrise, parte depois de /room/)
#   bot_token → Token gerado no painel de bots do Highrise
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  GUIA DE FUNÇÕES — o que cada método faz                                   │
# └─────────────────────────────────────────────────────────────────────────────┘
#
#  EVENTOS (chamados automaticamente pelo SDK):
#   on_start()           → executado quando o bot entra na sala; restaura outfit,
#                          vai ao spawn, inicia loops de estado
#   on_user_join()       → usuário entra → saudação + emote de boas-vindas
#   on_user_leave()      → usuário sai → cancela loops daquele usuário
#   on_chat()            → mensagem pública → encaminha para _handle_chat()
#   on_whisper()         → sussurro recebido → comandos de dono/ADM secretos
#   on_tip()             → gorjeta recebida → agradecimento no chat
#
#  PROCESSAMENTO CENTRAL:
#   _handle_chat()       → roteador principal: lê a mensagem, decide qual
#                          função chamar (emote, jogo, moderação, IA, etc.)
#
#  INTELIGÊNCIA ARTIFICIAL:
#   _jeffao_responde()   → monta o prompt e chama Groq ou Pollinations;
#                          detecta humor e faz o emote correspondente
#   _bot_emote()         → faz um emote rápido conforme o "humor" da IA
#   _voltar_para_lugar() → teleporta o bot de volta ao SPAWN_POSITION
#
#  SISTEMA DE EMOTES:
#   handle_emote_number()      → usuário digita número (1-220) → inicia loop
#   _handle_emote_at_user()    → emote direcionado a outro usuário (@nome)
#   start_emote_loop()         → inicia loop de emote para um user_id
#   _emote_loop_runner()       → loop principal: reenvia emote respeitando o
#                                tempo do emotes.py; mede latência de rede
#                                e subtrai do sleep para ciclo exato
#   stop_emote_loop()          → cancela loop de emote de um user_id
#   start_random_emote_loop()  → inicia loop de emote aleatório ("dança")
#   _random_emote_loop_runner()→ sorteia emote de secili_emote a cada ciclo
#   send_emote_list()          → envia lista numerada por sussurro ao usuário
#
#   COMO AJUSTAR TIMING DE EMOTE:
#     Abra emotes.py → encontre o emote pelo nome ou número → altere o
#     terceiro valor da tupla (duração em segundos).
#     ↑ aumentar = o loop espera mais antes de reiniciar
#     ↓ diminuir = o loop reinicia mais cedo (útil para evitar o avatar levantando)
#
#  SEGUIR / MOVIMENTAÇÃO:
#   follow()                  → bot segue um usuário em loop
#   stop_follow()             → cancela o follow
#   handle_follow_command()   → trata "vamos", "pare", "!seguir @x"
#   teleport()                → teleporta um usuário para uma Position
#   handle_teleport_command() → trata "!tp x y z", "!tp @user", "!tp cima" etc.
#   teleport_to_user()        → bot vai até a posição de outro usuário
#   cmd_tele_to_me()          → traz outro usuário até o bot
#   adjust_position()         → "+x5 -z2" — ajuste fino de posição
#   handle_platform_command() → !plataforma marcar/lista/remover/<nome>
#   switch_users()            → troca o bot de lugar com um usuário
#
#  MODERAÇÃO:
#   cmd_kick()         → expulsa usuário da sala
#   cmd_punir()        → inicia loop de teleporte punitivo
#   _punish_loop()     → loop interno da punição
#   cmd_inativo()      → encerra punição de um usuário
#   cmd_xd()           → trava usuário na posição atual (loop)
#   _lock_position_loop() → loop do travamento de posição
#   cmd_full_rtp()     → inicia teleportes aleatórios contínuos
#   _full_rtp_loop()   → loop interno do full rtp
#   cmd_all_dance()    → faz todos os usuários dançarem (emote por número)
#
#  REEMBOLSO DE GOLD:
#   _refund_gold()     → calcula denominações, envia tips ao usuário;
#                        se saldo insuficiente, notifica o dono via sussurro
#   _get_refund_tips() → helper: decompõe valor em denominações (algoritmo greedy)
#
#  CARGO / EQUIPE:
#   _cmd_cargo()       → dá ou remove cargo de designer/moderador/ambos
#   _cmd_ver_cargos()  → lista a equipe atual da sala
#
#  JOGOS:
#   cmd_jokenpo()      → pedra/papel/tesoura com placar persistente
#   cmd_placar_top()   → top 10 do jokenpô
#   cmd_meu_placar()   → stats individuais do usuário
#   cmd_dado()         → rola dado de 6 faces
#   cmd_moeda()        → cara ou coroa
#   cmd_8ball()        → bola 8 mágica
#   cmd_sorteio()      → sorteia usuário aleatório da sala
#   handle_match_command() → sorteia casal aleatório
#
#  ROUPA / OUTFIT:
#   handle_outfit_command()  → trata todos os subcomandos de !roupa
#   _send_current_outfit()   → lista outfit atual por sussurro
#   _cmd_roupa_whisper()     → veste item por categoria+id via sussurro
#   _cmd_muda_parte()        → troca parte específica do outfit
#
#  APELIDOS:
#   Procure: _cmd_alias / _handle_alias_command
#   Gerencia o aliases.json — apelidos de usuários para o bot reconhecer
#
#  ATUALIZAÇÃO AUTOMÁTICA (somente dono):
#   _cmd_auto_update() → baixa nova versão do código via sussurro e reinicia
#   _cmd_restore()     → restaura versão anterior em caso de falha
#
#  LISTAS DE COMANDOS:
#   _send_user_commands() → envia blocos de comandos ao usuário comum (!comandos)
#   _send_admin_list()    → envia blocos de comandos ao ADM (!admlista)
#
# ═══════════════════════════════════════════════════════════════════════════════

import asyncio
import time
import random
import json
import os
import sys
import aiohttp
import traceback
import subprocess
from datetime import datetime
from typing import Literal
from importlib import import_module
from asyncio import run as arun
from threading import Thread, Lock
import re

from highrise import BaseBot, CurrencyItem, Item, Position, User
from highrise.models import *
from highrise.__main__ import main, BotDefinition

from emotes import (
    EMOTES_LIST, TOTAL_EMOTES, emote_mapping, secili_emote, paid_emotes
)

# =====================================================================
# CONSTANTES GLOBAIS
# =====================================================================

BLOCKED_EMOTE_NUMS: dict[int, int | None] = {}

SPAWN_POSITION = {
    "enabled": True,
    "x": 10.0,
    "y": 0.0,
    "z": 6.5,
    "facing": "FrontLeft",
}

# =====================================================================
# IA — Groq API (mais rápida) ou Pollinations AI (grátis, sem chave)
# Configure a chave em Environment Secrets: GROQ_API_KEY
# =====================================================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# =====================================================================
# SISTEMA DE REEMBOLSO DE GOLD
# Denominações válidas do Highrise (do maior para o menor)
# =====================================================================
GOLD_DENOMINATIONS: list[int] = [10000, 5000, 1000, 500, 100, 50, 10, 5, 1]

def _get_refund_tips(amount: int) -> list[int]:
    """Decompõe um valor em denominações válidas de Gold do Highrise (greedy)."""
    remaining = amount
    tips: list[int] = []
    for denom in GOLD_DENOMINATIONS:
        while remaining >= denom:
            tips.append(denom)
            remaining -= denom
    return tips

ALIASES_FILE        = "aliases.json"
EMOTE_ALIASES_FILE  = "emote_aliases.json"
PLATFORMS_FILE      = "platforms.json"
PLACAR_FILE         = "placar.json"

# =====================================================================
# EMOTES DE EMOÇÃO — usados pela personalidade do Jeffão
# =====================================================================
EMOTION_EMOTES = {
    "curious":   "emote-confused",
    "happy":     "emote-hyped",
    "laugh":     "emote-laughing",
    "love":      "emote-hearteyes",
    "think":     "emote-think",
    "agree":     "emote-yes",
    "disagree":  "emote-no",
    "sad":       "emote-sad",
    "wow":       "emoji-mind-blown",
    "wave":      "emote-wave",
    "celebrate": "emote-celebrate",
    "shy":       "emote-shy",
    "wink":      "emote-kiss",
    "salute":    "emote-salute",
}

# =====================================================================
# PERSISTÊNCIA
# =====================================================================

def _load_json(path: str) -> dict:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
    return {}

def _save_json(path: str, data: dict) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {path}: {e}")

# ── Regex de itens do Highrise ──────────────────────────────────────────
_HR_ITEM_RE = re.compile(
    r'\b(shirt|pants|shoes|dress|bodysuit|jacket|coat|fullbody'
    r'|hair_front|hair_back|hair|face_eyes|eye|face_eyebrow'
    r'|face_nose|face_mouth|face_hair|body|skin'
    r'|bag|glasses|gloves|hat|necklace|bracelet|earrings'
    r'|watch|belt|tattoo|freckle|mole|lashes|blush|sock'
    r'|aura|fishing_rod|wing|tail)-[A-Za-z0-9_]+',
    re.IGNORECASE,
)

# Verbos que indicam intenção de vestir roupa no chat
_OUTFIT_VERBS = {
    "usa", "usar", "use", "veste", "vestir", "coloca", "colocar",
    "bota", "botar", "muda", "mudar", "troca", "trocar",
    "põe", "por", "pôr", "testa", "testar", "experimenta",
}

def _detect_item_ids(text: str) -> list[str]:
    """Extrai IDs de itens do Highrise de uma mensagem."""
    return [m.group(0) for m in _HR_ITEM_RE.finditer(text)]

def _is_pure_outfit_message(text: str) -> bool:
    """
    Retorna True se a mensagem é composta SOMENTE por IDs de itens
    (possivelmente separados por espaço/vírgula/nova-linha).
    """
    cleaned = _HR_ITEM_RE.sub("", text).strip(" ,;\n\t")
    return bool(_detect_item_ids(text)) and cleaned == ""

# ────────────────────────────────────────────────────────────────────────
def _load_aliases() -> dict:        return _load_json(ALIASES_FILE)
def _save_aliases(d: dict) -> None: _save_json(ALIASES_FILE, d)

def _load_emote_aliases() -> dict:        return _load_json(EMOTE_ALIASES_FILE)
def _save_emote_aliases(d: dict) -> None: _save_json(EMOTE_ALIASES_FILE, d)

def _load_platforms() -> dict:        return _load_json(PLATFORMS_FILE)
def _save_platforms(d: dict) -> None: _save_json(PLATFORMS_FILE, d)

def _load_placar() -> dict:        return _load_json(PLACAR_FILE)
def _save_placar(d: dict) -> None: _save_json(PLACAR_FILE, d)

CARGOS_FILE = "cargos.json"
def _load_cargos() -> dict:        return _load_json(CARGOS_FILE)
def _save_cargos(d: dict) -> None: _save_json(CARGOS_FILE, d)


def _register_jokenpo_result(username: str, resultado: str) -> None:
    placar = _load_placar()
    if username not in placar:
        placar[username] = {"vitorias": 0, "derrotas": 0, "empates": 0}
    if resultado == "vitoria":
        placar[username]["vitorias"] += 1
    elif resultado == "derrota":
        placar[username]["derrotas"] += 1
    else:
        placar[username]["empates"] += 1
    _save_placar(placar)


# =====================================================================
# AUTO-ATUALIZAÇÃO — salva e valida código novo antes de aplicar
# =====================================================================

def _safe_write_code(new_code: str) -> tuple[bool, str]:
    """
    1. Valida sintaxe com compile().
    2. Faz backup de main.py → main.py.bak antes de sobrescrever.
    3. Grava o novo código.
    """
    try:
        compile(new_code, "main.py", "exec")
    except SyntaxError as e:
        return False, f"Erro de sintaxe linha {e.lineno}: {e.msg}"
    try:
        script = os.path.abspath(__file__)
        try:
            with open(script, "r", encoding="utf-8") as f_orig:
                original = f_orig.read()
            with open(script + ".bak", "w", encoding="utf-8") as f_bak:
                f_bak.write(original)
        except Exception:
            pass
        with open(script, "w", encoding="utf-8") as f:
            f.write(new_code)
        return True, "ok"
    except Exception as e:
        return False, str(e)


def _read_own_code() -> str:
    try:
        with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _apply_patches(original: str, ai_response: str) -> tuple[str, list[str]]:
    """
    Aplica patches retornados pela IA ao código original.

    Formato esperado da IA:

        <<<PATCH>>>
        <<<FIND>>>
        [trecho EXATO do código a ser substituído]
        <<<END_FIND>>>
        <<<WITH>>>
        [novo código]
        <<<END_WITH>>>
        <<<END_PATCH>>>

        <<<INSERT>>>
        <<<AFTER>>>
        [trecho EXATO após o qual inserir]
        <<<END_AFTER>>>
        <<<CODE>>>
        [código a inserir]
        <<<END_CODE>>>
        <<<END_INSERT>>>

    Retorna (codigo_resultante, lista_de_avisos).
    Se nenhum bloco for encontrado, retorna o original sem alteração.
    """
    resultado = original
    avisos: list[str] = []

    for i, m in enumerate(re.finditer(r'<<<PATCH>>>(.*?)<<<END_PATCH>>>', ai_response, re.DOTALL), 1):
        bloco    = m.group(1)
        mf       = re.search(r'<<<FIND>>>(.*?)<<<END_FIND>>>',  bloco, re.DOTALL)
        mw       = re.search(r'<<<WITH>>>(.*?)<<<END_WITH>>>',  bloco, re.DOTALL)
        if not mf or not mw:
            avisos.append(f"Patch #{i}: bloco malformado (sem FIND/WITH)")
            continue
        find_txt = mf.group(1).strip("\n")
        with_txt = mw.group(1).strip("\n")
        if find_txt not in resultado:
            avisos.append(f"Patch #{i}: trecho não encontrado — verifique espaços/tabs")
            continue
        resultado = resultado.replace(find_txt, with_txt, 1)

    for i, m in enumerate(re.finditer(r'<<<INSERT>>>(.*?)<<<END_INSERT>>>', ai_response, re.DOTALL), 1):
        bloco  = m.group(1)
        ma     = re.search(r'<<<AFTER>>>(.*?)<<<END_AFTER>>>',  bloco, re.DOTALL)
        mc     = re.search(r'<<<CODE>>>(.*?)<<<END_CODE>>>',    bloco, re.DOTALL)
        if not ma or not mc:
            avisos.append(f"Insert #{i}: bloco malformado (sem AFTER/CODE)")
            continue
        after_txt = ma.group(1).strip("\n")
        code_txt  = mc.group(1).strip("\n")
        if after_txt not in resultado:
            avisos.append(f"Insert #{i}: ponto de inserção não encontrado")
            continue
        pos       = resultado.index(after_txt) + len(after_txt)
        resultado = resultado[:pos] + "\n" + code_txt + resultado[pos:]

    return resultado, avisos


# =====================================================================
# BOT PRINCIPAL
# =====================================================================

class Bot(BaseBot):

    # ------------------------------------------------------------------
    # CONFIGURAÇÕES DE CLASSE
    # ------------------------------------------------------------------

    PROTECTED_USERS       = ["Fenix_inthe_HR"]   # dono — nunca punir
    EMOTE_SWITCH_COOLDOWN =  1.0

    TELEPORT_LOCATIONS: dict[str, Position] = {
         "vip1": Position(16.0, 16.9, 18.0),
        "vip2": Position(14.5,  8.0, 23.5),
        "vip3": Position(11.0,  0.0, 25.0),
        "vip4": Position(11.0,  1.4,  3.0),
        "vip5": Position( 6.0, 12.0,  2.0),
     }    
    OUTFIT_CATEGORIES: dict[str, list[str]] = {
        "mascote":              ["fishing_rod-", "wing-", "tail-"],
        "parte de cima":        ["shirt-", "dress-", "bodysuit-", "jacket-", "coat-"],
        "parte de baixo":       ["pants-", "skirt-"],
        "corpo":                ["fullbody-"],
        "corpo todo":           ["fullbody-"],
        "body":                 ["fullbody-"],
        "aura":                 ["aura-"],
        "acessorios":           ["bag-", "glasses-", "gloves-", "hat-", "necklace-",
                                 "bracelet-", "earrings-", "watch-", "belt-", "tattoo-",
                                 "freckle-", "mole-", "lashes-", "blush-", "sock-"],
        "acessórios":           ["bag-", "glasses-", "gloves-", "hat-", "necklace-",
                                 "bracelet-", "earrings-", "watch-", "belt-", "tattoo-",
                                 "freckle-", "mole-", "lashes-", "blush-", "sock-"],
        "acessorio":            ["bag-", "glasses-", "gloves-", "hat-", "necklace-",
                                 "bracelet-", "earrings-", "watch-", "belt-", "tattoo-",
                                 "freckle-", "mole-", "lashes-", "blush-", "sock-"],
        "acessório":            ["bag-", "glasses-", "gloves-", "hat-", "necklace-",
                                 "bracelet-", "earrings-", "watch-", "belt-", "tattoo-",
                                 "freckle-", "mole-", "lashes-", "blush-", "sock-"],
        "calcados":             ["shoes-"],
        "calçados":             ["shoes-"],
        "sapato":               ["shoes-"],
        "calçado":              ["shoes-"],
        "calcado":              ["shoes-"],
        "cabelo":               ["hair_front-", "hair_back-", "hair-"],
        "cabelo frontal":       ["hair_front-"],
        "cabelo da frente":     ["hair_front-"],
        "cabelo frente":        ["hair_front-"],
        "hair front":           ["hair_front-"],
        "cabelo traseiro":      ["hair_back-"],
        "cabelo de tras":       ["hair_back-"],
        "cabelo de trás":       ["hair_back-"],
        "cabelo atras":         ["hair_back-"],
        "cabelo atrás":         ["hair_back-"],
        "hair back":            ["hair_back-"],
        "sobrancelha":          ["eyebrow-"],
        "sobrancelhas":         ["eyebrow-"],
        "olho":                 ["face_eyes-", "eye-"],
        "olhos":                ["face_eyes-", "eye-"],
        "nariz":                ["nose-"],
        "boca":                 ["mouth-"],
        "barba":                ["face_hair-"],
        "extra":                ["fishing_rod-", "wing-", "tail-"],
        "camisa":               ["shirt-", "dress-", "bodysuit-", "jacket-", "coat-"],
        "calça":                ["pants-", "skirt-"],
        "calca":                ["pants-", "skirt-"],
        "pele":                 ["body-", "skin-"],
        "skin":                 ["body-", "skin-"],
        "rosto":                ["face_", "body-skin"],
    }

    ACCESSORY_PREFIXES = (
        "bag-", "glasses-", "gloves-", "hat-", "necklace-", "bracelet-",
        "earrings-", "watch-", "belt-", "tattoo-", "freckle-", "mole-",
        "lashes-", "blush-", "sock-", "aura-", "fishing_rod-",
        "jacket-", "coat-", "wing-", "tail-",
    )

    OUTFIT_DISPLAY_ORDER = [
        ("Boca",           ("face_mouth-",)),
        ("Olho",           ("face_eyes-", "eye-")),
        ("Nariz",          ("face_nose-",)),
        ("Sobrancelha",    ("face_eyebrow-",)),
        ("Cabelo Frontal", ("hair_front-", "hair-")),
        ("Cabelo de Trás", ("hair_back-",)),
        ("Barba",          ("face_hair-",)),
        ("Camisa",         ("shirt-", "dress-", "bodysuit-", "jacket-", "coat-")),
        ("Calça",          ("pants-", "skirt-")),
        ("Sapato",         ("shoes-",)),
        ("Corpo Todo",     ("fullbody-",)),
        ("Acessório",      ("bag-", "glasses-", "gloves-", "hat-", "necklace-",
                            "bracelet-", "earrings-", "watch-", "belt-", "tattoo-",
                            "freckle-", "mole-", "lashes-", "blush-", "sock-")),
        ("Aura",           ("aura-",)),
        ("Extra",          ("fishing_rod-", "wing-", "tail-")),
    ]

    # ------------------------------------------------------------------
    # INIT
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self.following_user: User | None      = None
        self.following_user_id: str | None    = None
        self.follow_task: asyncio.Task | None = None

        self.user_emote_loops: dict[str, str]          = {}
        self.user_emote_tasks: dict[str, asyncio.Task] = {}
        self.user_emote_last_change: dict[str, float]  = {}

        self.is_teleporting_dict: dict[str, bool]      = {}
        self.punish_tasks: dict[str, asyncio.Task]     = {}

        self.position_tasks: dict[str, list]           = {}
        self.kus: dict[str, bool]                      = {}
        self.haricler: list[str]                       = []

        self._bot_user_id: str | None = None
        self._pending_outfit: dict[str, dict] = {}
        self._updating: bool = False
        self._event_loop = None

        # Cache de posições em tempo real — atualizado por on_user_move
        self._user_positions: dict[str, "Position"] = {}
        # Evento que acorda o loop de follow quando o alvo se move
        self._follow_move_event: asyncio.Event = asyncio.Event()

        # Snap-to-click: usuários que são teleportados instantaneamente para
        # onde clicaram no chão (elimina animação de andar)
        self._snap_users: set[str] = set()

        # XD lock event-driven: user_id → posição travada
        # Substituição do _lock_position_loop por eventos (sem polling)
        self._xd_locked_positions: dict[str, "Position"] = {}

        # Arremessador: ao clicar no chão, bot aguarda 1s e teleporta
        # o usuário para cima (Y alto) ou para baixo (Y=0) das coordenadas clicadas
        self._arremess_up: set[str] = set()    # força cima após 1s
        self._arremess_down: set[str] = set()  # força baixo após 1s

    # ------------------------------------------------------------------
    # EVENTOS DO HIGHRISE
    # ------------------------------------------------------------------

    async def on_start(self, session_metadata) -> None:
        self._event_loop  = asyncio.get_running_loop()
        self._bot_user_id = session_metadata.user_id if hasattr(session_metadata, "user_id") else None
        print("✅ Bot conectado à sala!")

        if SPAWN_POSITION.get("enabled", True):
            try:
                await self.highrise.walk_to(Position(
                    SPAWN_POSITION["x"], SPAWN_POSITION["y"],
                    SPAWN_POSITION["z"], SPAWN_POSITION.get("facing", "FrontLeft"),
                ))
            except Exception as e:
                print(f"[spawn] {e}")
        await self.highrise.chat(
            "Jeffão online. Pode me chamar pelo nome quando precisar. "
            "Digite !comandos para ver tudo que sei fazer."
        )

    async def on_user_join(self, user: User, position) -> None:
        # Armazena posição inicial no cache
        if isinstance(position, Position):
            self._user_positions[user.id] = position
        greetings = [
            f"@{user.username} entrou. Bem-vindo(a).",
            f"Boa, @{user.username}. Seja bem-vindo(a) à sala.",
            f"@{user.username} chegou. Pode ficar à vontade.",
        ]
        await self.highrise.chat(random.choice(greetings))
        await asyncio.sleep(0.3)
        try:
            await self.highrise.send_emote("emote-wave", self._bot_user_id or "")
        except Exception:
            pass

    async def on_user_leave(self, user: User) -> None:
        if user.id in self.user_emote_loops:
            await self.stop_emote_loop(user.id)
        if user.id in self.kus:
            self.kus[user.id] = False
        if user.id in self.is_teleporting_dict:
            self.is_teleporting_dict[user.id] = False
        # Limpa cache de posição
        self._user_positions.pop(user.id, None)
        # Limpa snap, xd lock e arremessador
        self._snap_users.discard(user.id)
        self._xd_locked_positions.pop(user.id, None)
        self._arremess_up.discard(user.id)
        self._arremess_down.discard(user.id)
        # Cancela tasks do position_tasks (XD loop antigo, fallback)
        for t in self.position_tasks.pop(user.id, []):
            t.cancel()
        # Se o usuário que saiu é o alvo do follow, para de seguir
        if self.following_user_id == user.id:
            await self.stop_follow()

    async def on_user_move(self, user: User, destination) -> None:
        """
        Atualiza cache de posição e aplica lógicas event-driven:
          • Follow: acorda o loop quando o alvo se move
          • XD lock: reteleporta instantaneamente se o usuário tentar sair da posição travada
          • Snap-to-click: teleporta o usuário instantaneamente para onde clicou (sem animação de andar)
        """
        if not isinstance(destination, Position):
            return

        self._user_positions[user.id] = destination

        # ── Follow ────────────────────────────────────────────────────
        if self.following_user_id == user.id:
            self._follow_move_event.set()

        # ── XD lock (event-driven, sem polling) ───────────────────────
        locked_pos = self._xd_locked_positions.get(user.id)
        if locked_pos is not None and destination != locked_pos:
            try:
                await self.highrise.teleport(user.id, locked_pos)
            except Exception:
                pass
            return  # Não processa snap se está travado

        # ── Arremessador (admin-only, precedência sobre snap) ──────────
        # Pega X/Z do clique e após 1s teleporta para cima ou para baixo
        if user.id in self._arremess_up:
            asyncio.create_task(self._arremess_delay(user.id, destination, direcao="cima"))
            return
        elif user.id in self._arremess_down:
            asyncio.create_task(self._arremess_delay(user.id, destination, direcao="baixo"))
            return

        # ── Snap-to-click GLOBAL ───────────────────────────────────────
        # Teleporta o usuário instantaneamente quando clica em ALTURA (y > 0.0).
        # Movimentos laterais no chão (y == 0.0) são ignorados — o usuário
        # pode andar normalmente sem ser teleportado.
        # _snap_users funciona como lista de EXCLUSÃO (snap OFF).
        # Bot não teleporta a si mesmo.
        if (self._bot_user_id and user.id == self._bot_user_id):
            return
        if user.id not in self._snap_users:   # snap_users = excluídos do snap global
            if destination.y > 0.0:           # ← só age em mudança de ALTURA, nunca lateral
                try:
                    await self.highrise.teleport(user.id, destination)
                except Exception:
                    pass

    async def on_chat(self, user: User, message: str) -> None:
        try:
            await self._handle_chat(user, message)
        except Exception as e:
            print(f"[on_chat] Erro: {e}")

    async def on_whisper(self, user: User, message: str) -> None:
        """
        Whisper do dono:
          @mensagem           → fala no chat público
          @jeff <pergunta>    → resposta privada via IA (só o dono vê)
          @update <pedido>    → auto-atualização do bot (só dono)
          @lercodigo          → envia o código atual (só dono)
          @roupa <cat> <id>   → troca roupa do bot (só dono)
          @funcoes            → lista funções do bot (só dono)
        """
        try:
            msg = message.strip()
            is_owner = user.username in self.PROTECTED_USERS

            if not msg.startswith("@"):
                return

            cmd = msg[1:].strip()
            cmd_lower = cmd.lower()

            if not is_owner and cmd:
                is_adm = await self.is_user_allowed(user)
                if is_adm:
                    await self.highrise.chat(cmd)
                else:
                    await self.highrise.send_whisper(user.id, "Sem permissão.")
                return

            if not is_owner:
                return

            if cmd_lower.startswith("jeff ") or cmd_lower.startswith("ai ") or cmd_lower.startswith("ia "):
                pergunta = cmd.split(maxsplit=1)[1].strip()
                await self._jeffao_responde(user, pergunta, whisper_back=True)
                return

            if cmd_lower.startswith("update ") or cmd_lower.startswith("atualizar "):
                pedido = cmd.split(maxsplit=1)[1].strip()
                await self._cmd_auto_update(user, pedido)
                return

            if cmd_lower.startswith("testar ") or cmd_lower.startswith("test "):
                pedido = cmd.split(maxsplit=1)[1].strip()
                await self._cmd_auto_update(user, pedido, dry_run=True)
                return

            if cmd_lower in ("restore", "restaurar", "reverter", "rollback", "desfazer"):
                await self._cmd_restore(user)
                return

            if cmd_lower.startswith("cargo ") or cmd_lower == "cargo":
                await self._cmd_cargo(user, "!cargo " + cmd[len("cargo"):].strip())
                return

            if cmd_lower in ("lercodigo", "ler codigo", "lercode", "codigo"):
                await self._cmd_ler_codigo(user)
                return

            if cmd_lower in ("funcoes", "funções", "funcao", "função", "listafuncoes"):
                await self._cmd_lista_funcoes(user)
                return

            if cmd_lower.startswith("roupa "):
                partes = cmd.split(maxsplit=2)
                if len(partes) >= 3:
                    cat   = partes[1].strip().lower()
                    iid   = partes[2].strip()
                    await self._cmd_roupa_whisper(user, cat, iid)
                else:
                    await self.highrise.send_whisper(user.id, "Uso: @roupa <categoria> <id>")
                return

            if cmd_lower.startswith("muda "):
                parte = cmd.split(maxsplit=1)[1].strip().lower()
                await self._cmd_muda_parte(user, parte)
                return

            if user.id in self._pending_outfit:
                info = self._pending_outfit.pop(user.id)
                await self._change_category(user, info["cat"], info["prefixes"], cmd.strip())
                return

            if cmd:
                await self.highrise.chat(cmd)

        except Exception as e:
            print(f"[on_whisper] Erro: {e}")

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        try:
            if isinstance(tip, CurrencyItem):
                await self.highrise.chat(
                    f"💰 @{sender.username} enviou {tip.amount} ouro para @{receiver.username}! Obrigado!"
                )
        except Exception as e:
            print(f"[on_tip] Erro: {e}")

    # ------------------------------------------------------------------
    # HANDLER PRINCIPAL DE CHAT
    # ------------------------------------------------------------------

    async def _handle_chat(self, user: User, message: str) -> None:
        msg = message.strip().lower()
        is_adm = await self.is_user_allowed(user)

        if is_adm:
            detected_ids = _detect_item_ids(message)
            if detected_ids:
                words_lower = set(msg.split())
                has_verb    = bool(_OUTFIT_VERBS & words_lower)
                is_pure     = _is_pure_outfit_message(message.strip())
                if is_pure or has_verb:
                    await self._equip_detected_ids(user, detected_ids)
                    return

        # Extrai palavras do msg para detectar apelidos em qualquer posição
        import re as _re
        _msg_words = _re.findall(r"[\wÀ-ú]+", msg)

        _matched_trigger: str | None = None
        for _t in JEFFAO_TRIGGERS:
            if _t in _msg_words:
                _matched_trigger = _t
                break

        if _matched_trigger:
            trigger = _matched_trigger
            # Extrai o texto depois (ou antes) do gatilho como a "pergunta"
            _idx    = msg.find(trigger)
            _after  = message.strip()[_idx + len(trigger):].strip().lstrip(",: ")
            _before = message.strip()[:_idx].strip().rstrip(",: ")
            rest    = _after if _after else (_before if _before else message.strip())
            rest_low = rest.lower()

            # "Jeffão volta pra seu lugar" ou similar → retorna ao spawn
            if any(w in rest_low for w in ("seu lugar", "volta pra", "voltar pra", "de volta", "lugar")):
                await self._voltar_para_lugar()
                await self.highrise.chat(f"Certo, @{user.username}.")
                return

            # Pergunta direta → responde com IA
            _QUESTION_STARTS = (
                "o que", "oque", "oq ", "como ", "quem ", "onde ",
                "quando ", "por que", "porque", "pq ", "qual ",
                "quais ", "você ", "vc ", "explique", "explica",
                "defin", "me di", "me fal", "me conta", "sabe ",
                "conhece", "entende", "existe", "é verdade",
            )
            is_question = (
                "?" in rest
                or any(rest_low.startswith(w) for w in _QUESTION_STARTS)
            )
            if is_question and rest:
                await self._jeffao_responde(user, rest, whisper_back=False)
            elif rest:
                # Chamada casual → vai até a pessoa
                try:
                    room_users = (await self.highrise.get_room_users()).content
                    pos = next((p for u, p in room_users if u.id == user.id), None)
                    if pos and isinstance(pos, Position):
                        nearby = Position(pos.x + 0.5, pos.y, pos.z, pos.facing)
                        await self.highrise.walk_to(nearby)
                except Exception:
                    pass
                await self.highrise.chat(f"@{user.username}, me chama. O que foi?")
            else:
                await self.highrise.chat(f"@{user.username}.")
            return

        if msg == "!comandos":
            await self._send_user_commands(user)
            return

        if msg in ("!admlista", "!admlias"):
            if is_adm:
                await self._send_admin_list(user)
            return

        if msg == "!lista":
            await self.send_emote_list(user)
            return

        if msg.startswith("!assistente"):
            parts = message.strip().split(maxsplit=1)
            if len(parts) >= 2 and parts[1].strip():
                await self._jeffao_responde(user, parts[1].strip(), whisper_back=False)
            else:
                await self.highrise.chat(
                    "Jeffão: me chama assim ó — Jeffão  <sua pergunta>  ou  !assistente <pergunta> 😄"
                )
            return

        if msg in ("stop", "dur", "0", "parar"):
            if user.id in self.user_emote_loops:
                await self.stop_emote_loop(user.id)
            if user.id in self.kus:
                self.kus[user.id] = False
            return

        if msg in ("dança", "danca"):
            if user.id not in self.user_emote_loops:
                await self.start_random_emote_loop(user.id)
            else:
                await self.stop_emote_loop(user.id)
            return

        if msg.startswith("!jokenpo"):
            await self.cmd_jokenpo(user, message)
            return

        if msg == "!placar":
            await self.cmd_placar_top(user)
            return

        if msg in ("!meu placar", "!meuplacar"):
            await self.cmd_meu_placar(user)
            return

        if msg == "!dado":
            await self.cmd_dado(user)
            return

        if msg == "!moeda":
            await self.cmd_moeda(user)
            return

        if msg.startswith("!8ball"):
            await self.cmd_8ball(user, message)
            return

        if msg == "!sorteio":
            await self.cmd_sorteio(user)
            return

        if msg == "!match":
            await self.handle_match_command(user)
            return

        if msg.startswith("!pedido "):
            youtube_url = message.strip()[8:].strip()
            asyncio.create_task(self._cmd_pedido_radio(user, youtube_url))
            return

        if msg == "!cargos":
            await self._cmd_ver_cargos(user)
            return

        if msg.startswith("!cargo") and is_adm:
            await self._cmd_cargo(user, message)
            return

        if msg.startswith("!reembolso") and is_adm:
            parts = message.strip().split()
            if len(parts) >= 3:
                target_name = parts[1].lstrip("@")
                try:
                    amt = int(parts[2])
                    if amt <= 0:
                        raise ValueError
                    asyncio.create_task(self._refund_gold(target_name, amt))
                except ValueError:
                    await self.highrise.send_whisper(
                        user.id, "Uso: !reembolso @usuario <quantidade>"
                    )
            else:
                await self.highrise.send_whisper(
                    user.id, "Uso: !reembolso @usuario <quantidade>"
                )
            return

        if (msg.startswith("info") or msg.startswith("userinfo")) and "@" in msg:
            target = message.split("@")[-1].strip()
            await self.cmd_userinfo(user, target)
            return

        if msg in self.TELEPORT_LOCATIONS:
            if msg == "vip1" and not is_adm:
                await self.highrise.send_whisper(user.id, "VIP1 é exclusivo para ADMs.")
                return
            await self.teleport(user, self.TELEPORT_LOCATIONS[msg])
            return

        # Teleporte vertical sem comando — basta digitar "cima" ou "baixo"
        if msg in ("cima", "up"):
            room_users = (await self.highrise.get_room_users()).content
            pos = next((p for u, p in room_users if u.id == user.id), None)
            if pos and isinstance(pos, Position):
                await self.teleport(user, Position(pos.x, pos.y + 2.0, pos.z, pos.facing))
            return

        if msg in ("baixo", "down"):
            room_users = (await self.highrise.get_room_users()).content
            pos = next((p for u, p in room_users if u.id == user.id), None)
            if pos and isinstance(pos, Position):
                await self.teleport(user, Position(pos.x, max(0.0, pos.y - 2.0), pos.z, pos.facing))
            return

        if msg in ("deneme1", "deneme2"):
            pos = Position(random.uniform(0, 20), 0.0, random.uniform(0, 20))
            await self.teleport(user, pos)
            return

        if len(msg) >= 2 and msg[0] in ("+", "-") and msg[1] in ("x", "y", "z"):
            await self.adjust_position(user, message)
            return

        if msg.startswith("!tp"):
            await self.handle_teleport_command(user, message)
            return

        if is_adm:
            if msg in ("!vamos", "vamos"):
                if self.is_teleporting_dict.get(user.id, False):
                    return  # Não segue usuários sendo punidos
                if self.following_user is not None:
                    await self.highrise.chat("Já estou seguindo alguém.")
                else:
                    self.follow_task = asyncio.create_task(self.follow(user))
                return

            if msg in ("!pare", "pare", "!parar", "parar"):
                if self.following_user is not None:
                    await self.highrise.chat("✅ Parei de seguir.")
                    await self.stop_follow()
                else:
                    await self.highrise.chat("Não estou seguindo ninguém. 🖐️")
                return

            if msg.startswith("!seguir"):
                await self.handle_follow_command(user, message)
                return

            if msg.startswith("kick "):
                await self.cmd_kick(user, message)
                return

            if msg.startswith("punir "):
                await self.cmd_punir(user, message)
                return

            if msg.startswith("inativo "):
                await self.cmd_inativo(user, message)
                return

            if msg.startswith("xd "):
                await self.cmd_xd(user, message)
                return

            if msg.startswith("!snap ") or msg.startswith("snap "):
                await self.cmd_snap(user, message)
                return

            if msg.startswith("arremessar ") or msg.startswith("!arremessar "):
                await self.cmd_arremessar(user, message)
                return

            if msg.startswith("switch "):
                target = message.split("@")[-1].strip()
                await self.switch_users(user, target)
                return

            if msg == "full rtp":
                await self.cmd_full_rtp(user)
                return

            if msg.startswith("all "):
                await self.cmd_all_dance(user, message)
                return

            if msg.startswith("t @") or msg.startswith("t@"):
                target = message.split("@")[-1].strip()
                await self.cmd_tele_to_me(user, target)
                return

            if msg.startswith("tele @") or msg.startswith("tele@"):
                target = message.split("@")[-1].strip()
                await self.teleport_to_user(user, target)
                return

            if msg.startswith("!roupa"):
                await self.handle_outfit_command(user, message)
                return

            if msg.startswith("!apelido"):
                await self.handle_alias_command(user, message)
                return

            if msg.startswith("!olhos "):
                color = message.split(maxsplit=1)[1].strip().lower()
                await self.cmd_olhos(user, color)
                return

            if msg.startswith("!plataforma"):
                await self.handle_platform_command(user, message)
                return

        emote_aliases = _load_emote_aliases()

        if msg.isdigit():
            await self.handle_emote_number(user, int(msg))
            return

        resolved = self._resolve_emote(msg, emote_aliases)
        if resolved:
            if user.id in self.user_emote_loops and self.user_emote_loops[user.id] == resolved:
                await self.stop_emote_loop(user.id)
            else:
                await self.start_emote_loop(user.id, resolved)
            return

        if "@" in msg:
            await self._handle_emote_at_user(user, message, emote_aliases, is_adm)

    # ------------------------------------------------------------------
    # JEFFÃO — RESPOSTA COM PERSONALIDADE + EMOTES
    # ------------------------------------------------------------------

    async def _jeffao_responde(
        self, user: User, pergunta: str, whisper_back: bool = False
    ) -> None:
        try:
            is_owner = user.username in self.PROTECTED_USERS

            outfit_context = ""
            if is_owner or await self.is_user_allowed(user):
                detected_ids = _detect_item_ids(pergunta)
                if detected_ids:
                    applied = await self._equip_detected_ids(user, detected_ids, silent=True)
                    if applied:
                        nomes = ", ".join(applied[:4]) + ("…" if len(applied) > 4 else "")
                        outfit_context = (
                            f"\n[AÇÃO JÁ REALIZADA] O usuário pediu para você vestir item(s) do Highrise. "
                            f"Você JÁ vestiu com sucesso: {nomes}. "
                            f"Confirme de forma animada e natural, comentando sobre a roupa se quiser."
                        )

            if self._bot_user_id:
                await self._bot_emote("think")

            if not whisper_back:
                await self.highrise.chat(f"Jeffão: um momento, @{user.username}.")

            system_prompt = (
                "Você é o Jeffão, bot do jogo mobile Highrise. Personalidade: maduro, sereno, direto e "
                "altamente inteligente. Não é arrogante, mas é assertivo e confiante. Fala com clareza, "
                "sem excessos de exclamações ou emojis. Só usa emoji quando for natural. "
                "Seu conhecimento é atualizado até maio de 2026 e é profundo em TODOS os assuntos: "
                "física, astronomia, química, biologia, tecnologia, inteligência artificial, "
                "jogos (especialmente Highrise), música, arte, filosofia, psicologia, história, "
                "matemática, programação, economia, geopolítica, cultura pop, esportes e tudo mais. "
                "\n\n"
                "=== MECÂNICAS DO HIGHRISE QUE VOCÊ CONHECE ===\n"
                "• ITENS/OUTFIT: cada item tem um ID único no formato categoria-nome (ex: shirt-n_basic_white). "
                "Categorias: shirt, pants, shoes, dress, bodysuit, jacket, coat, fullbody, "
                "hair_front, hair_back, hair, face_eyes, eye, face_eyebrow, face_nose, face_mouth, face_hair, "
                "body, skin, bag, glasses, gloves, hat, necklace, bracelet, earrings, watch, belt, "
                "tattoo, freckle, mole, lashes, blush, sock, aura, fishing_rod, wing, tail. "
                "• GOLD: moeda do jogo usada para comprar itens e dar gorjetas. "
                "Denominações válidas: 1, 5, 10, 50, 100, 500, 1000, 5000, 10000. "
                "• SALAS: espaços onde os avatares se encontram, públicas ou privadas. "
                "• EMOTES: animações/danças do avatar. O bot tem +220 emotes disponíveis. "
                "• GORJETAS (tips): jogadores enviam ouro para outros avatares ou bots. "
                "• MODERAÇÃO: moderadores de sala podem remover jogadores. "
                "• HIGHRISE STUDIO: ferramenta para criar itens e salas customizadas. "
                "\n"
                "=== COMANDOS QUE VOCÊ (BOT) ENTENDE ===\n"
                "Qualquer um: !comandos, !lista, Jeffão <frase/pergunta>, !assistente <pergunta>\n"
                "ADMs: !kick, !punir, !full rtp, !tp, !vamos, !pare, !xd, !cargo, !reembolso @user <valor>\n"
                "Dono (sussurro): @update, @testar, @roupa <cat> <id>, @muda, @jeff, @cargo\n"
                "VESTIR ROUPA: qualquer ADM/dono pode mandar um ID de item no chat e eu visto automaticamente!\n"
                "=== FIM DO CONTEXTO ===" + outfit_context + "\n\n"
                "Responda SEMPRE em português brasileiro. Seja preciso e direto. Máximo 220 caracteres. "
                "Ao final indique a emoção: "
                "[FELIZ] [CURIOSO] [ANIMADO] [PENSATIVO] [SURPRESO] [CONCORDO] [DISCORDO] [CARINHOSO] [NORMAL]"
            )

            payload = {
                "messages": [
                    {"role": "system",  "content": system_prompt},
                    {"role": "user",    "content": pergunta},
                ],
                "seed": random.randint(1, 9999),
            }

            if GROQ_API_KEY:
                url     = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type":  "application/json",
                }
                payload["model"]      = "llama-3.1-8b-instant"
                payload["max_tokens"] = 250
            else:
                url     = "https://text.pollinations.ai/openai"
                headers = {"Content-Type": "application/json"}
                payload["model"]      = "openai"

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, json=payload, headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status != 200:
                        err = await resp.text()
                        print(f"[jeffao] {resp.status}: {err[:200]}")
                        msg_err = "Jeffão: eita, deu ruim aqui no sistema, tenta de novo! 😅"
                        if whisper_back:
                            await self.highrise.send_whisper(user.id, msg_err)
                        else:
                            await self.highrise.chat(msg_err)
                        return
                    data     = await resp.json(content_type=None)
                    resposta = data["choices"][0]["message"]["content"].strip()

            emocao_tag = "NORMAL"
            for tag in ["FELIZ", "CURIOSO", "ANIMADO", "PENSATIVO",
                        "SURPRESO", "CONCORDO", "DISCORDO", "CARINHOSO"]:
                if f"[{tag}]" in resposta:
                    emocao_tag = tag
                    resposta   = resposta.replace(f"[{tag}]", "").strip()
                    break

            emote_map = {
                "FELIZ":      "happy",
                "CURIOSO":    "curious",
                "ANIMADO":    "celebrate",
                "PENSATIVO":  "think",
                "SURPRESO":   "wow",
                "CONCORDO":   "agree",
                "DISCORDO":   "disagree",
                "CARINHOSO":  "love",
                "NORMAL":     "wave",
            }
            await self._bot_emote(emote_map.get(emocao_tag, "wave"))

            if whisper_back:
                prefix = f"Jeffão (privado): {resposta}"
                await self.highrise.send_whisper(user.id, prefix[:250])
            else:
                texto  = f"Jeffão: {resposta}"
                chunks = []
                while len(texto) > 230:
                    idx = texto.rfind(" ", 0, 230)
                    if idx == -1:
                        idx = 230
                    chunks.append(texto[:idx])
                    texto = texto[idx:].strip()
                if texto:
                    chunks.append(texto)
                for chunk in chunks:
                    await self.highrise.chat(chunk)
                    if len(chunks) > 1:
                        await asyncio.sleep(0.7)

            await self._voltar_para_lugar()

        except asyncio.TimeoutError:
            msg_t = "Jeffão: demorei demais pra pensar, me perdoa! 😂 Tenta de novo!"
            if whisper_back:
                await self.highrise.send_whisper(user.id, msg_t)
            else:
                await self.highrise.chat(msg_t)
        except Exception as e:
            print(f"[_jeffao_responde] {e}")
            msg_e = "Jeffão: opa, deu um erro aqui. Tenta de novo! 🤖"
            if whisper_back:
                await self.highrise.send_whisper(user.id, msg_e)
            else:
                await self.highrise.chat(msg_e)

    async def _bot_emote(self, emotion_key: str) -> None:
        """Executa um emote no bot baseado na chave de emoção."""
        if not self._bot_user_id:
            return
        emote_id = EMOTION_EMOTES.get(emotion_key, "emote-wave")
        try:
            await self.highrise.send_emote(emote_id, self._bot_user_id)
        except Exception:
            pass

    async def _voltar_para_lugar(self) -> None:
        """Faz o bot voltar à posição de spawn após interagir."""
        if not SPAWN_POSITION.get("enabled", False):
            return
        try:
            await asyncio.sleep(1.0)
            await self.highrise.walk_to(Position(
                SPAWN_POSITION["x"], SPAWN_POSITION["y"],
                SPAWN_POSITION["z"], SPAWN_POSITION.get("facing", "FrontLeft"),
            ))
        except Exception:
            pass

    # ------------------------------------------------------------------
    # PEDIDO DE MÚSICA NA RÁDIO
    # ------------------------------------------------------------------

    async def _cmd_pedido_radio(self, user: User, youtube_url: str) -> None:
        """Baixa áudio do YouTube e adiciona à fila da Rádio Jeffão."""
        import re as _re
        url_pat = _re.compile(
            r'https?://(www\.)?(youtube\.com/(watch\?.*v=|shorts/|live/)|youtu\.be/)'
        )
        if not url_pat.match(youtube_url):
            await self.highrise.send_whisper(
                user.id,
                "❌ Link inválido. Use: !pedido https://youtube.com/watch?v=..."
            )
            return

        await self.highrise.chat(
            f"⏳ @{user.username} pediu uma música! Baixando do YouTube, aguarde..."
        )

        radio_api = os.environ.get(
            "RADIO_API_URL",
            "http://localhost:80/api"
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{radio_api}/radio/download",
                    json={
                        "youtubeUrl": youtube_url,
                        "requestedBy": user.username,
                        "addToQueue": True,
                    },
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as resp:
                    if resp.status == 201:
                        data = await resp.json()
                        title = data.get("song", {}).get("title", "?")
                        await self.highrise.chat(
                            f"🎵 @{user.username}: '{title}' adicionada à fila da Rádio Jeffão!"
                        )
                    else:
                        data = await resp.json()
                        err = data.get("error", "Erro desconhecido")
                        await self.highrise.send_whisper(user.id, f"❌ {err}")
        except Exception as e:
            await self.highrise.send_whisper(
                user.id,
                f"❌ Erro ao conectar com a rádio: {str(e)[:80]}"
            )

    # ------------------------------------------------------------------
    # REEMBOLSO DE GOLD
    # ------------------------------------------------------------------

    async def _refund_gold(self, target_username: str, amount: int) -> None:
        """
        Reembolsa Gold ao usuário usando denominações válidas do Highrise.
        Se o saldo for insuficiente, avisa o dono via sussurro informando
        o @ e a quantidade em falta.
        """
        tips = _get_refund_tips(amount)
        if not tips:
            return

        room_users = (await self.highrise.get_room_users()).content

        target = next(
            (u for u, _ in room_users if u.username.lower() == target_username.lower()), None
        )
        if not target:
            for owner_name in self.PROTECTED_USERS:
                owner = next((u for u, _ in room_users if u.username == owner_name), None)
                if owner:
                    await self.highrise.send_whisper(
                        owner.id,
                        f"⚠️ Reembolso pendente: @{target_username} não está na sala. "
                        f"Valor: {amount}g"
                    )
            return

        total_sent   = 0
        short_amount = 0

        for tip_amount in tips:
            try:
                await self.highrise.tip_user(
                    target.id, CurrencyItem(type="gold", amount=tip_amount)
                )
                total_sent += tip_amount
                await asyncio.sleep(0.4)
            except Exception as e:
                err = str(e).lower()
                if any(w in err for w in ("insufficient", "not enough", "balance", "gold", "saldo")):
                    short_amount = amount - total_sent
                    break
                print(f"[refund_gold] erro no tip: {e}")

        if short_amount > 0:
            for owner_name in self.PROTECTED_USERS:
                owner = next((u for u, _ in room_users if u.username == owner_name), None)
                if owner:
                    await self.highrise.send_whisper(
                        owner.id,
                        f"⚠️ Saldo insuficiente! Faltam {short_amount}g para reembolsar "
                        f"@{target_username} (enviado: {total_sent}g de {amount}g solicitado)."
                    )
        elif total_sent == amount:
            await self.highrise.chat(f"✅ {total_sent}g reembolsados para @{target_username}.")

    # ------------------------------------------------------------------
    # AUTO-ATUALIZAÇÃO (somente dono, via sussurro)
    # ------------------------------------------------------------------

    async def _cmd_auto_update(
        self, user, pedido: str, dry_run: bool = False, send_fn=None
    ) -> None:
        async def _send(msg: str) -> None:
            if send_fn is not None:
                await send_fn(msg)
            else:
                await self.highrise.send_whisper(user.id, msg)

        if self._updating:
            await _send("⚙️ Já estou me atualizando, aguarda...")
            return

        self._updating = True
        try:
            modo = "🔍 [SIMULAÇÃO]" if dry_run else "⚙️"
            await _send(f"{modo} Pedido recebido: '{pedido[:100]}'")
            await _send(f"{modo} Lendo meu código completo...")

            codigo_atual = _read_own_code()
            if not codigo_atual:
                await _send("❌ Não consegui ler meu código.")
                return

            total_linhas = len(codigo_atual.splitlines())
            await _send(f"{modo} Código lido: {total_linhas} linhas. Consultando IA...")

            system_prompt = (
                "Você é um especialista Python modificando o bot Jeffão para Highrise.\n"
                "Você receberá o código COMPLETO do bot e uma instrução de modificação.\n\n"
                "REGRA MAIS IMPORTANTE: Retorne SOMENTE os trechos que precisam mudar,\n"
                "usando EXATAMENTE este formato — sem texto extra, sem markdown, sem explicações:\n\n"
                "Para SUBSTITUIR um trecho existente:\n"
                "<<<PATCH>>>\n"
                "<<<FIND>>>\n"
                "[3 a 15 linhas EXATAS do código original — suficiente para ser único]\n"
                "<<<END_FIND>>>\n"
                "<<<WITH>>>\n"
                "[código substituto — pode ser maior ou menor]\n"
                "<<<END_WITH>>>\n"
                "<<<END_PATCH>>>\n\n"
                "Para INSERIR código novo sem remover nada:\n"
                "<<<INSERT>>>\n"
                "<<<AFTER>>>\n"
                "[3 a 10 linhas EXATAS do código que vem ANTES do ponto de inserção]\n"
                "<<<END_AFTER>>>\n"
                "<<<CODE>>>\n"
                "[novo código a inserir]\n"
                "<<<END_CODE>>>\n"
                "<<<END_INSERT>>>\n\n"
                "Regras adicionais:\n"
                "- O texto em FIND/AFTER deve ser IDÊNTICO ao código original (espaços, tabs, acentos)\n"
                "- Preserve indentação (4 espaços por nível)\n"
                "- Você pode ter quantos blocos PATCH/INSERT precisar\n"
                "- Nunca retorne o arquivo inteiro\n"
                "- O código modificado deve compilar sem erros em Python 3.10+"
            )

            user_prompt = f"PEDIDO DE MODIFICAÇÃO: {pedido}\n\nCÓDIGO COMPLETO (main.py):\n{codigo_atual}"

            payload: dict = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                "seed":       random.randint(1, 99999),
                "max_tokens": 4096,
            }

            if GROQ_API_KEY:
                url     = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type":  "application/json",
                }
                payload["model"] = "llama-3.1-70b-versatile"
            else:
                url     = "https://text.pollinations.ai/openai"
                headers = {"Content-Type": "application/json"}
                payload["model"] = "openai-large"

            await _send(f"{modo} Aguardando IA... (pode levar até 90s)")

            resposta_ia = None
            for tentativa in range(1, 3):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url, json=payload, headers=headers,
                            timeout=aiohttp.ClientTimeout(total=120),
                        ) as resp:
                            if resp.status != 200:
                                await _send(
                                    f"⚠️ IA retornou HTTP {resp.status} (tent. {tentativa}/2)"
                                )
                                if tentativa == 2:
                                    return
                                await asyncio.sleep(6)
                                continue
                            data        = await resp.json(content_type=None)
                            resposta_ia = data["choices"][0]["message"]["content"].strip()
                            break
                except asyncio.TimeoutError:
                    await _send(f"⚠️ Timeout na IA (tent. {tentativa}/2). Tentando novamente...")
                    if tentativa == 2:
                        return
                    await asyncio.sleep(5)
                except Exception as e:
                    await _send(f"⚠️ Erro de conexão (tent. {tentativa}/2): {str(e)[:80]}")
                    if tentativa == 2:
                        return
                    await asyncio.sleep(5)

            if not resposta_ia:
                await _send("❌ Nenhuma resposta da IA.")
                return

            await _send(f"{modo} Aplicando patches ao código...")
            novo_codigo, avisos = _apply_patches(codigo_atual, resposta_ia)

            n_patches = len(re.findall(r'<<<PATCH>>>', resposta_ia))
            n_inserts = len(re.findall(r'<<<INSERT>>>', resposta_ia))
            total_ops = n_patches + n_inserts

            if total_ops == 0:
                await _send(
                    "⚠️ IA não retornou patches no formato esperado. "
                    "Tente reformular o pedido."
                )
                return

            if avisos:
                for av in avisos:
                    await _send(f"⚠️ {av}")

            await _send(f"{modo} Verificando sintaxe Python...")
            try:
                compile(novo_codigo, "main.py", "exec")
            except SyntaxError as e:
                await _send(
                    f"❌ Erro de sintaxe linha {e.lineno}: {e.msg}. "
                    "Código ORIGINAL mantido."
                )
                return

            linhas_novas  = len(novo_codigo.splitlines())
            diff_linhas   = linhas_novas - total_linhas

            if dry_run:
                sinal = f"+{diff_linhas}" if diff_linhas >= 0 else str(diff_linhas)
                await _send(
                    f"✅ [SIMULAÇÃO] {total_ops} patch(es). "
                    f"{total_linhas} → {linhas_novas} linhas ({sinal}). "
                    "Nada foi gravado."
                )
                return

            ok, erro = _safe_write_code(novo_codigo)
            if not ok:
                await _send(f"❌ Erro ao gravar: {erro[:150]}.")
                return

            sinal = f"+{diff_linhas}" if diff_linhas >= 0 else str(diff_linhas)
            await _send(
                f"✅ {total_ops} patch(es)! "
                f"{total_linhas} → {linhas_novas} linhas ({sinal}). "
                "Reiniciando em 3s..."
            )
            await asyncio.sleep(3)

            script = os.path.abspath(__file__)
            subprocess.Popen(
                [sys.executable, script],
                cwd=os.path.dirname(script),
            )
            os._exit(0)

        except Exception as e:
            print(f"[_cmd_auto_update] {e}")
            await _send(f"❌ Erro inesperado: {str(e)[:150]}")
        finally:
            self._updating = False

    async def _cmd_restore(self, user: User) -> None:
        """Restaura main.py.bak → main.py e reinicia."""
        bak = os.path.abspath(__file__) + ".bak"
        if not os.path.exists(bak):
            await self.highrise.send_whisper(
                user.id, "❌ Nenhum backup encontrado (main.py.bak não existe)."
            )
            return
        try:
            with open(bak, "r", encoding="utf-8") as f:
                backup_code = f.read()
            linhas = len(backup_code.splitlines())
            try:
                compile(backup_code, "main.py", "exec")
            except SyntaxError as e:
                await self.highrise.send_whisper(
                    user.id,
                    f"❌ Backup também tem erro de sintaxe (linha {e.lineno}). "
                    "Não é possível restaurar automaticamente."
                )
                return
            with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
                f.write(backup_code)
            await self.highrise.send_whisper(
                user.id,
                f"✅ Backup restaurado! ({linhas} linhas). Reiniciando em 2s..."
            )
            await asyncio.sleep(2)
            script = os.path.abspath(__file__)
            subprocess.Popen([sys.executable, script], cwd=os.path.dirname(script))
            os._exit(0)
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"❌ Erro ao restaurar: {str(e)[:120]}")

    # ------------------------------------------------------------------
    # SISTEMA DE CARGOS — designer, moderador, ambos
    # ------------------------------------------------------------------

    async def _cmd_cargo(self, user, message: str) -> None:
        parts = message.strip().split()

        if len(parts) < 2:
            await self.highrise.send_whisper(
                user.id,
                "Uso: !cargo @usuario designer|moderador|ambos|remover  |  !cargo lista"
            )
            return

        sub = parts[1].lower().lstrip("@")

        if sub == "lista":
            await self._cmd_ver_cargos(user, whisper=True)
            return

        if len(parts) < 3:
            await self.highrise.send_whisper(
                user.id,
                "Uso: !cargo @usuario designer|moderador|ambos|remover"
            )
            return

        target = parts[1].lstrip("@")
        cargo  = parts[2].lower().strip()

        sinonimos = {
            "moderadora": "moderador",
            "mod":        "moderador",
            "design":     "designer",
            "des":        "designer",
            "todos":      "ambos",
            "tudo":       "ambos",
        }
        cargo = sinonimos.get(cargo, cargo)

        validos = {"designer", "moderador", "ambos", "remover"}
        if cargo not in validos:
            await self.highrise.send_whisper(
                user.id,
                "Cargos válidos: designer | moderador | ambos | remover"
            )
            return

        cargos = _load_cargos()

        if cargo == "remover":
            if target in cargos:
                cargo_antigo = cargos.pop(target)
                _save_cargos(cargos)
                await self.highrise.chat(f"🗑️ Cargo de {cargo_antigo.title()} removido de @{target}.")
            else:
                await self.highrise.send_whisper(user.id, f"@{target} não tem cargo atribuído.")
            return

        cargos[target] = cargo
        _save_cargos(cargos)

        emoji  = {"designer": "🎨", "moderador": "🛡️", "ambos": "👑"}.get(cargo, "⭐")
        titulo = {
            "designer":  "Designer da Sala",
            "moderador": "Moderador(a) da Sala",
            "ambos":     "Designer & Moderador(a)",
        }.get(cargo, cargo.title())

        await self.highrise.chat(f"{emoji} @{target} agora é {titulo}! Bem-vindo(a) à equipe! 🎉")

    async def _cmd_ver_cargos(self, user, whisper: bool = False) -> None:
        """!cargos — mostra a equipe da sala."""
        cargos = _load_cargos()
        extras = {u: "admin" for u in EXTRA_ADMINS if u not in cargos}
        todos  = {**cargos, **extras}

        if not todos:
            msg = "Nenhum cargo atribuído ainda. Use !cargo @usuario <cargo> para definir."
            await self.highrise.send_whisper(user.id, msg)
            return

        emoji_map = {
            "designer":  "🎨",
            "moderador": "🛡️",
            "ambos":     "👑",
            "admin":     "⭐",
        }
        titulo_map = {
            "designer":  "Designer",
            "moderador": "Moderador(a)",
            "ambos":     "Designer & Mod",
            "admin":     "Admin",
        }

        if whisper:
            lines = [f"@{u}: {emoji_map.get(c,'⭐')} {titulo_map.get(c, c.title())}"
                     for u, c in todos.items()]
            chunk = ""
            for l in lines:
                if len(chunk) + len(l) + 3 > 245:
                    await self.highrise.send_whisper(user.id, chunk.rstrip(" | "))
                    chunk = ""
                    await asyncio.sleep(0.1)
                chunk += l + " | "
            if chunk:
                await self.highrise.send_whisper(user.id, "👥 Equipe: " + chunk.rstrip(" | "))
        else:
            lines = [f"{emoji_map.get(c,'⭐')} @{u} ({titulo_map.get(c, c.title())})"
                     for u, c in todos.items()]
            await self.highrise.chat("👥 Equipe da sala: " + "  •  ".join(lines)[:220])

    async def _cmd_ler_codigo(self, user: User) -> None:
        """Envia partes do código atual via sussurro ao dono."""
        codigo = _read_own_code()
        if not codigo:
            await self.highrise.send_whisper(user.id, "❌ Não consegui ler o código.")
            return
        linhas = codigo.split("\n")
        total  = len(linhas)
        await self.highrise.send_whisper(
            user.id, f"📄 Código atual: {total} linhas. Enviando as primeiras 50..."
        )
        chunk = ""
        for i, linha in enumerate(linhas[:50]):
            part = f"{i+1}: {linha}\n"
            if len(chunk) + len(part) > 200:
                await self.highrise.send_whisper(user.id, chunk)
                chunk = ""
                await asyncio.sleep(0.15)
            chunk += part
        if chunk:
            await self.highrise.send_whisper(user.id, chunk)
        await self.highrise.send_whisper(
            user.id, f"📄 Total: {total} linhas. Use @update <pedido> para modificar."
        )

    async def _cmd_lista_funcoes(self, user: User) -> None:
        """Lista as principais funções e comandos secretos do bot para o dono."""
        seccoes = [
            "=== COMANDOS SECRETOS (sussurro @) ===",
            "@update <pedido>  → auto-atualiza o código via IA (patches cirúrgicos)",
            "@testar <pedido>  → simula o update sem aplicar (dry-run seguro)",
            "@restore          → desfaz a última atualização (restaura main.py.bak)",
            "@jeff <pergunta>  → resposta privada da IA",
            "@lercodigo        → envia as primeiras linhas do código",
            "@funcoes          → esta lista",
            "@roupa <cat> <id> → troca roupa direto",
            "@muda <parte>     → inicia fluxo interativo de roupa",
            "=== FUNÇÕES INTERNAS ===",
            "_cmd_auto_update(dry_run) — patches IA + backup + compile + restart",
            "_cmd_restore — restaura main.py.bak e reinicia",
            "_apply_patches — aplica blocos PATCH/INSERT da IA",
            "_safe_write_code — compile() + backup + grava",
            "_read_own_code — lê main.py completo (sem truncar)",
            "_jeffao_responde — IA com personalidade e emotes de emoção",
            "handle_outfit_command / _change_category — roupas",
            "cmd_jokenpo / cmd_dado / cmd_moeda / cmd_8ball — jogos",
            "cmd_kick / cmd_punir / cmd_inativo / cmd_xd — moderação",
            "handle_teleport_command / teleport_to_user — teleporte",
            "is_user_allowed — verificação de permissão ADM",
        ]
        for s in seccoes:
            await self.highrise.send_whisper(user.id, s)
            await asyncio.sleep(0.12)

    async def _cmd_roupa_whisper(self, user: User, cat: str, iid: str) -> None:
        """Troca roupa pelo sussurro do dono."""
        prefixes = self._category_prefixes(cat)
        if not prefixes:
            await self.highrise.send_whisper(
                user.id, f"Categoria '{cat}' não encontrada."
            )
            return
        await self._change_category(user, cat, prefixes, iid)

    async def _cmd_muda_parte(self, user: User, parte: str) -> None:
        parte_map = {
            "cor do olho": "olho",  "olho": "olho", "olhos": "olhos",
            "skin": "skin",         "pele": "pele",
            "cabelo da frente": "cabelo da frente",
            "cabelo de frente": "cabelo da frente",
            "cabelo frontal":   "cabelo da frente",
            "cabelo de tras":   "cabelo de tras",
            "cabelo de trás":   "cabelo de trás",
            "cabelo atrás":     "cabelo de trás",
            "cabelo traseiro":  "cabelo traseiro",
            "camisa": "camisa",  "calça": "calça",  "sapato": "sapato",
            "acessorio": "acessorio", "acessório": "acessório",
        }
        cat_real = parte_map.get(parte, parte)
        prefixes = self._category_prefixes(cat_real)
        if not prefixes:
            await self.highrise.send_whisper(
                user.id,
                f"Não reconheci a parte '{parte}'."
            )
            return
        self._pending_outfit[user.id] = {"cat": cat_real, "prefixes": prefixes}
        await self.highrise.send_whisper(
            user.id,
            f"Ok! Me manda o ID do item para '{cat_real}' (ex: {prefixes[0]}abc123)."
        )

    # ------------------------------------------------------------------
    # RESOLVE EMOTE
    # ------------------------------------------------------------------

    def _resolve_emote(self, text: str, emote_aliases: dict) -> str | None:
        if text in emote_mapping:
            return text
        if text in emote_aliases:
            val = emote_aliases[text]
            if val.isdigit():
                n = int(val)
                if 1 <= n <= TOTAL_EMOTES:
                    return EMOTES_LIST[n - 1][1]
            if val in emote_mapping:
                return val
        for prefix in ("emote-", "dance-", "emoji-", "idle-", "sit-", "idle_"):
            candidate = prefix + text
            if candidate in emote_mapping:
                return candidate
        return None

    # ------------------------------------------------------------------
    # EMOTE POR NÚMERO
    # ------------------------------------------------------------------

    async def handle_emote_number(self, user: User, emote_num: int) -> None:
        if emote_num in BLOCKED_EMOTE_NUMS:
            sub = BLOCKED_EMOTE_NUMS[emote_num]
            if sub is not None and 1 <= sub <= TOTAL_EMOTES:
                await self.highrise.send_whisper(
                    user.id, f"Emote {emote_num} bloqueado. Usando substituto {sub}."
                )
                emote_num = sub
            else:
                await self.highrise.send_whisper(user.id, f"Emote {emote_num} está bloqueado.")
                return

        if 1 <= emote_num <= TOTAL_EMOTES:
            emote_id = EMOTES_LIST[emote_num - 1][1]
            if user.id in self.user_emote_loops and self.user_emote_loops[user.id] == emote_id:
                await self.stop_emote_loop(user.id)
            else:
                await self.start_emote_loop(user.id, emote_id)

    # ------------------------------------------------------------------
    # EMOTE PARA @USUÁRIO
    # ------------------------------------------------------------------

    async def _handle_emote_at_user(
        self, user: User, message: str, emote_aliases: dict, is_adm: bool
    ) -> None:
        parts = message.split("@", 1)
        if len(parts) < 2:
            return
        emote_part      = parts[0].strip().lower()
        target_username = parts[1].strip()
        if not target_username:
            return

        response   = await self.highrise.get_room_users()
        users_list = [ru for ru, _ in response.content]
        target     = next(
            (u for u in users_list if u.username.lower() == target_username.lower()), None
        )
        if not target:
            return

        if emote_part in ("dança", "danca"):
            await self.start_random_emote_loop(target.id)
            return

        if emote_part in ("stop", "dur", "0", "parar") and is_adm:
            await self.stop_emote_loop(target.id)
            return

        if emote_part.isdigit():
            num = int(emote_part)
            if num in BLOCKED_EMOTE_NUMS:
                sub = BLOCKED_EMOTE_NUMS[num]
                if sub and 1 <= sub <= TOTAL_EMOTES:
                    num = sub
                else:
                    return
            if 1 <= num <= TOTAL_EMOTES:
                emote_id = EMOTES_LIST[num - 1][1]
                await self.start_emote_loop(target.id, emote_id)
            return

        resolved = self._resolve_emote(emote_part, emote_aliases)
        if resolved:
            await self.start_emote_loop(target.id, resolved)

    # ------------------------------------------------------------------
    # SISTEMA DE EMOTE (loops)
    # ------------------------------------------------------------------

    async def start_emote_loop(self, user_id: str, emote_name: str) -> None:
        if emote_name not in emote_mapping:
            return

        now  = time.monotonic()
        last = self.user_emote_last_change.get(user_id, 0)
        if now - last < self.EMOTE_SWITCH_COOLDOWN:
            return

        old = self.user_emote_tasks.get(user_id)
        if old and not old.done():
            old.cancel()
            try:
                await old
            except (asyncio.CancelledError, Exception):
                pass

        self.user_emote_loops[user_id]      = emote_name
        self.user_emote_last_change[user_id] = now
        task = asyncio.create_task(self._emote_loop_runner(user_id, emote_name))
        self.user_emote_tasks[user_id] = task

    async def _emote_loop_runner(self, user_id: str, emote_name: str) -> None:
        info          = emote_mapping[emote_name]
        emote_to_send = info["value"]
        emote_time    = info["time"]
        is_idle_pose  = emote_to_send.startswith(("idle-", "idle_", "sit-"))

        # Para idles/sits (animações cíclicas): pre-envia 0.3s antes do fim
        # para o próximo ciclo iniciar sem lacuna.
        # Para emotes regulares e danças: usa o tempo exato do arquivo sem
        # nenhuma margem adicional — o valor no emotes.py é a fonte de verdade.
        if is_idle_pose:
            base_sleep = max(0.3, emote_time - 0.3)
        else:
            base_sleep = emote_time

        try:
            while self.user_emote_loops.get(user_id) == emote_name:
                t0 = time.monotonic()
                try:
                    await self.highrise.send_emote(emote_to_send, user_id)
                except Exception as e:
                    err = str(e).lower()
                    if ("not in room" in err or "invalid" in err
                            or "not found" in err or "unknown" in err):
                        break
                # Desconta o tempo gasto na chamada de rede para que
                # o ciclo total seja exatamente base_sleep (sem acúmulo de atraso)
                elapsed      = time.monotonic() - t0
                actual_sleep = max(0.1, base_sleep - elapsed)
                await asyncio.sleep(actual_sleep)
        except asyncio.CancelledError:
            pass

    async def stop_emote_loop(self, user_id: str) -> None:
        self.user_emote_loops.pop(user_id, None)
        task = self.user_emote_tasks.pop(user_id, None)
        self.user_emote_last_change.pop(user_id, None)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass

    async def start_random_emote_loop(self, user_id: str) -> None:
        old = self.user_emote_tasks.get(user_id)
        if old and not old.done():
            old.cancel()
            try:
                await old
            except (asyncio.CancelledError, Exception):
                pass
        self.user_emote_loops[user_id] = "dança"
        task = asyncio.create_task(self._random_emote_loop_runner(user_id))
        self.user_emote_tasks[user_id] = task

    async def _random_emote_loop_runner(self, user_id: str) -> None:
        try:
            while self.user_emote_loops.get(user_id) == "dança":
                emote_id = random.choice(list(secili_emote.keys()))
                info     = secili_emote[emote_id]
                is_idle  = emote_id.startswith(("idle-", "idle_", "sit-"))
                if is_idle:
                    base_sleep = max(0.3, info["time"] - 0.3)
                else:
                    base_sleep = info["time"]

                t0 = time.monotonic()
                try:
                    await self.highrise.send_emote(emote_id, user_id)
                except Exception as e:
                    if "not in room" in str(e).lower():
                        break
                elapsed = time.monotonic() - t0
                await asyncio.sleep(max(0.1, base_sleep - elapsed))
        except asyncio.CancelledError:
            pass

    async def send_emote_list(self, user: User) -> None:
        try:
            await self.highrise.send_whisper(user.id, "=== LISTA DE EMOTES (número. nome) ===")
            await asyncio.sleep(0.05)
            pieces: list[str] = []
            for idx, em in enumerate(EMOTES_LIST, start=1):
                if idx in BLOCKED_EMOTE_NUMS:
                    continue
                pieces.append(f"{idx}.{em[0]}")
            chunk = ""
            for p in pieces:
                if len(chunk) + len(p) + 3 > 250:
                    await self.highrise.send_whisper(user.id, chunk.rstrip(" | "))
                    chunk = ""
                    await asyncio.sleep(0.1)
                chunk += p + " | "
            if chunk:
                await self.highrise.send_whisper(user.id, chunk.rstrip(" | "))
            await asyncio.sleep(0.1)
            await self.highrise.send_whisper(
                user.id,
                "Dica: digit o número (ex: 24) ou o nome (ex: kiss) no chat. "
                "Ou chama: Jeffão  <pergunta>"
            )
        except Exception as e:
            print(f"[send_emote_list] {e}")

    # ------------------------------------------------------------------
    # SEGUIR
    # ------------------------------------------------------------------

    async def follow(self, target: User) -> None:
        """
        Segue o usuário de forma event-driven: reage ao on_user_move em vez
        de fazer polling pesado de get_room_users(). Resultado: reação
        instantânea ao movimento, sem desperdício de API.
        """
        self.following_user    = target
        self.following_user_id = target.id
        self._follow_move_event.clear()

        # Popula cache inicial caso o usuário ainda não tenha se movido
        if target.id not in self._user_positions:
            try:
                room_users = (await self.highrise.get_room_users()).content
                pos = next((p for u, p in room_users if u.id == target.id), None)
                if pos and isinstance(pos, Position):
                    self._user_positions[target.id] = pos
            except Exception:
                pass

        try:
            while self.following_user_id == target.id:
                # Pausa se o alvo está sendo punido
                if self.is_teleporting_dict.get(target.id, False):
                    await asyncio.sleep(0.3)
                    continue

                pos = self._user_positions.get(target.id)
                if pos:
                    # Fica ao lado (x+1) na mesma altura e facing
                    nearby = Position(pos.x + 1.0, pos.y, pos.z, pos.facing)
                    try:
                        await self.highrise.walk_to(nearby)
                    except Exception:
                        pass

                # Aguarda o próximo on_user_move do alvo
                # Timeout de 5s como rede de segurança (ex.: alvo teleportado)
                self._follow_move_event.clear()
                try:
                    await asyncio.wait_for(
                        self._follow_move_event.wait(), timeout=5.0
                    )
                except asyncio.TimeoutError:
                    pass  # Verifica posição novamente após o timeout

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[follow] Erro: {e}")
        finally:
            self.following_user    = None
            self.following_user_id = None

    async def stop_follow(self) -> None:
        self.following_user    = None
        self.following_user_id = None
        self._follow_move_event.set()  # Desbloqueia o wait() para encerrar limpo
        if self.follow_task:
            self.follow_task.cancel()
            try:
                await self.follow_task
            except asyncio.CancelledError:
                pass
            self.follow_task = None

    async def handle_follow_command(self, user: User, message: str) -> None:
        parts = message.strip().split()
        if len(parts) < 2 or "@" not in message:
            await self.highrise.send_whisper(user.id, "Uso: !seguir @usuario")
            return
        target_name = message.split("@")[-1].strip()
        room_users  = (await self.highrise.get_room_users()).content
        target      = next((u for u, _ in room_users if u.username.lower() == target_name.lower()), None)
        if not target:
            await self.highrise.send_whisper(user.id, f"@{target_name} não está na sala.")
            return
        if self.following_user_id:
            await self.stop_follow()
        self.follow_task = asyncio.create_task(self.follow(target))
        await self.highrise.send_whisper(user.id, f"Seguindo @{target_name}!")

    # ------------------------------------------------------------------
    # MODERAÇÃO
    # ------------------------------------------------------------------

    async def cmd_kick(self, user: User, message: str) -> None:
        try:
            username   = message.split("@")[-1].strip() if "@" in message else message.split()[1]
            room_users = (await self.highrise.get_room_users()).content
            target     = next((u for u, _ in room_users if u.username.lower() == username.lower()), None)
            if not target:
                await self.highrise.send_whisper(user.id, f"@{username} não encontrado.")
                return
            if target.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso usar esse comando no dono do bot.")
                return
            await self.highrise.moderate_room(target.id, "kick")
        except Exception as e:
            print(f"[cmd_kick] {e}")

    async def cmd_punir(self, user: User, message: str) -> None:
        try:
            username   = message.split("@")[-1].strip() if "@" in message else message.split()[1]
            username   = username.lower()
            if username in self.haricler:
                return
            room_users = (await self.highrise.get_room_users()).content
            target     = next((u for u, _ in room_users if u.username.lower() == username), None)
            if not target:
                await self.highrise.send_whisper(user.id, f"@{username} não encontrado.")
                return
            if target.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso punir o dono do bot.")
                return
            if target.id in self.is_teleporting_dict:
                await self.highrise.send_whisper(user.id, f"@{username} já está sendo punido.")
                return
            self.is_teleporting_dict[target.id] = True
            task = asyncio.create_task(self._punish_loop(target))
            self.punish_tasks[target.id] = task
            await self.highrise.chat(f"⚡ @{username} está sendo punido!")
        except Exception as e:
            print(f"[cmd_punir] {e}")

    async def _punish_loop(self, target: User) -> None:
        try:
            while self.is_teleporting_dict.get(target.id, False):
                pos = Position(
                    float(random.randint(0, 25)), 0.0, float(random.randint(0, 25))
                )
                try:
                    await self.highrise.teleport(target.id, pos)
                    await self.highrise.walk_to(Position(pos.x + 1.0, pos.y, pos.z, pos.facing))
                except Exception as e:
                    print(f"[punish] {e}")
                await asyncio.sleep(1.2)
        except asyncio.CancelledError:
            pass
        finally:
            self.is_teleporting_dict.pop(target.id, None)

    async def cmd_inativo(self, user: User, message: str) -> None:
        try:
            username   = message.split("@")[-1].strip() if "@" in message else message.split()[1]
            username   = username.lower()
            room_users = (await self.highrise.get_room_users()).content
            target     = next((u for u, _ in room_users if u.username.lower() == username), None)
            if target:
                self.is_teleporting_dict[target.id] = False
                task = self.punish_tasks.pop(target.id, None)
                if task:
                    task.cancel()
                await self.highrise.chat(f"✅ Punição de @{username} encerrada.")
            else:
                for uid in list(self.is_teleporting_dict.keys()):
                    self.is_teleporting_dict[uid] = False
                await self.highrise.send_whisper(user.id, "Punições encerradas.")
        except Exception as e:
            print(f"[cmd_inativo] {e}")

    async def cmd_xd(self, user: User, message: str) -> None:
        """
        Trava a posição do usuário usando on_user_move (event-driven).
        Toda vez que o alvo tenta se mover, é reteleportado de volta
        instantaneamente — sem polling, resposta em < 1 frame.
        """
        try:
            username = message.split("@")[-1].strip() if "@" in message else message.split()[1]
            # Usa cache de posição se disponível; senão busca uma vez
            room_users = (await self.highrise.get_room_users()).content
            info = next(
                ((u, p) for u, p in room_users if u.username.lower() == username.lower()), None
            )
            if not info:
                await self.highrise.send_whisper(user.id, f"@{username} não encontrado.")
                return
            target_user, initial_pos = info
            if target_user.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso travar a posição do dono do bot.")
                return

            if target_user.id in self._xd_locked_positions:
                # Toggle OFF — libera
                del self._xd_locked_positions[target_user.id]
                # Cancela tasks legadas, se existirem
                for t in self.position_tasks.pop(target_user.id, []):
                    t.cancel()
                await self.highrise.send_whisper(user.id, f"@{username} livre para andar. 🔓")
            else:
                # Toggle ON — trava na posição atual via evento
                pos = self._user_positions.get(target_user.id)
                if pos is None and isinstance(initial_pos, Position):
                    pos = initial_pos
                if pos is None:
                    await self.highrise.send_whisper(user.id, f"Posição de @{username} desconhecida. Peça para ele andar primeiro.")
                    return
                self._xd_locked_positions[target_user.id] = pos
                self._user_positions[target_user.id] = pos
                await self.highrise.send_whisper(user.id, f"@{username} travado! 🔒 (on_user_move)")
        except Exception as e:
            print(f"[cmd_xd] {e}")

    async def _lock_position_loop(self, target: User, pos: Position) -> None:
        """Mantido como fallback legado — o novo sistema usa on_user_move."""
        try:
            while self.position_tasks.get(target.id):
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    async def _arremess_delay(self, user_id: str, destination: "Position", direcao: str) -> None:
        """Aguarda 1s e teleporta o usuário para cima (Y alto) ou para baixo (Y=0)
        mantendo o X/Z do ponto clicado."""
        await asyncio.sleep(1)
        # Verifica se ainda está no modo arremessador (pode ter sido desativado)
        if direcao == "cima" and user_id not in self._arremess_up:
            return
        if direcao == "baixo" and user_id not in self._arremess_down:
            return
        try:
            if direcao == "cima":
                destino = Position(destination.x, 10.0, destination.z)
            else:
                destino = Position(destination.x, 0.0, destination.z)
            await self.highrise.teleport(user_id, destino)
        except Exception as e:
            print(f"[_arremess_delay] {e}")

    async def cmd_arremessar(self, user: User, message: str) -> None:
        """
        !arremessar @usuario cima|baixo — Ativa modo arremessador:
        toda vez que o alvo clica no chão, o bot aguarda 1s e
        teleporta para cima (Y=10) ou baixo (Y=0) naquele X/Z.
        Chame sem direção ou com 'off' para desativar.
        """
        try:
            partes = message.split()
            # partes: ["arremessar", "@usuario", "cima|baixo|off"]
            username = partes[1].lstrip("@") if len(partes) > 1 else ""
            direcao  = partes[2].lower() if len(partes) > 2 else ""

            room_users = (await self.highrise.get_room_users()).content
            target = next((u for u, _ in room_users if u.username.lower() == username.lower()), None)
            if not target:
                await self.highrise.send_whisper(user.id, f"@{username} não encontrado.")
                return
            if target.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso arremessar o dono do bot.")
                return

            # Desativar se já ativo ou se pediu 'off'
            if direcao == "off" or (target.id in self._arremess_up or target.id in self._arremess_down):
                self._arremess_up.discard(target.id)
                self._arremess_down.discard(target.id)
                await self.highrise.send_whisper(user.id, f"Arremessador desativado para @{username}. 🔓")
                return

            if direcao == "cima":
                self._arremess_up.add(target.id)
                await self.highrise.send_whisper(user.id, f"Arremessador CIMA ativado para @{username}! ⬆️ Clique no chão → teleporta pra cima em 1s.")
            elif direcao == "baixo":
                self._arremess_down.add(target.id)
                await self.highrise.send_whisper(user.id, f"Arremessador BAIXO ativado para @{username}! ⬇️ Clique no chão → teleporta pro chão em 1s.")
            else:
                await self.highrise.send_whisper(user.id, "Uso: arremessar @usuario cima  |  arremessar @usuario baixo  |  arremessar @usuario off")
        except Exception as e:
            print(f"[cmd_arremessar] {e}")

    async def cmd_snap(self, user: User, message: str) -> None:
        """
        !snap @usuario — O snap agora é GLOBAL (todos são teleportados ao clicar).
        Este comando funciona como EXCLUSÃO: desativa o snap para um usuário específico
        para que ele possa andar normalmente. Chame de novo para reativar.
        """
        try:
            username = message.split("@")[-1].strip() if "@" in message else message.split()[1]
            room_users = (await self.highrise.get_room_users()).content
            target = next((u for u, _ in room_users if u.username.lower() == username.lower()), None)
            if not target:
                await self.highrise.send_whisper(user.id, f"@{username} não encontrado.")
                return

            if target.id in self._snap_users:
                # Estava excluído → reativa snap global para ele
                self._snap_users.discard(target.id)
                await self.highrise.send_whisper(user.id, f"Snap REATIVADO para @{username}. Teleporte instantâneo ao clicar. ⚡")
            else:
                # Exclui do snap global → anda normalmente
                self._snap_users.add(target.id)
                await self.highrise.send_whisper(user.id, f"Snap DESATIVADO para @{username}. Anda normalmente. 🚶")
        except Exception as e:
            print(f"[cmd_snap] {e}")

    async def cmd_full_rtp(self, user: User) -> None:
        if self.kus.get(user.id, False):
            self.kus[user.id] = False
            await self.highrise.send_whisper(user.id, "Full RTP parado.")
            return
        self.kus[user.id] = True
        asyncio.create_task(self._full_rtp_loop(user))
        await self.highrise.send_whisper(user.id, "Full RTP ativado! Digite 'stop' para parar.")

    async def _full_rtp_loop(self, user: User) -> None:
        try:
            while self.kus.get(user.id, False):
                pos = Position(
                    float(random.randint(0, 25)), float(random.randint(0, 5)),
                    float(random.randint(0, 25)),
                )
                try:
                    await self.highrise.teleport(user.id, pos)
                except Exception:
                    pass
                await asyncio.sleep(0.7)
        except asyncio.CancelledError:
            pass
        finally:
            self.kus[user.id] = False

    async def cmd_all_dance(self, user: User, message: str) -> None:
        try:
            parts = message.strip().split(maxsplit=1)
            if len(parts) < 2:
                await self.highrise.send_whisper(user.id, "Uso: all <numero_do_emote>")
                return
            arg      = parts[1].strip().lower()
            emote_id = None
            if arg.isdigit():
                n = int(arg)
                if 1 <= n <= TOTAL_EMOTES:
                    emote_id = EMOTES_LIST[n - 1][1]
            else:
                resolved = self._resolve_emote(arg, _load_emote_aliases())
                if resolved:
                    emote_id = emote_mapping[resolved]["value"]
            if not emote_id:
                await self.highrise.send_whisper(user.id, f"Emote '{arg}' não encontrado.")
                return
            room_users = (await self.highrise.get_room_users()).content
            await asyncio.gather(
                *(self.highrise.send_emote(emote_id, ru.id) for ru, _ in room_users),
                return_exceptions=True,
            )
        except Exception as e:
            print(f"[cmd_all_dance] {e}")

    async def switch_users(self, user: User, target_username: str) -> None:
        try:
            room_users  = (await self.highrise.get_room_users()).content
            my_pos      = next((p for u, p in room_users if u.id == user.id), None)
            target_info = next(
                ((u, p) for u, p in room_users if u.username.lower() == target_username.lower()), None
            )
            if not my_pos or not target_info:
                await self.highrise.send_whisper(user.id, "Usuário não encontrado.")
                return
            target_user, target_pos = target_info
            if target_user.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso trocar posição com o dono.")
                return
            await asyncio.gather(
                self.highrise.teleport(user.id, target_pos),
                self.highrise.teleport(target_user.id, my_pos),
            )
        except Exception as e:
            print(f"[switch_users] {e}")

    # ------------------------------------------------------------------
    # TELEPORTES
    # ------------------------------------------------------------------

    async def teleport(self, user: User, position: Position) -> None:
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"[teleport] {e}")

    async def handle_teleport_command(self, user: User, message: str) -> None:
        try:
            parts = message.strip().split()
            if len(parts) == 2 and parts[1].lower() in ("cima", "up"):
                room_users = (await self.highrise.get_room_users()).content
                pos = next((p for u, p in room_users if u.id == user.id), None)
                if pos and isinstance(pos, Position):
                    await self.teleport(user, Position(pos.x, pos.y + 2.0, pos.z, pos.facing))
                return
            if len(parts) == 2 and parts[1].lower() in ("baixo", "down"):
                room_users = (await self.highrise.get_room_users()).content
                pos = next((p for u, p in room_users if u.id == user.id), None)
                if pos and isinstance(pos, Position):
                    await self.teleport(user, Position(pos.x, max(0, pos.y - 2.0), pos.z, pos.facing))
                return
            if len(parts) == 2 and parts[1].startswith("@"):
                await self.teleport_to_user(user, parts[1][1:])
                return
            if len(parts) == 4:
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    await self.teleport(user, Position(x, y, z))
                    await self.highrise.send_whisper(user.id, f"Teleportado para ({x:.1f},{y:.1f},{z:.1f})")
                except ValueError:
                    await self.highrise.send_whisper(user.id, "Use: !tp x y z  ou  !tp @usuario")
                return
            if len(parts) == 2:
                nome      = parts[1].lower()
                platforms = _load_platforms()
                if nome in platforms:
                    p = platforms[nome]
                    await self.teleport(user, Position(p["x"], p["y"], p["z"]))
                    return
            await self.highrise.send_whisper(
                user.id, "Uso: !tp x y z | !tp @user | !tp cima | !tp baixo | !tp <plataforma>"
            )
        except Exception as e:
            print(f"[handle_teleport_command] {e}")

    async def teleport_to_user(self, user: User, target_username: str) -> None:
        try:
            room_users = (await self.highrise.get_room_users()).content
            info = next(
                ((u, p) for u, p in room_users if u.username.lower() == target_username.lower()), None
            )
            if not info:
                await self.highrise.send_whisper(user.id, f"@{target_username} não está na sala.")
                return
            _, pos = info
            if isinstance(pos, Position):
                await self.teleport(user, Position(pos.x + 1, pos.y, pos.z, pos.facing))
        except Exception as e:
            print(f"[teleport_to_user] {e}")

    async def cmd_tele_to_me(self, user: User, target_username: str) -> None:
        try:
            room_users = (await self.highrise.get_room_users()).content
            my_pos     = next((p for u, p in room_users if u.id == user.id), None)
            target     = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
            if not target or not my_pos:
                await self.highrise.send_whisper(user.id, f"@{target_username} não encontrado.")
                return
            if target.username in self.PROTECTED_USERS:
                await self.highrise.send_whisper(user.id, "Não posso teleportar o dono do bot.")
                return
            if isinstance(my_pos, Position):
                await self.highrise.teleport(target.id, Position(my_pos.x + 1, my_pos.y, my_pos.z, my_pos.facing))
        except Exception as e:
            print(f"[cmd_tele_to_me] {e}")

    async def adjust_position(self, user: User, message: str) -> None:
        try:
            raw = message.strip().lower()
            if len(raw) < 2:
                return
            sign    = -1 if raw[0] == "-" else 1
            axis    = raw[1]
            val_str = raw[2:].strip() or "1"
            try:
                delta = float(val_str) * sign
            except ValueError:
                return
            room_users = (await self.highrise.get_room_users()).content
            pos = next((p for u, p in room_users if u.id == user.id), None)
            if not pos or not isinstance(pos, Position):
                return
            if axis == "x":
                new_pos = Position(pos.x + delta, pos.y, pos.z, pos.facing)
            elif axis == "y":
                new_pos = Position(pos.x, pos.y + delta, pos.z, pos.facing)
            else:
                new_pos = Position(pos.x, pos.y, pos.z + delta, pos.facing)
            await self.teleport(user, new_pos)
        except Exception as e:
            print(f"[adjust_position] {e}")

    # ------------------------------------------------------------------
    # PLATAFORMAS
    # ------------------------------------------------------------------

    async def handle_platform_command(self, user: User, message: str) -> None:
        try:
            parts     = message.strip().split(maxsplit=2)
            platforms = _load_platforms()
            if len(parts) == 1 or parts[1].lower() in ("lista", "ver"):
                if not platforms:
                    await self.highrise.send_whisper(user.id, "Nenhuma plataforma salva ainda.")
                    return
                lines = [f"{k}: ({v['x']:.1f},{v['y']:.1f},{v['z']:.1f})" for k, v in platforms.items()]
                await self.highrise.send_whisper(user.id, " | ".join(lines))
                return
            sub = parts[1].lower()
            if sub in ("marcar", "add", "salvar") and len(parts) >= 3:
                nome       = parts[2].strip().lower()
                room_users = (await self.highrise.get_room_users()).content
                pos        = next((p for u, p in room_users if u.id == user.id), None)
                if not pos or not isinstance(pos, Position):
                    await self.highrise.send_whisper(user.id, "Posição não encontrada.")
                    return
                platforms[nome] = {"x": pos.x, "y": pos.y, "z": pos.z}
                _save_platforms(platforms)
                await self.highrise.send_whisper(
                    user.id, f"Plataforma '{nome}' salva em ({pos.x:.1f},{pos.y:.1f},{pos.z:.1f})!"
                )
                return
            if sub in ("remover", "del", "deletar") and len(parts) >= 3:
                nome = parts[2].strip().lower()
                if nome in platforms:
                    del platforms[nome]
                    _save_platforms(platforms)
                    await self.highrise.send_whisper(user.id, f"Plataforma '{nome}' removida.")
                else:
                    await self.highrise.send_whisper(user.id, f"Plataforma '{nome}' não encontrada.")
                return
            nome = sub
            if nome in platforms:
                p = platforms[nome]
                await self.teleport(user, Position(p["x"], p["y"], p["z"]))
            else:
                await self.highrise.send_whisper(
                    user.id,
                    "Uso: !plataforma lista | !plataforma marcar <nome> | "
                    "!plataforma <nome> | !plataforma remover <nome>"
                )
        except Exception as e:
            print(f"[handle_platform_command] {e}")

    # ------------------------------------------------------------------
    # JOGOS
    # ------------------------------------------------------------------

    async def cmd_jokenpo(self, user: User, message: str) -> None:
        try:
            parts    = message.strip().split()
            opcoes   = ["pedra", "papel", "tesoura"]
            simbolos = {"pedra": "🪨", "papel": "📄", "tesoura": "✂️"}
            ganha_de = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}
            escolha  = next((p.lower() for p in parts[1:] if p.lstrip("@").lower() in opcoes), None)
            if not escolha:
                await self.highrise.chat(f"@{user.username} use: !jokenpo pedra | papel | tesoura")
                return
            bot_choice = random.choice(opcoes)
            if escolha == bot_choice:
                resultado_txt  = "Empate! 🤝"
                resultado_stat = "empate"
            elif ganha_de[escolha] == bot_choice:
                resultado_txt  = f"@{user.username} ganhou! 🎉🏆"
                resultado_stat = "vitoria"
            else:
                resultado_txt  = "Jeffão ganhou! 🤖💪"
                resultado_stat = "derrota"
            _register_jokenpo_result(user.username, resultado_stat)
            await self.highrise.chat(
                f"🎮 Jokenpô! {user.username}: {simbolos[escolha]} vs Jeffão: "
                f"{simbolos[bot_choice]} — {resultado_txt}"
            )
            emote = "celebrate" if resultado_stat == "derrota" else ("sad" if resultado_stat == "vitoria" else "wave")
            await self._bot_emote(emote)
        except Exception as e:
            print(f"[cmd_jokenpo] {e}")

    async def cmd_placar_top(self, user: User) -> None:
        try:
            placar  = _load_placar()
            if not placar:
                await self.highrise.chat("🏆 Nenhuma partida registrada ainda. Jogue !jokenpo!")
                return
            ranking = sorted(placar.items(), key=lambda x: x[1].get("vitorias", 0), reverse=True)
            linhas  = ["🏆 TOP JOKENPÔ 🏆"]
            for i, (username, stats) in enumerate(ranking[:5], 1):
                v = stats.get("vitorias", 0)
                d = stats.get("derrotas", 0)
                e = stats.get("empates", 0)
                linhas.append(f"#{i} {username}: {v}V {d}D {e}E")
            await self.highrise.chat(" | ".join(linhas))
        except Exception as e:
            print(f"[cmd_placar_top] {e}")

    async def cmd_meu_placar(self, user: User) -> None:
        try:
            placar = _load_placar()
            stats  = placar.get(user.username, {"vitorias": 0, "derrotas": 0, "empates": 0})
            v      = stats.get("vitorias", 0)
            d      = stats.get("derrotas", 0)
            e      = stats.get("empates", 0)
            total  = v + d + e
            taxa   = f"{round(v/total*100)}%" if total > 0 else "0%"
            await self.highrise.send_whisper(
                user.id,
                f"🎮 Seu placar: {v}V | {d}D | {e}E | {total} Partidas | Taxa: {taxa}"
            )
        except Exception as e:
            print(f"[cmd_meu_placar] {e}")

    async def cmd_dado(self, user: User) -> None:
        resultado = random.randint(1, 6)
        faces     = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        await self.highrise.chat(f"🎲 @{user.username} tirou {faces[resultado-1]} ({resultado})!")

    async def cmd_moeda(self, user: User) -> None:
        resultado = random.choice(["Cara 🪙", "Coroa 👑"])
        await self.highrise.chat(f"@{user.username} jogou a moeda: {resultado}!")

    async def cmd_8ball(self, user: User, message: str) -> None:
        respostas = [
            "Sim! ✅", "Não! ❌", "Talvez... 🤔", "Com certeza! 💯",
            "Jamais! 🚫", "As estrelas dizem sim ⭐", "Muito improvável 😬",
            "Pergunte mais tarde 🔮", "Definitivamente sim! 🎉",
            "Não conte com isso 😅", "Pode apostar que sim! 🔥",
            "Minha resposta é não 🙅", "Sinais apontam que sim 👍",
        ]
        await self.highrise.chat(f"🎱 @{user.username}: {random.choice(respostas)}")

    async def cmd_sorteio(self, user: User) -> None:
        room_users = (await self.highrise.get_room_users()).content
        users_list = [u for u, _ in room_users]
        if not users_list:
            return
        sorteado = random.choice(users_list)
        await self.highrise.chat(f"🎉 Sorteio! O vencedor é @{sorteado.username}! 🏆 Parabéns!")
        await self._bot_emote("celebrate")

    async def handle_match_command(self, user: User) -> None:
        try:
            room_users = (await self.highrise.get_room_users()).content
            users_list = [u for u, _ in room_users]
            if len(users_list) < 2:
                await self.highrise.chat("Precisa de pelo menos 2 pessoas na sala! 💔")
                return
            u1 = random.choice(users_list)
            u2 = random.choice([u for u in users_list if u.id != u1.id])
            await self.highrise.chat(
                f"💕 CASAL DO MOMENTO: @{u1.username} + @{u2.username} 💘❤️"
            )
            await asyncio.gather(
                self.highrise.send_emote("emote-kiss", u1.id),
                self.highrise.send_emote("emote-kiss", u2.id),
                return_exceptions=True,
            )
            await self._bot_emote("love")
        except Exception as e:
            print(f"[handle_match_command] {e}")

    # ------------------------------------------------------------------
    # USER INFO
    # ------------------------------------------------------------------

    async def cmd_userinfo(self, user: User, target_username: str) -> None:
        target_username = target_username.split()[0].strip().lstrip("@")
        if not target_username:
            await self.highrise.send_whisper(user.id, "Uso: info @usuario")
            return
        try:
            resp = await asyncio.wait_for(
                self.webapi.get_users(username=target_username, limit=1), timeout=10.0
            )
            if not resp or not resp.users:
                await self.highrise.send_whisper(user.id, f"Usuário '{target_username}' não encontrado.")
                return
            uid  = resp.users[0].user_id
            data = await asyncio.wait_for(self.webapi.get_user(uid), timeout=10.0)
            u    = data.user
            try:
                days     = (datetime.now().date() - u.joined_at.date()).days
                days_txt = f"{days} dias"
            except Exception:
                days_txt = "N/A"
            followers = getattr(u, "num_followers", "?")
            friends   = getattr(u, "num_friends", "?")
            country   = getattr(u, "country_code", None) or "N/A"
            await self.highrise.chat(
                f"📋 @{target_username} | 👥 Seguidores: {followers} | "
                f"💕 Amigos: {friends} | 📅 {days_txt} | 🌍 {country}"
            )
        except asyncio.TimeoutError:
            await self.highrise.send_whisper(user.id, f"Timeout buscando '{target_username}'.")
        except Exception as e:
            print(f"[cmd_userinfo] {e}")
            await self.highrise.send_whisper(user.id, f"Erro ao buscar '{target_username}'.")

    # ------------------------------------------------------------------
    # ROUPA
    # ------------------------------------------------------------------

    def _category_prefixes(self, cat: str) -> list[str] | None:
        return self.OUTFIT_CATEGORIES.get(cat.strip().lower())

    async def handle_outfit_command(self, user: User, message: str) -> None:
        try:
            parts = message.strip().split(maxsplit=2)
            if len(parts) < 2 or parts[1].lower() in ("ajuda", "help"):
                await self.highrise.send_whisper(
                    user.id,
                    "Roupa: !roupa atual | !roupa <categoria> <id> | "
                    "!roupa remover <categoria> | !roupa limpar acessorios | "
                    "Categorias: camisa calça sapato corpo cabelo frontal cabelo de tras olho aura acessorio extra"
                )
                return
            sub = parts[1].lower()
            if sub in ("atual", "ver", "lista"):
                await self._send_current_outfit(user)
                return
            if sub in ("limpar", "clear"):
                rest = parts[2].lower() if len(parts) >= 3 else ""
                if "acessorio" in rest or "acessório" in rest:
                    await self._clear_accessories(user)
                    return
            if sub in ("remover", "tirar", "remove") and len(parts) >= 3:
                prefixes = self._category_prefixes(parts[2])
                if prefixes:
                    await self._remove_category(user, prefixes)
                else:
                    await self.highrise.send_whisper(user.id, f"Categoria inválida: {parts[2]}")
                return
            prefixes = self._category_prefixes(sub)
            if not prefixes:
                await self.highrise.send_whisper(user.id, f"Categoria '{sub}' inválida. Use !roupa ajuda")
                return
            if len(parts) < 3:
                await self.highrise.send_whisper(user.id, f"Faltou o ID. Ex: !roupa {sub} {prefixes[0]}id")
                return
            await self._change_category(user, sub, prefixes, parts[2].strip())
        except Exception as e:
            print(f"[handle_outfit_command] {e}")
            await self.highrise.send_whisper(user.id, f"Erro na roupa: {e}")

    async def _send_current_outfit(self, user: User) -> None:
        try:
            resp    = await self.highrise.get_my_outfit()
            items   = list(getattr(resp, "outfit", None) or [])
            if not items:
                await self.highrise.send_whisper(user.id, "Outfit vazio.")
                return
            aliases     = _load_aliases()
            id_to_alias = {v: k for k, v in aliases.items()}
            shown: set  = set()
            await self.highrise.send_whisper(user.id, f"== Outfit do bot ({len(items)} peças) ==")
            for label, prefixes in self.OUTFIT_DISPLAY_ORDER:
                for it in [i for i in items if any(i.id.startswith(p) for p in prefixes)]:
                    shown.add(it.id)
                    ap    = id_to_alias.get(it.id, "")
                    extra = f" [{ap}]" if ap else ""
                    await self.highrise.send_whisper(user.id, f"{label}: {it.id}{extra}")
                    await asyncio.sleep(0.1)
            for it in [i for i in items if i.id not in shown]:
                await self.highrise.send_whisper(user.id, f"Outro: {it.id}")
            await self.highrise.send_whisper(user.id, "Use !roupa <categoria> <id> para trocar.")
        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Erro ao ler outfit: {e}")

    async def _change_category(
        self, user: User, category: str, prefixes: list[str], new_id: str
    ) -> None:
        """Troca uma peça do outfit com correção do bug do cabelo."""
        aliases = _load_aliases()
        if new_id.lower() in aliases:
            new_id = aliases[new_id.lower()]

        is_acc = "acessorio" in category or "acessório" in category

        if not any(new_id.startswith(p) for p in prefixes):
            await self.highrise.send_whisper(
                user.id,
                f"ID '{new_id}' inválido para '{category}'. "
                f"Deve começar com: {', '.join(prefixes[:3])}"
            )
            return

        resp    = await self.highrise.get_my_outfit()
        current = list(getattr(resp, "outfit", None) or [])

        if is_acc:
            base       = new_id.split("-")[0] + "-"
            new_outfit = [it for it in current if not it.id.startswith(base)]
        else:
            specific_prefix = next((p for p in prefixes if new_id.startswith(p)), None)
            if specific_prefix and len(prefixes) > 1:
                new_outfit = [it for it in current if not it.id.startswith(specific_prefix)]
            else:
                new_outfit = [it for it in current if not any(it.id.startswith(p) for p in prefixes)]

        new_outfit.append(
            Item(type="clothing", amount=1, id=new_id, account_bound=False, active_palette=0)
        )
        result = await self.highrise.set_outfit(new_outfit)
        if isinstance(result, Error):
            await self.highrise.send_whisper(user.id, f"Falhou: {result.message}")
        else:
            await self.highrise.send_whisper(user.id, f"✅ {category} → {new_id}")

    async def _remove_category(self, user: User, prefixes: list[str]) -> None:
        resp       = await self.highrise.get_my_outfit()
        current    = list(getattr(resp, "outfit", None) or [])
        new_outfit = [it for it in current if not any(it.id.startswith(p) for p in prefixes)]
        if len(new_outfit) == len(current):
            await self.highrise.send_whisper(user.id, "Nada a remover nessa categoria.")
            return
        result = await self.highrise.set_outfit(new_outfit)
        if isinstance(result, Error):
            await self.highrise.send_whisper(user.id, f"Falhou: {result.message}")
        else:
            await self.highrise.send_whisper(user.id, "Removido com sucesso. ✅")

    async def _clear_accessories(self, user: User) -> None:
        resp       = await self.highrise.get_my_outfit()
        current    = list(getattr(resp, "outfit", None) or [])
        new_outfit = [it for it in current if not any(it.id.startswith(p) for p in self.ACCESSORY_PREFIXES)]
        result     = await self.highrise.set_outfit(new_outfit)
        if isinstance(result, Error):
            await self.highrise.send_whisper(user.id, f"Falhou: {result.message}")
        else:
            await self.highrise.send_whisper(user.id, "Acessórios removidos. ✅")

    async def _equip_detected_ids(
        self, user: User, ids: list[str], silent: bool = False
    ) -> list[str]:
        """Equipa uma lista de IDs de itens do Highrise."""
        aliases      = _load_aliases()
        resolved_ids = [aliases.get(i.lower(), i) for i in ids]

        resp    = await self.highrise.get_my_outfit()
        current = list(getattr(resp, "outfit", None) or [])
        new_outfit = list(current)

        applied: list[str] = []
        for item_id in resolved_ids:
            prefix_str = item_id.split("-")[0] + "-"
            new_outfit = [it for it in new_outfit if not it.id.startswith(prefix_str)]
            new_outfit.append(
                Item(type="clothing", amount=1, id=item_id, account_bound=False, active_palette=0)
            )
            applied.append(item_id)

        result = await self.highrise.set_outfit(new_outfit)
        if isinstance(result, Error):
            if not silent:
                await self.highrise.send_whisper(user.id, f"❌ Falhou ao vestir: {result.message}")
            return []

        if not silent:
            if len(applied) == 1:
                await self.highrise.send_whisper(user.id, f"✅ Vesti: {applied[0]}")
            else:
                preview = ", ".join(applied[:3]) + ("…" if len(applied) > 3 else "")
                await self.highrise.send_whisper(user.id, f"✅ Vesti {len(applied)} itens: {preview}")
        return applied

    async def cmd_olhos(self, user: User, color: str) -> None:
        aliases = _load_aliases()
        if color not in aliases:
            await self.highrise.send_whisper(
                user.id, f"Apelido '{color}' não encontrado. Cadastre com !apelido add {color} <id>"
            )
            return
        prefixes = self._category_prefixes("olho") or []
        await self._change_category(user, "olho", prefixes, aliases[color])

    # ------------------------------------------------------------------
    # APELIDOS
    # ------------------------------------------------------------------

    async def handle_alias_command(self, user: User, message: str) -> None:
        try:
            parts = message.strip().split(maxsplit=3)
            if len(parts) < 2 or parts[1].lower() in ("ajuda", "help"):
                await self.highrise.send_whisper(
                    user.id,
                    "Apelidos: !apelido lista | !apelido add <nome> <id_ou_emote> | !apelido remover <nome>"
                )
                return
            sub       = parts[1].lower()
            outfit_al = _load_aliases()
            emote_al  = _load_emote_aliases()
            if sub in ("lista", "ver"):
                if not outfit_al and not emote_al:
                    await self.highrise.send_whisper(user.id, "Nenhum apelido cadastrado.")
                    return
                if outfit_al:
                    await self.highrise.send_whisper(user.id, "== Roupa ==")
                    for k, v in outfit_al.items():
                        await self.highrise.send_whisper(user.id, f"{k} → {v}")
                        await asyncio.sleep(0.05)
                if emote_al:
                    await self.highrise.send_whisper(user.id, "== Emote ==")
                    for k, v in emote_al.items():
                        await self.highrise.send_whisper(user.id, f"{k} → {v}")
                        await asyncio.sleep(0.05)
                return
            if sub in ("add", "adicionar") and len(parts) >= 4:
                nome    = parts[2].strip().lower()
                item_id = parts[3].strip()
                is_emote = (
                    item_id.startswith(("emote-", "dance-", "idle-", "emoji-", "sit-"))
                    or item_id in emote_mapping
                    or item_id.isdigit()
                )
                if is_emote:
                    emote_al[nome] = item_id
                    _save_emote_aliases(emote_al)
                    await self.highrise.send_whisper(user.id, f"Apelido de emote '{nome}' = {item_id} ✅")
                else:
                    outfit_al[nome] = item_id
                    _save_aliases(outfit_al)
                    await self.highrise.send_whisper(user.id, f"Apelido de roupa '{nome}' = {item_id} ✅")
                return
            if sub in ("remover", "del") and len(parts) >= 3:
                nome    = parts[2].strip().lower()
                removed = False
                if nome in outfit_al:
                    del outfit_al[nome]
                    _save_aliases(outfit_al)
                    removed = True
                if nome in emote_al:
                    del emote_al[nome]
                    _save_emote_aliases(emote_al)
                    removed = True
                msg_r = f"Apelido '{nome}' removido." if removed else f"Apelido '{nome}' não encontrado."
                await self.highrise.send_whisper(user.id, msg_r)
                return
            await self.highrise.send_whisper(user.id, "Use !apelido ajuda")
        except Exception as e:
            print(f"[handle_alias_command] {e}")

    # ------------------------------------------------------------------
    # PERMISSÕES
    # ------------------------------------------------------------------

    async def is_user_allowed(self, user: User) -> bool:
        if user.username in self.PROTECTED_USERS:
            return True
        if user.username in EXTRA_ADMINS:
            return True
        cargos = _load_cargos()
        if user.username in cargos:
            return True
        try:
            priv = await self.highrise.get_room_privilege(user.id)
            return bool(priv.moderator)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # LISTAS DE COMANDOS
    # ------------------------------------------------------------------

    async def _send_user_commands(self, user: User) -> None:
        blocos = [
            (
                "🤖 JEFFÃO — IA",
                "Jeffão <frase> = chamar ou fazer pergunta  |  "
                "!assistente <pergunta> = Jeffão responde  |  "
                "Jeffão pode volta pra seu lugar = retorna ao spawn"
            ),
            (
                "💃 EMOTES",
                "1 a 220 = emote pelo número  |  dança = emote aleatório  |  "
                "stop = parar  |  45 @user = emote em outro usuário  |  "
                "!lista = ver todos os emotes"
            ),
            (
                "🎮 JOGOS",
                "!jokenpo pedra/papel/tesoura  |  !placar = ranking  |  "
                "!meu placar = seus stats  |  !dado  |  !moeda  |  "
                "!8ball <pergunta>  |  !sorteio  |  !match = casal aleatório"
            ),
            (
                "📍 POSIÇÃO & INFO",
                "+x5 / -y3 / +z10 = ajusta posição  |  "
                "!tp x y z = teleporta  |  !tp @user = vai ao usuário  |  "
                "vip2 vip3 vip4 vip5 = locais da sala (vip1 só ADMs)  |  "
                "info @user = perfil do usuário  |  !cargos = equipe da sala"
            ),
        ]
        await self.highrise.send_whisper(user.id, "╔══ COMANDOS DO JEFFÃO ══╗")
        await asyncio.sleep(0.05)
        for titulo, texto in blocos:
            await self.highrise.send_whisper(user.id, f"{titulo}: {texto}")
            await asyncio.sleep(0.08)
        await self.highrise.send_whisper(user.id, "ADMs: !admlista  |  Dono: sussurre @funcoes")

    async def _send_admin_list(self, user: User) -> None:
        blocos = [
            (
                "🚶 SEGUIR",
                "vamos / !vamos = bot segue você  |  pare = parar  |  "
                "!seguir @user = seguir outro usuário  |  "
                "tele @user = vai até o usuário  |  switch @user = trocar de lugar"
            ),
            (
                "⚡ MODERAÇÃO",
                "kick @user = expulsar  |  punir @user = teleporte infinito  |  "
                "inativo @user = encerrar punição  |  xd @user = travar posição  |  "
                "T @user = trazer para perto  |  full rtp = tp aleatório contínuo"
            ),
            (
                "💰 GOLD & CARGO",
                "!reembolso @user <valor> = devolve Gold pelas denominações exatas do HR  |  "
                "!cargo @user designer|moderador|ambos|remover  |  !cargo lista"
            ),
            (
                "👕 ROUPA & APELIDOS",
                "!roupa atual = ver outfit  |  !roupa <cat> <id> = vestir  |  "
                "!roupa remover <cat>  |  !roupa limpar acessorios  |  "
                "!apelido add/lista/remover  |  !olhos <apelido>"
            ),
            (
                "📍 EMOTES & POSIÇÃO",
                "all <num> = todos dançam  |  +x5 -y3 +z10 = ajustar posição  |  "
                "!tp x y z / !tp @user / !tp cima / !tp baixo  |  "
                "!plataforma marcar/lista/remover/<nome>  |  vip1 = VIP exclusivo"
            ),
            (
                "💬 OUTROS",
                "@mensagem no sussurro = fala no chat público  |  "
                "!admlista = este menu  |  @funcoes (sussurro) = comandos secretos do dono"
            ),
        ]
        await self.highrise.send_whisper(user.id, "╔══ COMANDOS ADM ══╗")
        await asyncio.sleep(0.05)
        for titulo, texto in blocos:
            await self.highrise.send_whisper(user.id, f"{titulo}: {texto}")
            await asyncio.sleep(0.08)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                  CONFIGURAÇÃO DO BOT                            ║
# ║  ► Edite aqui o token, room_id, dono e apelidos do bot          ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║  room_id        → ID da sala no Highrise                        ║
# ║  bot_token      → Token do bot (gere em https://highrise.game)  ║
# ║  OWNER          → Username do dono (em PROTECTED_USERS)         ║
# ║  JEFFAO_TRIGGERS → Nomes que ativam o bot (1 espaço depois)    ║
# ╚══════════════════════════════════════════════════════════════════╝

# ──────────────────────────────────────────────────────────────────
# ► LISTA DE ADMs EXTRAS — usuários com poderes de ADM mesmo sem
#   ser moderador da sala. Edite aqui e reinicie.
# ──────────────────────────────────────────────────────────────────
EXTRA_ADMINS: list[str] = [
    # "NomeDoUsuario1",
    # "NomeDoUsuario2",
]

# ──────────────────────────────────────────────────────────────────
# ► APELIDOS DE ATIVAÇÃO — como chamar o bot no chat
# ──────────────────────────────────────────────────────────────────
JEFFAO_TRIGGERS = [
    "jeffão",
    "jeffao",
    "jeffãoo",
    "jeffaoo",
    "jeff",
    "jefão",
    "jefao",
    "jef",
    "assistente",
    "bot",
]

class RunBot:
    # ──────────────────────────────────────────────────────────────
    # ► EDITE AQUI ◄
    room_id   = "0c98124c5dda50294e11ded0cd7df6d2082f31bcdb363d173e89f1ee30f3cbc5"
    bot_token = "0796f65b7f49c818055204db3cd559397a2e89686ce48879b911269502dbc58a"
    # ──────────────────────────────────────────────────────────────
    bot_file  = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id,
                self.bot_token,
            )
        ]

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception:
                traceback.print_exc()
                print("Reconectando em 3 segundos...")
                time.sleep(3)


if __name__ == "__main__":
    RunBot().run_loop()
