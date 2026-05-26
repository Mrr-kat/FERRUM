from flask import Flask, render_template, session, redirect, url_for
from datetime import timedelta
import os
import functools
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ferreteria-2024-secret-key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# Inicializar DB al arrancar (gunicorn ejecuta esto una vez por worker)
try:
    from database import init_db
    init_db()
    app.config['DB_INITIALIZED'] = True
    print("[INFO] Base de datos inicializada correctamente.", file=sys.stderr)
except Exception as e:
    app.config['DB_INITIALIZED'] = False
    print(f"[WARN] No se pudo inicializar la DB al arrancar: {e}", file=sys.stderr)
    print("[WARN] Se reintentará en el primer request.", file=sys.stderr)

from routes.inventory import bp as inv_bp
from routes.sales import bp as sales_bp
from routes.analytics import bp as analytics_bp
from routes.alerts import bp as alerts_bp
from routes.auth import bp as auth_bp

app.register_blueprint(inv_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(auth_bp)

@app.before_request
def ensure_db():
    """Reintento lazy si la DB no estaba disponible al arrancar."""
    if not app.config.get('DB_INITIALIZED', False):
        try:
            from database import init_db
            init_db()
            app.config['DB_INITIALIZED'] = True
            print("[INFO] DB inicializada en primer request.", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a la DB: {e}", file=sys.stderr)

def admin_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect('/?auth=required')
        return f(*args, **kwargs)
    return decorated

# Public routes
@app.route('/')
def index():
    return render_template('carrito.html')

# Admin-only routes
@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template('index.html')

@app.route('/inventario')
@admin_required
def inventario():
    return render_template('inventario.html')

@app.route('/ventas')
@admin_required
def ventas():
    return render_template('ventas.html')

@app.route('/analytics')
@admin_required
def analytics():
    return render_template('analytics.html')

@app.route('/alertas')
@admin_required
def alertas():
    return render_template('alertas.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
