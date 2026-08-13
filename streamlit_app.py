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
step_price = 100
step_cost = 50

if currency_choice == "BYN (Беларусь)":
    rate = 0.0359
    markup = 1.22
    currency_label = "Br"
    step_price = 5
    step_cost = 2

st.markdown("<br>", unsafe_allow_html=True)

c_in1, c_in2, c_in3, c_in4 = st.columns(4)

with c_in1:
    st.markdown(f"<b style='color:#4A1A60;'>👤 Клиенты и Цены ({currency_label})</b>", unsafe_allow_html=True)
    clients_face = st.slider("Лицо/Тело (процедур в день)", 0, 10, 3)
    price_face = st.slider(f"Цена Лицо/Тело ({currency_label})", min_value=int(5000 * rate), max_value=int(15000 * rate), value=int(9300 * rate), step=step_price)
    clients_hair = st.slider("Волосы (процедур в день)", 0, 10, 3)
    price_hair = st.slider(f"Цена Волосы ({currency_label})", min_value=int(5000 * rate), max_value=int(15000 * rate), value=int(11300 * rate), step=step_price)
    days = st.slider("Рабочих дней в мес.", 15, 30, 22)

with c_in2:
    st.markdown(f"<b style='color:#4A1A60;'>🧪 Себестоимость сеанса ({currency_label})</b>", unsafe_allow_html=True)
    base_cost_face = int(3100 * markup * rate) if currency_choice == "BYN (Беларусь)" else 3100
    cost_face = st.slider(f"Состав Лицо/Тело ({currency_label})", min_value=int(1500 * rate), max_value=int(6000 * markup * rate), value=base_cost_face, step=step_cost)
    base_cost_hair = int(3766 * rate)
    cost_hair = st.slider(f"Состав Волосы ({currency_label})", min_value=int(1500 * rate), max_value=int(6000 * rate), value=base_cost_hair, step=step_cost)
    base_manipula = int(425 * markup * rate) if currency_choice == "BYN (Беларусь)" else 425
    manipula = st.slider(f"Манипула/Насадка ({currency_label})", min_value=0, max_value=int(1000 * markup * rate), value=base_manipula, step=step_cost)

with c_in3:
    st.markdown(f"<b style='color:#005A36;'>📉 Оборудование ({currency_label})</b>", unsafe_allow_html=True)
    base_device_cost = math.ceil(1200000 * markup * rate) if currency_choice == "BYN (Беларусь)" else 1200000
    device_cost_input = st.number_input(f"Стоимость аппарата ({currency_label})", value=base_device_cost)
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5)
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    base_initial_invest = int(150000 * rate)
    initial_invest_input = st.number_input(f"Стартовый закуп ({currency_label})", value=base_initial_invest)

with c_in4:
    st.markdown(f"<b style='color:#005A36;'>🏢 Фикс. расходы ({currency_label})</b>", unsafe_allow_html=True)
    salary_base_input = st.number_input(f"Оклад мастера ({currency_label})", value=int(40000 * rate))
    salary_tax_input = st.number_input(f"Налоги на ФОТ ({currency_label})", value=int(20800 * rate))
    bonus_doctor_input = st.number_input(f"Премия / Мотивация ({currency_label})", value=int(80000 * rate))
    rent_and_other_input = st.number_input(f"Аренда и ОХР ({currency_label})", value=int(35000 * rate))

if lease_rate > 0 and lease_months > 0:
    monthly_rate = (lease_rate / 100) / 12
    lease_payment = device_cost_input * (monthly_rate * (1 + monthly_rate)**lease_months) / ((1 + monthly_rate)**lease_months - 1)
else:
    lease_payment = device_cost_input / lease_months if lease_months > 0 else 0

monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

total_variable_costs = (clients_face * days * (cost_face + manipula)) + (clients_hair * days * (cost_hair + manipula))
total_fixed_costs_with_lease = lease_payment + salary_base_input + salary_tax_input + bonus_doctor_input + rent_and_other_input

profit_before_tax = total_revenue - total_variable_costs - total_fixed_costs_with_lease
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)

c_m1, c_m2, c_m3 = st.columns(3)
c_m1.metric("📌 Общая выручка комплекса", f"{total_revenue:,.0f} {currency_label}/мес.")
c_m2.metric("📌 Расчетный платеж по лизингу", f"{lease_payment:,.0f} {currency_label}/мес.")
if net_profit > 0:
    st.markdown(f"<div style='color:#005A36; font-size:14px; font-weight:600;'>🟢 Чистая прибыль (налог 15%)</div><div style='font-size:24px; font-weight:600; color:#005A36;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='color:#b00020; font-size:14px; font-weight:600;'>🔴 Чистый убыток проекта</div><div style='font-size:24px; font-weight:600; color:#b00020;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)

c_graph1, c_graph2 = st.columns(2)

with c_graph1:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>🪐 СТРУКТУРА РАСПРЕДЕЛЕНИЯ ВЫРУЧКИ</b>", unsafe_allow_html=True)
    if total_revenue > 0 and net_profit > 0:
        pie_data = pd.DataFrame({"Категория": ["Чистая прибыль", "Переменные расходы", "Фикс. расходы и лизинг", "Налог (15%)"], "Сумма": [net_profit, total_variable_costs, total_fixed_costs_with_lease, tax]})
        brand_luxury_colors = ['#4A1A60', '#005A36', '#1A1A1A', '#8E5EA2']
        fig_pie = px.pie(pie_data, values="Сумма", names="Категория", color_discrete_sequence=brand_luxury_colors, hole=0.45)
        fig_pie.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=170, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Круговая диаграмма активируется при выходе проекта в прибыль.")

with c_graph2:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>📈 ПРОГНОЗ НАКОПИТЕЛЬНОГО БАЛАНСА (6 МЕСЯЦЕВ)</b>", unsafe_allow_html=True)
    months_list = ["Старт", "1 мес.", "2 мес.", "3 мес.", "4 мес.", "5 мес.", "6 мес."]
    cumulative_balances = [-initial_invest_input]
    current_balance = -initial_invest_input
    for m in range(1, 7):
        m_fixed = total_fixed_costs_with_lease if m <= lease_months else (total_fixed_costs_with_lease - lease_payment)
        m_profit_before_tax = total_revenue - total_variable_costs - m_fixed
        m_tax = m_profit_before_tax * 0.15 if m_profit_before_tax > 0 else 0
        current_balance += (m_profit_before_tax - m_tax)
        cumulative_balances.append(current_balance)
    df_line = pd.DataFrame({"Баланс проекта": cumulative_balances}, index=months_list)
    fig_line = px.line(df_line, y="Баланс проекта", markers=True, color_discrete_sequence=['#4A1A60'])
    fig_line.add_hline(y=0, line_dash="dash", line_color="#005A36", annotation_text="Точка окупаемости")
    fig_line.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=170, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)
st.markdown("<b style='font-size:14px; color:#4A1A60; font-family:Inter;'>⚖️ СРАВНИТЕЛЬНЫЙ АНАЛИЗ ЭФФЕКТИВНОСТИ ИСПОЛЬЗОВАНИЯ ИНФРАСТРУКТУРЫ САНАТОРИЯ</b>", unsafe_allow_html=True)

avg_aressage_price = (price_face + price_hair) / 2
avg_aressage_cost = (cost_face + cost_hair) / 2
aressage_margin_per_min = (avg_aressage_price - avg_aressage_cost) / 30

compare_data = {
    "Показатель эффективности": ["Средняя цена процедуры для гостя", "Длительность сеанса (минут)", "Себестоимость расходных материалов", "Маржинальный доход с 1 сеанса", "🔥 Доходность кабинета в минуту (RevPM)"],
    "Классический массаж / Уход": [f"{3200 * rate:,.0f} {currency_label}", "60 мин.", f"{350 * rate:,.0f} {currency_label}", f"{2850 * rate:,.0f} {currency_label}", f"{(2850 * rate / 60):,.1f} {currency_label} / мин."],
    "Классическое обертывание / Спа": [f"{4500 * rate:,.0f} {currency_label}", "90 мин.", f"{800 * rate:,.0f} {currency_label}", f"{3700 * rate:,.0f} {currency_label}", f"{(3700 * rate / 90):,.1f} {currency_label} / мин."],
    "ARESSAGE PRO (Аппаратный уход)": [f"{avg_aressage_price:,.0f} {currency_label}", "30 мин.", f"{avg_aressage_cost:,.0f} {currency_label}", f"{(avg_aressage_price - avg_aressage_cost):,.0f} {currency_label}", f"{aressage_margin_per_min:,.1f} {currency_label} / мин."] if total_revenue > 0 else ["0 Br", "30 мин.", "0 Br", "0 Br", "0.0 Br / мин."]
}
st.table(pd.DataFrame(compare_data))

st.markdown(f"""
<div style='background-color: #f4f6f4; padding: 10px; border-left: 4px solid #005A36; font-size: 12px; font-family: Inter; color: #333;'>
    <b>Резюме для руководства УК:</b> За счет высокой маржинальности состава и короткого времени сеанса (всего 30 минут без реабилитации), технология <b>ARESSAGE PRO</b> генерирует в среднем <b>В 2-3 РАЗА БОЛЬШЕ чистой прибыли на 1 минуту работы кабинета</b> и занятости персонала по сравнению с классическими спа-процедурами санатория. Это позволяет кратно поднять выручку без расширения площади медицинского центра.
</div>
""", unsafe_allow_html=True)
