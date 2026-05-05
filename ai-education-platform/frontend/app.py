"""AI 教育知識庫系統 - 前端佈局"""
import streamlit as st
import sys
import os

# 確保路徑正確
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 頁面配置
st.set_page_config(
    page_title="AI 教育知識庫系統",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 主標題
st.title("🎓 AI 教育知識庫系統")
st.markdown("**校本 AI 教學操作系統 (School AI OS)**")
st.markdown("---")

# 側邊欄 - 功能導航
with st.sidebar:
    st.header("功能導航")
    
    page = st.radio(
        "選擇功能",
        [
            "🏠 首頁",
            "📚 知識庫",
            "💬 AI 問答",
            "📝 AI 出題",
            "✅ AI 批改",
            "📊 學習分析",
            "👨‍🏫 教師工具",
            "⚙️ 設置"
        ]
    )

# 根據選擇的功能顯示不同內容
if page == "🏠 首頁":
    st.header("歡迎使用 AI 教育知識庫系統")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 知識庫文檔", "1,234")
        st.caption("已上傳教材數量")
    
    with col2:
        st.metric("💬 問答記錄", "5,678")
        st.caption("已回答問題數量")
    
    with col3:
        st.metric("📝 生成試卷", "89")
        st.caption("AI 生成試卷數量")
    
    st.markdown("---")
    st.subheader("🚀 快速開始")
    
    quick_start = st.columns(3)
    
    with quick_start[0]:
        if st.button("上傳教材", use_container_width=True):
            st.info("點擊上傳 PDF/Word/PPT 格式教材")
    
    with quick_start[1]:
        if st.button("開始問答", use_container_width=True):
            st.info("輸入問題獲取 AI 解答")
    
    with quick_start[2]:
        if st.button("生成試卷", use_container_width=True):
            st.info("選擇課題和難度生成試卷")

elif page == "📚 知識庫":
    st.header("📚 知識庫管理")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔍 搜索知識庫", placeholder="輸入關鍵詞搜索...")
    
    with col2:
        filter_type = st.selectbox("篩選類型", ["全部", "教材", "教案", "試卷"])
    
    st.markdown("---")
    
    # 知識庫列表
    st.subheader("📁 已上傳文檔")
    
    docs = [
        {"name": "中三中文閱讀理解教材.pdf", "type": "教材", "size": "2.5MB", "chunks": 156},
        {"name": "DSE 數學試卷範例.docx", "type": "試卷", "size": "1.2MB", "chunks": 89},
        {"name": "教師教案模板.docx", "type": "教案", "size": "0.5MB", "chunks": 34},
    ]
    
    for doc in docs:
        with st.expander(f"📄 {doc['name']}"):
            st.write(f"**類型**: {doc['type']}")
            st.write(f"**大小**: {doc['size']}")
            st.write(f"**Chunk 數量**: {doc['chunks']}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.button("🔍 查看內容", key=f"view_{doc['name']}")
            with col_btn2:
                st.button("🗑️ 刪除", key=f"delete_{doc['name']}")

elif page == "💬 AI 問答":
    st.header("💬 AI 智能問答")
    
    # 模式選擇
    mode = st.radio(
        "問答模式",
        ["👨‍🎓 學生模式", "👨‍🏫 教師模式", "👨‍👩‍👧 家長模式"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # 對話框
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 顯示歷史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # 輸入框
    if prompt := st.chat_input("輸入您的問題..."):
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # AI 回覆
        with st.chat_message("assistant"):
            response = f"這是 AI 的回覆：{prompt}"
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.button("🗑️ 清除對話"):
        st.session_state.messages = []
        st.rerun()

elif page == "📝 AI 出題":
    st.header("📝 AI 評估與出題")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.selectbox(
            "選擇課題",
            ["選擇課題...", "中三中文閱讀理解", "DSE 數學", "TSA 英文", "自主命題"]
        )
        
        if topic == "自主命題":
            custom_topic = st.text_input("輸入課題")
        
        difficulty = st.slider("難度", 1, 5, 3)
        question_count = st.number_input("題目數量", 5, 50, 10)
    
    with col2:
        exam_type = st.selectbox("考試類型", ["學校測驗", "DSE", "TSA"])
        question_types = st.multiselect(
            "題型",
            ["選擇題", "填空題", "問答題", "作文"],
            default=["選擇題"]
        )
    
    st.markdown("---")
    
    if st.button("🚀 生成試卷", use_container_width=True):
        st.success("試卷生成中...")
        st.info("AI 正在根據您的設置生成試卷...")
        
        # 顯示生成結果
        st.subheader("生成的試卷")
        
        for i in range(min(3, question_count)):
            with st.expander(f"題目 {i+1}"):
                st.write(f"這是第 {i+1} 題的內容...")
                
                if "選擇題" in question_types:
                    st.radio("選擇答案", ["A", "B", "C", "D"], horizontal=True)

elif page == "✅ AI 批改":
    st.header("✅ AI 智能批改")
    
    st.info("上傳學生作業或選擇已有作業進行 AI 批改")
    
    uploaded_file = st.file_uploader(
        "上傳學生作業",
        type=["pdf", "docx", "txt"],
        help="支援 PDF、Word、TXT 格式"
    )
    
    if uploaded_file:
        st.success(f"已上傳: {uploaded_file.name}")
        
        if st.button("開始批改"):
            st.info("AI 正在批改中，請稍候...")
            
            st.subheader("批改結果")
            
            col_score1, col_score2, col_score3 = st.columns(3)
            
            with col_score1:
                st.metric("總分", "85/100")
            
            with col_score2:
                st.metric("正確率", "85%")
            
            with col_score3:
                st.metric("預計等第", "B")
            
            st.markdown("---")
            
            st.subheader("📋 詳細反饋")
            st.write("**錯題分析**:")
            st.write("- 第 3 題：理解偏差，需要加強閱讀理解訓練")
            st.write("- 第 7 題：計算錯誤，注意驗算")
            
            st.write("**改進建議**:")
            st.write("1. 建議複習第三章內容")
            st.write("2. 增加閱讀練習")
            st.write("3. 練習答題技巧")

elif page == "📊 學習分析":
    st.header("📊 學習歷程與分析")
    
    # 學生選擇
    student_id = st.selectbox("選擇學生", ["S001 - 陳小明", "S002 - 李大同", "S003 - 王小華"])
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 學習趨勢")
        st.line_chart([1, 2, 3, 4, 5], height=200)
    
    with col_chart2:
        st.subheader("📊 課題掌握度")
        st.bar_chart([0.8, 0.6, 0.9, 0.5, 0.7], height=200)
    
    st.markdown("---")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.subheader("💪 強項")
        st.success("中文閱讀理解 - 掌握度 85%")
        st.success("寫作技巧 - 掌握度 78%")
    
    with col_info2:
        st.subheader("⚠️ 弱項")
        st.warning("數學應用題 - 掌握度 45%")
        st.warning("英文語法 - 掌握度 52%")
    
    st.markdown("---")
    
    st.subheader("🎯 學習建議")
    st.info("1. 每天練習 10 道數學應用題")
    st.info("2. 每週完成 2 篇英語閱讀")
    st.info("3. 建議參加課後輔導")

elif page == "👨‍🏫 教師工具":
    st.header("👨‍🏫 教師支援系統")
    
    col_tool1, col_tool2, col_tool3 = st.columns(3)
    
    with col_tool1:
        st.button("📋 AI 教案生成", use_container_width=True)
        st.caption("根據課題自動生成教案")
    
    with col_tool2:
        st.button("📊 班級分析報告", use_container_width=True)
        st.caption("查看班級整體學習情況")
    
    with col_tool3:
        st.button("👥 學生分組管理", use_container_width=True)
        st.caption("按能力分組進行教學")

elif page == "⚙️ 設置":
    st.header("⚙️ 系統設置")
    
    st.subheader("API 配置")
    
    st.text_input("OpenAI API Key", type="password")
    st.text_input("向量數據庫 URL", value="postgresql://localhost:5432/ai_education")
    
    st.subheader("學校配置")
    st.text_input("學校名稱")
    st.text_input("學校編碼")
    
    st.subheader("LMS 整合")
    st.selectbox("LMS 類型", ["Google Classroom", "Microsoft Teams", "Moodle", "其他"])
    
    st.markdown("---")
    
    if st.button("💾 保存設置", use_container_width=True):
        st.success("設置已保存")

# 頁腳
st.markdown("---")
st.markdown("**AI 教育知識庫系統 v1.0** | 基於香港教育局「智啟學教」政策")
st.markdown("© 2024 genz3000. All rights reserved.")