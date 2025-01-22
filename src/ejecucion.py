import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.mercadolibre.com.co/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}


# r = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky')
r = requests.get('https://listado.mercadolibre.com.co/_Container_fs-moda-hombre-v4#deal_print_id=98232580-d89d-11ef-b6ad-099c3d0153ab&c_id=carousel&c_element_order=3&c_campaign=CARHOMBRE&c_uid=98232580-d89d-11ef-b6ad-099c3d0153ab')
soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_= 'ui-search-result__wrapper')

# print(len(productlist))

productlinks = []


for item in productlist:
    # Verifica si se encuentra el enlace 'a' con atributo 'href'
    link = item.find('a', href=True)
    if link and link['href']:
        productlinks.append(link['href'])


Menproductslist = []

for link in productlinks:
    try:
        # Realiza la solicitud GET
        r = requests.get(link, headers=headers)
        
        # Verifica si la solicitud fue exitosa
        r.raise_for_status()  # 200
        
        soup = BeautifulSoup(r.content, 'lxml')

        name = (soup.find('h1', class_='ui-pdp-title').text.strip())

        prices = soup.find_all('span', class_='andes-money-amount__fraction')

        # Verifica si hay al menos dos elementos
        if len(prices) > 1:
            # Accede al segundo elemento
            price = '$' + prices[1].text.strip()
        else: 
            if len(prices) > 0:
                price = '$' + prices[0].text.strip() 
            else:
                price = "Precio no disponible"      

        product = {
            'name': name,
            'precio': price,
        }

        Menproductslist.append(product)
        print('Guardando...', product['name'])

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página {link}: {e}")
    except Exception as e:
        print(f"Se produjo un error al procesar {link}: {e}")


df = pd.DataFrame(Menproductslist)

print(df.head(20))


# Guardar como archivo HTML
html_content = df.to_html(index=False)

# HTML con el contenido y estilo CSS
html_output = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Productos de Hombre en MercadoLibre más populares hoy</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #ddd;
        }}
    </style>
</head>
<body>
    <h1>Productos de Hombre en MercadoLibre más populares hoy</h1>
    {html_content}
</body>
</html>
"""

# Guardar el contenido en un archivo HTML
with open("productos_mercadolibre.html", "w", encoding="utf-8") as file:
    file.write(html_output)

print("El archivo HTML ha sido generado correctamente.")

print("El script se ejecutó correctamente.")




