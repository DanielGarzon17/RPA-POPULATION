import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#Configuraciones del navegador por Default
options = Options() 
options.headless = True
print("Procesando...")

def selenium(browser, final_path):
    '''
    [Seguridad]

    1. Categoria
        
    2. Impacto operativo
        
    3. Scope
        Bases de datos. 
    4. Complejidad del desarrollo
        Complejidad Baja

    [Descripcion]
    
    Genera un CSV con los datos poblacionales desde el año 1950 hasta el 2100 segun previsiones de 
    la pagina de estadisticas mundiales

    [Creación]

        1. Autor:  Daniel Garzon
        2. Dia de Creación: 18/8/2023
        3. Incident: Desarrollador Junior

    [Modificación]

        1. Autor:  - 
        2. Dia de modificación: 
        3. Incident: 
        4. Descripcion:  

    [Proceso]

        1. Intancia el navegador Mozilla y lo inicializa
        2. Selecciona la pagina de "Population"
        3. Busca los elementos de la pagina que permiten desplegar las distintas opciones para configurar las tablas mediante Xpath
        4. Descarga el CSV con los datos generados
        5. Genera un solo CSV con el formato solicitado
            
    [Funciones]
        -select_countries: recibe el array de ciudades que desea seleccionar para el grafico y los selecciona
        -select_population: ejecuta las instrucciones para llegar a los menus de configuracion de las tablas
        -download csv: ejecuta las instrucciones para descargar el csv de cada tabla

    '''
    #------------------------------------
    # FUNCIONES
    #------------------------------------
    def select_countries(countries,modo):
        """Selecciona las ciudades, recibe argumentos\n
            -countries[]: vector con nombres de ciudades\n
            -modo: 1 para seleccionar boton "No change", 0 para evitarlo
        """
        # itera el vector de ciudades
        for i in range(len(countries)):
            # Por cada ciudad espera que se pueda seleccionar
            country_checkbox = wait_20.until(EC.element_to_be_clickable((By.XPATH,f'//option[contains(text(), "{countries[i]}")]')),"no sale en lista")
            country_checkbox.click()
            
            # Revisa y espera que la ciudad haya sido añadida para poder continuar
            wait_20.until(EC.presence_of_element_located((By.XPATH, f'//ul[@id="listcountry"]/li[contains(text(),"{countries[i]}")]')))
            
            # Si necesita presionar el boton de no_change 
            if modo==1 and i==0:
                try:
                    no_change_selection = browser.find_elements(By.XPATH, Xpaths_dict["no_change_selection"] )[2]
                    no_change_selection.click()
                except:
                    print("no se encontro el selector 'No change'")
    
    def select_population(num_option):
        """Seleciona una opcion de poblacion\n
        num_option: de 0-3 corresponde a la opcion del menu "total_population" que desea seleccionar"""
        # selecciona el boton de population inicial y lo presiona
        population_button = wait_20.until(EC.element_to_be_clickable((By.XPATH,'//a[@id="aTopic11"]')),
                                        "El boton de population no se encontro")
        population_button.click()
        # selecciona el boton de total_population y lo presiona
        total_population_button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH,Xpaths_dict["total_population_button"])),
                                                "No se habilito el boton de total population")
        total_population_button.click()
        # selecciona la opcion indicada del listado que se despliegue luego de oprimir el anterior boton
        total_population_options = browser.find_elements(By.XPATH, Xpaths_dict["total_population_options"])
        total_population_options[num_option].click()
    
    def download_csv():
        # Ubica el menu desplegable de todas las lineas y escoge "all" 
        select_all = browser.find_element(By.XPATH, Xpaths_dict["select_all_lines"])
        select_all.click()
        # Ubica el boton de descarga de CSV 
        export_csv= browser.find_element(By.XPATH, Xpaths_dict["csv_button"])
        export_csv.click()
    #----------------------------------------------------------------------------------------------------------------------------
    # VARIABLES DE CONFIGURACION
    #----------------------------------------------------------------------------------------------------------------------------
    URL = "https://world-statistics.org/"
    COUNTRIES = ["Bolivia (Plurinational State of)",
                 "Brazil",
                 "Chile",
                 "Colombia",
                 "Ecuador",
                 "Guyana",
                 "Paraguay",
                 "Peru", 
                 "Suriname",
                 "Trinidad and Tobago",
                 "Uruguay",
                 "Venezuela (Bolivarian Republic of)",
                 "Argentina"]
    NOW = datetime.now().strftime('%d-%m-%Y')
    Xpaths_dict= {
        'indicators_button': '//ul/li/a[contains(@href, "indicators")]',
        'total_population_button': '//div[@id="subtopic117"]/a',
        'total_population_options': '//div[@id="list117"]/a',
        'select_all_lines': '//select/option[@value="-1"]',
        'csv_button': '//a[@title="CSV"]',
        'browse_indicators': '//a[contains(text(),"browse")]',
        'no_change_selection': '//select[@id="selColDim1"]/option[@value="No change"]'
    }
    wait_20= WebDriverWait(browser, 20)
    #----------------------------------------------------------------------------------------------------------------------------
    

    # Abrir la página
    browser.get(URL) 

    # Encuentra en el Navbar el boton "indicators" y presiona
    indicators_button = wait_20.until(EC.element_to_be_clickable((By.XPATH, Xpaths_dict["indicators_button"])),
                                        "No se encontro el boton de indicadores")
    indicators_button.click()

    # Selecciona la opcion "population, Total(UN estimates 1950-2020)"
    select_population(1)
    # Selecciona las ciudades para 1950-2020 (modo 0) y descarga el csv
    select_countries(COUNTRIES,0)
    download_csv()
    
    #vuelve a la pagina anterior
    browser.find_element(By.XPATH, Xpaths_dict["browse_indicators"]).click()

    # Selecciona la opcion "population, Total(UN estimates 2020-2100)"
    select_population(2)

    # Descargar un CSV por cada 3 ciudades para reducir tiempos
    for i in range(0, len(COUNTRIES), 3):
        sub_countries = COUNTRIES[i:i + 3]
        select_countries(sub_countries,1)
        download_csv()
        browser.refresh()
    # Cierra el navegador
    browser.quit()
    
    # Filtra los archivos descargados por tipo (por extensión .csv)
    archivos_csv = [archivo for archivo in os.listdir(final_path) if archivo.endswith(".csv")]

    # Renombra los archivos CSV descargados para poder trabajar mas facilmente con ellos 
    for i in range(len(archivos_csv)):    
        nuevo_nombre = f"{i}.csv"
        ruta_antigua = os.path.join(final_path, archivos_csv[i])
        ruta_nueva = os.path.join(final_path, nuevo_nombre)
        os.rename(ruta_antigua, ruta_nueva)
        
    
    # Filtrar los archivos para quedarnos con los archivos CSV renombrados
    archivos_csv = [archivo for archivo in os.listdir(final_path) if archivo.endswith(".csv")]
    # Leer los archivos CSV y genera los dataframes
    dataframes = [pd.read_csv(final_path+"\\"+file) for file in archivos_csv]

    # Para cada dataframe de los años 2020-2100 elimina las 2da columna y "2020" que se repite en 1950-2020
    for i in range(5):
        name_of_column = dataframes[i].columns[1:3]
        dataframes[i] = dataframes[i].drop(columns=name_of_column, axis=1)

    # Se genera un dataframe para 1950-2020 y otro para para 2020-2100
    df_past= dataframes[5]
    df_future =pd.concat(dataframes[:5], ignore_index=True)

    # Une los dataframes para que vaya de 1950-2100 y los formatea con melt
    df_final = pd.melt(df_past.merge(df_future, on='Country'),
                        id_vars=['Country'], var_name='Year', 
                        value_name='Population')
    
    # Renombra columna, ordena por Pais y año y filtra de valores esperados
    df_final.columns = ['Country', 'Year', 'Population']
    df_final = df_final.sort_values(by=['Country','Year'])
    df_final = df_final[df_final['Population'] != 'No change']

    # Eliminar las comas y convertir la columna 'Population' a valores numéricos
    df_final['Population'] = df_final['Population'].str.replace(',', '').astype(int)

    # Genera un CSV Final
    df_final.to_csv(final_path+"\\Population_1950_2100.csv", index=False)
    
    #Elimina los CSV descargados
    for i in range(6):    
        nombre = f"\\{i}.csv"
        os.remove(final_path+nombre)


if __name__ == "__main__":

    # Se determina la ruta donde se van a guardar los archivos al finalizar el proceso
    final_path = os.path.dirname(os.path.abspath(__file__))
    # Se configura la carpeta de descargas local como la carpeta donde se encuentra el RPA 
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", final_path)

    # Configura el navegador a utilizar e inicia el proceso
    browser = webdriver.Firefox(options=options)
    
    selenium(browser,final_path)