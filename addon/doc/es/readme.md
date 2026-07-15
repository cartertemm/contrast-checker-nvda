# Comprobador de contraste de color para NVDA

Los evaluadores de accesibilidad digital necesitan habitualmente asegurarse de que las relaciones de contraste de color se encuentren dentro de los umbrales definidos por las Pautas de Accesibilidad para el Contenido Web (WCAG). Sin embargo, históricamente ha sido difícil para los evaluadores ciegos hacer esto sin depender de compañeros videntes o de soluciones automatizadas. La mayoría de las soluciones automatizadas del mercado, incluidas WAVE y axe DevTools, solo filtran los problemas de contraste como "sugerencias", se dejan cosas y no examinan el indicador de foco.

Este complemento te permite comprobar el contraste del elemento enfocado con NVDA+F, el elemento bajo el cursor de revisión con NVDA+Shift+F, el indicador de foco con NVDA+Shift+C, y ejecutar una auditoría de toda la página de todos los fallos de contraste de texto con NVDA+Shift+Ctrl+F.

| Tarea | Comando | Alcance |
| --- | --- | --- |
| Comprobar el contraste del texto enfocado | **NVDA+F** | Información de formato del elemento enfocado, incluida la relación de contraste |
| Comprobar el contraste del texto en el cursor de revisión | **NVDA+Shift+F** | Información de formato en la posición del cursor de revisión, incluida la relación de contraste |
| Comprobar el contraste del indicador de foco | **NVDA+Shift+C** | Anillo de foco frente al fondo circundante |
| Ejecutar una auditoría de texto de toda la página | **NVDA+Shift+Ctrl+F** | Texto visible en la página actual, agrupado por umbral de contraste WCAG |

## Contraste del texto

Este complemento amplía los comandos de información de formato existentes de NVDA. Pulsa **NVDA+F** sobre cualquier texto para escuchar la información de formato, incluida la relación de contraste. Ejemplo:

- Source Sans 3 ExtraLight
- 10.5pt
- negro sobre blanco
- alineación a la izquierda
- `#000000 sobre #FFFFFF, contraste 21.0:1`

Pulsa dos veces rápidamente para abrir un diálogo navegable. **NVDA+Shift+F** usa la posición del cursor de revisión en lugar del cursor del sistema.

WCAG AA exige 4.5:1 para el texto normal y 3:1 para el texto grande. WCAG AAA exige 7:1.

## Contraste del indicador de foco

Pulsa **NVDA+Shift+C** sobre cualquier elemento enfocado para escuchar el contraste entre su anillo de foco y el fondo circundante:

> `Indicador de foco: #000000 sobre #FFFFFF, contraste 21.0:1`

WCAG evalúa los indicadores de foco a través de requisitos relacionados. El contraste de elementos no textuales exige que el indicador visual de foco tenga al menos 3:1 de contraste frente a los colores adyacentes, y la apariencia del foco de WCAG 2.2 añade requisitos sobre el contraste del cambio y el tamaño del indicador. Este complemento informa de la medición del contraste; los evaluadores deberían evaluar igualmente el requisito completo de apariencia del foco.

## Auditoría de contraste de toda la página

Pulsa **NVDA+Shift+Ctrl+F** para analizar de una vez cada fragmento de texto de la página actual. Los resultados se abren en un diálogo navegable, agrupados por gravedad:

- Por debajo de 3:1 (texto grande)
- Por debajo de 4.5:1 (texto normal o pequeño)
- Por debajo de 7:1 (contraste de texto AAA)

El texto que alcanza 7:1 o más pasa todos los umbrales de WCAG y se omite. Si nada falla, NVDA lo anuncia en lugar de abrir el diálogo.

Ten en cuenta que este comando solo comprueba el texto visible en el estado actual de la página. Aún necesitas mostrar y probar otros estados como el foco, el paso del puntero, el contenido expandido o contraído, el contenido cargado de forma diferida y el texto personalizado o basado en imágenes. El contraste del anillo de foco se comprueba por separado con **NVDA+Shift+C**.

## Cómo funciona

Este complemento se ejecuta completamente en tu equipo. No usa inteligencia artificial y no realiza ninguna petición de red.

Para el contraste del texto, lee los colores de primer plano y de fondo que NVDA expone para el texto actual. Convierte cada color sRGB a luminancia relativa y después aplica la [fórmula de contraste de WCAG](https://www.w3.org/WAI/GL/wiki/Contrast_ratio).

Para los indicadores de foco, captura una pequeña área de la pantalla alrededor del elemento enfocado mediante las API de captura de pantalla de Windows. Se muestrean los píxeles alrededor del elemento para identificar el fondo circundante y la transición de color de mayor contraste cerca de sus bordes. Después, la relación de contraste entre esos colores se calcula con la misma fórmula.

## Instalación

1. Instálalo desde la tienda de complementos de NVDA (menú NVDA -> Herramientas -> Tienda de complementos -> pestaña Complementos disponibles -> Comprobador de contraste de color para NVDA -> Acciones -> Instalar). Como alternativa, descarga la última versión desde [este enlace](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/).
2. Si no lo obtienes desde la tienda de complementos, abre el archivo .nvda-addon con NVDA en ejecución. NVDA te pedirá que lo instales.

## Pruébalo

Abre `tests/test_contrast.html` localmente, o [la página de pruebas renderizada](https://ctemm.me/files/test_contrast.html) en un navegador con NVDA en ejecución.
Cubre varios escenarios habituales como el contraste de texto, anillos de foco en proporciones conocidas, anillos ausentes, anillos con box-shadow, fondos no blancos y distintos tipos de elementos.

## Compilación desde el código fuente

Requiere Git, Python y SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

El archivo `.nvda-addon` compilado aparece en la raíz del proyecto.

## Licencia

GPL 2.0
