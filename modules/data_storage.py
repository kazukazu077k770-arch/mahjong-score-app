"""
データ永続化モジュール - ローカルストレージでのデータ保存・読み込み
"""
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# データ保存用ディレクトリ
DATA_DIR = Path("./data")
STATS_FILE = DATA_DIR / "mahjong_stats.json"
HISTORY_FILE = DATA_DIR / "mahjong_history.json"
SETTINGS_FILE = DATA_DIR / "app_settings.json"

def ensure_data_directory():
    """データディレクトリの存在確認と作成"""
    try:
        DATA_DIR.mkdir(exist_ok=True)
        return True
    except (PermissionError, OSError):
        # クラウド環境で書き込み権限がない場合はスキップ
        return False

def save_stats():
    """統計データの保存"""
    if not ensure_data_directory():
        # ディレクトリ作成に失敗した場合はスキップ
        return False
    
    data = {
        "stats": st.session_state.get("stats", {}),
        "last_updated": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        # クラウド環境ではファイル保存をスキップ
        return False
        return False

def load_stats():
    """統計データの読み込み"""
    if not STATS_FILE.exists():
        return {}
    
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("stats", {})
    except Exception as e:
        st.error(f"統計データの読み込みに失敗しました: {e}")
        return {}

def save_history():
    """対戦履歴の保存"""
    if not ensure_data_directory():
        return False
    
    data = {
        "history": st.session_state.get("history", []),
        "last_updated": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

def load_history():
    """対戦履歴の読み込み"""
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("history", [])
    except Exception as e:
        st.error(f"対戦履歴の読み込みに失敗しました: {e}")
        return []

def save_settings():
    """アプリ設定の保存"""
    if not ensure_data_directory():
        return False
    
    data = {
        "settings": {
            "rate": st.session_state.get("rate", 1.0),
            "game_type": st.session_state.get("game_type", "四麻"),
            "available_players": st.session_state.get("available_players", []),
            "selected_players": st.session_state.get("selected_players", []),
            "players": st.session_state.get("players", []),
            # ウマ設定
            "uma_1st": st.session_state.get("uma_1st", 10),
            "uma_2nd": st.session_state.get("uma_2nd", 5),
            "uma_3rd": st.session_state.get("uma_3rd", -5),
            "uma_4th": st.session_state.get("uma_4th", -10),
            "uma_1st_sanma": st.session_state.get("uma_1st_sanma", 15),
            "uma_2nd_sanma": st.session_state.get("uma_2nd_sanma", -5),
            "uma_3rd_sanma": st.session_state.get("uma_3rd_sanma", -10),
        },
        "last_updated": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

def load_settings():
    """アプリ設定の読み込み"""
    if not SETTINGS_FILE.exists():
        return {}
    
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("settings", {})
    except Exception as e:
        st.error(f"設定の読み込みに失敗しました: {e}")
        return {}

def auto_save():
    """自動保存（統計、履歴、設定をまとめて保存）"""
    results = []
    results.append(save_stats())
    results.append(save_history())
    results.append(save_settings())
    return all(results)

def auto_load():
    """自動読み込み（アプリ起動時）"""
    try:
        # 統計データの読み込み
        stats = load_stats()
        if stats:
            st.session_state.stats = stats
        
        # 対戦履歴の読み込み
        history = load_history()
        if history:
            st.session_state.history = history
        
        # 設定の読み込み
        settings = load_settings()
        if settings:
            for key, value in settings.items():
                if key not in st.session_state or st.session_state[key] != value:
                    st.session_state[key] = value
        
        return True
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return False

def export_all_data():
    """全データのエクスポート（バックアップ用）"""
    ensure_data_directory()
    
    export_data = {
        "stats": st.session_state.get("stats", {}),
        "history": st.session_state.get("history", []),
        "settings": {
            "rate": st.session_state.get("rate", 1.0),
            "game_type": st.session_state.get("game_type", "四麻"),
            "available_players": st.session_state.get("available_players", []),
            "selected_players": st.session_state.get("selected_players", []),
            "players": st.session_state.get("players", []),
            "uma_1st": st.session_state.get("uma_1st", 10),
            "uma_2nd": st.session_state.get("uma_2nd", 5),
            "uma_3rd": st.session_state.get("uma_3rd", -5),
            "uma_4th": st.session_state.get("uma_4th", -10),
            "uma_1st_sanma": st.session_state.get("uma_1st_sanma", 15),
            "uma_2nd_sanma": st.session_state.get("uma_2nd_sanma", -5),
            "uma_3rd_sanma": st.session_state.get("uma_3rd_sanma", -10),
        },
        "export_date": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    export_filename = f"mahjong_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_path = DATA_DIR / export_filename
    
    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        return export_path
    except Exception as e:
        st.error(f"データのエクスポートに失敗しました: {e}")
        return None
