import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, render_template, request

app = Flask(__name__)

def create_plots(data, iterations, method, dist_type):
    n = len(data)
    mu, sigma = np.mean(data), np.std(data)
    
    # Common layout settings
    layout_settings = dict(
        template="plotly_white",
        margin=dict(l=40, r=40, t=80, b=40),  # Increased top margin for subtitles
        title_y=0.9,
        title_x=0.5,
        font=dict(size=12)
    )

    # --- STEP 1: Population Model ---
    subtitle = ""
    if method == 'bootstrap':
        pop_data = data
        pop_title = "Step 1: Empirical Data"
        subtitle = f"N={n} original points"
    else:
        if dist_type == 'normal':
            pop_data = np.random.normal(loc=mu, scale=sigma, size=1000)
            pop_title = "Step 1: Theoretical World (Normal)"
            subtitle = f"Parameters: μ={mu:.2f}, σ={sigma:.2f}"
        elif dist_type == 'uniform':
            low, high = np.min(data), np.max(data)
            pop_data = np.random.uniform(low=low, high=high, size=1000)
            pop_title = "Step 1: Theoretical World (Uniform)"
            subtitle = f"Range: [{low:.2f} to {high:.2f}]"
        elif dist_type == 'exponential':
            pop_data = np.random.exponential(scale=mu, size=1000)
            pop_title = "Step 1: Theoretical World (Exponential)"
            subtitle = f"λ (1/mean): {1/mu:.4f}"
        elif dist_type == 'lognormal':
            # Parameters for lognormal distribution
            pop_data = np.random.lognormal(mean=np.log(mu), sigma=0.5, size=1000)
            pop_title = "Step 1: Theoretical World (Log-Normal)"
            subtitle = f"Base Mean: {mu:.2f}"

    fig1 = go.Figure(data=[go.Histogram(x=pop_data, nbinsx=30, marker_color='#636EFA')])
    # We combine Title and Subtitle using HTML line break <br>
    fig1.update_layout(
        title=f"<b>{pop_title}</b><br><span style='font-size:10px; color:gray;'>{subtitle}</span>",
        height=350, 
        **layout_settings
    )

    # --- STEP 2: A Single Random Sample ---
    if method == 'bootstrap':
        single_sample = np.random.choice(data, size=n, replace=True)
    else:
        if dist_type == 'normal': single_sample = np.random.normal(loc=mu, scale=sigma, size=n)
        elif dist_type == 'uniform': single_sample = np.random.uniform(low=np.min(data), high=np.max(data), size=n)
        elif dist_type == 'exponential': single_sample = np.random.exponential(scale=mu, size=n)
        elif dist_type == 'lognormal': single_sample = np.random.lognormal(mean=np.log(mu), sigma=0.5, size=n)

    fig2 = go.Figure(data=[go.Bar(y=single_sample, marker_color='#EF553B')])
    fig2.update_layout(title=f"<b>Step 2: One Sample</b><br><span style='font-size:10px; color:gray;'>Random draw of {n} items</span>", height=350, **layout_settings)

    # --- STEP 3: The Sampling Distribution ---
    if method == 'bootstrap':
        resamples = np.random.choice(data, size=(iterations, n), replace=True)
    else:
        if dist_type == 'normal': resamples = np.random.normal(loc=mu, scale=sigma, size=(iterations, n))
        elif dist_type == 'uniform': resamples = np.random.uniform(low=np.min(data), high=np.max(data), size=(iterations, n))
        elif dist_type == 'exponential': resamples = np.random.exponential(scale=mu, size=(iterations, n))
        elif dist_type == 'lognormal': resamples = np.random.lognormal(mean=np.log(mu), sigma=0.5, size=(iterations, n))

    sim_means = np.mean(resamples, axis=1)
    low, high = np.percentile(sim_means, [2.5, 97.5])
    
    fig3 = go.Figure(data=[go.Histogram(x=sim_means, nbinsx=40, marker_color='#00CC96')])
    fig3.add_vline(x=low, line_dash="dash", line_color="red")
    fig3.add_vline(x=high, line_dash="dash", line_color="red")
    fig3.update_layout(title=f"<b>Step 3: Distribution of Means</b><br><span style='font-size:10px; color:gray;'>Result of {iterations} simulations</span>", height=400, **layout_settings)

    return (pio.to_html(fig1, full_html=False, config={'responsive': True}), 
            pio.to_html(fig2, full_html=False, config={'responsive': True}), 
            pio.to_html(fig3, full_html=False, config={'responsive': True}), 
            low, high)

@app.route('/', methods=['GET', 'POST'])
def index():
    plots = None
    if request.method == 'POST':
        try:
            data = np.array([float(x.strip()) for x in request.form.get('data_points').split(',')])
            iterations = int(request.form.get('iterations', 2000))
            method = request.form.get('method')
            dist_type = request.form.get('dist_type', 'normal')
            
            p1, p2, p3, low, high = create_plots(data, iterations, method, dist_type)
            plots = {'p1': p1, 'p2': p2, 'p3': p3, 'low': round(low, 2), 'high': round(high, 2), 'mu': round(np.mean(data), 2)}
        except Exception as e:
            print(f"Error: {e}")
            
    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)