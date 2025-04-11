import streamlit as st
import pandas as pd
import jdatetime
from pathlib import Path
import os
import sys

st.set_page_config(page_title="آریانما", layout="wide")
st.markdown("""
    <style>
        body {direction: rtl; text-align: right;}
        .stDataEditor div[data-testid="stHorizontalBlock"] {direction: rtl;}
        th {text-align: right !important;}
    </style>
""", unsafe_allow_html=True)

st.title("💥 سیستم مدیریت حسابداری 💥")

if getattr(sys, 'frozen', False):
    DATA_DIR = sys._MEIPASS
else:
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(DATA_DIR, 'data.csv')
expected_cols = ["ردیف", "تاریخ", "نوع جنس", "تعداد", "فی", "جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل", "وضعیت"]
if not Path(DATA_FILE).exists():
    pd.DataFrame(columns=expected_cols).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def jalali_date_selector(label):
    cols = st.columns(3)
    year_options = list(range(1402, 1421))
    default_year_index = 16 if label == "تا" else 0
    with cols[0]:
        year = st.selectbox("سال " + label, year_options, index=default_year_index, key=f"{label}_year")
    with cols[1]:
        month = st.selectbox("ماه " + label, list(jdatetime.date.j_months_fa), key=f"{label}_month")
    with cols[2]:
        day = st.selectbox("روز " + label, list(range(1, 32)), key=f"{label}_day")
    try:
        return jdatetime.date(year, list(jdatetime.date.j_months_fa).index(month) + 1, day).strftime("%Y-%m-%d")
    except Exception as e:
        st.error("❌ تاریخ نامعتبر")
        return None

default_types = ["سیمان", "سیمان سفید", "گچ", "گچ2", "سفال", "پودرسنگ"]
df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
# اطمینان از تبدیل ستون‌های عددی به مقدار عددی
for col in ["تعداد", "فی", "جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
if "نوع جنس" in df.columns and not df.empty:
    available_types = list(set(df["نوع جنس"].dropna().tolist() + default_types))
else:
    available_types = default_types

selected_type = st.selectbox("📦 نوع جنس", available_types + ["سایر"], key="selected_type")
item_type = None
if selected_type == "سایر":
    new_type = st.text_input("🆕 نوع جنس جدید", key="new_type")
    item_type = new_type.strip() if new_type.strip() else None
else:
    item_type = selected_type
if selected_type == "سایر" and not item_type:
    st.warning("لطفاً نوع جنس جدید را وارد کنید.")

with st.form("form"):
    st.subheader("➕ افزودن تراکنش جدید")
    date = jalali_date_selector("تاریخ")
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("🔢 تعداد", min_value=0, step=10, value=0)
        unit_price = st.number_input("💰 فی", min_value=0, step=1000, value=0)
    with col2:
        payment = st.number_input("💸 پرداختی", min_value=0, step=100, value=0)
        prev_balance = st.number_input("🏦 مانده قبلی", step=100, value=0)
    submitted = st.form_submit_button("✅ ثبت")
    if submitted and date and item_type:
        df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
        # تبدیل ستون‌های عددی به عددی جهت جلوگیری از خطاهای محاسباتی
        for col in ["تعداد", "فی", "جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0
        new_id = int(df["ردیف"].max()) + 1 if not df.empty and pd.notnull(df["ردیف"].max()) else 1
        item_total = quantity * unit_price
        balance_change = payment - item_total
        # محاسبه نهایی کل بر اساس مانده قبلی
        final_total = balance_change - prev_balance
        status = "🟥 بدهکاری" if final_total < 0 else "🟩 بستانکاری"
        new_data = {
            "ردیف": new_id,
            "تاریخ": date,
            "نوع جنس": item_type,
            "تعداد": quantity,
            "فی": unit_price,
            "جمع قیمت کالا": item_total,
            "پرداختی": payment,
            "بدهکاری/بستانکاری": balance_change,
            "مانده قبلی": prev_balance,
            "کل": final_total,
            "وضعیت": status
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
        st.success("✅ تراکنش ثبت شد!")

with st.sidebar:
    st.subheader("🔎 فیلترها")
    with st.expander("📅 فیلتر تاریخ"):
        start_date = jalali_date_selector("از")
        end_date = jalali_date_selector("تا")
    df_filter = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    for col in ["تعداد", "فی", "جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]:
        if col in df_filter.columns:
            df_filter[col] = pd.to_numeric(df_filter[col], errors='coerce').fillna(0)
    types_in_data = list(set(df_filter["نوع جنس"].dropna().tolist())) if "نوع جنس" in df_filter.columns and not df_filter.empty else default_types
    selected_filter = st.multiselect("📦 فیلتر بر اساس نوع جنس", options=types_in_data, default=types_in_data)
    debt_filter = st.checkbox("💸 نمایش فقط بدهکاری‌ها")
    credit_filter = st.checkbox("💰 نمایش فقط بستانکاری‌ها")

def format_number(n):
    if abs(n) < 1_000:
        return f"{n:,}"
    elif abs(n) < 1_000_000:
        return f"{n/1_000:.2f} هزار"
    elif abs(n) < 1_000_000_000:
        return f"{n/1_000_000:.2f} میلیون"
    else:
        return f"{n/1_000_000_000:.2f} میلیارد"

try:
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    for col in ["تعداد", "فی", "جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    if not df.empty:
        if start_date and end_date:
            df = df[(df["تاریخ"] >= start_date) & (df["تاریخ"] <= end_date)]
        if selected_filter:
            df = df[df["نوع جنس"].isin(selected_filter)]
        if debt_filter:
            df = df[df["کل"] < 0]
        if credit_filter:
            df = df[df["کل"] >= 0]
        # به‌روز رسانی وضعیت بر اساس مقدار "کل"
        df["وضعیت"] = df["کل"].apply(lambda x: "🟥 بدهکاری" if x < 0 else "🟩 بستانکاری")
        display_order = expected_cols[::-1]
        st.subheader("📋 لیست تراکنش‌ها")
        df_display = df.copy()
        for col in ["جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]:
            df_display[col] = df_display[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else x)
        edited_df = st.data_editor(
            df_display[display_order],
            column_config={"وضعیت": {"disabled": True}, "تاریخ": {"disabled": True}, "ردیف": {"disabled": True}},
            hide_index=True,
            use_container_width=True
        )
        selected_rows = st.multiselect("انتخاب ردیف‌های جهت حذف", options=edited_df["ردیف"].tolist())
        if st.button("حذف سطرهای انتخاب شده"):
            full_df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
            full_df = full_df[~full_df["ردیف"].isin(selected_rows)]
            full_df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("ردیف(های) انتخاب شده حذف شدند. لطفاً صفحه را رفرش کنید.")
        totals_data = {
            "آمار": ["💰 جمع قیمت کالا", "💸 پرداختی", "🧾 بدهکاری/بستانکاری", "🏦 مانده قبلی", "💲 کل"],
            "مقدار": [f"{int(df[col].sum()):,}".replace(',', '٬') for col in ["جمع قیمت کالا", "پرداختی", "بدهکاری/بستانکاری", "مانده قبلی", "کل"]]
        }

        st.subheader("📊 آمار کلی")
        st.markdown("""
        <style>
            .rtl-table {
                direction: rtl;
                text-align: right;
                margin: auto;
                border-collapse: collapse;
            }
            .rtl-table th, .rtl-table td {
                text-align: right !important;
                padding: 10px;
            }
            .table-container {
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)

        totals_df = pd.DataFrame(totals_data)
        totals_html = totals_df.to_html(index=False, header=False)
        totals_html = totals_html.replace('<table', '<table class="rtl-table"')

        st.markdown(f'<div class="table-container">{totals_html}</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ خطا: {str(e)}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>designed by M.Yar</p>", unsafe_allow_html=True)

#pyinstaller --onefile --windowed main.py
