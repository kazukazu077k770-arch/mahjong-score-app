"""
点数入力ページ - メイン
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.score_utils import (
    validate_scores, update_player_stats, create_stats_dataframe, 
    format_score, export_stats_to_csv, record_game, undo_last_game
)
from modules.data_init import clear_all_data, init_widget_defaults, reset_widget_values, init_uma_settings, save_current_state

def show_mobile_score_entry():
    """点数入力画面"""
    st.title("🀄 麻雀スコア管理")
    
    # ウィジェットのデフォルト値を初期化
    init_widget_defaults()
    init_uma_settings()
    
    # プレイヤー設定セクション
    with st.expander("⚙️ ゲーム設定", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            game_type = st.selectbox("ゲーム種別", ["四麻", "三麻"], index=0)
            if game_type != st.session_state.game_type:
                st.session_state.game_type = game_type
                if game_type == "三麻":
                    st.session_state.players = st.session_state.get("selected_players", ["杉村", "三瓶", "福原"])[:3]
                else:
                    st.session_state.players = st.session_state.get("selected_players", ["杉村", "三瓶", "福原", "松井"])[:4]
                st.rerun()
        
        with col2:
            rate = st.number_input("レート", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
            st.session_state.rate = rate
        
        # プレイヤー選択セクション
        st.write("### 参加プレイヤー選択")
        
        # 利用可能プレイヤーがない場合は初期化
        if "available_players" not in st.session_state:
            st.session_state.available_players = [
                "杉村", "三瓶", "福原", "松井"
            ]
        
        if st.session_state.game_type == "四麻":
            # 四麻の場合の4人選択
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                player1 = st.selectbox("1番目", st.session_state.available_players, index=0, key="player_select_1")
            with col2:
                available_for_2 = [p for p in st.session_state.available_players if p != player1]
                player2 = st.selectbox("2番目", available_for_2, index=0, key="player_select_2")
            with col3:
                available_for_3 = [p for p in st.session_state.available_players if p not in [player1, player2]]
                player3 = st.selectbox("3番目", available_for_3, index=0, key="player_select_3")
            with col4:
                available_for_4 = [p for p in st.session_state.available_players if p not in [player1, player2, player3]]
                player4 = st.selectbox("4番目", available_for_4, index=0, key="player_select_4")
            
            # 選択されたプレイヤーを更新
            selected_players = [player1, player2, player3, player4]
        else:
            # 三麻の場合の3人選択
            col1, col2, col3 = st.columns(3)
            with col1:
                player1 = st.selectbox("1番目", st.session_state.available_players, index=0, key="sanma_player1")
            with col2:
                available_for_2 = [p for p in st.session_state.available_players if p != player1]
                player2 = st.selectbox("2番目", available_for_2, index=0, key="sanma_player2")
            with col3:
                available_for_3 = [p for p in st.session_state.available_players if p not in [player1, player2]]
                player3 = st.selectbox("3番目", available_for_3, index=0, key="sanma_player3")
            
            # 選択されたプレイヤーを更新
            selected_players = [player1, player2, player3]
        
        # プレイヤー選択が変更された場合
        if selected_players != st.session_state.get("selected_players", []):
            st.session_state.selected_players = selected_players
            st.session_state.players = selected_players
            st.rerun()
        
        # ウマ・オカ設定
        st.write("### ウマ・オカ設定")
        if st.session_state.game_type == "四麻":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                uma_1st = st.number_input("1位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_1st", 10), step=1, key="uma_1st")
            with col2:
                uma_2nd = st.number_input("2位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_2nd", 5), step=1, key="uma_2nd")
            with col3:
                uma_3rd = st.number_input("3位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_3rd", -5), step=1, key="uma_3rd")
            with col4:
                uma_4th = st.number_input("4位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_4th", -10), step=1, key="uma_4th")
        else:
            # 三麻のウマ設定
            col1, col2, col3 = st.columns(3)
            with col1:
                uma_1st_sanma = st.number_input("1位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_1st_sanma", 15), step=1, key="uma_1st_sanma")
            with col2:
                uma_2nd_sanma = st.number_input("2位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_2nd_sanma", -5), step=1, key="uma_2nd_sanma")
            with col3:
                uma_3rd_sanma = st.number_input("3位ウマ", min_value=-50, max_value=50, value=st.session_state.get("uma_3rd_sanma", -10), step=1, key="uma_3rd_sanma")
        
        # 役満祝儀設定
        st.write("### 役満祝儀設定")
        col1, col2 = st.columns(2)
        with col1:
            yakuman_bonus = st.number_input("役満祝儀（+1の場合）", min_value=0, max_value=100, value=st.session_state.get("yakuman_bonus", 40), step=5, key="yakuman_bonus", help="役満祝儀が+1の時の加点")
        with col2:
            yakuman_penalty = st.number_input("役満祝儀（-1の場合）", min_value=0, max_value=100, value=st.session_state.get("yakuman_penalty", 20), step=5, key="yakuman_penalty", help="役満祝儀が-1の時の減点")
        
        # プレイヤー名編集
        st.write("### プレイヤー名編集")
        st.info("利用可能プレイヤーリストを編集できます。")
        
        # 現在の利用可能プレイヤーを編集（4人まで）
        for i in range(min(4, len(st.session_state.available_players))):
            if i < len(st.session_state.available_players):
                current_name = st.session_state.available_players[i]
                new_name = st.text_input(f"プレイヤー {i+1}", value=current_name, key=f"edit_player_{i}")
                if new_name != current_name and new_name.strip():
                    # 統計データの名前も変更
                    if current_name in st.session_state.stats:
                        st.session_state.stats[new_name.strip()] = st.session_state.stats.pop(current_name)
                    
                    # 利用可能プレイヤーリストを更新
                    st.session_state.available_players[i] = new_name.strip()
                    
                    # 現在選択されているプレイヤーも更新
                    if "selected_players" in st.session_state:
                        if current_name in st.session_state.selected_players:
                            idx = st.session_state.selected_players.index(current_name)
                            st.session_state.selected_players[idx] = new_name.strip()
                    
                    # 現在のプレイヤーリストも更新
                    if current_name in st.session_state.players:
                        idx = st.session_state.players.index(current_name)
                        st.session_state.players[idx] = new_name.strip()
                    
                    # 設定を保存
                    save_current_state()
                    st.rerun()
        
        # 統計データクリーンアップ
        st.write("### 統計データ管理")
        if st.button("🗑️ プレイヤー1〜8の統計データを削除", help="プレイヤー1、プレイヤー2...プレイヤー8の統計データを削除します"):
            deleted_players = []
            for i in range(1, 9):
                player_name = f"プレイヤー{i}"
                if player_name in st.session_state.stats:
                    del st.session_state.stats[player_name]
                    deleted_players.append(player_name)
                
                # 今回の戦績からも削除
                if hasattr(st.session_state, 'current_session_stats') and player_name in st.session_state.current_session_stats:
                    del st.session_state.current_session_stats[player_name]
                
                # 利用可能プレイヤーリストからも削除
                if player_name in st.session_state.available_players:
                    st.session_state.available_players.remove(player_name)
            
            if deleted_players:
                st.success(f"✅ {', '.join(deleted_players)} の統計データを削除しました")
                save_current_state()
                st.rerun()
            else:
                st.info("削除対象のプレイヤーが見つかりませんでした")
    
    # 点数入力セクション - スマホ特化2x2グリッド
    st.markdown("### 点数入力")
    
    # 強制2×2グリッドのHTMLマークアップ
    st.markdown('<div class="mobile-grid-container">', unsafe_allow_html=True)
    
    # スマホ向け2x2グリッドレイアウト
    scores = {}
    special_flags = {}  # 跳び・跳ばしフラグ
    yakuman_counts = {}  # 役満祝儀回数
    
    if len(st.session_state.players) == 4:
        # 四麻: 2x2グリッド
        # 上段：東・南
        col1, col2 = st.columns(2)
        with col1:
            player = st.session_state.players[0]  # 1番目プレイヤー
            st.markdown(f'<div class="player-name">{player}</div>', unsafe_allow_html=True)
            
            # 基本点数入力
            base_score = st.number_input(
                "点数", 
                min_value=-100000, 
                max_value=100000, 
                value=st.session_state.get(f"score_{player}", 25000), 
                step=1000,
                key=f"score_{player}",
                label_visibility="collapsed"
            )
            
            # 跳び・跳ばし選択
            special_option = st.selectbox(
                "特殊",
                ["なし", "跳び", "跳ばし"],
                index=["なし", "跳び", "跳ばし"].index(st.session_state.get(f"special_{player}", "なし")),
                key=f"special_{player}",
                label_visibility="collapsed"
            )
            
            # 役満祝儀入力
            yakuman_count = st.number_input(
                "役満祝儀",
                min_value=-10,
                max_value=10,
                value=st.session_state.get(f"yakuman_{player}", 0),
                step=1,
                key=f"yakuman_{player}",
                label_visibility="collapsed"
            )
            
            # 役満祝儀による点数調整（合計には影響しない）
            yakuman_adjustment = 0
            if yakuman_count > 0:
                yakuman_adjustment = yakuman_count * 40000 * st.session_state.rate
            elif yakuman_count < 0:
                yakuman_adjustment = yakuman_count * 20000 * st.session_state.rate
            
            # 最終スコア計算
            final_score = base_score
            if special_option == "跳び":
                final_score -= 10000  # 跳びペナルティ
                special_flags[player] = "跳び"
            elif special_option == "跳ばし":
                final_score += 10000  # 跳ばしボーナス
                special_flags[player] = "跳ばし"
            else:
                special_flags[player] = "なし"
                
            scores[player] = final_score
            yakuman_counts[player] = yakuman_count
            
        with col2:
            player = st.session_state.players[1]  # 2番目プレイヤー
            st.markdown(f'<div class="player-name">{player}</div>', unsafe_allow_html=True)
            
            # 基本点数入力
            base_score = st.number_input(
                "点数", 
                min_value=-100000, 
                max_value=100000, 
                value=st.session_state.get(f"score_{player}", 25000), 
                step=1000,
                key=f"score_{player}",
                label_visibility="collapsed"
            )
            
            # 跳び・跳ばし選択
            special_option = st.selectbox(
                "特殊",
                ["なし", "跳び", "跳ばし"],
                index=["なし", "跳び", "跳ばし"].index(st.session_state.get(f"special_{player}", "なし")),
                key=f"special_{player}",
                label_visibility="collapsed"
            )
            
            # 役満祝儀入力
            yakuman_count = st.number_input(
                "役満祝儀",
                min_value=-10,
                max_value=10,
                value=st.session_state.get(f"yakuman_{player}", 0),
                step=1,
                key=f"yakuman_{player}",
                label_visibility="collapsed"
            )
            
            # 最終スコア計算
            final_score = base_score
            if special_option == "跳び":
                final_score -= 10000
                special_flags[player] = "跳び"
            elif special_option == "跳ばし":
                final_score += 10000
                special_flags[player] = "跳ばし"
            else:
                special_flags[player] = "なし"
                
            scores[player] = final_score
            yakuman_counts[player] = yakuman_count

        # 下段：西・北
        col3, col4 = st.columns(2)
        with col3:
            player = st.session_state.players[2]  # 3番目プレイヤー
            st.markdown(f'<div class="player-name">{player}</div>', unsafe_allow_html=True)
            
            # 基本点数入力
            base_score = st.number_input(
                "点数", 
                min_value=-100000, 
                max_value=100000, 
                value=st.session_state.get(f"score_{player}", 25000), 
                step=1000,
                key=f"score_{player}",
                label_visibility="collapsed"
            )
            
            # 跳び・跳ばし選択
            special_option = st.selectbox(
                "特殊",
                ["なし", "跳び", "跳ばし"],
                index=["なし", "跳び", "跳ばし"].index(st.session_state.get(f"special_{player}", "なし")),
                key=f"special_{player}",
                label_visibility="collapsed"
            )
            
            # 役満祝儀入力
            yakuman_count = st.number_input(
                "役満祝儀",
                min_value=-10,
                max_value=10,
                value=st.session_state.get(f"yakuman_{player}", 0),
                step=1,
                key=f"yakuman_{player}",
                label_visibility="collapsed"
            )
            
            # 最終スコア計算
            final_score = base_score
            if special_option == "跳び":
                final_score -= 10000
                special_flags[player] = "跳び"
            elif special_option == "跳ばし":
                final_score += 10000
                special_flags[player] = "跳ばし"
            else:
                special_flags[player] = "なし"
                
            scores[player] = final_score
            yakuman_counts[player] = yakuman_count
            
        with col4:
            player = st.session_state.players[3]  # 4番目プレイヤー
            st.markdown(f'<div class="player-name">{player}</div>', unsafe_allow_html=True)
            
            # 基本点数入力
            base_score = st.number_input(
                "点数", 
                min_value=-100000, 
                max_value=100000, 
                value=st.session_state.get(f"score_{player}", 25000), 
                step=1000,
                key=f"score_{player}",
                label_visibility="collapsed"
            )
            
            # 跳び・跳ばし選択
            special_option = st.selectbox(
                "特殊",
                ["なし", "跳び", "跳ばし"],
                index=["なし", "跳び", "跳ばし"].index(st.session_state.get(f"special_{player}", "なし")),
                key=f"special_{player}",
                label_visibility="collapsed"
            )
            
            # 役満祝儀入力
            yakuman_count = st.number_input(
                "役満祝儀",
                min_value=-10,
                max_value=10,
                value=st.session_state.get(f"yakuman_{player}", 0),
                step=1,
                key=f"yakuman_{player}",
                label_visibility="collapsed"
            )
            
            # 最終スコア計算
            final_score = base_score
            if special_option == "跳び":
                final_score -= 10000
                special_flags[player] = "跳び"
            elif special_option == "跳ばし":
                final_score += 10000
                special_flags[player] = "跳ばし"
            else:
                special_flags[player] = "なし"
                
            scores[player] = final_score
            yakuman_counts[player] = yakuman_count
        
    else:
        # 三麻: 横3列
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        for i, player in enumerate(st.session_state.players):
            with cols[i]:
                st.markdown(f'<div class="player-name">{player}</div>', unsafe_allow_html=True)
                
                # 基本点数入力
                base_score = st.number_input(
                    "点数", 
                    min_value=-100000, 
                    max_value=100000, 
                    value=st.session_state.get(f"score_{player}", 35000), 
                    step=1000,
                    key=f"score_{player}",
                    label_visibility="collapsed"
                )
                
                # 跳び・跳ばし選択
                special_option = st.selectbox(
                    "特殊",
                    ["なし", "跳び", "跳ばし"],
                    index=["なし", "跳び", "跳ばし"].index(st.session_state.get(f"special_{player}", "なし")),
                    key=f"special_{player}",
                    label_visibility="collapsed"
                )
                
                # 役満祝儀入力
                yakuman_count = st.number_input(
                    "役満祝儀",
                    min_value=-10,
                    max_value=10,
                    value=st.session_state.get(f"yakuman_{player}", 0),
                    step=1,
                    key=f"yakuman_{player}",
                    label_visibility="collapsed"
                )
                
                # 最終スコア計算
                final_score = base_score
                if special_option == "跳び":
                    final_score -= 10000
                    special_flags[player] = "跳び"
                elif special_option == "跳ばし":
                    final_score += 10000
                    special_flags[player] = "跳ばし"
                else:
                    special_flags[player] = "なし"
                    
                scores[player] = final_score
                yakuman_counts[player] = yakuman_count
    
    # グリッドコンテナ終了
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 合計点数表示 - スマホ特化カード
    total_score = sum(scores.values())
    if len(st.session_state.players) == 4:
        expected_total = 100000
    else:  # 三麻
        expected_total = 105000
    
    # ウマ・オカのプレビュー計算
    if total_score == expected_total:
        # 順位計算
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranks = {}
        for i, (player, score) in enumerate(sorted_scores):
            ranks[player] = i + 1
        
        # ウマ・オカの表示
        st.markdown("### 🏆 順位とウマ・オカ")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            base_score = 25000 if len(st.session_state.players) == 4 else 35000
            score_diff = score - base_score
            
            # ウマ計算
            if len(st.session_state.players) == 4:
                uma_1st = st.session_state.get("uma_1st", 10)
                uma_2nd = st.session_state.get("uma_2nd", 5)
                uma_3rd = st.session_state.get("uma_3rd", -5)
                uma_4th = st.session_state.get("uma_4th", -10)
                uma_values = {1: uma_1st, 2: uma_2nd, 3: uma_3rd, 4: uma_4th}
            else:
                uma_1st = st.session_state.get("uma_1st_sanma", 15)
                uma_2nd = st.session_state.get("uma_2nd_sanma", -5)
                uma_3rd = st.session_state.get("uma_3rd_sanma", -10)
                uma_values = {1: uma_1st, 2: uma_2nd, 3: uma_3rd}
            
            uma_score = uma_values[rank] * 1000
            final_score = score_diff + uma_score
            
            # 役満祝儀による追加得点（合計には含まない）
            yakuman_count = yakuman_counts.get(player, 0)
            yakuman_bonus = 0
            if yakuman_count > 0:
                yakuman_bonus_value = st.session_state.get("yakuman_bonus", 40)
                yakuman_bonus = yakuman_count * yakuman_bonus_value * 1000 * st.session_state.rate
            elif yakuman_count < 0:
                yakuman_penalty_value = st.session_state.get("yakuman_penalty", 20)
                yakuman_bonus = yakuman_count * yakuman_penalty_value * 1000 * st.session_state.rate
            
            # 確定値（レート×点数÷10）
            confirmed_value = (final_score + yakuman_bonus) * st.session_state.rate / 10
            
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣"][rank-1] if len(st.session_state.players) == 4 else ["🥇", "🥈", "🥉"][rank-1]
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #f8f9fa, #e9ecef); padding: 0.8rem; margin: 0.3rem 0; border-radius: 8px; border-left: 4px solid {'#28a745' if final_score >= 0 else '#dc3545'};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 1.1rem;">{rank_emoji} {player}</span>
                    <span style="font-weight: 700; font-size: 1.2rem; color: {'#28a745' if final_score >= 0 else '#dc3545'};">
                        {final_score:+,}pt
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.2rem;">
                    基本: {score_diff:+,} + ウマ: {uma_score:+,} = 最終: {final_score:+,}
                </div>
                {f'<div style="font-size: 0.85rem; color: #dc3545; margin-top: 0.2rem;">役満祝儀: {yakuman_bonus:+.0f}pt | 確定値: {confirmed_value:+.1f}</div>' if yakuman_count != 0 else ''}
            </div>
            """, unsafe_allow_html=True)
    
    # 合計点数カード
    card_class = "total-card"
    if total_score != expected_total:
        card_class += " warning"
        status_icon = "⚠️"
        status_text = "点数を確認"
    else:
        status_icon = "✅"
        status_text = "正常"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">
            {status_icon} 合計点数: {total_score:,}点
        </div>
        <div style="font-size: 0.95rem; opacity: 0.9;">
            期待値: {expected_total:,}点 | 差額: {total_score - expected_total:+,}点 | {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 役満祝儀による点数変動表示
    total_yakuman_adjustment = 0
    yakuman_details = []
    
    for player, yakuman_count in yakuman_counts.items():
        if yakuman_count != 0:
            if yakuman_count > 0:
                yakuman_bonus_value = st.session_state.get("yakuman_bonus", 40)
                adjustment = yakuman_count * yakuman_bonus_value * 1000 * st.session_state.rate
                yakuman_details.append(f"{player}: +{yakuman_count}役満 = +{adjustment:,.0f}pt")
            else:
                yakuman_penalty_value = st.session_state.get("yakuman_penalty", 20)
                adjustment = yakuman_count * yakuman_penalty_value * 1000 * st.session_state.rate
                yakuman_details.append(f"{player}: {yakuman_count}役満 = {adjustment:,.0f}pt")
            total_yakuman_adjustment += adjustment
    
    if yakuman_details:
        st.markdown("### 🎯 役満祝儀による点数変動")
        
        # 個別詳細
        for detail in yakuman_details:
            st.markdown(f"- {detail}")
        
        # 合計変動とレート反映
        confirmed_adjustment = total_yakuman_adjustment * st.session_state.rate / 10  # 確定値用の計算
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #fff3cd, #ffeaa7); padding: 0.8rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #f39c12;">
            <div style="font-weight: 600; font-size: 1.1rem; color: #856404;">
                📊 役満祝儀合計: {total_yakuman_adjustment:+,.0f}pt
            </div>
            <div style="font-size: 0.9rem; color: #856404; margin-top: 0.3rem;">
                レート {st.session_state.rate}倍 | 確定値への反映: {confirmed_adjustment:+.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 記録ボタン - 大きなタッチ対応
    record_button_disabled = total_score != expected_total
    
    if not record_button_disabled:
        if st.button("📝 記録", type="primary", use_container_width=True):
            record_game(scores, special_flags, yakuman_counts)
            st.success("✅ ゲーム結果を記録しました！")
            # ウィジェット値をリセット
            reset_widget_values()
            st.rerun()
    else:
        st.button("📝 記録（点数を確認してください）", disabled=True, use_container_width=True)
    
    # 直近ゲーム取り消しボタン
    if st.session_state.get("history") and len(st.session_state.history) > 0:
        if st.button("↩️ 直近ゲーム取り消し", type="secondary", use_container_width=True, help="最後に記録したゲームを取り消します"):
            success, message = undo_last_game()
            if success:
                st.success(f"✅ {message}")
            else:
                st.warning(f"⚠️ {message}")
            st.rerun()
    
    # 統計表示
    show_statistics()

def show_statistics():
    """統計表示"""
    st.markdown("### 📊 統計")
    
    if not st.session_state.stats:
        st.info("まだ記録がありません。")
        return
    
    # 統計データをDataFrameに変換
    stats_data = []
    for player, stats in st.session_state.stats.items():
        total_games = stats["1位"] + stats["2位"] + stats["3位"] + stats["4位"]
        if total_games > 0:
            top_rate = stats["1位"] / total_games * 100  # 1位率
            second_rate = stats["2位"] / total_games * 100  # 2位率
            third_rate = stats["3位"] / total_games * 100  # 3位率
        else:
            top_rate = 0
            second_rate = 0
            third_rate = 0
        
        stats_data.append({
            "プレイヤー": player,
            "得点": f"{stats['総合勝ち得点']:+.1f}",
            "確定値": f"{stats['確定値']:+.1f}",
            "1位": stats["1位"],
            "2位": stats["2位"],
            "3位": stats["3位"],
            "4位": stats["4位"],
            "1位率": f"{top_rate:.0f}%",
            "2位率": f"{second_rate:.0f}%",
            "3位率": f"{third_rate:.0f}%",
            "跳ばし": stats["跳ばし"],
            "跳び": stats["跳び"],
            "役満": stats["役満"],
            "総合勝ち得点_数値": stats['総合勝ち得点'],
            "確定値_数値": stats['確定値'],
            "1位率_数値": top_rate,
            "2位率_数値": second_rate,
            "3位率_数値": third_rate,
            "総ゲーム数": total_games
        })
    
    if stats_data:
        df = pd.DataFrame(stats_data)
        # 得点でソート
        df = df.sort_values("得点", key=lambda x: x.str.replace("+", "").astype(float), ascending=False)
        
        # タブで表示を切り替え
        tab1, tab2, tab3 = st.tabs(["📋 統計表", "📊 グラフ", "🏆 順位分析"])
        
        with tab1:
            # 従来の統計表
            display_df = df[["プレイヤー", "得点", "確定値", "1位", "2位", "3位", "4位", "1位率", "2位率", "3位率", "跳ばし", "跳び", "役満"]].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        with tab2:
            # グラフ表示
            show_statistics_graphs(df)
        
        with tab3:
            # 順位分析
            show_rank_analysis(df)
        
        # 統計リセットボタン（警告付き）
        if st.button("⚠️ 統計リセット", type="secondary"):
            # 警告ダイアログの代わりにsession stateで確認
            if "reset_confirmation" not in st.session_state:
                st.session_state.reset_confirmation = False
            
            if not st.session_state.reset_confirmation:
                st.session_state.reset_confirmation = True
                st.warning("⚠️ 本当に統計をリセットしますか？この操作は元に戻せません。")
                st.rerun()
        
        # 確認状態の場合、実行ボタンとキャンセルボタンを表示
        if st.session_state.get("reset_confirmation", False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ 実行", type="primary"):
                    for player in st.session_state.stats:
                        st.session_state.stats[player] = {
                            "総合勝ち得点": 0, "1位": 0, "2位": 0, "3位": 0, "4位": 0,
                            "跳ばし": 0, "跳び": 0, "役満": 0, "確定値": 0
                        }
                    st.session_state.reset_confirmation = False
                    # データを保存
                    save_current_state()
                    st.success("統計をリセットしました。")
                    st.rerun()
            with col2:
                if st.button("❌ キャンセル"):
                    st.session_state.reset_confirmation = False
                    st.rerun()

def show_statistics_graphs(df):
    """統計データのグラフ表示"""
    if df.empty:
        st.info("表示するデータがありません。")
        return
    
    # フィルタ：ゲーム数が0より多いプレイヤーのみ
    active_df = df[df["総ゲーム数"] > 0].copy()
    
    if active_df.empty:
        st.info("ゲーム記録のあるプレイヤーがいません。")
        return
    
    # 1. 総合得点と確定値の比較バーチャート
    st.markdown("#### 💰 得点比較")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**総合勝ち得点**")
        chart_data = active_df.set_index("プレイヤー")["総合勝ち得点_数値"]
        st.bar_chart(chart_data, height=300)
    
    with col2:
        st.markdown("**確定値**")
        chart_data = active_df.set_index("プレイヤー")["確定値_数値"]
        st.bar_chart(chart_data, height=300)
    
    # 3. 1位率・2位率・3位率
    st.markdown("#### 🎯 順位率")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1位率**")
        chart_data = active_df.set_index("プレイヤー")["1位率_数値"]
        st.bar_chart(chart_data, height=300)
    
    with col2:
        st.markdown("**2位率**")
        chart_data = active_df.set_index("プレイヤー")["2位率_数値"]
        st.bar_chart(chart_data, height=300)
    
    with col3:
        st.markdown("**3位率**")
        chart_data = active_df.set_index("プレイヤー")["3位率_数値"]
        st.bar_chart(chart_data, height=300)
    
    # 4. 順位分布の積み上げ棒グラフ
    st.markdown("#### 🏆 順位分布")
    rank_data = active_df[["プレイヤー", "1位", "2位", "3位", "4位"]].set_index("プレイヤー")
    st.bar_chart(rank_data, height=350)

def show_rank_analysis(df):
    """順位分析の詳細表示"""
    if df.empty:
        st.info("表示するデータがありません。")
        return
    
    # フィルタ：ゲーム数が0より多いプレイヤーのみ
    active_df = df[df["総ゲーム数"] > 0].copy()
    
    if active_df.empty:
        st.info("ゲーム記録のあるプレイヤーがいません。")
        return
    
    # 順位分析のサマリー
    st.markdown("#### 🏅 順位分析サマリー")
    
    # 最高成績プレイヤー
    best_player = active_df.loc[active_df["総合勝ち得点_数値"].idxmax()]
    worst_player = active_df.loc[active_df["総合勝ち得点_数値"].idxmin()]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🥇 最高得点",
            value=best_player["プレイヤー"],
            delta=f"{best_player['総合勝ち得点_数値']:+.1f}pt"
        )
    
    with col2:
        st.metric(
            label="🎯 最高1位率",
            value=active_df.loc[active_df["1位率_数値"].idxmax(), "プレイヤー"],
            delta=f"{active_df['1位率_数値'].max():.1f}%"
        )
    
    with col3:
        st.metric(
            label="📊 ゲーム数最多",
            value=active_df.loc[active_df["総ゲーム数"].idxmax(), "プレイヤー"],
            delta=f"{active_df['総ゲーム数'].max()}ゲーム"
        )
    
    # 詳細統計
    st.markdown("#### 📈 詳細分析")
    
    # パフォーマンス指標
    for idx, row in active_df.iterrows():
        with st.expander(f"🎮 {row['プレイヤー']} の詳細"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **基本統計**
                - 総ゲーム数: {row['総ゲーム数']}回
                - 総合勝ち得点: {row['総合勝ち得点_数値']:+.1f}pt
                - 確定値: {row['確定値_数値']:+.1f}
                - 1位率: {row['1位率_数値']:.1f}%
                - 2位率: {row['2位率_数値']:.1f}%
                - 3位率: {row['3位率_数値']:.1f}%
                """)
            
            with col2:
                st.markdown(f"""
                **特殊統計**
                - 跳ばし回数: {row['跳ばし']}回
                - 跳び回数: {row['跳び']}回
                - 役満回数: {row['役満']}回
                """)
            
            # 個人の順位分布円グラフ
            if row['総ゲーム数'] > 0:
                rank_values = [row['1位'], row['2位'], row['3位'], row['4位']]
                rank_labels = ['1位', '2位', '3位', '4位']
                
                # 0でない値のみを表示
                non_zero_values = [(label, value) for label, value in zip(rank_labels, rank_values) if value > 0]
                
                if non_zero_values:
                    labels, values = zip(*non_zero_values)
                    fig = px.pie(
                        values=values, 
                        names=labels, 
                        title=f"{row['プレイヤー']} の順位分布",
                        color_discrete_map={
                            '1位': '#FFD700',  # ゴールド
                            '2位': '#C0C0C0',  # シルバー
                            '3位': '#CD7F32',  # ブロンズ
                            '4位': '#808080'   # グレー
                        }
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

    # 今回の戦績機能（セッション統計）
    render_current_session_stats()


def render_current_session_stats():
    """今回の戦績表示UIコンポーネント"""
    if not hasattr(st.session_state, 'current_session_stats') or not st.session_state.current_session_stats:
        return
    
    # セッション統計の確認
    has_session_data = False
    for player_stats in st.session_state.current_session_stats.values():
        total_games = player_stats.get('1位', 0) + player_stats.get('2位', 0) + player_stats.get('3位', 0) + player_stats.get('4位', 0)
        if total_games > 0:
            has_session_data = True
            break
    
    if not has_session_data:
        return
    
    st.markdown("### 🎯 今回の戦績")
    
    # セッション統計をDataFrameに変換
    session_df = create_current_session_dataframe()
    
    if not session_df.empty:
        # 表示用データフレームを作成
        display_data = []
        for _, row in session_df.iterrows():
            player = row['プレイヤー']
            total_games = row['1位'] + row['2位'] + row['3位'] + row['4位']
            
            if total_games > 0:
                avg_rank = (row['1位'] * 1 + row['2位'] * 2 + row['3位'] * 3 + row['4位'] * 4) / total_games
                rate = st.session_state.get("rate", 1.0)
                
                display_data.append({
                    'プレイヤー': player,
                    'ゲーム数': total_games,
                    '平均順位': avg_rank,
                    '1位率': row['1位'] / total_games,
                    '2位率': row['2位'] / total_games,
                    '3位率': row['3位'] / total_games,
                    '4位率': row['4位'] / total_games,
                    '累計得点': row['総合勝ち得点'],
                    'レート込み': row['総合勝ち得点'] * rate,
                    '役満': row['役満'],
                    '跳ばし': row['跳ばし'],
                    '跳び': row['跳び']
                })
        
        if display_data:
            display_df = pd.DataFrame(display_data)
            
            # スタイリングされたテーブル表示
            styled_df = display_df.style.format({
                "ゲーム数": "{:.0f}",
                "平均順位": "{:.2f}",
                "1位率": "{:.1%}",
                "2位率": "{:.1%}",
                "3位率": "{:.1%}",
                "4位率": "{:.1%}",
                "累計得点": "{:.1f}",
                "レート込み": "{:.1f}",
                "役満": "{:.0f}",
                "跳ばし": "{:.0f}",
                "跳び": "{:.0f}"
            }).set_properties(**{
                'text-align': 'center'
            })
            
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # 清算ボタン - 目立つスタイル
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <p style="color: #ff6b35; font-weight: bold; margin-bottom: 0.5rem;">
                    💰 今回の戦績を確定値に反映しますか？
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🧮 清算実行", type="primary", use_container_width=True, help="今回の戦績を確定値に反映し、今回の戦績をリセットします"):
                    settle_current_session()
                    st.success("✅ 今回の戦績を確定値に反映しました！")
                    st.rerun()


def create_current_session_dataframe():
    """今回のセッション統計をDataFrameに変換"""
    if not hasattr(st.session_state, 'current_session_stats'):
        return pd.DataFrame()
    
    session_data = []
    for player, stats in st.session_state.current_session_stats.items():
        session_data.append({
            'プレイヤー': player,
            '1位': stats.get('1位', 0),
            '2位': stats.get('2位', 0), 
            '3位': stats.get('3位', 0),
            '4位': stats.get('4位', 0),
            '総合勝ち得点': stats.get('総合勝ち得点', 0),
            '役満': stats.get('役満', 0),
            '跳ばし': stats.get('跳ばし', 0),
            '跳び': stats.get('跳び', 0)
        })
    
    return pd.DataFrame(session_data)


def settle_current_session():
    """今回の戦績を確定値に反映"""
    if not hasattr(st.session_state, 'current_session_stats'):
        return
    
    # 現在の統計に今回の戦績を加算
    for player, session_stats in st.session_state.current_session_stats.items():
        if player not in st.session_state.stats:
            st.session_state.stats[player] = {
                '1位': 0, '2位': 0, '3位': 0, '4位': 0,
                '総合勝ち得点': 0, '役満': 0, '跳ばし': 0, '跳び': 0
            }
        
        # 統計を加算
        for key, value in session_stats.items():
            st.session_state.stats[player][key] = st.session_state.stats[player].get(key, 0) + value
    
    # 今回の戦績をリセット
    st.session_state.current_session_stats = {}
    
    # データを保存
    save_current_state()
