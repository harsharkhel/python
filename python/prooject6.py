import numpy as np
import pandas as pd
n = 1000
vechiles = np.random.randint(10 , 40 , n)
print(vechiles)
speed = np.random.randint(20 , 80 , n)
speed = 80 - (vechiles * 0.2) + np.random.randint(0 , 5 , n)
hours = np.random.randint(1 , 5 , n)
peak_hour = (
    ((hours >= 7) & (hours <= 10)) |
    ((hours >= 17) & (hours <= 21))
)
weather = np.random.choice(['rainy', 'cloudy', 'sunny'], n)
conditions = [
    (weather == 'rainy'),
    (weather == 'cloudy'),
    (weather == 'sunny')
]

choices = ['High', 'Medium', 'Low']

congestion = np.select(conditions, choices, default='Unknown')
congestion = np.where(
    speed < 25,
    "high",
    np.where(speed < 50, "medium", "low")
)
df = pd.DataFrame({'vechiles' : vechiles , 'speed' : speed, 'hours' : hours, 'peak_hour' : peak_hour, 'weather' : weather, 'congestion' : congestion})
print(df.head())
print(df.shape())