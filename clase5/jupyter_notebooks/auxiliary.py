import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap


def plot_boundary(X, y, model,
                  step_x=(0.1, 0.1),
                  max_x=(1, 1),
                  min_x=(-1, -1),
                  point_size=5,
                  figsize=(7, 5),
                  label_point=("1", "0"),
                  colormap_frontier=('#ffb7fe', '#93c7ff', '#a9e5c5'),
                  colormap_points=('#ff48fd', '#007aff', '#44c57f'),
                  labels_axis=("x1", "x2"),
                  legend=True,
                  legend_title=None
                  ):
    # Hotfix for bug in matplotlib 3.8.0.
    # https://github.com/matplotlib/matplotlib/issues/26949/
    if type(colormap_frontier) is tuple:
        colormap_frontier = list(colormap_frontier)
    if type(colormap_points) is tuple:
        colormap_points = list(colormap_points)

    dict_class = {
        'setosa': 0,
        'versicolor': 1,
        'virginica': 2,
    }

    # Crear la malla de puntos para el gráfico
    X1, X2 = np.meshgrid(
        np.arange(start=X[:, 0].min() + min_x[0], stop=X[:, 0].max() + max_x[0], step=step_x[0]),
        np.arange(start=X[:, 1].min() + min_x[1], stop=X[:, 1].max() + max_x[1], step=step_x[1])
    )
    X_cont = np.array([X1.ravel(), X2.ravel()]).T

    y_cat = model.predict(X_cont).reshape(X1.shape)
    y_values = np.ones_like(y_cat) * dict_class['setosa']
    y_values[y_cat == 'versicolor'] = dict_class['versicolor']
    y_values[y_cat == 'virginica'] = dict_class['virginica']
    y_values = y_values.astype("float")

    # Crear el gráfico de contorno
    plt.figure(figsize=figsize)
    plt.contourf(
        X1, X2, y_values,
        alpha=0.75, cmap=ListedColormap(colormap_frontier)
    )
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())

    # Graficar los puntos de entrenamiento
    for i, j in enumerate(np.unique(y)):
        plt.scatter(
            X[y == j, 0], X[y == j, 1],
            c=colormap_points[i], label=label_point[i],
            s=point_size
        )

    plt.xlabel(labels_axis[0])
    plt.ylabel(labels_axis[1])
    if legend:
        plt.legend(title=legend_title)