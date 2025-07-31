from app import create_app, db

def test_app_creation():
    app = create_app()
    with app.app_context():
        assert app is not None
        try:
            conn = db.engine.connect()
            conn.close()
            print("✅ Conexión a la base de datos exitosa.")
        except Exception as e:
            print("❌ Error de conexión a la base de datos:", e)

if __name__ == "__main__":
    test_app_creation()