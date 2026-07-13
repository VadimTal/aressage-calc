import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ФинПлан ARESSAGE PRO 2.0", layout="wide")

st.title("📊 Комплексный финансовый план ARESSAGE PRO")
st.write("Настройте параметры ниже, чтобы увидеть полную структуру расходов, налогов и динамику прибыли.")

# Разделение экрана на две колонки: слева настройки, справа графики и цифры
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.header("🎛️ Интерактивная панель")
    
    with st.expansions("👤 1. Поток клиентов и Цены"):
        clients_face = st.slider("Процедур 'Лицо/Тело' в день", 0, 10, 3)
        price_face = st.slider("Цена 'Лицо/Тело' для гостя (руб.)", 5000, 15000, 9300, step=100)
        clients_hair = st.slider("Процедур 'Волосы' в день", 0, 10, 3)
        price_hair = st.slider("Цена 'Волосы' для гостя (руб.)", 5000, 15000, 11300, step=100)
        days = st.slider("Рабочих дней кабинета в месяце", 15, 30, 22)

    with st.expansions("🧪 2. Переменные расходы (на 1 процедуру)"):
        cost_face = st.slider("Расходники: состав Лицо/Тело (руб.)", 1500, 6000, 3100, step=50)
        cost_hair = st.slider("Расходники: состав Волосы (руб.)", 1500, 6000, 3766, step=50)
        manipula = st.slider("Амортизация манипулы/насадки (руб.)", 0, 1000, 425, step=25)

    with st.expansions("📉 3. Инвестиции и Лизинг"):
        lease_payment = st.number_input("Месячный платеж по лизингу аппарата (руб.)", value=33333)
        lease_percent = st.number_input("Проценты по лизингу в месяц (руб.)", value=4000)
        lease_months = st.slider("Срок лизинга (месяцев)", 6, 36, 12)
        initial_invest = st.number_input("Стартовый закуп составов/обучение (руб.)", value=150000)

    with st.expansions("🏢 4. Фиксированные расходы в месяц"):
        salary_base = st.number_input("Оклад мастера/медсестры (руб.)", value=40000)
        salary_tax = st.number_input("Налоги на ФОТ (руб.)", value=20800)
        bonus_doctor = st.number_input("Премия врача / Мотивация (руб.)", value=80000)
        rent_and_other = st.number_input("Аренда и общехозяйственные расходы (руб.)", value=35000)

# Математические расчеты (Логика вашей Excel-модели)
monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

# Общие переменные за месяц
total_cost_face = clients_face * days * (cost_face + manipula)
total_cost_hair = clients_hair * days * (cost_hair + manipula)
total_variable_costs = total_cost_face + total_cost_hair

# Общие фиксированные за месяц
total_fixed_costs = lease_payment + lease_percent + salary_base + salary_tax + bonus_doctor + rent_and_other

# Прибыль и налоги
profit_before_tax = total_revenue - total_variable_costs - total_fixed_costs
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

# Вывод результатов в правую колонку
with col_right:
    st.header("📈 Финансовые результаты")
    
    c1, c2 = st.columns(2)
    c1.metric("Общая выручка в месяц", f"{total_revenue:,.0f} руб.")
    if net_profit > 0:
        c2.metric("Чистая прибыль (после налогов 15%)", f"{net_profit:,.0f} руб.", delta_color="normal")
    else:
        c2.metric("Чистая прибыль", f"{net_profit:,.0f} руб.", delta_color="inverse")

    # 1. Круговая диаграмма состава цены (Pie Chart)
    st.subheader("🍕 Структура распределения выручки")
    if total_revenue > 0 and net_profit > 0:
        pie_data = pd.DataFrame({
            "Категория": ["Чистая прибыль", "Расходники и составы", "Фиксированные расходы + Лизинг", "Налог (15%)"],
            "Сумма (руб.)": [net_profit, total_variable_costs, total_fixed_costs, tax]
        })
        fig_pie = px.pie(pie_data, values="Сумма (руб.)", names="Категория", 
                         color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("⚠️ Выручка отсутствует или проект в убытке. Круговая диаграмма появится при выходе в прибыль.")

    # 2. Линейный график динамики по месяцам (Прогноз на полгода)
    st.subheader("📅 Прогноз баланса и окупаемости проекта (6 месяцев)")
    months_list = [f"Месяц {i}" for i in range(1, 7)]
    cumulative_balances = []
    
    # Стартуем с минуса (первоначальный закуп)
    current_balance = -initial_invest
    
    for m in range(1, 7):
        # Если лизинг еще выплачивается, вычитаем его, если срок кончился — фиксированные расходы уменьшаются
        current_fixed = total_fixed_costs if m <= lease_months else (total_fixed_costs - lease_payment - lease_percent)
        m_profit_before_tax = total_revenue - total_variable_costs - current_fixed
        m_tax = m_profit_before_tax * 0.15 if m_profit_before_tax > 0 else 0
        m_net_profit = m_profit_before_tax - m_tax
        
        current_balance += m_net_profit
        cumulative_balances.append(current_balance)
        
    df_line = pd.DataFrame({"Баланс проекта (руб.)": cumulative_balances}, index=months_list)
    st.line_chart(df_line)
    st.caption("График учитывает прекращение лизинговых платежей после завершения указанного вами срока лизинга.")
