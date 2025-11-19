import requests
import json
import pandas as pd
from collections import Counter, defaultdict
import datetime
import itertools

# ==== 1. KHAI BÁO API ====
# Danh sách API đầy đủ
ALL_STATIONS = {
    # -- Miền Bắc --
    "Miền Bắc": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=200&gameCode=miba", "region": "MB"},
    # -- Miền Nam --
    "Hồ Chí Minh": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=tphc", "region": "MN"},
    "Đồng Tháp": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=doth", "region": "MN"},
    "Cà Mau": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=cama", "region": "MN"},
    "Bến Tre": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=betr", "region": "MN"},
    "Vũng Tàu": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=vuta", "region": "MN"},
    "Bạc Liêu": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=bali", "region": "MN"},
    "Đồng Nai": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=dona", "region": "MN"},
    "Cần Thơ": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=cath", "region": "MN"},
    "Sóc Trăng": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=sotr", "region": "MN"},
    "Tây Ninh": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=tani", "region": "MN"},
    "An Giang": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=angi", "region": "MN"},
    "Bình Thuận": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=bith", "region": "MN"},
    "Vĩnh Long": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=vilo", "region": "MN"},
    "Bình Dương": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=bidu", "region": "MN"},
    "Trà Vinh": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=trvi", "region": "MN"},
    "Long An": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=loan", "region": "MN"},
    "Bình Phước": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=biph", "region": "MN"},
    "Hậu Giang": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=hagi", "region": "MN"},
    "Tiền Giang": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=tigi", "region": "MN"},
    "Kiên Giang": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=kigi", "region": "MN"},
    "Đà Lạt": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=dalat", "region": "MN"},
    # -- Miền Trung --
    "Đà Nẵng": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=dana", "region": "MT"},
    "Khánh Hòa": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=khho", "region": "MT"},
    "Đắk Lắk": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=dalak", "region": "MT"},
    "Quảng Nam": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=quna", "region": "MT"},
    "Bình Định": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=bidi", "region": "MT"},
    "Quảng Trị": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=qutr", "region": "MT"},
    "Quảng Bình": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=qubi", "region": "MT"},
    "Gia Lai": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=gila", "region": "MT"},
    "Ninh Thuận": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=nith", "region": "MT"},
    "Quảng Ngãi": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=qung", "region": "MT"},
    "Đắk Nông": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=dano", "region": "MT"},
    "Kon Tum": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=kotu", "region": "MT"},
    "Thừa Thiên Huế": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=thth", "region": "MT"},
    "Phú Yên": {"url": "https://www.kqxs88.live/api/front/open/lottery/history/list/game?limitNum=60&gameCode=phye", "region": "MT"},
}

# ==== 2. HELPER FUNCTIONS ====
def fetch_data(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json().get("t", {}).get("issueList", [])
    except:
        return []

def flatten_detail_to_18(detail_json):
    """Chuyển detail thành list 18 giải (form MN/MT)"""
    numbers = []
    for field in detail_json:
        for x in field.split(","):
            x = x.strip().replace('"', '').replace("'", "")
            if x:
                numbers.append(x)
    numbers = numbers[:18]
    if len(numbers) < 18:
        numbers += [""] * (18 - len(numbers))
    return numbers

def parse_detail_all(detail_str):
    """Lấy tất cả số, không cắt"""
    try:
        data = json.loads(detail_str)
        numbers = []
        for field in data:
            for x in field.split(","):
                x = x.strip().replace('"', '').replace("'", "")
                if x:
                    numbers.append(x)
        return numbers
    except:
        return []

def get_last2(s):
    s = str(s).strip()
    if len(s) >= 2 and s.isdigit():
        return s[-2:]
    return None

# ==== 3. LOGIC TAB MN/MT THỨ 7 ====
def get_data_thu7(station_name):
    """Lấy dữ liệu chỉ các ngày Thứ 7 của đài"""
    if station_name not in ALL_STATIONS: return []
    url = ALL_STATIONS[station_name]["url"]
    
    data = fetch_data(url)
    rows = []
    for item in data:
        date_str = item['turnNum']
        try:
            d = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            if d.weekday() == 5: # Thứ 7
                detail = json.loads(item['detail'])
                prizes = flatten_detail_to_18(detail)
                rows.append({
                    "Date": date_str,
                    "ObjDate": d,
                    "Prizes": prizes
                })
        except:
            pass
    return rows

def get_mb_full_dict(limit=100):
    """Lấy dict KQMB {ngày: [list 27 giải]}"""
    url = ALL_STATIONS["Miền Bắc"]["url"]
    data = fetch_data(url)
    mb_dict = {}
    for item in data:
        try:
            detail = json.loads(item['detail'])
            prizes = []
            for field in detail:
                prizes += field.split(",")
            prizes = (prizes + [""] * 27)[:27]
            mb_dict[item['turnNum']] = prizes
        except:
            pass
    return mb_dict

def analyze_nhi_hop(prizes, selected_indices):
    """Tính nhị hợp từ các giải được chọn"""
    digits = ""
    for idx in selected_indices:
        if idx < len(prizes):
            digits += str(prizes[idx])
    
    if not digits: return []
    # Tạo nhị hợp (cặp 2 số từ các chữ số có trong giải)
    # Lưu ý: Logic gốc dùng itertools.product(digits, repeat=2) -> "12" -> 11, 12, 21, 22
    nhi_hop = sorted(set(f"{a}{b}" for a, b in itertools.product(digits, repeat=2)))
    return nhi_hop

def read_level(level):
    digit_map = {'0': "không", '1': "một", '2': "hai", '3': "ba", '4': "bốn",
                 '5': "năm", '6': "sáu", '7': "bảy", '8': "tám", '9': "chín"}
    return ''.join(digit_map.get(ch, ch) for ch in str(level))

# ==== 4. LOGIC TAB CẦU TỰ ĐỘNG ====
def algo_pascal(s_a, s_b):
    base = (s_a or "") + (s_b or "")
    base = "".join([c for c in base if c.isdigit()])
    if len(base) < 2: return (None, None)
    arr = [int(ch) for ch in base]
    while len(arr) > 2:
        nxt = [(arr[i] + arr[i+1]) % 10 for i in range(len(arr)-1)]
        arr = nxt
    return (f"{arr[0]}{arr[1]}", f"{arr[1]}{arr[0]}")

def scan_cau_dong(url, method="POSPAIR", depth=30, min_streak=2):
    issues = fetch_data(url)
    if not issues: return []
    issues = issues[:depth][::-1] 
    days = []
    for it in issues:
        raw = parse_detail_all(it.get("detail", "[]"))
        los = set([get_last2(s) for s in raw if get_last2(s)])
        days.append({"date": it.get("turnNum"), "raw": raw, "los": los})
    if len(days) < 2: return []

    limit_pos = min(len(days[-1]["raw"]), 20) 
    results = []
    for i in range(limit_pos):
        for j in range(i+1, limit_pos):
            hits = []
            for k in range(len(days)-1):
                curr_raw = days[k]["raw"]
                next_los = days[k+1]["los"]
                val_a = curr_raw[i] if i < len(curr_raw) else ""
                val_b = curr_raw[j] if j < len(curr_raw) else ""
                
                pred_ab, pred_ba = (None, None)
                if method == "PASCAL":
                    pred_ab, pred_ba = algo_pascal(val_a, val_b)
                else: # POSPAIR
                    da = val_a[-1] if val_a and val_a[-1].isdigit() else None
                    db = val_b[-1] if val_b and val_b[-1].isdigit() else None
                    if da and db: pred_ab, pred_ba = da+db, db+da
                
                if pred_ab:
                    hits.append((pred_ab in next_los) or (pred_ba in next_los))
                else:
                    hits.append(False)
            
            streak = 0
            for h in reversed(hits):
                if h: streak += 1
                else: break
            
            if streak >= min_streak:
                last_raw = days[-1]["raw"]
                v_a = last_raw[i] if i < len(last_raw) else ""
                v_b = last_raw[j] if j < len(last_raw) else ""
                p_ab, p_ba = (None, None)
                if method == "PASCAL":
                    p_ab, p_ba = algo_pascal(v_a, v_b)
                elif method == "POSPAIR":
                    da = v_a[-1] if v_a and v_a[-1].isdigit() else ""
                    db = v_b[-1] if v_b and v_b[-1].isdigit() else ""
                    if da and db: p_ab, p_ba = da+db, db+da
                
                if p_ab:
                    results.append({
                        "Vị trí": f"Pos {i} - Pos {j}",
                        "Kiểu": method,
                        "Streak": streak,
                        "Dự đoán": f"{p_ab} - {p_ba}"
                    })
    results.sort(key=lambda x: x["Streak"], reverse=True)
    return results

# ==== 5. LOGIC CẶP LÔ ĐI CÙNG ====
def scan_cap_lo_di_cung(target, region_filter, mode_count="day", progress_callback=None):
    urls_to_scan = []
    for name, info in ALL_STATIONS.items():
        if region_filter == "ALL" or info["region"] == region_filter:
            urls_to_scan.append((name, info["url"]))
    
    if not urls_to_scan: return None, "Không có đài nào."

    co_counter = Counter()
    details_log = []
    total = len(urls_to_scan)
    
    for idx, (station_name, url) in enumerate(urls_to_scan):
        if progress_callback: progress_callback(idx / total, f"Quét {station_name}...")
        issues = fetch_data(url)
        for item in issues:
            raw = parse_detail_all(item.get("detail", "[]"))
            los_raw = [get_last2(x) for x in raw if get_last2(x)]
            if target in los_raw:
                others = [x for x in los_raw if x != target]
                if mode_count == "day":
                    unique_others = set(others)
                    co_counter.update(unique_others)
                    nums_str = ", ".join(sorted(unique_others))
                else:
                    co_counter.update(others)
                    nums_str = ", ".join(sorted(others))
                details_log.append({"Ngày": item.get("turnNum"), "Đài": station_name, "Số về cùng": nums_str})

    if progress_callback: progress_callback(1.0, "Hoàn tất!")
    if not details_log: return [], []
    
    freq_data = [{"Số đi cùng": num, "Lần gặp": count} for num, count in co_counter.most_common()]
    return freq_data, details_log