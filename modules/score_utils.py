"""
共通ユーティリティモジュール - 計算とデータ処理
"""
import streamlit as st
import pandas as pd
from .data_storage import auto_save

def calculate_score_difference(scores, base_score=25000):
    """点数差の計算"""
    differences = {}
    for player, score in scores.items():
        differences[player] = score - base_score
    return differences

def update_player_stats(player, score_diff, position, yakuman_count=0, uma_score=0):
    """プレイヤー統計の更新"""
    if player not in st.session_state.stats:
        st.session_state.stats[player] = {
            "総合勝ち得点": 0, "1位": 0, "2位": 0, "3位": 0, "4位": 0,
            "跳ばし": 0, "跳び": 0, "役満": 0, "確定値": 0
        }
    
    # 基本点数差（ウマ・オカを含む最終スコア）
    final_score = score_diff + uma_score
    
    # 役満祝儀による追加得点計算
    yakuman_bonus = 0
    if yakuman_count > 0:
        yakuman_bonus_value = st.session_state.get("yakuman_bonus", 40)
        yakuman_bonus = yakuman_count * yakuman_bonus_value * 1000 * st.session_state.rate
    elif yakuman_count < 0:
        yakuman_penalty_value = st.session_state.get("yakuman_penalty", 20)
        yakuman_bonus = yakuman_count * yakuman_penalty_value * 1000 * st.session_state.rate
    
    # 基本統計更新（得点はレート影響なし）
    st.session_state.stats[player]["総合勝ち得点"] += final_score
    st.session_state.stats[player][f"{position}位"] += 1
    
    # 確定値（レート×点数÷10の計算）
    confirmed_value = (final_score * st.session_state.rate + yakuman_bonus) / 10
    st.session_state.stats[player]["確定値"] += confirmed_value
    
    # 役満回数の更新（+1の場合のみカウント）
    if yakuman_count > 0:
        st.session_state.stats[player]["役満"] += yakuman_count
    
    # 跳ばし/跳び判定は特殊フラグで処理するため、ここでは削除

def validate_scores(scores):
    """スコアの妥当性チェック"""
    total = sum(scores.values())
    expected_total = len(scores) * 25000
    
    return {
        'is_valid': abs(total - expected_total) < 100,  # 100点の誤差を許容
        'total': total,
        'expected': expected_total,
        'difference': total - expected_total
    }

def create_stats_dataframe():
    """統計データフレームの作成"""
    if not st.session_state.stats:
        return pd.DataFrame()
    
    df_data = []
    for player, stats in st.session_state.stats.items():
        row = {"プレイヤー": player}
        row.update(stats)
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # 順位付け（総合勝ち得点順）
    if not df.empty:
        df = df.sort_values("総合勝ち得点", ascending=False).reset_index(drop=True)
        df.index += 1  # 1から始まる順位
    
    return df

def format_score(score):
    """スコアのフォーマット"""
    if score >= 0:
        return f"+{score:,}"
    else:
        return f"{score:,}"

def export_stats_to_csv():
    """統計データのCSVエクスポート"""
    df = create_stats_dataframe()
    if not df.empty:
        return df.to_csv(index=True, index_label="順位").encode('utf-8-sig')
    return None

def record_game(scores, special_flags=None, yakuman_counts=None):
    """ゲーム結果の記録"""
    # プレイヤーの存在確認と統計初期化
    for player in scores.keys():
        if player not in st.session_state.stats:
            st.session_state.stats[player] = {
                "総合勝ち得点": 0, "1位": 0, "2位": 0, "3位": 0, "4位": 0,
                "跳ばし": 0, "跳び": 0, "役満": 0, "確定値": 0
            }
    
    # 順位計算
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranks = {}
    for i, (player, score) in enumerate(sorted_scores):
        ranks[player] = i + 1
    
    # ウマ・オカの計算
    uma_scores = calculate_uma_scores(scores, ranks)
    
    # 基本点数の設定
    base_score = 25000 if len(st.session_state.players) == 4 else 35000
    rate = st.session_state.get("rate", 1.0)
    
    # 各プレイヤーの統計更新
    for player in scores:
        # 基本点数差
        score_diff = scores[player] - base_score
        position = ranks[player]
        uma_score = uma_scores[player]
        
        # 役満祝儀の回数
        yakuman_count = yakuman_counts.get(player, 0) if yakuman_counts else 0
        
        # 特殊フラグの処理用の今回の戦績更新（総合統計には反映しない）
        if special_flags and player in special_flags:
            flag = special_flags[player]
            # 今回の戦績に特殊フラグを記録（必要に応じて後で実装）
    
    # 履歴に追加
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # 今回の戦績統計を初期化
    if "current_session_stats" not in st.session_state:
        st.session_state.current_session_stats = {}
    
    # 履歴記録用のゲームデータ
    game_record = {}
    
    # 各プレイヤーのゲーム記録を作成
    for player in scores:
        score_diff = scores[player] - base_score
        position = ranks[player]
        uma_score = uma_scores[player]
        yakuman_count = yakuman_counts.get(player, 0) if yakuman_counts else 0
        special_flag = special_flags.get(player, "なし") if special_flags else "なし"
        
        # 役満祝儀による追加得点計算
        yakuman_bonus = 0
        if yakuman_count > 0:
            yakuman_bonus_value = st.session_state.get("yakuman_bonus", 40)
            yakuman_bonus = yakuman_count * yakuman_bonus_value * 1000 * rate
        elif yakuman_count < 0:
            yakuman_penalty_value = st.session_state.get("yakuman_penalty", -20)
            yakuman_bonus = yakuman_count * abs(yakuman_penalty_value) * 1000 * rate
        
        # 確定値計算
        final_score = score_diff + uma_score
        confirmed_value = (final_score + yakuman_bonus) * rate / 10
        
        # ゲーム記録に追加
        game_record[player] = {
            'score': scores[player],
            'score_diff': final_score,
            'position': position,
            'yakuman': yakuman_count,
            'special': special_flag,
            'confirmed_value': confirmed_value
        }
        
        # 今回の戦績統計を更新
        if player not in st.session_state.current_session_stats:
            st.session_state.current_session_stats[player] = {
                '1位': 0, '2位': 0, '3位': 0, '4位': 0,
                '総合勝ち得点': 0, '役満': 0, '跳ばし': 0, '跳び': 0, '確定値': 0
            }
        
        st.session_state.current_session_stats[player][f"{position}位"] += 1
        st.session_state.current_session_stats[player]["総合勝ち得点"] += final_score
        st.session_state.current_session_stats[player]["確定値"] += confirmed_value
        
        if special_flag == "跳ばし":
            st.session_state.current_session_stats[player]["跳ばし"] += 1
        elif special_flag == "跳び":
            st.session_state.current_session_stats[player]["跳び"] += 1
        
        if yakuman_count > 0:
            st.session_state.current_session_stats[player]["役満"] += yakuman_count
    
    st.session_state.history.append(game_record)
    
    # データの自動保存
    auto_save()

def calculate_uma_scores(scores, ranks):
    """ウマ・オカのスコア計算"""
    uma_scores = {}
    
    if len(st.session_state.players) == 4:
        # 四麻のウマ設定（個別設定値を使用）
        uma_1st = st.session_state.get("uma_1st", 10)
        uma_2nd = st.session_state.get("uma_2nd", 5)
        uma_3rd = st.session_state.get("uma_3rd", -5)
        uma_4th = st.session_state.get("uma_4th", -10)
        
        uma_values = {1: uma_1st, 2: uma_2nd, 3: uma_3rd, 4: uma_4th}
    else:
        # 三麻のウマ設定
        uma_1st = st.session_state.get("uma_1st_sanma", 15)
        uma_2nd = st.session_state.get("uma_2nd_sanma", -5)
        uma_3rd = st.session_state.get("uma_3rd_sanma", -10)
        
        uma_values = {1: uma_1st, 2: uma_2nd, 3: uma_3rd}
    
    # 各プレイヤーにウマ・オカを適用
    for player, score in scores.items():
        rank = ranks[player]
        uma_scores[player] = uma_values[rank] * 1000  # ウマは千点単位
    
    return uma_scores


def undo_last_game():
    """直近のゲーム結果を取り消す"""
    if not hasattr(st.session_state, 'history') or not st.session_state.history:
        return False, "取り消すゲーム記録がありません"
    
    # 最後のゲーム記録を取得
    last_game = st.session_state.history.pop()
    
    # 統計から最後のゲームの結果を減算
    for player, game_data in last_game.items():
        if player in st.session_state.stats:
            # 順位統計を減算
            position = game_data.get('position', 1)
            st.session_state.stats[player][f"{position}位"] -= 1
            
            # 得点を減算
            st.session_state.stats[player]["総合勝ち得点"] -= game_data.get('score_diff', 0)
            st.session_state.stats[player]["確定値"] -= game_data.get('confirmed_value', 0)
            
            # 特殊記録を減算
            if game_data.get('special') == '跳ばし':
                st.session_state.stats[player]["跳ばし"] -= 1
            elif game_data.get('special') == '跳び':
                st.session_state.stats[player]["跳び"] -= 1
            
            # 役満記録を減算
            yakuman_count = game_data.get('yakuman', 0)
            if yakuman_count > 0:
                st.session_state.stats[player]["役満"] -= yakuman_count
    
    # 今回の戦績からも減算
    if hasattr(st.session_state, 'current_session_stats'):
        for player, game_data in last_game.items():
            if player in st.session_state.current_session_stats:
                position = game_data.get('position', 1)
                st.session_state.current_session_stats[player][f"{position}位"] -= 1
                st.session_state.current_session_stats[player]["総合勝ち得点"] -= game_data.get('score_diff', 0)
                
                if game_data.get('special') == '跳ばし':
                    st.session_state.current_session_stats[player]["跳ばし"] -= 1
                elif game_data.get('special') == '跳び':
                    st.session_state.current_session_stats[player]["跳び"] -= 1
                
                yakuman_count = game_data.get('yakuman', 0)
                if yakuman_count > 0:
                    st.session_state.current_session_stats[player]["役満"] -= yakuman_count
    
    # データを保存
    auto_save()
    
    return True, "直近のゲーム記録を取り消しました"
