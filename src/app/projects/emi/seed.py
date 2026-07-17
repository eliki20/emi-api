import asyncio

from app.projects.emi.infra.db.mongo import get_database

PRODUCTOS_RAW = [
    {"nombre": "Cuaderno A4 Cuadriculado", "categoria": "Cuadernos", "marca": "Standford", "precio": 5.30, "stock": 45, "descripcion": "Cuaderno A4 cuadriculado de 100 hojas.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302838/cuaderno_stanford_dovioy.png"},
    {"nombre": "Cuaderno A4 Cuadriculado", "categoria": "Cuadernos", "marca": "Alpha", "precio": 4.20, "stock": 50, "descripcion": "Cuaderno A4 cuadriculado de 100 hojas.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302837/cuaderno_alpha_wz3cxj.jpg"},
    {"nombre": "Cuaderno A4 Cuadriculado", "categoria": "Cuadernos", "marca": "Justus", "precio": 3.90, "stock": 35, "descripcion": "Cuaderno A4 cuadriculado de 100 hojas.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302838/cuaderno_justus_gyoksy.jpg"},
    {"nombre": "Cuaderno Universitario Rayado", "categoria": "Cuadernos", "marca": "Norma", "precio": 21.90, "stock": 40, "descripcion": "Cuaderno universitario rayado de 100 hojas.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302838/cuaderno_universitario_norma_qlx8nn.jpg"},
    {"nombre": "Lápiz HB", "categoria": "Lápices", "marca": "Faber-Castell", "precio": 2.50, "stock": 180, "descripcion": "Lápiz HB para escritura.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302843/lapiz-HB_faberCastell_yov1i3.jpg"},
    {"nombre": "Cuaderno Universitario Rayado", "categoria": "Cuadernos", "marca": "Standford", "precio": 20.90, "stock": 40, "descripcion": "Cuaderno universitario rayado de 100 hojas.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302839/cuaderno_universitario_stanford_m9alkw.jpg"},
    {"nombre": "Cuaderno Universitario Rayado", "categoria": "Cuadernos", "marca": "Oxford", "precio": 22.90, "stock": 35, "descripcion": "Cuaderno universitario rayado de 100 hojas.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302839/cuaderno_universitario_oxford_ordygs.webp"},
    {"nombre": "Lápiz HB", "categoria": "Lápices", "marca": "Maped", "precio": 2.20, "stock": 150, "descripcion": "Lápiz grafito HB para escritura.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302843/lapiz_HB_maped_b9vq8a.jpg"},
    {"nombre": "Lápiz 2B", "categoria": "Lápices", "marca": "Faber-Castell", "precio": 3.50, "stock": 100, "descripcion": "Lápiz de dibujo 2B.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302841/lapiz_2B_faberCastell_vlve7w.jpg"},
    {"nombre": "Lápiz 2B", "categoria": "Lápices", "marca": "Staedtler", "precio": 4.20, "stock": 90, "descripcion": "Lápiz de dibujo 2B.", "imagen_url":""},
    {"nombre": "Lápiz 2B", "categoria": "Lápices", "marca": "Maped", "precio": 3.80, "stock": 80, "descripcion": "Lápiz de dibujo 2B.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302841/lapiz_2b_staedtler_wf9hpg.jpg"},
    {"nombre": "Lápiz 6B", "categoria": "Lápices", "marca": "Faber-Castell", "precio": 5.50, "stock": 70, "descripcion": "Lápiz de dibujo 6B.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302842/lapiz_6b_faberCastell_vtgabw.jpg"},
    {"nombre": "Lápiz 6B", "categoria": "Lápices", "marca": "Staedtler", "precio": 6.50, "stock": 65, "descripcion": "Lápiz de dibujo 6B.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302842/lapiz_6B_staedtler_f9xgwc.jpg"},
    {"nombre": "Lápiz 6B", "categoria": "Lápices", "marca": "Derwent", "precio": 7.20, "stock": 50, "descripcion": "Lápiz profesional para dibujo 6B.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302842/lapiz_6b_derwent_kpmpdb.jpg"},
    {"nombre": "Caja de Colores x12", "categoria": "Colores", "marca": "Faber-Castell", "precio": 14.90, "stock": 60, "descripcion": "Caja de 12 colores largos.", "imagen_url":""},
    {"nombre": "Caja de Colores x12", "categoria": "Colores", "marca": "Artesco", "precio": 12.90, "stock": 70, "descripcion": "Caja de 12 colores largos.", "imagen_url":""},
    {"nombre": "Caja de Colores x12", "categoria": "Colores", "marca": "Maped", "precio": 15.90, "stock": 55, "descripcion": "Caja de 12 colores largos.", "imagen_url":""},
    {"nombre": "Caja de Colores x24", "categoria": "Colores", "marca": "Faber-Castell", "precio": 28.90, "stock": 50, "descripcion": "Caja de 24 colores largos.", "imagen_url":""},
    {"nombre": "Caja de Colores x24", "categoria": "Colores", "marca": "Artesco", "precio": 24.90, "stock": 45, "descripcion": "Caja de 24 colores largos.", "imagen_url":""},
    {"nombre": "Caja de Colores x24", "categoria": "Colores", "marca": "Maped", "precio": 29.90, "stock": 40, "descripcion": "Caja de 24 colores largos.", "imagen_url":""},
    {"nombre": "Plumones x12", "categoria": "Plumones", "marca": "Faber-Castell", "precio": 18.90, "stock": 45, "descripcion": "Caja de 12 plumones escolares.", "imagen_url":""},
    {"nombre": "Plumones x12", "categoria": "Plumones", "marca": "Artesco", "precio": 16.90, "stock": 50, "descripcion": "Caja de 12 plumones escolares.", "imagen_url":""},
    {"nombre": "Plumones x12", "categoria": "Plumones", "marca": "Maped", "precio": 19.90, "stock": 35, "descripcion": "Caja de 12 plumones escolares.", "imagen_url":""},
    {"nombre": "Crayones x12", "categoria": "Crayones", "marca": "Faber-Castell", "precio": 11.90, "stock": 60, "descripcion": "Caja de 12 crayones de colores.", "imagen_url":""},
    {"nombre": "Crayones x12", "categoria": "Crayones", "marca": "Artesco", "precio": 10.90, "stock": 55, "descripcion": "Caja de 12 crayones de colores.", "imagen_url":""},
    {"nombre": "Crayones x12", "categoria": "Crayones", "marca": "Layconsa", "precio": 9.90, "stock": 50, "descripcion": "Caja de 12 crayones escolares.", "imagen_url":""},
    {"nombre": "Tempera 250 ml", "categoria": "Pintura", "marca": "Artesco", "precio": 8.90, "stock": 40, "descripcion": "Témpera líquida de 250 ml.", "imagen_url":""},
    {"nombre": "Tempera 250 ml", "categoria": "Pintura", "marca": "Faber-Castell", "precio": 9.90, "stock": 35, "descripcion": "Témpera líquida de 250 ml.", "imagen_url":""},
    {"nombre": "Tempera 250 ml", "categoria": "Pintura", "marca": "Pelikan", "precio": 10.50, "stock": 30, "descripcion": "Témpera líquida de 250 ml.", "imagen_url":""},
    {"nombre": "Acuarelas x12", "categoria": "Pintura", "marca": "Faber-Castell", "precio": 22.90, "stock": 30, "descripcion": "Caja de acuarelas con 12 colores.", "imagen_url":""},
    {"nombre": "Acuarelas x12", "categoria": "Pintura", "marca": "Pelikan", "precio": 20.90, "stock": 25, "descripcion": "Caja de acuarelas con 12 colores.", "imagen_url":""},
    {"nombre": "Acuarelas x12", "categoria": "Pintura", "marca": "Giotto", "precio": 24.90, "stock": 20, "descripcion": "Caja de acuarelas con 12 colores.", "imagen_url":""},
    {"nombre": "Bloc de Dibujo A4", "categoria": "Papelería", "marca": "Canson", "precio": 18.90, "stock": 30, "descripcion": "Bloc de dibujo A4 de 20 hojas.", "imagen_url":""},
    {"nombre": "Bloc de Dibujo A4", "categoria": "Papelería", "marca": "Standford", "precio": 16.90, "stock": 35, "descripcion": "Bloc de dibujo A4 de 20 hojas.", "imagen_url":""},
    {"nombre": "Bloc de Dibujo A4", "categoria": "Papelería", "marca": "Alpha", "precio": 15.90, "stock": 40, "descripcion": "Bloc de dibujo A4 de 20 hojas.", "imagen_url":""},
    {"nombre": "Cartulina Blanca", "categoria": "Papelería", "marca": "Standford", "precio": 1.50, "stock": 300, "descripcion": "Cartulina blanca tamaño pliego.", "imagen_url":""},
    {"nombre": "Cartulina Blanca", "categoria": "Papelería", "marca": "Alpha", "precio": 1.40, "stock": 250, "descripcion": "Cartulina blanca tamaño pliego.", "imagen_url":""},
    {"nombre": "Cartulina Blanca", "categoria": "Papelería", "marca": "Justus", "precio": 1.60, "stock": 220, "descripcion": "Cartulina blanca tamaño pliego.", "imagen_url":""},
    {"nombre": "Cartulina de Colores", "categoria": "Papelería", "marca": "Standford", "precio": 1.80, "stock": 280, "descripcion": "Cartulina de colores tamaño pliego.", "imagen_url":""},
    {"nombre": "Cartulina de Colores", "categoria": "Papelería", "marca": "Alpha", "precio": 1.70, "stock": 250, "descripcion": "Cartulina de colores tamaño pliego.", "imagen_url":""},
    {"nombre": "Cartulina de Colores", "categoria": "Papelería", "marca": "Justus", "precio": 1.90, "stock": 230, "descripcion": "Cartulina de colores tamaño pliego.", "imagen_url":""},
    {"nombre": "Papel Bond A4 x500 hojas", "categoria": "Papelería", "marca": "Chamex", "precio": 29.90, "stock": 70, "descripcion": "Resma de papel bond A4 de 75 g.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302840/hojas_bond_chamez_sl4lhq.png"},
    {"nombre": "Papel Bond A4 x500 hojas", "categoria": "Papelería", "marca": "Autor", "precio": 27.90, "stock": 60, "descripcion": "Resma de papel bond A4 de 75 g.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302840/hojas_bond_autor_atnaqf.jpg"},
    {"nombre": "Papel Bond A4 x500 hojas", "categoria": "Papelería", "marca": "Xerox", "precio": 31.90, "stock": 55, "descripcion": "Resma de papel bond A4 de 75 g.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302841/hojas_bond_xerox_jf8x78.jpg"},
    {"nombre": "Goma de Borrar Blanca", "categoria": "Borradores", "marca": "Faber-Castell", "precio": 2.50, "stock": 150, "descripcion": "Goma de borrar blanca libre de PVC.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302837/borrador_faberCatell_ywxbxn.png"},
    {"nombre": "Goma de Borrar Blanca", "categoria": "Borradores", "marca": "Artesco", "precio": 1.80, "stock": 180, "descripcion": "Goma de borrar escolar.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302837/borrador_artesco_kpx8pa.jpg"},
    {"nombre": "Goma de Borrar Blanca", "categoria": "Borradores", "marca": "Maped", "precio": 2.90, "stock": 140, "descripcion": "Goma de borrar de alta precisión.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302836/borrador_maped_hfwypd.jpg"},
    {"nombre": "Tajador Metálico", "categoria": "Tajadores", "marca": "Faber-Castell", "precio": 3.90, "stock": 120, "descripcion": "Tajador metálico de un orificio.", "imagen_url":""},
    {"nombre": "Tajador Metálico", "categoria": "Tajadores", "marca": "Artesco", "precio": 2.90, "stock": 140, "descripcion": "Tajador metálico escolar.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302845/tajador_artesco_lmff3d.jpg"},
    {"nombre": "Tajador Metálico", "categoria": "Tajadores", "marca": "Maped", "precio": 4.20, "stock": 100, "descripcion": "Tajador metálico de larga duración.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302845/trabajador_Maped_lirddj.jpg"},
    {"nombre": "Regla 30 cm", "categoria": "Geometría", "marca": "Artesco", "precio": 3.50, "stock": 120, "descripcion": "Regla transparente de 30 cm.", "imagen_url":""},
    {"nombre": "Regla 30 cm", "categoria": "Geometría", "marca": "Maped", "precio": 4.90, "stock": 100, "descripcion": "Regla transparente de 30 cm.", "imagen_url":""},
    {"nombre": "Regla 30 cm", "categoria": "Geometría", "marca": "Faber-Castell", "precio": 4.50, "stock": 90, "descripcion": "Regla de plástico resistente de 30 cm.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302844/regla_faberCastell_sykebw.png"},
    {"nombre": "Escuadra 45°", "categoria": "Geometría", "marca": "Artesco", "precio": 4.90, "stock": 90, "descripcion": "Escuadra de 45 grados para uso escolar.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302839/escuadra_artesco_mgytf5.png"},
    {"nombre": "Escuadra 45°", "categoria": "Geometría", "marca": "Maped", "precio": 5.90, "stock": 80, "descripcion": "Escuadra transparente de 45 grados.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302840/escuadra_maped_bs5vkc.jpg"},
    {"nombre": "Escuadra 45°", "categoria": "Geometría", "marca": "Faber-Castell", "precio": 5.50, "stock": 70, "descripcion": "Escuadra de alta precisión.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302839/escuadra_faberCastell_v8cuyn.jpg"},
    {"nombre": "Compás Escolar", "categoria": "Geometría", "marca": "Faber-Castell", "precio": 18.90, "stock": 45, "descripcion": "Compás metálico escolar.", "imagen_url":""},
    {"nombre": "Compás Escolar", "categoria": "Geometría", "marca": "Maped", "precio": 17.90, "stock": 40, "descripcion": "Compás metálico con adaptador.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302837/compas_maped_ovrspc.jpg"},
    {"nombre": "Compás Escolar", "categoria": "Geometría", "marca": "Staedtler", "precio": 21.90, "stock": 35, "descripcion": "Compás de precisión.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302837/Comp%C3%A1s_staedtler_ishg3p.jpg"},
    {"nombre": "Transportador 180°", "categoria": "Geometría", "marca": "Artesco", "precio": 2.50, "stock": 150, "descripcion": "Transportador transparente de 180 grados.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302845/transportador_artesco_kn4syp.jpg"},
    {"nombre": "Transportador 180°", "categoria": "Geometría", "marca": "Maped", "precio": 3.50, "stock": 120, "descripcion": "Transportador escolar de 180 grados.", "imagen_url":"https://res.cloudinary.com/njkjl8ht/image/upload/v1784302846/transportador_maped_qj7pvm.jpg"},
    {"nombre": "Transportador 180°", "categoria": "Geometría", "marca": "Faber-Castell", "precio": 3.90, "stock": 100, "descripcion": "Transportador de alta precisión.", "imagen_url": "https://res.cloudinary.com/njkjl8ht/image/upload/v1784302846/transportador_faberCastell_yhnmlw.jpg"},
]

PRODUCTOS = PRODUCTOS_RAW

async def main():
    db = get_database()
    collection = db["productos"]
    await collection.delete_many({})
    result = await collection.insert_many(PRODUCTOS)
    print(f"✅ {len(result.inserted_ids)} productos insertados")


asyncio.run(main())