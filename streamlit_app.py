import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы на широкий формат и скрытие лишних отступов
st.set_page_config(page_title="ФинПлан ARESSAGE PRO", layout="wide", initial_sidebar_state="collapsed")

# Внедрение фирменных шрифтов и стилей через CSS (шрифты Inter/Abhaya, цвета бренда)
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        .main-title {
            font-family: 'Abhaya Libre', serif;
            color: #4A1A60; /* Фирменный фиолетовый Finn */
            text-align: center;
            margin-top: -40px;
            margin-bottom: 5px;
            font-size: 32px;
            letter-spacing: 1px;
        }
        .sub-title {
            font-family: 'Inter', sans-serif;
            color: #005A36; /* Фирменный зеленый Office green */
            text-align: center;
            margin-bottom: 25px;
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

# Официальный брендированный заголовок калькулятора
st.markdown("<div class='main-title'>A R E S S A G E</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Aesthetic Regenerative Message • Финансовая Модель</div>", unsafe_allow_html=True)

# 4 ультра-компактные колонки для ввода данных (умещаются в одну строку на экране)
c_in1, c_in2, c_in3, c_in4 = st.columns(4)

with c_in1:
    st.markdown("<b style='color:#4A1A60;'>👤 Клиенты и Цены</b>", unsafe_allow_html=True)
    clients_face = st.slider("Лицо/Тело (процедур в день)", 0, 10, 3)
    price_face = st.slider("Цена Лицо/Тело (руб.)", 5000, 15000, 9300, step=100)
    clients_hair = st.slider("Волосы (процедур в день)", 0, 10, 3)
    price_hair = st.slider("Цена Волосы (руб.)", 5000, 15000, 11300, step=100)
    days = st.slider("Рабочих дней в мес.", 15, 30, 22)

with c_in2:
    st.markdown("<b style='color:#4A1A60;'>🧪 Себестоимость сеанса</b>", unsafe_allow_html=True)
    cost_face = st.slider("Состав Лицо/Тело (руб.)", 1500, 6000, 3100, step=50)
    cost_hair = st.slider("Состав Волосы (руб.)", 1500, 6000, 3766, step=50)
    manipula = st.slider("Манипула/Насадка (руб.)", 0, 1000, 425, step=25)

with c_in3:
    st.markdown("<b style='color:#005A36;'>📉 Оборудование и Лизинг</b>", unsafe_allow_html=True)
    device_cost = st.number_input("Стоимость аппарата (руб.)", value=1200000, step=50000)
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5)
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    initial_invest = st.number_input("Стартовый закуп (руб.)", value=150000, step=10000)

with c_in4:
    st.markdown("<b style='color:#005A36;'>🏢 Фикс. расходы в месяц</b>", unsafe_allow_html=True)
    salary_base = st.number_input("Оклад мастера (руб.)", value=40000)
    salary_tax = st.number_input("Налоги на ФОТ (руб.)", value=20800)
    bonus_doctor = st.number_input("Премия / Мотивация (руб.)", value=80000)
    rent_and_other = st.number_input("Аренда и ОХР (руб.)", value=35000)

# --- МАТЕМАТИЧЕСКАЯ ЛОГИКА (ЛИЗИНГ И ДОХОДЫ) ---
if lease_rate > 0 and lease_months > 0:
    monthly_rate = (lease_rate / 100) / 12
    lease_payment = device_cost * (monthly_rate * (1 + monthly_rate)**lease_months) / ((1 + monthly_rate)**lease_months - 1)
else:
    lease_payment = device_cost / lease_months if lease_months > 0 else 0

# Расчет операционных показателей за месяц
monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

total_variable_costs = (clients_face * days * (cost_face + manipula)) + (clients_hair * days * (cost_hair + manipula))
total_fixed_costs_with_lease = lease_payment + salary_base + salary_tax + bonus_doctor + rent_and_other

# Прибыль текущего месяца (когда лизинг еще платится)
profit_before_tax = total_revenue - total_variable_costs - total_fixed_costs_with_lease
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

st.markdown("<hr style='margin: 12px 0; border-color: #efefef;'>", unsafe_allow_html=True)

# Главные финансовые метрики в одну компактную строку
c_m1, c_m2, c_m3 = st.columns(3)
c_m1.metric("📌 Общая выручка комплекса", f"{total_revenue:,.0f} руб./мес.")
c_m2.metric("📌 Расчетный платеж по лизингу", f"{lease_payment:,.0f} руб./мес.")
if net_profit > 0:
    c_m3.markdown(f"<div style='color:#005A36; font-size:14px; font-weight:600;'>🟢 Чистая прибыль (налог 15%)</div><div style='font-size:24px; font-weight:600; color:#005A36;'>{net_profit:,.0f} руб./мес.</div>", unsafe_allow_html=True)
else:
    c_m3.markdown(f"<div style='color:#b00020; font-size:14px; font-weight:600;'>🔴 Чистый убыток проекта</div><div style='font-size:24px; font-weight:600; color:#b00020;'>{net_profit:,.0f} руб./мес.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Графический блок 50/50 по горизонтали
c_graph1, c_graph2 = st.columns(2)

with c_graph1:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>🪐 СТРУКТУРА РАСПРЕДЕЛЕНИЯ ВЫРУЧКИ</b>", unsafe_allow_html=True)
    if total_revenue > 0 and net_profit > 0:
        pie_data = pd.DataFrame({
            "Категория": ["Чистая прибыль", "Переменные расходы (составы)", "Фикс. расходы и лизинг", "Налог (15%)"],
            "Сумма (руб.)": [net_profit, total_variable_costs, total_fixed_costs_with_lease, tax]
        })
        # Градиентная палитра по брендбуку: Фиолетовый (Finn), Зеленый (Office Green), Графит (Black), Светло-пурпурный
        brand_luxury_colors = ['#4A1A60', '#005A36', '#1A1A1A', '#8E5EA2']
        fig_pie = px.pie(pie_data, values="Сумма (руб.)", names="Категория", 
                         color_discrete_sequence=brand_luxury_colors, hole=0.45)
        fig_pie.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=210, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Круговая диаграмма активируется при выходе проекта в прибыль.")

with c_graph2:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>📈 ПРОГНОЗ НАКОПИТЕЛЬНОГО БАЛАНСА (6 МЕСЯЦЕВ)</b>", unsafe_allow_html=True)
    
    # Исправление логики графика: корректный расчет накопления
    months_list = ["Старт", "1 мес.", "2 мес.", "3 мес.", "4 мес.", "5 мес.", "6 мес."]
    
    # В точке "Старт" баланс равен только стоимости первоначального закупа (минус)
    cumulative_balances = [-initial_invest]
    current_balance = -initial_invest
    
    for m in range(1, 7):
        # Пересчитываем расходы: если месяц превышает срок лизинга, платеж по лизингу убирается
        if m <= lease_months:
            m_fixed = total_fixed_costs_with_lease
        else:
            m_fixed = total_fixed_costs_with_lease - lease_payment
            
        m_profit_before_tax = total_revenue - total_variable_costs - m_fixed
        m_tax = m_profit_before_tax * 0.15 if m_profit_before_tax > 0 else 0
        m_net_profit = m_profit_before_tax - m_tax
        
        current_balance += m_net_profit
        cumulative_balances.append(current_balance)
        
    df_line = pd.DataFrame({"Баланс проекта (руб.)": cumulative_balances}, index=months_list)
    
    # Построение красивого линейного графика в фирменном фиолетовом цвете бренда
    fig_line = px.line(df_line, y="Баланс проекта (руб.)", markers=True, color_discrete_sequence=['#4A1A60'])
    fig_line.add_hline(y=0, line_dash="dash", line_color="#005A36", annotation_text="Точка окупаемости")
    fig_line.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=210, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_line, use_container_width=True)
