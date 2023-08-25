import streamlit as st
import pandas as pd
import seaborn as sns
import time

st.title("Uber pickups in NYC")

# df = pd.DataFrame({"a": list(range(21)), "b": list(range(0, 41, 2))})

# df2 = pd.DataFrame({"a": list(range(11)), "b": list(range(0, 21, 2))})


def give_df(i: int):
    # df = pd.DataFrame({"a": list(range(i + 11)), "b": list(range(0, 2 * i + 21, 2))})
    df = pd.DataFrame({"a": list(), "b": list()})
    df["a"] = pd.to_datetime(df["a"])
    time.sleep(2)
    return df


def give_df2(i: int):
    df = pd.DataFrame({"a": list(range(i + 21)), "b": list(range(0, 2 * i + 41, 2))})
    time.sleep(2)
    return df


# st.pyplot(sns.lineplot(x=df["a"], y=df["b"]))
p1 = st.empty()
p2 = st.empty()

# with p1.container():
count = 0
while True:
    df = give_df(count)
    df2 = give_df2(count)
    p1.line_chart(data=df, x="a", y="b")
    p2.line_chart(data=df2, x="a", y="b")
    count += 1
