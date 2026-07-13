import streamlit as st

st.set_page_config(page_title="Калькулятор ARESSAGE PRO", layout="centered")

st.title("📊 Финансовый калькулятор ARESSAGE PRO")
st.write("Передвигайте ползунки, чтобы увидеть динамику окупаемости.")

# Блок настроек параметров
st.header("🎛️ Настройки параметров")
price = st.slider("Стоимость одной процедуры для гостя (руб.)", 5000, 15000, 9800, step=500)
cost = st.slider("Себестоимость расходных материалов (руб.)", 2000, 5000, 3300, step=100)
clients_per_day = st.slider("Количество процедур в день на 1 кабинет", 1, 10, 3)
investments = st.number_input("Стартовые инвестиции (аппарат + первая партия белка), руб.", value=350000, step=10000)

# Математическая логика расчета
margin_per_proc = price - cost
monthly_volume = clients_per_day * 30
monthly_profit = monthly_volume * margin_per_proc
payback_period = investments / monthly_profit if monthly_profit > 0 else 0

# Красивый вывод финансовых результатов
st.header("📈 Финансовые показатели")
st.success(f"💰 Ежемесячная чистая прибыль кабинета: {monthly_profit:,.0f} руб.")
st.warning(f"🎯 Маржинальность одной процедуры: {round((margin_per_proc/price)*100)}%")
st.info(f"⏳ Полная окупаемость вложений: {round(payback_period, 1)} мес.")

# Построение интерактивного графика накопленного дохода
st.header("📊 Прогноз прибыли по месяцам")
months = [f"Месяц {i}" for i in range(1, 7)]
cumulative_balances = []
current_balance = -investments

for i in range(1, 7):
    current_balance += monthly_profit
    cumulative_balances.append(current_balance)

# Отображение встроенного линейного графика
st.line_chart(cumulative_balances)
st.caption("Линия показывает баланс проекта. Точка пересечения нуля — это момент полной окупаемости инвестиций.")

