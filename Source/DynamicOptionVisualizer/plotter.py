import plotly.graph_objects as go
import numpy as np
from option_library import *

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


def create_pnl_simulator(S_grid, T_grid, price_grid):
    # Assume we bought 10 contracts (1000 shares) at the center of the grid
    # Entry: S=100, T=30 days. Let's find that price in our grid.
    entry_price = price_grid[-1, len(S_grid)//2] 
    pnl_grid = (price_grid - entry_price) * 1000 # 10 contracts
    
    fig = go.Figure()

    # 1. Add the 3D P&L Surface
    fig.add_trace(go.Surface(x=S_grid, y=T_grid*365, z=pnl_grid, 
                             colorscale='RdYlGn', name="Total P&L"))

    # 2. Add a 'Zero Plane' (To see where you start losing money)
    zero_plane = np.zeros_like(pnl_grid)
    fig.add_trace(go.Surface(x=S_grid, y=T_grid*365, z=zero_plane, 
                             showscale=False, opacity=0.3, colorscale=[[0, 'grey'], [1, 'grey']]))

    fig.update_layout(
        title="Live Portfolio P&L Stress Test",
        scene=dict(
            xaxis_title="Stock Price",
            yaxis_title="Days Left",
            zaxis_title="Profit / Loss ($)"
        )
    )
    
    fig.show()

def create_pnl_slider_demo(S_range, K, r, sigma):
    # 1. Setup the Time Steps (from 30 days to 0.5 days)
    days_to_expiry = np.arange(30, 0, -1)
    
    # 2. Calculate Entry Price (at Day 30, Spot=100)
    # We'll use the mid-point of our S_range as the 'purchase' spot
    S_entry = 100
    T_entry = 30 / 365
    v_entry, _, _, _, _ = calculate_bs_metrics(S_entry, K, T_entry, r, sigma)

    # 3. Create the Frames (One for each day)
    frames = []
    for day in days_to_expiry:
        T_current = day / 365
        # Calculate P&L for the entire price range at THIS specific day
        prices, _, _, _, _ = calculate_bs_metrics(S_range, K, T_current, r, sigma)
        pnl = (prices - v_entry) * 100 # Profit for 1 contract (100 shares)
        
        frames.append(go.Frame(
            data=[go.Scatter(x=S_range, y=pnl, mode='lines', line=dict(color="green", width=3))],
            name=str(day)
        ))

    # 4. Create the Base Figure
    fig = go.Figure(
        data=[frames[0].data[0]], # Start with Day 30
        layout=go.Layout(
            title="Interactive P&L Stress Test: Time Decay (Theta)",
            xaxis=dict(title="Stock Price", range=[min(S_range), max(S_range)]),
            yaxis=dict(title="Profit / Loss ($)")
        ),
        frames=frames
    )

    # 5. Add the actual Slider
    sliders = [dict(
        steps=[dict(method="animate", args=[[f.name], dict(mode="immediate", frame=dict(duration=100, redraw=True))],
                    label=f"{f.name} Days") for f in frames],
        transition=dict(duration=0),
        x=0, y=0, currentvalue=dict(font=dict(size=12), prefix="Days to Expiration: ", visible=True, xanchor="right")
    )]
    
    fig.update_layout(sliders=sliders)
    fig.show()