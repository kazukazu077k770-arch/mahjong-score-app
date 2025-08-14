"""
データ初期化モジュール - アプリケーション状態の管理
"""
import streamlit as st
from .data_storage import auto_load, auto_save

def init_players():
    """プレイヤー情報の初期化"""
    if "players" not in st.session_state:
        st.session_state.players = ["杉村", "三瓶", "福原", "松井"]
        st.session_state.game_type = "四麻"
    
    # 利用可能プレイヤーリストの初期化
    if "available_players" not in st.session_state:
        st.session_state.available_players = [
            "杉村", "三瓶", "福原", "松井", 
            "プレイヤー1", "プレイヤー2", "プレイヤー3", "プレイヤー4",
            "プレイヤー5", "プレイヤー6", "プレイヤー7", "プレイヤー8"
        ]

def init_scores():
    """スコア情報の初期化"""
    if "stats" not in st.session_state:
        st.session_state.rate = 1.0
        st.session_state.stats = {}
        for player in st.session_state.players:
            st.session_state.stats[player] = {
                "総合勝ち得点": 0, "1位": 0, "2位": 0, "3位": 0, "4位": 0,
                "跳ばし": 0, "跳び": 0, "役満": 0, "確定値": 0
            }

def init_uma_settings():
    """ウマ・オカ設定の初期化"""
    # 四麻のウマ設定（個別設定）
    if "uma_1st" not in st.session_state:
        st.session_state.uma_1st = 10
    if "uma_2nd" not in st.session_state:
        st.session_state.uma_2nd = 5
    if "uma_3rd" not in st.session_state:
        st.session_state.uma_3rd = -5
    if "uma_4th" not in st.session_state:
        st.session_state.uma_4th = -10
    
    # 三麻のウマ設定
    if "uma_1st_sanma" not in st.session_state:
        st.session_state.uma_1st_sanma = 15
    if "uma_2nd_sanma" not in st.session_state:
        st.session_state.uma_2nd_sanma = -5
    if "uma_3rd_sanma" not in st.session_state:
        st.session_state.uma_3rd_sanma = -10

def init_widget_defaults():
    """ウィジェットのデフォルト値を初期化"""
    for player in st.session_state.players:
        default_score = 25000 if len(st.session_state.players) == 4 else 35000
        
        # スコアウィジェットの初期値（存在しない場合のみ設定）
        score_key = f"score_{player}"
        if score_key not in st.session_state:
            st.session_state[score_key] = default_score
            
        # 特殊フラグウィジェットの初期値（存在しない場合のみ設定）
        special_key = f"special_{player}"
        if special_key not in st.session_state:
            st.session_state[special_key] = "なし"
            
        # 役満祝儀ウィジェットの初期値（存在しない場合のみ設定）
        yakuman_key = f"yakuman_{player}"
        if yakuman_key not in st.session_state:
            st.session_state[yakuman_key] = 0

def reset_widget_values():
    """ウィジェット値をリセット（記録後に呼び出し）"""
    # 古いキーを削除してリセット
    keys_to_remove = []
    for key in st.session_state.keys():
        if key.startswith("score_") or key.startswith("special_") or key.startswith("yakuman_"):
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del st.session_state[key]
    
    # 新しいデフォルト値を設定
    init_widget_defaults()

def init_ui_state():
    """UI状態の初期化"""
    if "ui_theme" not in st.session_state:
        st.session_state.ui_theme = "desktop"
    
    if "data_cleared" not in st.session_state:
        st.session_state.data_cleared = False

def clear_all_data():
    """全データの消去"""
    keys_to_keep = ['ui_theme']  # UIテーマは保持
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    
    # 基本データを再初期化
    init_players()
    init_scores()
    st.session_state.data_cleared = True

def init_app_state():
    """アプリケーション状態の完全初期化"""
    # まず保存されたデータを読み込み
    if "data_loaded" not in st.session_state:
        auto_load()
        st.session_state.data_loaded = True
    
    init_ui_state()
    init_players()
    init_scores()
    init_uma_settings()
    init_widget_defaults()

def save_current_state():
    """現在の状態を保存"""
    auto_save()
