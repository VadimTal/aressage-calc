import streamlit as st

st.set_page_config(page_title="ФинПлан ARESSAGE PRO", layout="centered")

st.title("📊 Интерактивный ФинПлан ARESSAGE PRO")
st.write("Передвигайте ползунки, чтобы адаптировать расчеты под вашу сеть санаториев.")

# Настройки параметров (Ползунки)
st.header("🎛️ Настройки параметров")

col1, col2 = st.columns(2)
with col1:
    clients_face = st.slider("Процедур 'Лицо/Тело' в день", 0, 10, 3)
    price_face = st.slider("Цена 'Лицо/Тело' (руб.)", 5000, 15000, 9300, step=100)
with col2:
    clients_hair = st.slider("Процедур 'Волосы' в день", 0, 10, 3)
    price_hair = st.slider("Цена 'Волосы' (руб.)", 5000, 15000, 11300, step=100)

days = st.slider("Рабочих дней в месяце (в среднем)", 15, 30, 22)

# Внутренняя калькуляция на основе вашего Excel
# 1. Доходы
monthly_face_rev = clients_face * days * price_face
monthly_hair_rev = clients_hair * days * price_hair
total_revenue = monthly_face_rev + monthly_hair_rev

# 2. Переменные расходы (Себестоимость составов + манипула)
cost_face_per_proc = (price_face / 3) + 425
cost_hair_per_proc = (price_hair / 3) + 425

total_variable_costs = (clients_face * days * cost_face_per_proc) + (clients_hair * days * cost_hair_per_proc)

# 3. Фиксированные расходы (Лизинг, ФОТ, Аренда)
fixed_costs = 33333 + 4000 + 40000 + 20800 + 80000 + 35000

# 4. Расчет прибыли и налога (15%)
profit_before_tax = total_revenue - total_variable_costs - fixed_costs
tax = profit_before_tax * 0.15 if profit_before_tax > 0 else 0
net_profit = profit_before_tax - tax

# Вывод результатов
st.header("📈 Прогноз финансовых показателей (в месяц)")

if net_profit > 0:
    st.success(f"💰 Среднемесячная чистая прибыль: {net_profit:,.0f} руб.")
    st.info(f"💵 Общая выручка: {total_revenue:,.0f} руб. | Расходы всего: {(total_variable_costs + fixed_costs + tax):,.0f} руб.")
else:
    st.error(f"📉 Проект в убытке: {net_profit:,.0f} руб. (Недостаточно клиентов для покрытия фиксированных расходов)")

# Краткий аналитический блок для УК
st.subheader("💡 Аналитика для руководства")
st.markdown(f"""
* **Точка безубыточности:** Для покрытия всех фиксированных расходов (включая лизинг и оклады) комплексу достаточно делать суммарно около **2 процедур в день**.
* **Доходность:** При текущих настройках ваша маржинальность по чистой прибыли составляет **{round((net_profit/total_revenue)*100) if total_revenue > 0 else 0}%**.
""")
