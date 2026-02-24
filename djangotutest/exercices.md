# 2.2.1 Interface d'administration

- Voyez-vous tous les attributs de vos classes ? **Au click, sinon non**
- Pouvez-vous filtrer vos données suivant tous les attributs ? **Non**
- Pouvez-vous trier vos données suivant tous les attributs ? **Non**
- Pouvez-vous chercher un contenu parmi tous les champs ? **Non**
- Ajoutez un nouvel utilisateur via l'interface d'admin. Ne lui donnez pas le "Statut équipe" ni le "Statut super-utilisateur". Déconnectez-vous et essayez de vous reconnecter avec ce nouveau compte. Y parvenez-vous ? **Non**

---

# 2.2.2 Exercice shell

## 1. Afficher toutes les questions

```python
for q in Question.objects.all():
    print(q.id, q.question_text, q.pub_date)
```

---

## 2. Filtrer par mois

```python
data = Question.objects.filter(pub_date__month=2)
for q in data:
    print(q)
```

**Résultat :**
```
What's up?
Quel est la masse du soleil
Contre qui le psg a-til gagne la LDC ?
chat gpt ou claude ?
l'oeuf ou la poule
```

>  What's Up → date : `2026-02-03 10:12:38+00:00`

Avec variables :

```python
month = 2
year = 2026

data = Question.objects.filter(
    pub_date__year=year,
    pub_date__month=month
)
for q in data:
    print(q)
```

**Résultat :**
```
What's up?
Quel est la masse du soleil
Contre qui le psg a-til gagne la LDC ?
chat gpt ou claude ?
l'oeuf ou la poule
```

---

## 3. Afficher les choix d'une question

```python
data = Question.objects.get(id=2)
for choice in data.choice_set.all():
    print(choice.choice_text)
```

**Résultat :**
```
Paris
Madrid
Madagascar
```

---

## 4. Afficher toutes les questions avec leurs réponses

```python
data = Question.objects.all()
for q in data:
    print("---------------------------question------------------------------")
    print(q)
    print("------------------------------reponse------------------------------")
    for choice in q.choice_set.all():
        print(choice)
```

**Résultat :**
```
---------------------------question------------------------------
What's up?
------------------------------reponse------------------------------
Not much
The sky
...
```

---

## 5. Compter les réponses par question

```python
data = Question.objects.all()
for q in data:
    print("---------------------------question------------------------------")
    print(q)
    print("------------------------------reponse------------------------------")
    print("Nombre de réponse :", q.choice_set.count())
```

**Résultat :**
```
---------------------------question------------------------------
What's up?
------------------------------reponse------------------------------
Nombre de réponses : 2
...
```

---

## 7. Trier les questions par date décroissante

```python
Question.objects.all().order_by("-pub_date")
```

**Résultat :**
```
[
  <Question: Capitale de la France>,
  <Question: Contre qui le psg a-til gagne la LDC ?>,
  <Question: Quel est la masse du soleil>,
  <Question: chat gpt ou claude ?>,
  <Question: l'oeuf ou la poule>,
  <Question: What's up?>
]
```

info : 
> Capitale de la France → date : `2026-05-23 09:12:38+00:00`  
> What's up? → date : `2026-02-03 10:12:38+00:00`

---
## 9.
q = Question(question_text="Qui est l'inventeur du btc ?", pub_date=timezone.now())
q.save()

## 10.

>>> q.question_text
"Qui est l'inventeur du btc ?"
>>> q.choice_set.create(choice_text="Satoshi nakamoto", votes=0)
<Choice: Satoshi nakamoto>
>>> q.choice_set.create(choice_text="Jonatemps Meilleur", votes=0)
<Choice: Jonatemps Meilleur>
>>> q.choice_set.create(choice_text="Remi camionette", votes=0)
<Choice: Remi camionette>

## 11.
for i in q:
    print(i.was_published_recently())

**Résultat :**
False
True
False
False
False
False
True

## 12.
>>> from django.contrib.auth.models import User
>>> users = User.objects.all()
>>> for user in users:
...     print(user)

**Résultat :**
admin
user