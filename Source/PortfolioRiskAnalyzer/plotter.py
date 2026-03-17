import plotly.graph_objects as go
import numpy as np
import plotly.subplots as sp

def create_risk_dashboard(port_returns, initial_investment=100000):
    # --- 1. DATA PREPARATION ---
    # Cumulative Returns
    cum_returns = (1 + port_returns).cumprod()
    portfolio_value = initial_investment * cum_returns
    
    # Drawdowns
    running_max = portfolio_value.cummax()
    drawdown = (portfolio_value / running_max) - 1
    
    # Rolling VaR (95% confidence, 21-day window)
    rolling_var = port_returns.rolling(window=21).apply(lambda x: np.percentile(x, 5))

    # --- 2. CREATE SUBPLOTS ---
    fig = sp.make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.08,
        subplot_titles=("Cumulative Portfolio Value ($)", "Percentage Drawdown", "21-Day Rolling VaR (95%)")
    )

    # Plot 1: Cumulative Growth
    fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value, name="Equity Curve", fill='tozeroy'), row=1, col=1)

    # Plot 2: Drawdowns (Shaded Red)
    fig.add_trace(go.Scatter(x=drawdown.index, y=drawdown, name="Drawdown", fill='tozeroy', line_color='red'), row=2, col=1)

    # Plot 3: Rolling VaR
    fig.add_trace(go.Scatter(x=rolling_var.index, y=rolling_var, name="Rolling VaR", line_color='orange'), row=3, col=1)

    # --- 3. STYLING ---
    fig.update_layout(height=900, title_text="Portfolio Performance & Risk Analysis", showlegend=False, template="plotly_white")
    fig.update_yaxes(tickformat="$,.0f", row=1, col=1)
    fig.update_yaxes(tickformat=".1%", row=2, col=1)
    fig.update_yaxes(tickformat=".1%", row=3, col=1)
    
    return fig

def plot_var_heatmap(port_returns_unweighted):
    # 1. Define our ranges
    aapl_weights = np.linspace(0, 1, 21)  # 0% to 100% in 5% steps
    conf_levels = [0.10, 0.05, 0.01]      # 90%, 95%, 99%
    conf_labels = ["90%", "95%", "99%"]
    
    # 2. Build the Matrix
    var_matrix = []
    
    for conf in conf_levels:
        row = []
        for w in aapl_weights:
            # Create weights: [w_aapl, w_tsla]
            weights = np.array([w, 1-w])
            # Calculate daily portfolio returns
            p_returns = port_returns_unweighted.dot(weights)
            # Calculate Historical VaR (negative percentile)
            v = np.percentile(p_returns, conf * 100)
            row.append(v)
        var_matrix.append(row)

    # 3. Create the Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=var_matrix,
        x=[f"{int(w*100)}% AAPL" for w in aapl_weights],
        y=conf_labels,
        colorscale='Reds_r', # Red for high loss, lighter for low loss
        colorbar=dict(title="VaR %", tickformat=".1%")
    ))

    fig.update_layout(
        title="Risk Sensitivity Heatmap: Asset Weight vs. Confidence Level",
        xaxis_title="Portfolio Allocation",
        yaxis_title="Confidence Level",
        template="plotly_white"
    )
    
    return fig

def create_optimization_dashboard(returns_df):
    aapl_weights = np.linspace(0, 1, 21)
    
    # Pre-calculate our 3 datasets
    rets, vars_list, effs = [], [], []
    
    for w in aapl_weights:
        weights = np.array([w, 1-w])
        p_returns = returns_df.dot(weights)
        
        r = p_returns.sum()
        v = abs(np.percentile(p_returns, 5)) # 95% VaR
        
        rets.append(r)
        vars_list.append(v)
        effs.append(r / v if v != 0 else 0)

    # Create the base figure with the first view (Efficiency)
    fig = go.Figure()

    # Add the three different "Trace" versions
    # Trace 0: Return
    fig.add_trace(go.Bar(x=aapl_weights, y=rets, name="Total Return", visible=False, marker_color='green'))
    # Trace 1: VaR
    fig.add_trace(go.Bar(x=aapl_weights, y=vars_list, name="VaR (95%)", visible=False, marker_color='red'))
    # Trace 2: Efficiency (The Default)
    fig.add_trace(go.Bar(x=aapl_weights, y=effs, name="Return/Risk Ratio", visible=True, marker_color='blue'))

    # Add Buttons to toggle visibility
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            direction="right",
            x=0.5, y=1.15,
            showactive=True,
            buttons=[
                dict(label="Logic (Efficiency)", method="update", args=[{"visible": [False, False, True]}, {"title": "Risk-Adjusted Efficiency"}]),
                dict(label="Greed (Returns)", method="update", args=[{"visible": [True, False, False]}, {"title": "Total Portfolio Returns"}]),
                dict(label="Fear (VaR)", method="update", args=[{"visible": [False, True, False]}, {"title": "Value at Risk Exposure"}])
            ]
        )],
        title="Portfolio Optimization Strategy",
        xaxis_title="Weight of AAPL (Balance is TSLA)",
        template="plotly_white"
    )
    
    return fig