# Vérificateur de contraste de couleur pour NVDA

Les testeurs d'accessibilité numérique doivent régulièrement s'assurer que les relations de contraste de couleur se situent dans les seuils définis par les Règles pour l'accessibilité des contenus Web (WCAG). Or, il a toujours été difficile pour les testeurs aveugles de le faire sans dépendre de collègues voyants ou de solutions automatisées. La plupart des solutions automatisées du marché, dont WAVE et axe DevTools, ne filtrent les problèmes de contraste que sous forme de « suggestions », passent à côté de certaines choses et n'examinent pas l'indicateur de focus.

Ce module complémentaire vous permet de vérifier le contraste de l'élément ciblé avec NVDA+F, de l'élément sous le curseur de revue avec NVDA+Shift+F, de l'indicateur de focus avec NVDA+Shift+C, et de lancer un audit de toute la page de tous les défauts de contraste de texte avec NVDA+Shift+Ctrl+F.

| Tâche | Commande | Portée |
| --- | --- | --- |
| Vérifier le contraste du texte ciblé | **NVDA+F** | Informations de formatage de l'élément ciblé, dont la relation de contraste |
| Vérifier le contraste du texte au curseur de revue | **NVDA+Shift+F** | Informations de formatage à la position du curseur de revue, dont la relation de contraste |
| Vérifier le contraste de l'indicateur de focus | **NVDA+Shift+C** | Anneau de focus par rapport à l'arrière-plan environnant |
| Lancer un audit de texte sur toute la page | **NVDA+Shift+Ctrl+F** | Texte visible sur la page actuelle, regroupé par seuil de contraste WCAG |

## Contraste du texte

Ce module complémentaire étend les commandes d'information de formatage existantes de NVDA. Appuyez sur **NVDA+F** sur n'importe quel texte pour entendre les informations de formatage, dont la relation de contraste. Exemple :

- Source Sans 3 ExtraLight
- 10.5pt
- noir sur blanc
- aligné à gauche
- `#000000 sur #FFFFFF, contraste 21.0:1`

Appuyez deux fois rapidement pour obtenir une boîte de dialogue navigable. **NVDA+Shift+F** utilise la position du curseur de revue au lieu du curseur système.

WCAG AA exige 4.5:1 pour le texte normal et 3:1 pour le texte large. WCAG AAA exige 7:1.

## Contraste de l'indicateur de focus

Appuyez sur **NVDA+Shift+C** sur n'importe quel élément ciblé pour entendre le contraste entre son anneau de focus et l'arrière-plan environnant :

> `Indicateur de focus : #000000 sur #FFFFFF, contraste 21.0:1`

WCAG évalue les indicateurs de focus à travers des exigences connexes. Le contraste des éléments non textuels exige que l'indicateur visuel de focus présente au moins 3:1 de contraste par rapport aux couleurs adjacentes, et l'apparence du focus de WCAG 2.2 ajoute des exigences sur le contraste du changement et la taille de l'indicateur. Ce module complémentaire rend compte de la mesure du contraste ; les testeurs devraient tout de même évaluer l'exigence complète d'apparence du focus.

## Audit de contraste de toute la page

Appuyez sur **NVDA+Shift+Ctrl+F** pour analyser d'un coup chaque fragment de texte de la page actuelle. Les résultats s'ouvrent dans une boîte de dialogue navigable, regroupés par gravité :

- Inférieur à 3:1 (texte large)
- Inférieur à 4.5:1 (texte normal ou petit)
- Inférieur à 7:1 (contraste de texte AAA)

Le texte qui atteint 7:1 ou mieux passe tous les seuils WCAG et est omis. Si rien n'échoue, NVDA l'annonce au lieu d'ouvrir la boîte de dialogue.

Veuillez noter que cette commande ne vérifie que le texte visible dans l'état actuel de la page. Vous devez encore révéler et tester d'autres états comme le focus, le survol, le contenu déplié ou replié, le contenu chargé de manière différée, et le texte personnalisé ou basé sur des images. Le contraste de l'anneau de focus se vérifie séparément avec **NVDA+Shift+C**.

## Fonctionnement

Ce module complémentaire s'exécute entièrement sur votre machine. Il n'utilise pas d'intelligence artificielle et n'effectue aucune requête réseau.

Pour le contraste du texte, il lit les couleurs de premier plan et d'arrière-plan que NVDA expose pour le texte actuel. Il convertit chaque couleur sRGB en luminance relative, puis applique la [formule de contraste WCAG](https://www.w3.org/WAI/GL/wiki/Contrast_ratio).

Pour les indicateurs de focus, il capture une petite zone de l'écran autour de l'élément ciblé à l'aide des API de capture d'écran de Windows. Des pixels sont échantillonnés autour de l'élément pour identifier l'arrière-plan environnant et la transition de couleur au contraste le plus élevé près de ses bords. Ensuite, la relation de contraste entre ces couleurs est calculée avec la même formule.

## Installation

1. Installez-le depuis la boutique de modules complémentaires de NVDA (menu NVDA -> Outils -> Boutique de modules complémentaires -> onglet Modules complémentaires disponibles -> Vérificateur de contraste de couleur pour NVDA -> Actions -> Installer). Vous pouvez aussi télécharger la dernière version depuis [ce lien](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/).
2. Si vous ne l'obtenez pas depuis la boutique de modules complémentaires, ouvrez le fichier .nvda-addon avec NVDA en cours d'exécution. NVDA vous proposera de l'installer.

## Essayez-le

Ouvrez `tests/test_contrast.html` en local, ou [la page de test rendue](https://ctemm.me/files/test_contrast.html) dans un navigateur avec NVDA en cours d'exécution.
Elle couvre divers scénarios courants comme le contraste de texte, les anneaux de focus à des proportions connues, les anneaux manquants, les anneaux en box-shadow, les arrière-plans non blancs et différents types d'éléments.

## Compilation depuis les sources

Nécessite Git, Python et SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

Le fichier `.nvda-addon` compilé apparaît à la racine du projet.

## Licence

GPL 2.0
