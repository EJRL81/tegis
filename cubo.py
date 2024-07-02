# Código completo en Python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generar datos ficticios
np.random.seed(42)
n = 1000
data = {
    'timestamp': pd.date_range(start='2023-01-01', periods=n, freq='h'),
    'ip_origen': np.random.choice(['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'], n),
    'ip_destino': np.random.choice(['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4'], n),
    'tipo_evento': np.random.choice(['login', 'logout', 'data_transfer', 'error'], n),
    'severidad': np.random.choice(['low', 'medium', 'high'], n)
}
df = pd.DataFrame(data)

# Crear dimensiones de tiempo
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day
df['hour'] = df['timestamp'].dt.hour

# Crear dimensiones de IP de origen y destino
dim_ip_origen = df[['ip_origen']].drop_duplicates().reset_index(drop=True)
dim_ip_destino = df[['ip_destino']].drop_duplicates().reset_index(drop=True)

# Crear hechos
hechos = df[['timestamp', 'ip_origen', 'ip_destino', 'tipo_evento', 'severidad']]

# Crear una figura
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Crear una muestra para representar el cubo
sample = hechos.sample(100)

# Asignar colores según la severidad
colors = {'low': 'blue', 'medium': 'orange', 'high': 'red'}
sample['color'] = sample['severidad'].map(colors)

# Graficar puntos en el cubo
ax.scatter(sample['hour'], sample['day'], sample['month'], c=sample['color'], s=50, alpha=0.6, edgecolors='w')

# Etiquetas de los ejes
ax.set_xlabel('Hour')
ax.set_ylabel('Day')
ax.set_zlabel('Month')

# Título
ax.set_title('Cubo OLAP de Seguridad en la Red')

plt.show()
