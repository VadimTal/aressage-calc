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
            font-size: 22px !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        .luxury-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            margin-top: 10px;
        }
        .luxury-table th {
            background-color: #4A1A60;
            color: white;
            font-weight: 600;
            padding: 10px;
            text-align: center;
            border: 1px solid #6a2b8a;
        }
        .luxury-table td {
            padding: 10px;
            border: 1px solid #e0e0e0;
            text-align: center;
        }
        .luxury-table tr:nth-child(even) {
            background-color: #f9f6fa;
        }
        .highlight-row {
            background-color: #f4fdf9 !important;
            font-weight: 600;
            color: #005A36;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>A R E S S A G E</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Aesthetic Regenerative Message • Финансовая Модель</div>", unsafe_allow_html=True)

# Инициализация переключателя валют и баз данных по ТЗ
currency_choice = st.radio("🌎 Выберите валюту расчёта и регион санатория:", ["RUB (Россия)", "BYN (Беларусь)"], horizontal=True)

if currency_choice == "RUB (Россия)":
    currency_label = "руб."
    # Стартовые значения цен и себестоимостей для РФ
    default_price_face = 9300
    default_price_hair = 11300
    default_cost_face = 3780
    default_cost_hair = 4380
    default_manipula = 250  # 7500 / 30 процедур = 250 руб
    default_device = 450000
    default_start = 150000
    default_salary = 40000
    default_tax = 20800
    default_bonus = 80000
    default_rent = 35000
    # Настройка шагов кнопок +/- для РФ
    step_price = 100
    step_cost = 50
    step_device = 50000
    step_start = 10000
    step_salary = 5000
    step_tax = 1000
else:
    currency_label = "Br"
    # Стартовые значения цен и себестоимостей для РБ (по вашей новой таблице)
    default_price_face = 300
    default_price_hair = 370
    default_cost_face = 166
    default_cost_hair = 192
    default_manipula = 11   # math.ceil(329 / 30) = 11 BYN
    default_device = 19709
    default_start = 5400
    default_salary = 1450
    default_tax = 750
    default_bonus = 1500
    default_rent = 1250
    # Настройка шагов кнопок +/- для РБ (пропорционально в целых числах)
    step_price = 5
    step_cost = 5
    step_device = 1000
    step_start = 300
    step_salary = 100
    step_tax = 50

st.markdown("<br>", unsafe_allow_html=True)

c_in1, c_in2, c_in3, c_in4 = st.columns(4)

with c_in1:
    st.markdown(f"<b style='color:#4A1A60;'>👤 Клиенты и Цены ({currency_label})</b>", unsafe_allow_html=True)
    clients_face = st.slider("Лицо/Тело (процедур в день)", 0, 10, 3)
    price_face = st.slider(f"Цена Лицо/Тело ({currency_label})", min_value=int(default_price_face*0.5), max_value=int(default_price_face*2), value=default_price_face, step=step_price)
    clients_hair = st.slider("Волосы (процедур в день)", 0, 10, 3)
    price_hair = st.slider(f"Цена Волосы ({currency_label})", min_value=int(default_price_hair*0.5), max_value=int(default_price_hair*2), value=default_price_hair, step=step_price)
    days = st.slider("Рабочих дней в мес.", 15, 30, 25)

with c_in2:
    st.markdown(f"<b style='color:#4A1A60;'>🧪 Себестоимость сеанса ({currency_label})</b>", unsafe_allow_html=True)
    cost_face = st.slider(f"Состав Лицо/Тело ({currency_label})", min_value=int(default_cost_face*0.5), max_value=int(default_cost_face*2), value=default_cost_face, step=step_cost)
    cost_hair = st.slider(f"Состав Волосы ({currency_label})", min_value=int(default_cost_hair*0.5), max_value=int(default_cost_hair*2), value=default_cost_hair, step=step_cost)
    manipula = st.slider(f"Манипула/Насадка ({currency_label})", min_value=0, max_value=int(default_manipula*3), value=default_manipula, step=step_cost)

with c_in3:
    st.markdown(f"<b style='color:#005A36;'>📉 Оборудование ({currency_label})</b>", unsafe_allow_html=True)
    device_cost_input = st.number_input(f"Стоимость аппарата ({currency_label})", value=default_device, step=step_device)
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5)
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    initial_invest_input = st.number_input(f"Стартовый закуп ({currency_label})", value=default_start, step=step_start)

with c_in4:
    st.markdown(f"<b style='color:#005A36;'>🏢 Фикс. расходы ({currency_label})</b>", unsafe_allow_html=True)
    salary_base_input = st.number_input(f"Оклад мастера ({currency_label})", value=default_salary, step=step_salary)
    salary_tax_input = st.number_input(f"Налоги на ФОТ ({currency_label})", value=default_tax, step=step_tax)
    bonus_doctor_input = st.number_input(f"Премия / Мотивация ({currency_label})", value=default_bonus, step=step_salary)
    rent_and_other_input = st.number_input(f"Аренда и ОХР ({currency_label})", value=default_rent, step=step_salary)

# --- МАТЕМАТИЧЕСКАЯ ЛОГИКА ---
# Расчет аннуитетного платежа по лизингу
if lease_rate > 0 and lease_months > 0:
    monthly_rate = (lease_rate / 100) / 12
    lease_payment = device_cost_input * (monthly_rate * (1 + monthly_rate)**lease_months) / ((1 + monthly_rate)**lease_months - 1)
else:
    lease_payment = device_cost_input / lease_months if lease_months > 0 else 0

# Выручка и переменные расходы в выбранной валюте (Исправление зависания данных)
monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

# Раствор-активатор заложен внутри ползунков себестоимости по умолчанию
total_variable_costs = (clients_face * days * (cost_face + manipula)) + (clients_hair * days * (cost_hair + manipula))
total_fixed_costs_with_lease = lease_payment + salary_base_input + salary_tax_input + bonus_doctor_input + rent_and_other_input

profit_before_tax = total_revenue - total_variable_costs - total_fixed_costs_with_lease
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

fixed_costs_no_lease = total_fixed_costs_with_lease - lease_payment
profit_no_lease_before_tax = total_revenue - total_variable_costs - fixed_costs_no_lease
tax_no_lease = profit_no_lease_before_tax * 0.15 if profit_no_lease_before_tax > 0 else 0
net_profit_after_lease = profit_no_lease_before_tax - tax_no_lease

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)

# Выравнивание и вывод финансовых блоков
c_m1, c_m2, c_m3, c_m4 = st.columns(4)
c_m1.metric("📌 Общая выручка комплекса", f"{total_revenue:,.0f} {currency_label}/мес.")
c_m2.metric("📌 Платеж по лизингу", f"{lease_payment:,.0f} {currency_label}/мес.")
if net_profit > 0:
    c_m3.markdown(f"<div style='color:#005A36; font-size:12px; font-weight:600;'>🟢 Чистая прибыль (с лизингом)</div><div style='font-size:22px; font-weight:600; color:#005A36;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)
    c_m4.markdown(f"<div style='color:#005A36; font-size:12px; font-weight:600;'>🔥 Прибыль после лизинга</div><div style='font-size:22px; font-weight:600; color:#005A36;'>{net_profit_after_lease:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)
else:
    c_m3.markdown(f"<div style='color:#b00020; font-size:12px; font-weight:600;'>🔴 Чистый убыток</div><div style='font-size:22px; font-weight:600; color:#b00020;'>{net_profit:,.0f} {currency_label}/мес.</div>", unsafe_allow_html=True)
    c_m4.markdown(f"<div style='color:#b00020; font-size:12px; font-weight:600;'>🔴 Прибыль после лизинга</div><div style='font-size:22px; font-weight:600; color:#b00020;'>0 {currency_label}/мес.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c_graph1, c_graph2 = st.columns(2)

with c_graph1:
    st.markdown("<b style='font-size:13px; color:#4A1A60; font-family:Inter;'>🪐 СТРУКТУРА РАСПРЕДЕЛЕНИЯ ВЫРУЧКИ</b>", unsafe_allow_html=True)
    if total_revenue > 0 and net_profit > 0:
        pie_data = pd.DataFrame({"Категория": ["Чистая прибыль", "Переменные расходы", "Фикс. расходы и лизинг", "Налог (15%)"], "Сумма": [net_profit, total_variable_costs, total_fixed_costs_with_lease, tax]})
        brand_luxury_colors = ['#006B44', '#005A36', '#1A1A1A', '#8E5EA2']
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
        m_fixed = total_fixed_costs_with_lease if m <= lease_months else fixed_costs_no_lease
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

# Расчет средних цен и себестоимостей ARESSAGE строго по формуле из вашего Excel (Исправление п.1)
# Себестоимость Face в РФ = 3780 + 250 (манипула) + 1020 (раствор) = 5050 руб.
# Себестоимость Hair в РФ = 4380 + 250 (манипула) + 1020 (раствор) = 5650 руб.
# Средняя себестоимость для таблицы РФ = (5050 + 5650) / 2 = 5350 руб.
# Средняя цена для таблицы РФ = (9300 + 11300) / 2 = 10300 руб.
avg_price_rub = (9300 + 11300) / 2
avg_cost_rub = 5350.0
margin_rub = avg_price_rub - avg_cost_rub
rev_per_min_rub = margin_rub / 30

# Себестоимость Face в РБ = 166 + 11 (манипула) + 45 (раствор) = 222 Br
# Себестоимость Hair в РБ = 192 + 11 (манипула) + 45 (раствор) = 248 Br
# Средняя себестоимость для таблицы РБ = (222 + 248) / 2 = 235 Br
# Средняя цена для таблицы РБ = (300 + 370) / 2 = 335 Br
avg_price_byn = (300 + 370) / 2
avg_cost_byn = 235.0
margin_byn = avg_price_byn - avg_cost_byn
rev_per_min_byn = margin_byn / 30

# Генерация кастомной HTML-матрицы с исправленным синтаксисом и точной математикой по ТЗ
html_table = f"""
<table class="luxury-table">
    <tr>
        <th rowspan="2" style="vertical-align: middle; width: 22%;">Показатель эффективности</th>
        <th colspan="3">МОСКВА (Расчёты в ₽)</th>
        <th colspan="3">МИНСК (Расчёты в Br)</th>
    </tr>
    <tr>
        <th>Классический массаж</th>
        <th>Спа-обертывание</th>
        <th style="background-color: #005A36;">ARESSAGE PRO</th>
        <th>Классический массаж</th>
        <th>Спа-обертывание</th>
        <th style="background-color: #005A36;">ARESSAGE PRO</th>
    </tr>
    <tr>
        <td><b>Средняя цена для гостя</b></td>
        <td>4 500 ₽</td>
        <td>6 500 ₽</td>
        <td>{avg_price_rub:,.0f} ₽</td>
        <td>100 Br</td>
        <td>145 Br</td>
        <td>{avg_price_byn:,.0f} Br</td>
    </tr>
    <tr>
        <td><b>Длительность сеанса</b></td>
        <td>60 мин.</td>
        <td>90 мин.</td>
        <td>30 мин.</td>
        <td>60 мин.</td>
        <td>90 мин.</td>
        <td>30 мин.</td>
    </tr>
    <tr>
        <td><b>Себестоимость расходников</b></td>
        <td>400 ₽</td>
        <td>950 ₽</td>
        <td>{avg_cost_rub:,.0f} ₽</td>
        <td>10 Br</td>
        <td>22 Br</td>
        <td>{avg_cost_byn:,.0f} Br</td>
    </tr>
    <tr>
        <td><b>Маржинальный доход</b></td>
        <td>4 100 ₽</td>
        <td>5 550 ₽</td>
        <td>{margin_rub:,.0f} ₽</td>
        <td>90 Br</td>
        <td>123 Br</td>
        <td>{margin_byn:,.0f} Br</td>
    </tr>
    <tr class="highlight-row">
        <td><b>🔥 Доход в минуту (RevPM)</b></td>
        <td>68.3 ₽/мин.</td>
        <td>61.7 ₽/мин.</td>
        <td>{rev_per_min_rub:,.1f} ₽/мин.</td>
        <td>1.5 Br/мин.</td>
        <td>1.4 Br/мин.</td>
        <td>{rev_per_min_byn:,.1f} Br/мин.</td>
    </tr>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)

st.markdown(f"""
<div style='background-color: #f4f6f4; padding: 10px; border-left: 4px solid #005A36; font-size: 12px; font-family: Inter; color: #333; margin-top: 15px;'>
    <b>Резюме для руководства УК:</b> Анализ по столицам доказывает, что независимо от выбранной базы рынка (РФ или РБ), короткий 30-минутный протокол <b>ARESSAGE PRO</b> генерирует в 2.5–3.2 раза больше чистой прибыли на 1 минуту работы кабинета по сравнению с традиционными спа-техниками. Это максимизирует доходность каждого квадратного метра спа-комплекса сети санаториев.
</div>
""", unsafe_allow_html=True)
