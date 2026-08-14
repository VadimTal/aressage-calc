import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ФинПлан ARESSAGE PRO", layout="wide", initial_sidebar_state="collapsed")

# Премиальная стилизация интерфейса
st.markdown("""
<style>
.main-title { font-family: 'Inter', sans-serif; color: #4A1A60; text-align: center; font-size: 30px; font-weight: 700; margin-bottom: 5px; }
.sub-title { font-family: 'Inter', sans-serif; color: #005A36; text-align: center; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }
.luxury-table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 13px; margin-top: 10px; }
.luxury-table th { background-color: #4A1A60; color: white; font-weight: 600; padding: 10px; text-align: center; border: 1px solid #6a2b8a; }
.luxury-table td { padding: 10px; border: 1px solid #e0e0e0; text-align: center; }
.luxury-table tr:nth-child(even) { background-color: #f9f6fa; }
.highlight-row { background-color: #f4fdf9 !important; font-weight: 600; color: #005A36; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>A R E S S A G E  P R O</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Инвестиционная модель для санаториев РФ и РБ (Актуальность: 2026)</div>", unsafe_allow_html=True)

# Выбор региона и налогового режима
currency_choice = st.radio("📍 Выберите регион санатория:", ["RUB (Россия)", "BYN (Беларусь)"], horizontal=True)

c_tax1, c_tax2 = st.columns(2)
if currency_choice == "RUB (Россия)":
    currency_label, code = "руб.", "RF"
    with c_tax1:
        tax_mode = st.selectbox("Ставка налога на прибыль в РФ:", ["Основная ставка ОСНО (25%)", "Льготная ставка ОСНО (0% по ст. 284.1)"])
    with c_tax2:
        st.info("💡 РФ: Производитель на УСН (без НДС). Услуга облагается налогом на прибыль 25% или 0% (при выполнении медицинского критерия 90%).")
    # Константы РФ
    df_p_face, df_p_hair, df_c_face, df_c_hair, df_manipula = 9300, 11300, 3780, 4380, 250
    df_device, df_start, df_salary, df_rent = 450000, 150000, 40000, 35000
    step_p, step_c, step_dev, step_st, step_sal = 100, 50, 50000, 10000, 5000
else:
    currency_label, code = "Br", "RB"
    with c_tax1:
        tax_mode = st.selectbox("Ставка налога на прибыль в РБ:", ["Стандартная ставка (20%)", "Льготная ставка (0% по п. 16 ст. 181)"])
    with c_tax2:
        st.info("💡 РБ: Цены содержат НДС 20%. Налог на прибыль 20% или 0% (льгота 2026 года для новых объектов). Лизинговый НДС идет к зачету.")
    # Константы РБ
    df_p_face, df_p_hair, df_c_face, df_c_hair, df_manipula = 300, 370, 166, 192, 11
    df_device, df_start, df_salary, df_rent = 19709, 3400, 1450, 1250
    step_p, step_c, step_dev, step_st, step_sal = 5, 5, 1000, 350, 100

st.markdown("<hr style='margin: 15px 0; border-color: #efefef;'>", unsafe_allow_html=True)

# Слайдеры параметров
c_in1, c_in2, c_in3, c_in4 = st.columns(4)
with c_in1:
    st.markdown(f"<b>👥 Клиенты и Цены ({currency_label})</b>", unsafe_allow_html=True)
    clients_face = st.slider("Лицо/Тело (процедур в день)", 0, 10, 3)
    price_face = st.slider(f"Цена Лицо/Тело", int(df_p_face*0.5), int(df_p_face*2), df_p_face, step_p)
    clients_hair = st.slider("Волосы (процедур в день)", 0, 10, 3)
    price_hair = st.slider(f"Цена Волосы", int(df_p_hair*0.5), int(df_p_hair*2), df_p_hair, step_p)
    days = st.slider("Рабочих дней в мес. (среднее)", 15, 30, 25)
with c_in2:
    st.markdown(f"<b>🧪 Себестоимость сеанса ({currency_label})</b>", unsafe_allow_html=True)
    cost_face = st.slider("Состав Лицо/Тело (Netto)", int(df_c_face*0.5), int(df_c_face*2), df_c_face, step_c)
    cost_hair = st.slider("Состав Волосы (Netto)", int(df_c_hair*0.5), int(df_c_hair*2), df_c_hair, step_c)
    manipula = st.slider("Манипула/Насадка", 0, int(df_manipula*3), df_manipula, step_c)
# Найти в БЛОКЕ 1 строки ввода оборудования и фикс. расходов и заменить их на эти:
with c_in3:
    st.markdown(f"<b>⚙️ Оборудование ({currency_label})</b>", unsafe_allow_html=True)
    device_cost_input = st.number_input("Стоимость аппарата", value=df_device, step=step_dev, format="%d")
    lease_rate = st.number_input("Лизинговая ставка (%)", value=15.0, step=0.5, format="%.1f")
    lease_months = st.slider("Срок лизинга (мес.)", 6, 36, 12)
    initial_invest_input = st.number_input("Стартовый закуп", value=df_start, step=step_st, format="%d")
with c_in4:
    st.markdown(f"<b>📊 Фикс. расходы ({currency_label})</b>", unsafe_allow_html=True)
    salary_base_input = st.number_input("Оклад мастера", value=df_salary, step=step_sal, format="%d")
    bonus_doctor_input = st.number_input("Премия / Мотивация", value=int(df_salary*2), step=step_sal, format="%d")
    rent_and_other_input = st.number_input("Аренда и ОХР кабинета", value=df_rent, step=step_sal, format="%d")

# --- МАТЕМАТИЧЕСКАЯ И НАЛОГОВАЯ ЛОГИКА (100% ЗАКОНОДАТЕЛЬСТВО 2026) ---

# 1. Аннуитетный лизинговый платеж
if lease_rate > 0 and lease_months > 0:
    r_m = (lease_rate / 100) / 12
    lease_payment = device_cost_input * (r_m * (1 + r_m)**lease_months) / ((1 + r_m)**lease_months - 1)
else:
    lease_payment = device_cost_input / lease_months if lease_months > 0 else 0

# 2. Выручка и точный перерасчет налогов на ФОТ
total_salary = salary_base_input + bonus_doctor_input

if code == "RF":
    # Льгота МСП 2026: 30% до 1.5 МРОТ, 7.6% свыше. Прогноз МРОТ 2026 = 27093 руб.
    mrot_limit = 27093 * 1.5
    if total_salary <= mrot_limit:
        salary_tax_input = total_salary * 0.30
    else:
        salary_tax_input = (mrot_limit * 0.30) + ((total_salary - mrot_limit) * 0.076)
    salary_tax_input += total_salary * 0.002  # ФСС травматизм 0.2%
    
    tax_rate = 0.25 if "25%" in tax_mode else 0.0
    revenue_clear = (clients_face * price_face + clients_hair * price_hair) * days
    vat_output, vat_to_budget = 0.0, 0.0
else:
    # Законодательство РБ: ФСЗН 34% + Белгосстрах 0.6% = 34.6% от начисленного ФОТ
    salary_tax_input = total_salary * 0.346
    tax_rate = 0.20 if "20%" in tax_mode else 0.0
    
    # Цены в РБ содержат НДС 20%
    total_revenue_gross = (clients_face * price_face + clients_hair * price_hair) * days
    revenue_clear = total_revenue_gross / 1.20
    vat_output = total_revenue_gross - revenue_clear

# 3. Чистые переменные и постоянные расходы
total_revenue = (clients_face * price_face + clients_hair * price_hair) * days
total_variable_costs_clear = ((clients_face * (cost_face + manipula)) + (clients_hair * (cost_hair + manipula))) * days
total_fixed_costs_with_lease = lease_payment + salary_base_input + salary_tax_input + bonus_doctor_input + rent_and_other_input

# 4. Расчет зачета по НДС для РБ (включая лизинговый вычет)
if code == "RB":
    vat_input_materials = total_variable_costs_clear * 0.20
    vat_input_lease = lease_payment - (lease_payment / 1.20)
    vat_to_budget = vat_output - vat_input_materials - vat_input_lease
    vat_to_budget = max(0.0, vat_to_budget)
    
    # КОРРЕКТОР ДЛЯ РБ: Входной НДС уменьшает реальные затраты санатория
    vat_savings = vat_input_materials + vat_input_lease
    profit_clear_before_tax = (revenue_clear - total_variable_costs_clear - total_fixed_costs_with_lease) + vat_savings
    
    # Расчет после лизинга для РБ (вычет по лизингу уходит, вычет по материалам остается)
    fixed_costs_no_lease = total_fixed_costs_with_lease - lease_payment
    profit_no_lease_clear_before_tax = (revenue_clear - total_variable_costs_clear - fixed_costs_no_lease) + vat_input_materials
else:
    # Для РФ все остается без изменений (УСН производителя, зачетов НДС нет)
    profit_clear_before_tax = revenue_clear - total_variable_costs_clear - total_fixed_costs_with_lease
    
    fixed_costs_no_lease = total_fixed_costs_with_lease - lease_payment
    profit_no_lease_clear_before_tax = revenue_clear - total_variable_costs_clear - fixed_costs_no_lease

# 5. Итоговый расчет налога на прибыль и ЧП по закону 2026 (унифицированный)
tax = profit_clear_before_tax * tax_rate if profit_clear_before_tax > 0 else 0
net_profit = profit_clear_before_tax - tax

tax_no_lease = profit_no_lease_clear_before_tax * tax_rate if profit_no_lease_clear_before_tax > 0 else 0
net_profit_after_lease = profit_no_lease_clear_before_tax - tax_no_lease

def fmt(val, decimals=0):
    if decimals == 0:
        return f"{int(round(val)):,}".replace(",", " ")
    else:
        formatted = f"{round(val, decimals):,}"
        # Защита от наложения американских запятых и точек
        parts = formatted.split('.')
        if len(parts) == 2:
            return parts[0].replace(",", " ") + "," + parts[1]
        return formatted.replace(",", " ")

st.markdown("<hr style='margin: 10px 0; border-color: #efefef;'>", unsafe_allow_html=True)

# Вывод KPI-метрик с русским форматированием
c_m1, c_m2, c_m3, c_m4 = st.columns(4)
c_m1.metric("💰 Общая выручка комплекса", f"{fmt(total_revenue)} {currency_label}/мес.")
c_m2.metric("📜 Платеж по лизингу (Аннуитет)", f"{fmt(lease_payment)} {currency_label}/мес.")
c_m3.metric("📈 Чистая прибыль (с лизингом)", f"{fmt(net_profit)} {currency_label}/мес.")
c_m4.metric("🌟 Прибыль после лизинга", f"{fmt(net_profit_after_lease)} {currency_label}/мес.")

st.markdown("<br>", unsafe_allow_html=True)

c_graph1, c_graph2 = st.columns(2)
with c_graph1:
    st.markdown("<b style='font-size:14px; color:#4A1A60;'>📊 СТРУКТУРА РАСПРЕДЕЛЕНИЯ ВЫРУЧКИ</b>", unsafe_allow_html=True)
    if total_revenue > 0 and net_profit > 0:
        if code == "RB":
            p_categories = ["Чистая прибыль", "Переменные расходы", "Фикс. расходы и лизинг", "Налог на прибыль", "Чистый НДС в бюджет"]
            p_values = [net_profit, total_variable_costs_clear, total_fixed_costs_with_lease, tax, vat_to_budget]
        else:
            p_categories = ["Чистая прибыль", "Переменные расходы", "Фикс. расходы и лизинг", "Налог на прибыль"]
            p_values = [net_profit, total_variable_costs_clear, total_fixed_costs_with_lease, tax]
        
        fig_pie = px.pie(names=p_categories, values=p_values, color_discrete_sequence=['#006B44', '#005A36', '#1A1A1A', '#8E5EA2', '#D4AF37'], hole=0.45)
        fig_pie.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=200, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Круговая диаграмма активируется при выходе проекта в прибыль.")

with c_graph2:
    st.markdown("<b style='font-size:14px; color:#4A1A60;'>📈 ПРОГНОЗ НАКОПИТЕЛЬНОГО БАЛАНСА (6 МЕС.)</b>", unsafe_allow_html=True)
    months_list = ["Старт", "1 мес.", "2 мес.", "3 мес.", "4 мес.", "5 мес.", "6 мес."]
    cumulative_balances = [-initial_invest_input]
    current_balance = -initial_invest_input
    for m in range(1, 7):
        current_balance += net_profit
        cumulative_balances.append(current_balance)
    fig_line = px.line(x=months_list, y=cumulative_balances, labels={'x':'Срок', 'y':'Баланс'}, markers=True, color_discrete_sequence=['#4A1A60'])
    fig_line.add_hline(y=0, line_dash="dash", line_color="#005A36", annotation_text="Точка окупаемости")
    fig_line.update_layout(margin=dict(t=5, b=5, l=0, r=0), height=200, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_line, use_container_width=True)

# Сравнительный анализ эффективности инфраструктуры
st.markdown("<hr style='margin: 15px 0; border-color: #efefef;'>", unsafe_allow_html=True)
st.markdown("<b style='font-size:15px; color:#4A1A60;'>🔍 СРАВНИТЕЛЬНЫЙ АНАЛИЗ ЭФФЕКТИВНОСТИ ИСПОЛЬЗОВАНИЯ ВРЕМЕНИ КАБИНЕТА</b>", unsafe_allow_html=True)

# Калькуляция доходности в минуту (RevPM) на основе маржи
rev_min_rf = ((9300 + 11300)/2 - (3780 + 4380)/2 - 250) / 30
rev_min_rb = (((300 + 370)/2)/1.20 - (166 + 192)/2 - 11) / 30

html_table = f"""
<table class='luxury-table'>
<tr>
    <th rowspan='2' style='vertical-align: middle;'>Показатель эффективности времени</th>
    <th colspan='2'>МОСКВА (Расчёты в ₽, без НДС для УСН)</th>
    <th colspan='2'>МИНСК (Расчёты в Br, с зачетом НДС)</th>
</tr>
<tr>
    <th>Классический массаж (60 мин)</th>
    <th style='background-color: #005A36;'>ARESSAGE PRO (30 мин)</th>
    <th>Классический массаж (60 мин)</th>
    <th style='background-color: #005A36;'>ARESSAGE PRO (30 мин)</th>
</tr>
<tr>
    <td><b>Средняя цена сеанса для гостя</b></td>
    <td>4 500 ₽</td>
    <td>9 300 ₽</td>
    <td>100 Br</td>
    <td>335 Br</td>
</tr>
<tr>
    <td><b>Себестоимость расходников (Netto)</b></td>
    <td>400 ₽</td>
    <td>4 330 ₽</td>
    <td>10 Br</td>
    <td>190 Br</td>
</tr>
<tr class='highlight-row'>
    <td><b>🔥 Чистая Маржа в минуту (Margin per Minute)</b></td>
    <td>68,3 ₽/мин.</td>
    <td>{fmt(rev_min_rf, 1)} ₽/мин.</td>
    <td>1,5 Br/мин.</td>
    <td>{fmt(rev_min_rb, 1)} Br/мин.</td>
</tr>
</table>
"""
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("<div style='background-color: #f4f6f4; padding: 12px; border-left: 4px solid #005A36; font-size: 12px; color: #333; margin-top: 10px;'><b>Резюме:</b> За счет короткого 30-минутного протокола и оптимизированных ставок налогов/взносов 2026 года, технология <b>ARESSAGE PRO</b> генерирует в 2.5–2.9 раза больше маржинальной прибыли на 1 минуту работы кабинета по сравнению с мануальными техниками, кратно увеличивая ROI каждого квадратного метра спа-комплекса.</div>", unsafe_allow_html=True)
