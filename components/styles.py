"""
CSSスタイル管理モジュール
"""
import streamlit as st

def load_mobile_css():
    """CSSスタイルをロードする"""
    css_content = """
    <style>
    /* モバイル専用スタイル */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f5f7fa !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* メインコンテナ */
    .main .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
        margin: 0 !important;
    }
    
    /* タイトル - 通常サイズ */
    h1 {
        font-size: 1.8rem !important;
        margin: 0.5rem 0 1rem 0 !important;
        text-align: center;
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 1.2rem !important;
        margin: 1rem 0 0.5rem 0 !important;
        color: #34495e !important;
        font-weight: 600 !important;
    }
    
    /* 2×2グリッドレイアウト強制 */
    .mobile-grid-container {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
        width: 100% !important;
    }
    
    [data-testid="column"] {
        width: 50% !important;
        margin-bottom: 1rem !important;
        padding: 0.5rem !important;
    }
    
    /* プレイヤー名表示 */
    .player-name, strong {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* 点数入力フィールド - 大きなタッチターゲット */
    .stNumberInput > div > div > input {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 0.8rem !important;
        border: 2px solid #bdc3c7 !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        width: 100% !important;
        min-height: 60px !important;
        box-sizing: border-box !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3498db !important;
        background: white !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.15) !important;
        outline: none !important;
    }
    
    /* プラスマイナスボタン - 大きなタッチターゲット */
    .stNumberInput > div > div > div > button {
        width: 44px !important;
        height: 44px !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border: 2px solid #bdc3c7 !important;
        background: #ecf0f1 !important;
        color: #2c3e50 !important;
        margin: 2px !important;
    }
    
    .stNumberInput > div > div > div > button:hover,
    .stNumberInput > div > div > div > button:active {
        background: #3498db !important;
        color: white !important;
        border-color: #3498db !important;
        transform: scale(1.05) !important;
    }
    
    /* セレクトボックス - 大きなタッチターゲットと表示改善 */
    .stSelectbox > div > div > select {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border: 2px solid #bdc3c7 !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        min-height: 50px !important;
        width: 100% !important;
        text-align: center !important;
        color: #2c3e50 !important;
        -webkit-appearance: none !important;
        appearance: none !important;
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e") !important;
        background-repeat: no-repeat !important;
        background-position: right 12px center !important;
        background-size: 16px !important;
        cursor: pointer !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #3498db !important;
        background-color: white !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.15) !important;
        outline: none !important;
    }
    
    /* セレクトボックスのオプション表示改善 */
    .stSelectbox > div > div > select option {
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
        background: white !important;
        color: #2c3e50 !important;
    }
    
    /* セレクトボックスのドロップダウン位置調整 */
    .stSelectbox > div {
        position: relative !important;
        z-index: 1000 !important;
    }
    
    /* 合計点数表示 */
    .total-card {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.25) !important;
        font-size: 1rem !important;
    }
    
    .total-card.warning {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.25) !important;
    }
    
    /* 記録ボタン - 大きなタッチターゲット */
        /* ボタンスタイル */
    [data-testid="stButton"] button {
        width: 100% !important;
        min-height: 48px !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        margin: 0.3rem 0 !important;
        touch-action: manipulation !important;
    }
    
    /* 役満祝儀の±ボタン専用スタイル */
    [data-testid="stButton"] button:contains("➖"),
    [data-testid="stButton"] button:contains("➕") {
        min-height: 40px !important;
        width: 40px !important;
        font-size: 1.2rem !important;
        border-radius: 50% !important;
        background-color: #e9ecef !important;
        color: #495057 !important;
        border: 2px solid #dee2e6 !important;
        padding: 0 !important;
        margin: 0.2rem 0 !important;
    }
    
    [data-testid="stButton"] button:contains("➕") {
        background-color: #d4edda !important;
        border-color: #c3e6cb !important;
        color: #155724 !important;
    }
    
    [data-testid="stButton"] button:contains("➖") {
        background-color: #f8d7da !important;
        border-color: #f5c6cb !important;
        color: #721c24 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.25) !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:active {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(231, 76, 60, 0.3) !important;
    }
    
    .stButton > button:disabled {
        background: #95a5a6 !important;
        color: white !important;
        opacity: 0.7 !important;
        cursor: not-allowed !important;
    }
    
    /* エキスパンダー */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #34495e, #2c3e50) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }
    
    /* テキスト入力 */
    .stTextInput > div > div > input {
        font-size: 1rem !important;
        padding: 0.8rem !important;
        border: 2px solid #bdc3c7 !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        min-height: 48px !important;
        text-align: center !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db !important;
        background: white !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.15) !important;
        outline: none !important;
    }
    
    /* 統計テーブル */
    .dataframe {
        width: 100% !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 12px 8px !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe td {
        text-align: center !important;
        padding: 10px 6px !important;
        border-bottom: 1px solid #ecf0f1 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* 2×2グリッド専用の追加CSS */
    @media (max-width: 768px) {
        /* モバイルで2×2グリッドを確実にする */
        .row-widget.stColumns {
            display: flex !important;
            flex-wrap: wrap !important;
            width: 100% !important;
        }
        
        .row-widget.stColumns > div {
            flex: 0 0 50% !important;
            max-width: 50% !important;
            padding: 0.5rem !important;
            box-sizing: border-box !important;
        }
        
        /* セレクトボックスの選択肢表示位置を中央に */
        .stSelectbox select {
            position: relative !important;
        }
        
        /* iOS Safari対応 */
        .stSelectbox > div > div > select {
            -webkit-appearance: none !important;
            border-radius: 8px !important;
        }
    }
    
    /* フォントサイズの調整 */
    .element-container, .stMarkdown, .stText {
        font-size: 1rem !important;
    }
    
    /* サイドバーの調整 */
    .css-1d391kg {
        background-color: white !important;
        padding: 1rem !important;
    }
    
    /* レスポンシブな余白 */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        .stNumberInput > div > div > input {
            min-height: 50px !important;
            font-size: 1.1rem !important;
        }
    }
    </style>
    """
    
    st.markdown(css_content, unsafe_allow_html=True)
