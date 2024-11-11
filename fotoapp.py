# fotoapp.py
from PIL import Image, ImageFilter
import requests
from io import BytesIO
import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
# 1 anda
def redimensionarImagen(path, platforma):

    dimensions = {
        "Youtube": (1280, 720),
        "Instagram": (1080, 1080),
        "Twitter": (1200, 675),
        "Facebook": (1200, 630)
    }
    
    if platforma not in dimensions:
        raise ValueError("Plataforma no encontrada")
    
    if path.startswith("http"):
        response = requests.get(path) #bajo la imagen
        img = Image.open(BytesIO(response.content))
    else:
        raise ValueError("La ruta no es una direccion URL")
    img = img.resize(dimensions[platforma])
    #plt.imshow(img) lo comento por que cada vez que llamo a la funcion para probrar las otras me imprime la imagen
    return img   #devuelvo la imagen para utilizarla con las otras funciones

# 2 anda
def ajustarContraste(img):
    imgNP = np.array(img)
    # RGB A YUV
    imgYUV = cv2.cvtColor(imgNP, cv2.COLOR_RGB2YUV)
    # Histoframa
    imgYUV[:, :, 0] = cv2.equalizeHist(imgYUV[:, :, 0])
    #YUV a RGB
    imgEcu = cv2.cvtColor(imgYUV, cv2.COLOR_YUV2RGB)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(imgNP)
    plt.axis('off')

    plt.subplot(1, 2, 2)

    plt.title("Ecualizada")
    plt.imshow(imgEcu)
    plt.axis('off')
    fecha = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f") #Lo guardo por fecha asi no se reescribe, me parecia mas facil que un contador
    plt.savefig(f"imgs/2/contraste ajustado {fecha}.png")
    
    plt.show()
    
    return imgEcu

# 3 anda
def aplicarFiltro(img, filtro):
    filtros = {
        "BLUR": ImageFilter.BLUR,
        "CONTOUR": ImageFilter.CONTOUR,
        "DETAIL": ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
        "EMBOSS": ImageFilter.EMBOSS,
        "FIND_EDGES": ImageFilter.FIND_EDGES,
        "SHARPEN": ImageFilter.SHARPEN,
        "SMOOTH": ImageFilter.SMOOTH
    }
    if filtro not in filtros:
        raise ValueError("Filtro no soportado")
    imgFil = img.filter(filtros[filtro])
    plt.imshow(imgFil)
    plt.title(filtro)
    plt.axis('off')
    fecha = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f") 
    plt.savefig(f"imgs/3/filtro seleccionado {fecha}.png")
    plt.show()


    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes[0,0].imshow(img)
    axes[0,0].set_title('ORIGINAL')
    axes[0,0].axis('off')
    fil, col = 0, 1
    for nombre,comando in filtros.items():
        if nombre != filtro:
            imgFiltros = img.filter(comando)
            axes[fil, col].imshow(imgFiltros) 
            axes[fil, col].set_title(nombre) 
            axes[fil, col].axis('off')
            col += 1 
            if col == 3: 
                col = 0 
                fil += 1
    fecha = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f") 
    plt.savefig(f"imgs/3/otros filtros {fecha}.png")

    return imgFil


# 4 anda
def crearBoceto(img, persona=True):
    if not persona:
        raise ValueError("La imagen no contiene una persona")
    img = np.array(img)

    # Deteccion de bordes
    borde = cv2.Canny(img, 70, 140) #los mejores valores que encontre para esa imagen, se perdia parte del brazo
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img, cmap="gray")
    
    plt.subplot(1, 2, 2)
    plt.title("Boceto")
    plt.imshow(borde, cmap="gray")
    fecha = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f") 
    plt.savefig(f"imgs/4/boceto {fecha}.png")
    plt.show()
    
    return borde  #utilizo el ejemplo de que esta en el tp ya que es la mejor manera de hacer un boceto, tienendo solo los bordes.

def menu():
    print(f"BIENVENIDO A FOTO APP\n")

    while True:
        
        print("Opciones:")
        print("1. Redimensionar imagen")
        print("2. Ajustar contraste")
        print("3. Aplicar filtro")
        print("4. Crear boceto")
        print(f"5. Salir\n")
        
        
        opcion = input(f"Seleccione una opcion: ")
        print()
        imagenAjustada = False
        if opcion == "1":
            path = input("Ingrese la ruta de la imagen: ")
            platforma = input("Ingrese la plataforma (Youtube, Instagram, Twitter, Facebook): ")
            img = redimensionarImagen(path, platforma)
            img.show()
            imagenAjustada = True  #no se me ocurrio otra forma de hacerlo, para que la imagen pase por la op 1 antes
        elif opcion == "2":
            if imagenAjustada:
                ajustarContraste(img)
            else:
                print("Primero ajustemos la imagen, opcion 1")
                pass
        elif opcion == "3":
            if imagenAjustada:
                filtro = input("Ingrese el nombre del filtro: ")
                img = aplicarFiltro(img, filtro)
            else:
                print("Primero ajustemos la imagen, opcion 1")
                pass
        elif opcion == "4":
            if imagenAjustada:        
                path = input("Ingrese la ruta de la imagen: ")
                crearBoceto(img)
            else:
                print("Primero ajustemos la imagen, opcion 1")
                pass
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion no valida")

if __name__ == "__main__": #para que no se ejecute el menu con los test
    menu()