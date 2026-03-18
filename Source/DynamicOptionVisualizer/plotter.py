import plotly.graph_objects as go

def plot_3d_option_surface(S, T, price, delta, gamma):
    # Convert T back to days for the axis label (looks better)
    T_days = T * 365
    
    fig = go.Figure()

    # Add the "Price" Surface (Visible by default)
    fig.add_trace(go.Surface(x=S, y=T_days, z=price, name="Price", colorscale='Viridis'))

    # Add the "Delta" Surface (Hidden by default)
    fig.add_trace(go.Surface(x=S, y=T_days, z=delta, name="Delta", colorscale='RdBu', visible=False))

    # Add the "Gamma" Surface (Hidden by default)
    fig.add_trace(go.Surface(x=S, y=T_days, z=gamma, name="Gamma", colorscale='Plasma', visible=False))

    # Add Dropdown Menu to switch surfaces
    fig.update_layout(
        updatemenus=[dict(
            buttons=[
                dict(label="Option Price", method="update", args=[{"visible": [True, False, False]}]),
                dict(label="Delta (Speed)", method="update", args=[{"visible": [False, True, False]}]),
                dict(label="Gamma (Acceleration)", method="update", args=[{"visible": [False, False, True]}])
            ],
            direction="down", showactive=True, x=0.1, y=1.1
        )],
        title="Dynamic Option Risk Surface",
        scene=dict(
            xaxis_title='Stock Price (Spot)',
            yaxis_title='Days to Expiration',
            zaxis_title='Metric Value',
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.7), # Flattens the Z slightly for better viewing.
        )
    )

    fig.show()