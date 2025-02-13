# **Rapport de Synthèse : Implémentation d'une API CRUD pour la Gestion des Produits et Magasins**

## **1. Introduction**

Ce document présente l'implémentation d'une API CRUD pour la gestion des produits, des magasins et des prix en utilisant Django et Django REST Framework. L'objectif est d'assurer un suivi efficace des produits disponibles dans différents magasins et de comparer les prix en fonction de divers critères.

---

## **2. Structure de la Base de Données**

### **2.1 Tables Principales**

La base de données est structurée autour des tables suivantes :

1. **products** : Stocke les informations des produits.
2. **store** : Contient les détails des magasins.
3. **rel_store_price** : Gère la relation entre les produits et les magasins avec les prix correspondants.

### **2.2 Tables Supplémentaires**

Afin de compléter le modèle relationnel, nous avons ajouté :

1. **capacity** : Définit la capacité des produits (ex: 500ml, 1kg).
2. **unit_of_measure** : Définit les unités de mesure (kg, g, L).
3. **taxe_rate** : Stocke les taux de taxe appliqués.
4. **category** : Catégorise les produits.
5. **product_state** : Indique l'état du produit (disponible, en rupture de stock, etc.).

### **2.3 Relations Clés**

- `products` est lié à `category`, `capacity`, `unit_of_measure` et `product_state` par des clés étrangères.
- `rel_store_price` relie un `product` à un `store` en enregistrant son prix.
- `rel_store_price` contient une référence à `taxe_rate` pour calculer le prix hors taxe.

---

## **3. Implémentation des Modèles Django**

Les modèles ont été définis en respectant les contraintes suivantes :

- **Produits (`products`)** :
    - `generic_label_id` permet de comparer les produits similaires.
    - `id_capacity` et `uom_id` référencent respectivement `capacity` et `unit_of_measure`.
- **Prix en magasin (`rel_store_price`)** :
    - `price_exclude` stocke le prix hors taxe.
    - `taxe_rate_id` référence `taxe_rate`.
    - `discounted_price` permet de stocker les prix promotionnels.
    - `proof` stocke l'URL d'une preuve de prix.

---

## **4. API CRUD : Routes et Fonctionnalités**

L'API REST a été mise en place avec Django REST Framework et expose les routes suivantes :

### **4.1 Routes Disponibles**

| Ressource | Méthode HTTP | URL | Description |
| --- | --- | --- | --- |
| Produits | GET | `/api/products/` | Liste des produits |
| Produits | POST | `/api/products/` | Création d'un produit |
| Produits | GET | `/api/products/{id}/` | Détails d'un produit |
| Produits | PUT/PATCH | `/api/products/{id}/` | Mise à jour d'un produit |
| Produits | DELETE | `/api/products/{id}/` | Suppression d'un produit |
| Magasins | GET | `/api/stores/` | Liste des magasins |
| Magasins | POST | `/api/stores/` | Création d'un magasin |
| Magasins | PUT/PATCH | `/api/stores/{id}/` | Mise à jour d'un magasin |
| Magasins | DELETE | `/api/stores/{id}/` | Suppression d'un magasin |
| Prix en magasin | GET | `/api/prices/` | Liste des prix |
| Prix en magasin | POST | `/api/prices/` | Ajout d'un prix |
| Prix en magasin | PUT/PATCH | `/api/prices/{id}/` | Mise à jour d'un prix |
| Prix en magasin | DELETE | `/api/prices/{id}/` | Suppression d'un prix |

### **4.2 Choix de l'Architecture**

L'utilisation de `ModelViewSet` simplifie l'implémentation CRUD et garantit un code propre et maintenable.

---

## **5. Processus d'Initialisation du Projet**

Pour initialiser et déployer ce projet, suivez ces étapes :

1. **Cloner le référentiel** :
    
    ```bash
    git clone https://github.com/BenjaminPeronne/comparator
    cd comparator
    ```
    
2. **Installer les dépendances** :
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Configurer PostgreSQL** (fichier `.env` si applicable)
4. **Exécuter les migrations** :
    
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

---

## **6. Tests Unitaires avec pytest**

Nous avons mis en place des tests unitaires pour vérifier le bon fonctionnement des modèles et des routes API.

- **Tests sur les Modèles** :
    - Création de produits, magasins et relations de prix.
    - Vérification des contrôles d'unicité (ex: barcode unique).
    - Vérification de la suppression cascade.
- **Tests sur l'API** :
    - Création, lecture, modification et suppression de produits via l'API.
    - Tests de validation des données (champs obligatoires, format incorrect).

### **6.1 Test de Création d'un Magasin**

### **Requête cURL**

```bash
curl -X POST <http://localhost:9000/api/stores/> \
     -H "Content-Type: application/json" \
     -d '{
           "store_label": "SUPER U SAINTE ROSE",
           "address": "Adresse inconnue",
           "postal_code": "97115",
           "city": "SAINTE ROSE",
           "country": "France",
           "longitude": null,
           "latitude": null
         }'
```

Exécution des tests :

```bash
pytest -v
```

---

## **7. Conclusion et Améliorations Possibles**

L'implémentation de l'API CRUD a été réalisée en respectant les meilleures pratiques Django.

### **Améliorations futures** :

- Ajout d'un système d'authentification JWT.
- Gestion avancée des promotions avec historique des prix.
- Optimisation des requêtes avec `select_related` et `prefetch_related`.
- Ajout d'un système de recherche et de filtrage avancé.

---

**Auteur :** Equipe de développement - M2 MIAGE