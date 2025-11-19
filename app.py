import streamlit as st
import pandas as pd
import utils
from collections import Counter
import datetime

# Cấu hình trang
st.set_page_config(page_title="Siêu Gà 18+", layout="wide", page_icon="🐔")

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; font-weight: 700; color: #d90429; text-align: center; margin-bottom: 20px;}
    .block-container {padding-top: 2rem;}
    div[data-testid="stExpander"] details summary p {font-weight: bold; font-size: 1.1rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🐔 HỆ THỐNG SOI CẦU SIÊU GÀ 18+</div>', unsafe_allow_html=True)

# Menu Tabs
tabs = st.tabs([
    "📋 KQXS MB Full", 
    "🗓️ MN/MT Thứ 7", 
    "🔢 Tần Suất Dàn", 
    "🤖 Cầu Tự Động", 
    "🔗 Cặp Lô Đi Cùng"
])

# =================================================
# TAB 1: KQXS MIỀN BẮC (FULL GIẢI)
# =================================================
with tabs[0]:
    st.subheader("Kết quả XSMB (Đầy đủ các giải)")
    if st.button("Tải lại KQMB"):
        with st.spinner("Đang tải dữ liệu MB..."):
            mb_dict = utils.get_mb_full_dict(limit=100)
            if mb_dict:
                # Chuyển dict thành list để hiển thị
                data_display = []
                for date, prizes in mb_dict.items():
                    # prizes là list 27 phần tử
                    row = {"Ngày": date, "ĐB": prizes[0], "G1": prizes[1]}
                    # Gộp các giải nhỏ lại cho gọn
                    row["G2"] = ", ".join(prizes[2:4])
                    row["G3"] = ", ".join(prizes[4:10])
                    row["G4"] = ", ".join(prizes[10:14])
                    row["G5"] = ", ".join(prizes[14:20])
                    row["G6"] = ", ".join(prizes[20:23])
                    row["G7"] = ", ".join(prizes[23:27])
                    data_display.append(row)
                
                df_mb = pd.DataFrame(data_display)
                st.dataframe(df_mb, use_container_width=True, height=600)
            else:
                st.error("Không tải được dữ liệu MB.")

# --- Cột 2: Chọn Giải (Đã sửa theo yêu cầu Combo) ---
    with col_t7_2:
        st.write("<b>Chọn Giải để tính Nhị Hợp:</b>", unsafe_allow_html=True)
        
        prizes_labels = ["ĐB", "G1", "G2", "G3-1", "G3-2", "G4-1", "G4-2", "G4-3", "G4-4", "G4-5", "G4-6", "G4-7", "G5", "G6-1", "G6-2", "G6-3", "G7", "G8"]
        
        # Khởi tạo session state nếu chưa có
        if "t7_selected_prizes" not in st.session_state:
            st.session_state.t7_selected_prizes = []

        # === TẠO 2 NÚT COMBO + 1 NÚT XÓA ===
        c_btn1, c_btn2, c_btn3 = st.columns(3)
        
        # Combo 1: G1 + ĐB
        if c_btn1.button("G1 + ĐB", use_container_width=True):
            st.session_state.t7_selected_prizes = ["ĐB", "G1"]
            st.rerun()
        
        # Combo 2: G7 + G8
        if c_btn2.button("G7 + G8", use_container_width=True):
            st.session_state.t7_selected_prizes = ["G7", "G8"]
            st.rerun()

        # Nút Xóa (để reset nếu muốn chọn lại từ đầu)
        if c_btn3.button("❌ Xóa", use_container_width=True):
            st.session_state.t7_selected_prizes = []
            st.rerun()

        # Multiselect liên kết với session_state
        selected_prizes = st.multiselect(
            "Danh sách giải đang chọn:", 
            prizes_labels, 
            key="t7_selected_prizes"
        )
        
        # Chuyển labels thành index để xử lý
        selected_indices = [prizes_labels.index(p) for p in selected_prizes]

# =================================================
# TAB 3: TẦN SUẤT DÀN SỐ
# =================================================
with tabs[2]:
    st.subheader("Đếm tần suất từ dàn số")
    
    txt_input = st.text_area("Nhập dàn số (copy paste vào đây):", height=150, placeholder="Ví dụ: 01 02 03, 04 05...")
    
    if txt_input:
        # Xử lý chuỗi
        raw_nums = []
        for x in txt_input.replace(",", " ").replace(".", " ").split():
            s = x.strip()
            if s.isdigit() and len(s) <= 2: # Chấp nhận số 1 chữ số
                raw_nums.append(s.zfill(2))
        
        if raw_nums:
            counter = Counter(raw_nums)
            max_c = max(counter.values())
            
            col_ts1, col_ts2 = st.columns(2)
            
            with col_ts1:
                st.markdown("### Kết quả phân mức")
                for muc in range(max_c, 0, -1):
                    grp = sorted([n for n, c in counter.items() if c == muc])
                    if grp:
                        lv_name = utils.read_level(muc)
                        st.write(f"**Mức {lv_name} ({len(grp)} số):**")
                        st.code(" ".join(grp))
                
                # Mức 0
                all_nums = set(f"{i:02d}" for i in range(100))
                exist = set(raw_nums)
                missing = sorted(list(all_nums - exist))
                st.write(f"**Mức không ({len(missing)} số):**")
                st.code(" ".join(missing))
                
            with col_ts2:
                st.markdown("### Biểu đồ")
                df_chart = pd.DataFrame(list(counter.items()), columns=["Số", "Lần"])
                st.bar_chart(df_chart.set_index("Số"))

# =================================================
# TAB 4: CẦU TỰ ĐỘNG (GIỮ NGUYÊN)
# =================================================
with tabs[3]:
    st.subheader("Quét Cầu PASCAL / POSPAIR")
    c1, c2, c3 = st.columns(3)
    with c1:
        s_cau = st.selectbox("Đài soi cầu", list(utils.ALL_STATIONS.keys()), index=0)
    with c2:
        method = st.selectbox("Thuật toán", ["POSPAIR", "PASCAL"])
    with c3:
        min_str = st.number_input("Streak (chuỗi) tối thiểu", value=3, min_value=1)
    
    if st.button("🚀 Quét Cầu"):
        u = utils.ALL_STATIONS[s_cau]["url"]
        with st.spinner(f"Đang chạy thuật toán {method} trên đài {s_cau}..."):
            results = utils.scan_cau_dong(u, method=method, min_streak=min_str)
            if results:
                df_res = pd.DataFrame(results)
                st.success(f"Tìm thấy {len(results)} cầu!")
                st.dataframe(df_res.style.applymap(lambda x: 'font-weight: bold; color: blue', subset=['Dự đoán']), use_container_width=True)
            else:
                st.warning("Không tìm thấy cầu nào.")

# =================================================
# TAB 5: CẶP LÔ ĐI CÙNG (GIỮ NGUYÊN)
# =================================================
with tabs[4]:
    st.subheader("Phân tích Cặp Lô Đi Cùng")
    
    col_inp1, col_inp2, col_inp3 = st.columns(3)
    with col_inp1:
        target_lo = st.text_input("Nhập Lô mục tiêu (VD: 68)", max_chars=2)
    with col_inp2:
        region_opt = st.selectbox("Khu vực", ["MB (Miền Bắc)", "MN (Miền Nam)", "MT (Miền Trung)", "ALL (Tất cả)"])
        region_code = {"MB (Miền Bắc)": "MB", "MN (Miền Nam)": "MN", "MT (Miền Trung)": "MT", "ALL (Tất cả)": "ALL"}[region_opt]
    with col_inp3:
        mode_opt = st.radio("Chế độ đếm", ["Theo ngày (Không trùng)", "Theo lần xuất hiện (Có trùng)"])
        mode_code = "day" if "ngày" in mode_opt else "hit"

    if st.button("🔍 Phân tích ngay"):
        if not target_lo or not target_lo.isdigit() or len(target_lo) != 2:
            st.error("Vui lòng nhập đúng định dạng 2 chữ số.")
        else:
            my_bar = st.progress(0, text="Đang khởi tạo...")
            freq_list, logs = utils.scan_cap_lo_di_cung(
                target_lo, region_code, mode_code, 
                progress_callback=lambda prog, msg: my_bar.progress(prog, text=msg)
            )
            my_bar.empty()

            if freq_list is None:
                st.error(logs)
            elif not freq_list:
                st.warning(f"Không tìm thấy số {target_lo} trong lịch sử.")
            else:
                st.success(f"Tìm thấy {target_lo} trong {len(logs)} kỳ.")
                res_c1, res_c2 = st.columns([1, 2])
                with res_c1:
                    st.write(f"**Top số hay về cùng {target_lo}:**")
                    df_freq = pd.DataFrame(freq_list)
                    # Fix lỗi matplotlib nếu chưa cài: chỉ hiển thị bảng thường
                    st.dataframe(df_freq, use_container_width=True, height=400)
                with res_c2:
                    st.write("**Nhật ký xuất hiện:**")

                    st.dataframe(pd.DataFrame(logs), use_container_width=True, height=400)


