import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Настройка страницы на широкий формат
st.set_page_config(page_title="ФинПлан ARESSAGE PRO", layout="wide", initial_sidebar_state="collapsed")

# Компактный заголовок
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>📊 Финансовая модель ARESSAGE PRO для УК Санаториев</h2>", unsafe_allow_html=True)

# Входные параметры распределяем в 4 компактные колонки (вместо длинных списков)
c_in1, c_in2, c_in3, c_in4 = st.columns(4)

with c_in1:
    st.markdown("**👤 Поток и Цены**")
    clients_face = st.slider("Лицо/Тело в день", 0, 10, 3)
    price_face = st.slider("Цена Лицо/Тело (руб.)", 5000, 15000, 9300, step=100)
    clients_hair = st.slider("Волосы в день", 0, 10, 3)
    price_hair = st.slider("Цена Волосы (руб.)", 5000, 15000, 11300, step=100)
    days = st.slider("Рабочих дней в мес.", 15, 30, 22)

with c_in2:
    st.markdown("**🧪 Себестоимость сеанса**")
    cost_face = st.slider("Состав Лицо/Тело (руб.)", 1500, 6000, 3100, step=50)
    cost_hair = st.slider("Состав Волосы (руб.)", 1500, 6000, 3766, step=50)
    manipula = st.slider("Манипула/Насадка (руб.)", 0, 1000, 425, step=25)

with c_in3:
    st.markdown("**📉 Оборудование и Лизинг**")
    device_cost = st.number_input("Стоимость аппарата (руб.)", value=1200000, step=50000)
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5)
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    initial_invest = st.number_input("Старт (закуп/обучение), руб.", value=150000, step=10000)

with c_in4:
    st.markdown("**🏢 Фикс. расходы в месяц**")
    salary_base = st.number_input("Оклад мастера (руб.)", value=40000)
    salary_tax = st.number_input("Налоги на ФОТ (руб.)", value=20800)
    bonus_doctor = st.number_input("Премия / Мотивация (руб.)", value=80000)
    rent_and_other = st.number_input("Аренда и общехозяйственные (руб.)", value=35000)

# --- МАТЕМАТИЧЕСКАЯ ЛОГИКА ---
# Расчет ежемесячного платежа по лизингу (Формула аннуитета)
if lease_rate > 0 and lease_months > 0:
    monthly_rate = (lease_rate / 100) / 12
    lease_payment = device_cost * (monthly_rate * (1 + monthly_rate)**lease_months) / ((1 + monthly_rate)**lease_months - 1)
else:
    lease_payment = device_cost / lease_months if lease_months > 0 else 0

# Выручка
monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

# Переменные расходы за месяц
total_variable_costs = (clients_face * days * (cost_face + manipula)) + (clients_hair * days * (cost_hair + manipula))

# Общие фиксированные расходы (с учетом расчетного лизинга)
total_fixed_costs = lease_payment + salary_base + salary_tax + bonus_doctor + rent_and_other

# Расчет прибыли и налогов
profit_before_tax = total_revenue - total_variable_costs - total_fixed_costs
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

# Главные финансовые метрики в одну строку
c_m1, c_m2, c_m3 = st.columns(3)
c_m1.metric("📌 Общая выручка в месяц", f"{total_revenue:,.0f} руб.")
c_m2.metric("📌 Расчетный платеж по лизингу", f"{lease_payment:,.0f} руб./мес.")
if net_profit > 0:
    c_m3.metric("🟢 Чистая прибыль (налог 15%)", f"{net_profit:,.0f} руб.")
else:
    c_m3.metric("🔴 Чистый убыток проекта", f"{net_profit:,.0f} руб.")

st.markdown("<br>", unsafe_allow_html=True)

# Блок графиков: делим экран 50/50 по горизонтали
c_graph1, c_graph2 = st.columns(2)

with c_graph1:
    st.markdown("<b style='font-size:14px;'>🪐 Структура распределения доходов</b>", unsafe_allow_html=True)
    if total_revenue > 0 and net_profit > 0:
        pie_data = pd.DataFrame({
            "Категория": ["Чистая прибыль", "Переменные расходы", "Фикс. расходы + Лизинг", "Налог 15%"],
            "Сумма (руб.)": [net_profit, total_variable_costs, total_fixed_costs, tax]
        })
        # Премиальная биотех-гамма: Изумрудный, Золотой, Оливковый, Темно-зеленый
        luxury_colors = ['#004B49', '#D4AF37', '#708238', '#002524']
        fig_pie = px.pie(pie_data, values="Сумма (руб.)", names="Категория", 
                         color_discrete_sequence=luxury_colors, hole=0.4)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Круговая диаграмма активируется при выходе проекта в прибыль.")

with c_graph2:
    st.markdown("<b style='font-size:14px;'>📈 Прогноз баланса и окупаемости (6 месяцев)</b>", unsafe_allow_html=True)
    months_list = [f"Мес. {i}" for i in range(1, 7)]
    cumulative_balances = []
    
    # Стартуем с первоначальных инвестиций
    current_balance = -initial_invest
    
    for m in range(1, 7):
        # Если срок лизинга истек, убираем лизинговый платеж из расходов
        current_fixed = total_fixed_costs if m <= lease_months else (total_fixed_costs - lease_payment)
        m_profit_before_tax = total_revenue - total_variable_costs - current_fixed
        m_tax = m_profit_before_tax * 0.15 if m_profit_before_tax > 0 else 0
        m_net_profit = m_profit_before_tax - m_tax
        
        current_balance += m_net_profit
        cumulative_balances.append(current_balance)
        
    df_line = pd.DataFrame({"Баланс (руб.)": cumulative_balances}, index=months_list)
    # Отображаем компактный график
    st.line_chart(df_line, height=220)

st.caption("💡 Модель динамически пересчитывает лизинг методом аннуитета и отключает платежи по истечении его срока.")
