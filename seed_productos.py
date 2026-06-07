# Datos de prueba de productos. Idempotente.
from app.database import SessionLocal
from app import models

db = SessionLocal()

if db.query(models.Producto).count() == 0:
    productos = [
        models.Producto(nombre="Microfono Shure SM7B", descripcion="Microfono dinamico de estudio.",
                        tipo="venta", precio_venta=399.00, stock=8,
                        imagen_url="https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80"),
        models.Producto(nombre="Altavoz JBL EON615", descripcion="Altavoz activo 1000W para eventos.",
                        tipo="alquiler", precio_alquiler_dia=45.00, stock=6,
                        imagen_url="https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&q=80"),
        models.Producto(nombre="Consola Yamaha MG16XU", descripcion="Mezcladora 16 canales.",
                        tipo="ambos", precio_venta=599.00, precio_alquiler_dia=80.00, stock=3,
                        imagen_url="https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800&q=80"),
        models.Producto(nombre="Guitarra Fender Stratocaster", descripcion="Guitarra electrica.",
                        tipo="ambos", precio_venta=850.00, precio_alquiler_dia=35.00, stock=4,
                        imagen_url="https://images.unsplash.com/photo-1550985616-10810253b84d?w=800&q=80"),
        models.Producto(nombre="Audifonos Audio-Technica M50x", descripcion="Audifonos de monitoreo.",
                        tipo="venta", precio_venta=149.00, stock=12,
                        imagen_url="https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&q=80"),
    ]
    db.add_all(productos)
    db.commit()
    print("Productos de prueba insertados.")
else:
    print("Ya existen productos, no se inserto nada.")

db.close()