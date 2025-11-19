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

# =================================================
# TAB 2: MN/MT THỨ 7 (LOGIC PHỨC TẠP)
# =================================================
with tabs[1]:
    st.subheader("Phân tích Thứ 7 (MN/MT) & So sánh MB")
    
    col_t7_1, col_t7_2, col_t7_3 = st.columns(3)
    with col_t7_1:
        # Chọn miền -> Lọc đài
        region_t7 = st.radio("Chọn Miền", ["Miền Nam", "Miền Trung"], horizontal=True)
        filter_reg = "MN" if region_t7 == "Miền Nam" else "MT"
        
        # Lọc danh sách đài thuộc miền đã chọn
        stations_t7 = [k for k, v in utils.ALL_STATIONS.items() if v["region"] == filter_reg]
        # Các đài hay quay thứ 7 (Gợi ý)
        default_t7 = []
        if filter_reg == "MN": default_t7 = ["Hồ Chí Minh", "Long An", "Bình Phước", "Hậu Giang"]
        else: default_t7 = ["Đà Nẵng", "Quảng Ngãi", "Đắk Nông"]
        
        # Chỉ lấy những đài có trong danh sách API
        valid_defaults = [s for s in default_t7 if s in stations_t7]
        station_sel = st.selectbox("Chọn đài Thứ 7", stations_t7, index=stations_t7.index(valid_defaults[0]) if valid_defaults else 0)

    with col_t7_2:
        st.write("<b>Chọn Giải để tính Nhị Hợp:</b>", unsafe_allow_html=True)
        # Mapping tên giải với index (0-17)
        prizes_labels = ["ĐB", "G1", "G2", "G3-1", "G3-2", "G4-1", "G4-2", "G4-3", "G4-4", "G4-5", "G4-6", "G4-7", "G5", "G6-1", "G6-2", "G6-3", "G7", "G8"]
        
        # Mặc định chọn không giải nào để user tự tick
        selected_prizes = st.multiselect("Tick giải:", prizes_labels, default=[])
        # Chuyển labels thành index
        selected_indices = [prizes_labels.index(p) for p in selected_prizes]

    with col_t7_3:
        st.write("<b>Cấu hình so sánh:</b>", unsafe_allow_html=True)
        lui_tuan = st.number_input("Lùi (tuần)", min_value=0, max_value=10, value=0)
        
    if st.button("⚡ Phân tích Thứ 7"):
        with st.spinner("Đang xử lý..."):
            # 1. Lấy data đài Thứ 7
            rows_mn = utils.get_data_thu7(station_sel)
            # 2. Lấy data MB full
            mb_dict = utils.get_mb_full_dict(limit=150)
            
            if not rows_mn:
                st.error("Không có dữ liệu cho đài này.")
            else:
                # Chỉ lấy tuần được chọn (lùi)
                idx_tuan = min(lui_tuan, len(rows_mn)-1)
                target_row = rows_mn[idx_tuan]
                target_date = target_row["ObjDate"]
                
                st.info(f"Đang phân tích ngày: **{target_row['Date']}** ({station_sel})")
                
                # === PHẦN 1: NHỊ HỢP ===
                nhi_hop_res = utils.analyze_nhi_hop(target_row["Prizes"], selected_indices)
                
                c_res1, c_res2 = st.columns(2)
                with c_res1:
                    st.markdown("#### 1. Kết quả Nhị Hợp")
                    if nhi_hop_res:
                        st.text_area("Dàn số tạo được:", ", ".join(nhi_hop_res), height=100)
                        # Đếm tần suất các số trong Nhị hợp
                        counts = Counter(nhi_hop_res)
                        max_cnt = max(counts.values()) if counts else 0
                        
                        # Phân loại mức
                        st.markdown("**Phân loại mức số:**")
                        levels_found = []
                        for muc in range(max_cnt, 0, -1):
                            group = [n for n, c in counts.items() if c == muc]
                            if group:
                                lv_text = utils.read_level(muc)
                                st.write(f"- Mức {lv_text} ({len(group)} số): {', '.join(group)}")
                                levels_found.extend(group)
                        
                        # Mức không (00-99 không có trong nhị hợp)
                        all_set = set(f"{i:02d}" for i in range(100))
                        missing = sorted(list(all_set - set(nhi_hop_res)))
                        st.write(f"- Mức không ({len(missing)} số): {', '.join(missing)}")
                    else:
                        st.warning("Vui lòng tick chọn ít nhất 1 giải để tính nhị hợp.")

                # === PHẦN 2: SO SÁNH VỚI MB TUẦN TIẾP THEO ===
                with c_res2:
                    st.markdown("#### 2. Đối chiếu MB (T7 -> T7 tuần sau)")
                    # Tìm 8 ngày tiếp theo (T7 này -> T7 tuần sau)
                    next_days = []
                    for i in range(8):
                        d = target_date + datetime.timedelta(days=i)
                        d_str = d.strftime("%d/%m/%Y")
                        next_days.append(d_str)
                    
                    # Kiểm tra xem các số trong Nhị Hợp có về ĐB MB trong tuần đó không
                    found_in_mb = []
                    
                    mb_check_log = []
                    for day in next_days:
                        prizes_mb = mb_dict.get(day, [])
                        if prizes_mb:
                            # Lấy ĐB MB
                            db_mb = prizes_mb[0][-2:] if prizes_mb[0] else "??"
                            mb_check_log.append(f"{day}: ĐB {db_mb}")
                            
                            if db_mb in nhi_hop_res:
                                found_in_mb.append(f"{day} (ĐB {db_mb})")
                        else:
                            mb_check_log.append(f"{day}: Chưa xổ")

                    with st.expander("Chi tiết KQMB tuần đối chiếu"):
                        st.write("\n".join(mb_check_log))
                        
                    if found_in_mb:
                        st.success(f"🎉 Đã nổ ở MB: {', '.join(found_in_mb)}")
                    else:
                        st.info("Chưa thấy nổ ở giải ĐB MB trong tuần này.")

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