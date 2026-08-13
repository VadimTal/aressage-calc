import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.set_page_config(page_title="ФинПлан ARESSAGE PRO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        @import url('https://googleapis.com');
        .main-title {
            font-family: 'Abhaya Libre', serif;
            color: #4A1A60;
            text-align: center;
            margin-top: -40px;
            margin-bottom: 5px;
            font-size: 32px;
            letter-spacing: 1px;
        }
        .sub-title {
            font-family: 'Inter', sans-serif;
            color: #005A36;
            text-align: center;
            margin-bottom: 15px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>A R E S S A G E</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Aesthetic Regenerative Message • Финансовая Модель</div>", unsafe_allow_html=True)

currency_choice = st.radio("🌎 Выберите валюту расчёта и регион санатория:", ["RUB (Россия)", "BYN (Беларусь)"], horizontal=True)

rate = 1.0
markup = 1.0
currency_label = "руб."

if currency_choice == "BYN (Беларусь)":
    rate = 0.0359
    markup = 1.22
    currency_label = "Br"

st.markdown("<br>", unsafe_allow_html=True)

c_in1, c_in2, c_in3, c_in4 = st.columns(4)

with c_in1:
    st.markdown("<b style='color:#4A1A60;'>👤 Клиенты и Цены</b>", unsafe_allow_html=True)
    clients_face = st.slider("Лицо/Тело (процедур в день)", 0, 10, 3)
    price_face = st.slider("Цена Лицо/Тело (базовая)", 5000, 15000, 9300, step=100)
    clients_hair = st.slider("Волосы (процедур в день)", 0, 10, 3)
    price_hair = st.slider("Цена Волосы (базовая)", 5000, 15000, 11300, step=100)
    days = st.slider("Рабочих дней в мес.", 15, 30, 22)

with c_in2:
    st.markdown("<b style='color:#4A1A60;'>🧪 Себестоимость сеанса</b>", unsafe_allow_html=True)
    cost_face = st.slider("Состав Лицо/Тело (базовый)", 1500, 6000, 3100, step=50)
    cost_hair = st.slider("Состав Волосы (базовый)", 1500, 6000, 3766, step=50)
    manipula = st.slider("Манипула/Насадка (базовая)", 0, 1000, 425, step=25)

with c_in3:
    st.markdown("<b style='color:#005A36;'>📉 Оборудование и Лизинг</b>", unsafe_allow_html=True)
    device_cost = st.number_input("Стоимость аппарата (базовая)", value=1200000, step=50000)
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5)
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    initial_invest = st.number_input("Стартовый закуп (базовый)", value=150000, step=10000)

with c_in4:
    st.markdown("<b style='color:#005A36;'>🏢 Фикс. расходы в месяц</b>", unsafe_allow_html=True)
    salary_base = st.number_input("Оклад мастера (базовый)", value=40000)
    salary_tax = st.number_input("Налоги на ФОТ (базовые)", value=20800)
    bonus_doctor = st.number_input("Премия / Мотивация (базовая)", value=80000)
    rent_and_other = st.number_input("Аренда и ОХР (базовые)", value=35000)

final_device_cost = math.ceil(device_cost * markup) if currency_choice == "BYN (Беларусь)" else device_cost

if lease_rate > 0 and lease_months > 0:
    monthly_rate = (lease_rate / 100) / 12
    lease_payment = final_device_cost * (monthly_rate * (1 + monthly_rate)**lease_months) / ((1 + monthly_rate)**lease_months - 1)
else:
    lease_payment = final_device_cost / lease_months if lease_months > 0 else 0

monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

final_cost_face = math.ceil(cost_face * markup) if currency_choice == "BYN (Беларусь)" else cost_face
final_cost_hair = cost_hair
final_manipula = math.ceil(manipula * markup) if currency_choice == "BYN (Беларусь)" else manipula

total_variable_costs = (clients_face * days * (final_cost_face + final_manipula)) + (clients_hair * days * (final_cost_hair + final_manipula))
total_fixed_costs_with_lease = lease_payment + salary_base + salary_tax + bonus_doctor + rent_and_other

total_revenue_converted = total_revenue * rate
lease_payment_converted = lease_payment * rate
total_variable_costs_converted = total_variable_costs * rate
total_fixed_costs_with_lease_converted = total_fixed_costs_with_lease * rate
initial_invest_converted = initial_invest * rate

profit_before_tax = total_revenue_converted - total_variable_costs_converted - total_fixed_costs_with_lease_converted
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)

c_m1, c_m2, c_m3 = st.columns(3)
c_m1.metric("📌 Общая выручка комплекса", f"{total_revenue_converted:,.0f} {currency_label}/мес.")
c_m2.metric("📌 Расчетный платеж по лизингу", f"{lease_payment_converted:,.0f} {currency_label}/мес.")
if net_profit > 0:
    c_m3.markdown(f"<div style='color:#005A36; font-size:14px; font-weight:600;'>🟢 Чистая прибыль (налог 15%)</div><div style='font-size:24px; font-weight:600; color:#005A36;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)
else:
    c_m3.markdown(f"<div style='color:#b00020; font-size:14px; font-weight:600;'>🔴 Чистый убыток проекта</div><div style='font-size:24px; font-weight:600; color:#b00020;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)

c_graph1, c_graph2 = st.columns(2)

with c_graph1:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>🪐 СТРУКТУРА РАСПРЕДЕЛЕНИЯ ВЫРУЧКИ</b>", unsafe_allow_html=True)
    if total_revenue_converted > 0 and net_profit > 0:
        pie_data = pd.DataFrame({
            "Категория": ["Чистая прибыль", "Переменные расходы", "Фикс. расходы и лизинг", "Налог (15%)"],
            "Сумма": [net_profit, total_variable_costs_converted, total_fixed_costs_with_lease_converted, tax]
        })
        brand_luxury_colors = ['#4A1A60', '#005A36', '#1A1A1A', '#8E5EA2']
        fig_pie = px.pie(pie_data, values="Сумма", names="Категория", 
                         color_discrete_sequence=brand_luxury_colors, hole=0.45)
        fig_pie.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=170, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Круговая диаграмма активируется при выходе проекта в прибыль.")

with c_graph2:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>📈 ПРОГНОЗ НАКОПИТЕЛЬНОГО БАЛАНСА (6 МЕСЯЦЕВ)</b>", unsafe_allow_html=True)
    months_list = ["Старт", "1 мес.", "2 мес.", "3 мес.", "4 мес.", "5 мес.", "6 мес."]
    
    cumulative_balances = [-initial_invest_converted]
    current_balance = -initial_invest_converted
    
    for m in range(1, 7):
        if m <= lease_months:
            m_fixed = total_fixed_costs_with_lease_converted
        else:
            m_fixed = total_fixed_costs_with_lease_converted - lease_payment_converted
            
        m_profit_before_tax = total_revenue_converted - total_variable_costs_converted - m_fixed
        m_tax = m_profit_before_tax * 0.15 if m_profit_before_tax > 0 else 0
        m_net_profit = m_profit_before_tax - m_tax
        
        current_balance += m_net_profit
        cumulative_balances.append(current_balance)
        
    df_line = pd.DataFrame({"Баланс проекта": cumulative_balances}, index=months_list)
    fig_line = px.line(df_line, y="Баланс проекта", markers=True, color_discrete_sequence=['#4A1A60'])
    fig_line.add_hline(y=0, line_dash="dash", line_color="#005A36", annotation_text="Точка окупаемости")
    fig_line.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=170, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)
st.markdown("<b style='font-size:14px; color:#4A1A60; font-family:Inter;'>⚖️ СРАВНИТЕЛЬНЫЙ АНАЛИЗ ЭФФЕКТИВНОСТИ ИСПОЛЬЗОВАНИЯ ИНФРАСТРУКТУРЫ САНАТОРИЯ</b>", unsafe_allow_html=True)

avg_aressage_price_converted = ((price_face + price_hair) / 2) * rate
avg_aressage_cost_converted = (((final_cost_face + final_manipula) + (final_cost_hair + final_manipula)) / 2) * rate
aressage_margin_per_min_converted = (avg_aressage_price_converted - avg_aressage_cost_converted) / 30

compare_data = {
    "Показатель эффективности": [
        "Средняя цена процедуры для гостя",
        "Длительность сеанса (минут)",
        "Себестоимость расходных материалов",
        "Маржинальный доход с 1 сеанса",
        "🔥 Доходность кабинета в минуту (RevPM)"
    ],
    "Классический массаж / Уход": [
        f"{3200 * rate:,.0f} {currency_label}",
        "60 мин.",
        f"{350 * rate:,.0f} {currency_label}",
        f"{2850 * rate:,.0f} {currency_label}",
        f"{(2850 * rate / 60):,.1f} {currency_label} / мин."
    ],
    "Классическое обертывание / Спа": [
        f"{4500 * rate:,.0f} {currency_label}",
        "90 мин.",
        f"{800 * rate:,.0f} {currency_label}",
        f"{3700 * rate:,.0f} {currency_label}",
        f"{(3700 * rate / 90):,.1f} {currency_label} / мин."
    ],
    "ARESSAGE PRO (Аппаратный уход)": [
        f"{avg_aressage_price_converted:,.0f} {currency_label}",
        "30 мин.",
        f"{avg_aressage_cost_converted:,.0f} {currency_label}",
        f"{(avg_aressage_price_converted - avg_aressage_cost_converted):,.0f} {currency_label}",
        f"{aressage_margin_per_min_converted:,.1f} {currency_label} / мин."
    ]
}

df_compare = pd.DataFrame(compare_data)
st.table(df_compare)

st.markdown(f"""

<div style='background-color: #f4f6f4; padding: 10px; border-left: 4px solid #005A36; font-size: 12px; font-family: Inter; color: #333;'>
    <b>Резюме:</b> За счет высокой маржинальности состава и короткого времени сеанса (всего 30 минут без реабилитации), технология <b>ARESSAGE PRO</b> генерирует в среднем <b>В 2-3 РАЗА БОЛЬШЕ чистой прибыли на 1 минуту работы кабинета</b> и занятости персонала по сравнению с классическими спа-процедурами санатория. Это позволяет кратно поднять выручку без расширения площади медицинского центра.
</div>
""", unsafe_allow_html=True)
