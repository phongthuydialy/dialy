import streamlit as st
import os
import pandas as pd
import streamlit.components.v1 as components
import math
from datetime import date, timedelta, datetime
import pytz
import numpy as np
import random
import requests

st.set_page_config(layout="wide")
def main():
    
    st.markdown("""
    <div style="background:linear-gradient(90deg,#f9d423,#ff4e50);padding:24px 8px 20px 8px;border-radius:16px;margin-bottom:24px;">
        <h1 style='color:white;text-align:center;margin:0;font-size:36px;'>🔯 ỨNG DỤNG  ĐỊA LÝ </h1>
        <p style='color:white;text-align:center;font-size:20px;margin:0;'>Kết hợp Địa mạch, số liệu Từ trường</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 1.PHONG THỦY ĐỊA LÝ – BẢN ĐỒ ĐỊA MẠCH
    """)
    
    # Khởi tạo session state
    if "selected_idx" not in st.session_state:
        st.session_state.selected_idx = None
    # Thư mục chứa HTML
    html_dir = "dulieu"
    html_files = sorted([f for f in os.listdir(html_dir) if f.endswith(".html")])
    df = pd.DataFrame({"Tên công trình": html_files})
    # Phân trang
    per_page = 5
    total_pages = math.ceil(len(df) / per_page)
    page = st.number_input(f"📄 Trang (1–{total_pages}):", min_value=1, max_value=total_pages, value=1, step=1)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    df_page = df.iloc[start_idx:end_idx]
    # Hiển thị danh sách từng trang
    for i, (_, row) in enumerate(df_page.iterrows()):
        idx = start_idx + i
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"🔸 **{row['Tên công trình']}**")
        with col2:
            if st.button("Xem", key=row['Tên công trình']):
                st.session_state.selected_idx = idx
    
    
    
    
    # Hiển thị bản đồ
    if "selected_idx" not in st.session_state:
        st.session_state.selected_idx = None
    
    # Nếu có danh sách HTML
    if html_files:
        df = pd.DataFrame({"Tên công trình": html_files})
    
        # Nếu chưa chọn gì → hiển thị mặc định bản đồ đầu tiên
        if st.session_state.selected_idx is None:
            default_html = random.choice(html_files)
            html_path = os.path.join(html_dir, default_html)
            st.subheader(f"📍 Bản đồ mặc định: {default_html}")
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                components.html(html_content, height=900, scrolling=True)
    
        # Nếu đã chọn → hiển thị bản đồ có nút tiến lùi
        else:
            selected_html = df.iloc[st.session_state.selected_idx]['Tên công trình']
    
            col1, _, col3 = st.columns([1, 6, 1])
            with col1:
                if st.button("⬅️ Lùi") and st.session_state.selected_idx > 0:
                    st.session_state.selected_idx -= 1
                    st.rerun()
            with col3:
                if st.button("Tiến ➡️") and st.session_state.selected_idx < len(df) - 1:
                    st.session_state.selected_idx += 1
                    st.rerun()
    
            st.markdown("---")
            st.subheader(f"🗺️ Bản đồ: {selected_html}")
            html_path = os.path.join(html_dir, selected_html)
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                components.html(html_content, height=900, scrolling=True)
    else:
        st.warning("Không tìm thấy file HTML nào trong thư mục 'dulieu/'")
    
    st.markdown("""
    ### 📌 Hướng dẫn
    - Danh sách 200 công trình được thường xuyên thay đổi/ 4900 công trình tâm linh được tác giả thu thập tại Việt Nam.
    - Công nghệ: Ứng dụng công nghệ tự động hóa địa không gian để xác định vector các hướng địa mạch tự động tại các công trình.
    - Phiên bản: V1.0 phiên bản web ưu tiên số liệu nhẹ, vector hướng mạch mang tính tham khảo- không chính xác tuyệt đối.
    - Cách dùng: Các bạn chọn trang → Bấm `Xem` → Bản đồ sẽ hiển thị bên dưới.
    """)
      
    
    st.markdown("""
    ### 2.🌐Biểu đồ cộng hưởng Schumann Trái Đất trực tuyến
    Nguồn: [Tomsk, Russia Space Observing System]
    """)
    st.image("https://sosrff.tsu.ru/new/shm.jpg", caption="Schumann Resonance - Live", use_container_width=True)
    
    st.markdown("""
    ### 3.🧲 Dữ liệu địa từ trực tuyến""")
    start_date = (datetime.today() - timedelta(days=15)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    iframe_url = f"https://imag-data.bgs.ac.uk/GIN_V1/GINForms2?" \
                 f"observatoryIagaCode=PHU&publicationState=Best+available" \
                 f"&dataStartDate={start_date}&dataDuration=30" \
                 f"&samplesPerDay=minute&submitValue=View+%2F+Download&request=DataView"
    # Hiển thị trong Streamlit
    st.components.v1.iframe(iframe_url, height=1000,scrolling=True)
    
    st.markdown("""
    ###  4.Chỉ số Kp – Cảnh báo Bão Từ
    """)
    
    kp_url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    
    def interpret_kp(kp):
        if kp <= 2:
            return "🟢 Rất an toàn"
        elif kp == 3:
            return "🟢 An toàn"
        elif kp == 4:
            return "🟡 Trung bình – chú ý nhẹ"
        elif kp == 5:
            return "🟠 Cảnh báo nhẹ – Bão từ cấp G1"
        elif kp == 6:
            return "🔴 Cảnh báo – Bão từ cấp G2"
        elif kp == 7:
            return "🔴 Nguy hiểm – Bão từ cấp G3"
        elif kp == 8:
            return "🔴 Rất nguy hiểm – G4"
        else:
            return "🚨 Cực kỳ nguy hiểm – G5"
    
    try:
        kp_data = requests.get(kp_url).json()
        df_kp = pd.DataFrame(kp_data)
    
        if 'kp_index' in df_kp.columns and not df_kp.empty:
            df_kp['time_tag'] = pd.to_datetime(df_kp['time_tag'])
            df_kp.set_index('time_tag', inplace=True)
    
            latest_kp = df_kp['kp_index'].iloc[-1]
            st.metric("🌐 Kp Index (hiện tại)", f"{latest_kp}", delta=interpret_kp(latest_kp))
    
            # Hiển thị biểu đồ 3 ngày gần nhất
            df_kp['date'] = df_kp.index.date
            last_3_days = sorted(df_kp['date'].unique())[-3:]
            df_plot = df_kp[df_kp['date'].isin(last_3_days)]
            st.line_chart(df_plot['kp_index'])
    
        else:
            st.warning("⚠️ Không tìm thấy cột 'kp_index' trong dữ liệu.")
    except Exception as e:
        st.error("❌ Lỗi khi tải dữ liệu Kp Index.")
        st.text(str(e))
    
   
    
  
    st.markdown("""
    ### 5. MÔ HÌNH MA PHƯƠNG
    """)
    
    # Bảng ánh xạ bậc ma phương → hành tinh (theo yêu cầu riêng của bạn)
    planet_map = {
        3: "Thổ tinh (Saturn)",
        4: "Mộc tinh (Jupiter)",
        5: "Hỏa tinh (Mars)",
        6: "Mặt Trời (Sun)",
        7: "Kim tinh (Venus)",
        8: "Thủy tinh (Mercury)",
        9: "Mặt Trăng (Moon)"
    }
    
    n = st.number_input("Nhập bậc ma phương:", min_value=3, step=1, value=4)
    hanh_tinh = planet_map.get(n, "")
    
    st.markdown(f"**→ Bậc {n} tương ứng với hành tinh:** 🪐 __{hanh_tinh}__")
    
    def magic_square_6_custom():
        return np.array([
            [6, 32, 3, 34, 35, 1],
            [7, 11, 27, 28, 8, 30],
            [19, 14, 16, 15, 23, 24],
            [18, 20, 22, 21, 17, 13],
            [25, 29, 10, 9, 26, 12],
            [36, 5, 33, 4, 2, 31]
        ])
    
    def magic_square_doubly_even(n):
        square = np.arange(1, n*n+1).reshape(n, n)
        mask = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(n):
                if (i % 4 == j % 4) or ((i % 4 + j % 4) == 3):
                    mask[i, j] = True
        square[mask] = n*n + 1 - square[mask]
        return square
    
    def generate_magic_square_southeast(n):
        if n % 2 == 0:
            raise ValueError("Chỉ hỗ trợ ma phương bậc lẻ.")
        square = np.zeros((n, n), dtype=int)
        i, j = n // 2 + 1, n // 2
        for num in range(1, n * n + 1):
            square[i % n, j % n] = num
            new_i, new_j = (i + 1) % n, (j + 1) % n
            if square[new_i, new_j] != 0:
                i = (i + 2) % n
            else:
                i, j = new_i, new_j
        return square
    
    def singly_even_magic(n):
        def odd_magic(m):
            magic = np.zeros((m, m), dtype=int)
            i, j = 0, m // 2
            for k in range(1, m*m + 1):
                magic[i, j] = k
                i2, j2 = (i - 1) % m, (j + 1) % m
                if magic[i2, j2]:
                    i = (i + 1) % m
                else:
                    i, j = i2, j2
            return magic
    
        m = n // 2
        mini_square = odd_magic(m)
        square = np.zeros((n, n), dtype=int)
        add = [0, 2*m*m, 3*m*m, m*m]
        for i in range(2):
            for j in range(2):
                square[i*m:(i+1)*m, j*m:(j+1)*m] = mini_square + add[i*2+j]
        k = (n - 2) // 4
        for i in range(m):
            for j in range(n):
                if (j < k or j >= n - k):
                    if not (j == 0 and i == k):
                        square[i, j], square[i+m, j] = square[i+m, j], square[i, j]
        j = k
        for i in range(m):
            square[i, j], square[i+m, j] = square[i+m, j], square[i, j]
        return square
    
    try:
        # Dùng ma phương custom cho bậc 6
        if n == 6:
            square = magic_square_6_custom()
            phan_loai = "Mặt Trời- Surya yantra"
        elif n % 2 == 1:
            square = generate_magic_square_southeast(n)
            phan_loai = "Bậc lẻ (kiểu Đông Nam, xuất phát gần tâm)"
        elif n % 4 == 0:
            square = magic_square_doubly_even(n)
            phan_loai = "Chẵn chia hết cho 4"
            square = np.flipud(square)
        else:
            square = singly_even_magic(n)
            phan_loai = "Chẵn lẻ (không chia hết cho 4)"
        df = pd.DataFrame(square)
        st.write(f"**Ma phương loại:** {phan_loai}")
        styled_df = df.style.set_properties(**{
        'font-size': '18px',      # Đổi cỡ chữ
        'font-weight': 'bold',    # Đậm
        'text-align': 'center'
        })
    
        # Hiển thị với Streamlit
        st.dataframe(styled_df, use_container_width=False)
    
    
        # Kiểm tra tổng
        row_sums = df.sum(axis=1)
        col_sums = df.sum(axis=0)
        diag1 = np.trace(square)
        diag2 = np.trace(np.fliplr(square))
        magic_const = n * (n ** 2 + 1) // 2
    
        st.markdown(f"- Tổng chuẩn (magic constant): **{magic_const}**")
        st.markdown(f"- Tổng hàng 1: **{row_sums.iloc[0]}**")
        st.markdown(f"- Tổng cột 1: **{col_sums.iloc[0]}**")
        st.markdown(f"- Tổng đường chéo chính: **{diag1}**")
        st.markdown(f"- Tổng đường chéo phụ: **{diag2}**")
    
        if (
            all(row_sums == magic_const)
            and all(col_sums == magic_const)
            and diag1 == magic_const
            and diag2 == magic_const
        ):
            st.success("✅ Ma phương hợp lệ!")
        else:
            st.warning("⚠️ Ma phương này KHÔNG hợp lệ.")
    
        # Bảng chia hết cho 9
        st.markdown("#### Bảng ma phương chia hết cho 9:")
        df_mod9 = (df % 9).replace(0, 9)
        st.dataframe(df_mod9, use_container_width=False)
        tong_cot_dau = df_mod9.iloc[:, 0].sum()
        st.markdown(f"🧾 Tổng cột đầu: **{tong_cot_dau}**")
        # Bảng chia hết cho 10
        st.markdown("#### Bảng ma phương chia hết cho 10:")
        df_mod10 = (df % 10)
        st.dataframe(df_mod10, use_container_width=False)
        tong_cot_dau = df_mod10.iloc[:, 0].sum()
        st.markdown(f"🧾 Tổng cột đầu: **{tong_cot_dau}**")
    except Exception as e:
        st.error(f"Lỗi: {e}")

    
    st.markdown("---\n### Tác giả Nguyễn Duy Tuấn – với mục đích phụng sự tâm linh và cộng đồng. SĐT&ZALO: 0377442597. DONATE: nguyenduytuan techcombank 19033167089018")

if __name__ == "__main__":
    main()
