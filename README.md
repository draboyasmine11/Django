# Gestion Scolaire

Une mini application Django pour la gestion des étudiants et enseignants.

## Fonctionnalités

- **Gestion des étudiants** : Ajouter, modifier, supprimer et lister les étudiants
- **Gestion des enseignants** : Ajouter, modifier, supprimer et lister les enseignants
- **Interface moderne** : Design responsive avec Bootstrap 5
- **Messages de confirmation** : Notifications pour les actions réussies

## Modèles de données

### Étudiant (Student)
- Nom et prénom
- Email (unique)
- Date de naissance
- Date d'inscription (automatique)
- Classe

### Enseignant (Teacher)
- Nom et prénom
- Email (unique)
- Téléphone (optionnel)
- Matière enseignée
- Date d'embauche (automatique)

## Installation

1. Clonez le projet ou copiez les fichiers
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Appliquez les migrations :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Lancez le serveur de développement :
   ```bash
   python manage.py runserver
   ```

5. Accédez à l'application dans votre navigateur : `http://127.0.0.1:8000`

## Structure du projet

```
gestion_scolaire/
├── gestion_scolaire/          # Configuration du projet
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── school/                   # Application principale
│   ├── models.py            # Modèles Student et Teacher
│   ├── views.py             # Vues pour la gestion
│   ├── forms.py             # Formulaires Django
│   ├── urls.py              # URLs de l'application
│   ├── templates/school/    # Templates HTML
│   └── static/school/       # Fichiers statiques (CSS)
├── manage.py
├── requirements.txt
└── README.md
```

## URLs de l'application

- `/` : Page d'accueil
- `/students/` : Liste des étudiants
- `/students/add/` : Ajouter un étudiant
- `/students/<id>/edit/` : Modifier un étudiant
- `/students/<id>/delete/` : Supprimer un étudiant
- `/teachers/` : Liste des enseignants
- `/teachers/add/` : Ajouter un enseignant
- `/teachers/<id>/edit/` : Modifier un enseignant
- `/teachers/<id>/delete/` : Supprimer un enseignant
- `/admin/` : Interface d'administration Django

## Technologies utilisées

- **Python 3.x**
- **Django 4.2.7**
- **Bootstrap 5** pour le design
- **SQLite** comme base de données (développement)

## Développement

Pour ajouter de nouvelles fonctionnalités :

1. Modifiez les modèles dans `school/models.py`
2. Créez les migrations : `python manage.py makemigrations`
3. Appliquez les migrations : `python manage.py migrate`
4. Mettez à jour les vues dans `school/views.py`
5. Ajoutez les URLs nécessaires dans `school/urls.py`
6. Créez ou modifiez les templates dans `school/templates/school/`

## Licence

Ce projet est créé à des fins éducatives.
