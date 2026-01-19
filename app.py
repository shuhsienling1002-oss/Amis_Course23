import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 23: O Hekal", page_icon="🏞️", layout="centered")

# --- CSS 美化 (自然綠色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #43A047;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #1B5E20; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F1F8E9;
        border-left: 5px solid #81C784;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #C8E6C9; color: #1B5E20; border: 2px solid #43A047; padding: 12px;
    }
    .stButton>button:hover { background-color: #A5D6A7; border-color: #2E7D32; }
    .stProgress > div > div > div > div { background-color: #43A047; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 23: 14個單字 - 句子提取的新詞) ---
vocab_data = [
    {"amis": "Hekal", "chi": "世界 / 外部", "icon": "🌍", "source": "Row 2204"},
    {"amis": "Kanatal", "chi": "國家 / 島嶼", "icon": "🗾", "source": "Row 2204"},
    {"amis": "Cidal", "chi": "太陽", "icon": "☀️", "source": "Row 732"},
    {"amis": "La'eno", "chi": "下方 / 底部", "icon": "⬇️", "source": "Row 732"},
    {"amis": "Kakarayan", "chi": "天空", "icon": "☁️", "source": "Row 798"},
    {"amis": "Ma'efer", "chi": "飛", "icon": "🦅", "source": "Row 798"},
    {"amis": "Ma'orad", "chi": "下雨", "icon": "🌧️", "source": "Row 259"},
    {"amis": "Mikilidong", "chi": "躲雨 / 遮蔽", "icon": "☂️", "source": "Row 259"},
    {"amis": "Fanaw", "chi": "池塘", "icon": "💧", "source": "Row 1453"},
    {"amis": "Miparakar", "chi": "放魚籠(陷阱)", "icon": "🎣", "source": "Row 1453"},
    {"amis": "Talariyar", "chi": "去海邊", "icon": "🌊", "source": "Row 223"},
    {"amis": "Mifoting", "chi": "捕魚", "icon": "🐟", "source": "Row 223"},
    {"amis": "Folad", "chi": "月亮 / 月份", "icon": "🌙", "source": "Row 1815"},
    {"amis": "Matayal", "chi": "工作 / 勞動", "icon": "⚒️", "source": "Row 732"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "O samakapahay a kanatal i hekal ko Taiwan.", "chi": "台灣是世界上最美麗的國家。", "icon": "🇹🇼", "source": "Row 2204"},
    {"amis": "Tahakowa kami a matayal i la'eno no cidal?", "chi": "我們在太陽下要工作到何時？", "icon": "☀️", "source": "Row 732"},
    {"amis": "Ma'efer kako i kakarayan.", "chi": "我在天空飛翔。", "icon": "🦅", "source": "Row 798"},
    {"amis": "Ano ma'orad 'i, mikilidong kita i kala'eno no kilang.", "chi": "如果下雨呢，我們就去樹下躲避。", "icon": "🌳", "source": "Row 259"},
    {"amis": "Miparakar i fanaw.", "chi": "在池塘放魚籠陷阱。", "icon": "🎣", "source": "Row 1453"},
    {"amis": "Talariyar a mifoting ci mama.", "chi": "爸爸去海上捕魚。", "icon": "🌊", "source": "Row 223"},
    {"amis": "Minokay kako i nacila a folad.", "chi": "我上個月(昨天的月亮)回家。", "icon": "🌙", "source": "Row 1815"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "O samakapahay a kanatal i hekal ko Taiwan.",
        "audio": "O samakapahay a kanatal i hekal ko Taiwan",
        "options": ["台灣是世界上最美的國家", "台灣是很大的島", "台灣有很多山"],
        "ans": "台灣是世界上最美的國家",
        "hint": "Kanatal (國家), Hekal (世界) (Row 2204)"
    },
    {
        "q": "Ano ma'orad 'i, mikilidong kita...",
        "audio": "Ano ma'orad 'i, mikilidong kita",
        "options": ["如果下雨，我們去躲雨", "如果出太陽，我們去游泳", "如果颳風，我們回家"],
        "ans": "如果下雨，我們去躲雨",
        "hint": "Ma'orad (下雨), Mikilidong (躲避) (Row 259)"
    },
    {
        "q": "單字測驗：Miparakar",
        "audio": "Miparakar",
        "options": ["放魚籠/陷阱", "游泳", "洗澡"],
        "ans": "放魚籠/陷阱",
        "hint": "在 Fanaw 做的事 (Row 1453)"
    },
    {
        "q": "單字測驗：La'eno",
        "audio": "La'eno",
        "options": ["下方", "上方", "裡面"],
        "ans": "下方",
        "hint": "Row 732: i la'eno no cidal (在太陽下)"
    },
    {
        "q": "Tahakowa kami a matayal i la'eno no cidal?",
        "audio": "Tahakowa kami a matayal i la'eno no cidal",
        "options": ["我們在太陽下工作到何時？", "我們在樹下休息到何時？", "我們在家裡睡到何時？"],
        "ans": "我們在太陽下工作到何時？",
        "hint": "Matayal (工作), Cidal (太陽)"
    },
    {
        "q": "單字測驗：Kanatal",
        "audio": "Kanatal",
        "options": ["國家/島嶼", "海洋", "城市"],
        "ans": "國家/島嶼",
        "hint": "Taiwan o kanatal (Row 2204)"
    },
    {
        "q": "單字測驗：Ma'efer",
        "audio": "Ma'efer",
        "options": ["飛", "跑", "跳"],
        "ans": "飛",
        "hint": "在 Kakarayan (天空) 的動作 (Row 798)"
    },
    {
        "q": "Talariyar a mifoting ci mama.",
        "audio": "Talariyar a mifoting ci mama",
        "options": ["爸爸去海邊捕魚", "爸爸去山上打獵", "爸爸去河邊玩水"],
        "ans": "爸爸去海邊捕魚",
        "hint": "Tala-riyar (去海邊) (Row 223)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #1B5E20;'>Unit 23: O Hekal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>大自然與環境 (CSV Extracted)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (從句子提取)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #1B5E20;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #C8E6C9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #1B5E20;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經掌握這些自然詞彙了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
