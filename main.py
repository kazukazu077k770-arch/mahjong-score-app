"""
麻雀スコア管理アプリケーション - 統合版
"""
import streamlit as st
from modules.data_init import init_app_state
from components.styles import load_mobile_css
from pages.score_entry import show_mobile_score_entry

def setup_page_config():
    """ページ設定"""
    st.set_page_config(
        page_title="🀄 麻雀スコア管理",
        page_icon="🀄",
        layout="centered",
        initial_sidebar_state="collapsed"  # サイドバーを非表示
    )

def main():
    """アプリケーションのメインエントリーポイント"""
    # ページ設定
    setup_page_config()
    
    # アプリケーション状態の初期化
    init_app_state()
    
    # モバイル特化CSSの適用
    load_mobile_css()
    
    # メインインターフェース表示
    show_mobile_score_entry()

if __name__ == "__main__":
    main()
