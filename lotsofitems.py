from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Items, User

import random

engine = create_engine('postgresql:///catalogwithusers')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Random text for descriptions
randomText = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliis esse maiora, illud dubium, ad id, quod summum bonum dicitis, ecquaenam possit fieri accessio. Ne discipulum abducam, times. Atque ab his initiis profecti omnium virtutum et originem et progressionem persecuti sunt. Habes, inquam, Cato, formam eorum, de quibus loquor, philosophorum. Duo Reges: constructio interrete. Quae cum dixisset paulumque institisset, Quid est?",
            "Immo vero, inquit, ad beatissime vivendum parum est, ad beate vero satis. Ergo instituto veterum, quo etiam Stoici utuntur, hinc capiamus exordium. Praeclarae mortes sunt imperatoriae",
            "Sed quae tandem ista ratio est? Nam Pyrrho, Aristo, Erillus iam diu abiecti. Conferam tecum, quam cuique verso rem subicias; Utinam quidem dicerent alium alio beatiorem! Iam ruinas videres.",
            "Quae diligentissime contra Aristonem dicuntur a Chryippo. Age, inquies, ista parva sunt. Quem Tiberina descensio festo illo die tanto gaudio affecit, quanto L. Si longus, levis; Quod idem cum vestri faciant, non satis magnam tribuunt inventoribus gratiam. Inde igitur, inquit, ordiendum est. Sed id ne cogitari quidem potest quale sit, ut non repugnet ipsum sibi.",
            "Non enim iam stirpis bonum quaeret, sed animalis. Qui-vere falsone, quaerere mittimus-dicitur oculis se privasse; Ecce aliud simile dissimile. Quamquam te quidem video minime esse deterritum. Habent enim et bene longam et satis litigiosam disputationem."
    ]


# Items for Soccer
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

item1 = Items(user_id=1,
              name="Jersey",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category1)
session.add(item1)
session.commit()

item2 = Items(user_id=1,
              name="Shinguards",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category1)
session.add(item2)
session.commit()

item3 = Items(user_id=1,
              name="Two shinguards",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category1)
session.add(item3)
session.commit()

item4 = Items(user_id=1,
              name="Soccer Cleats",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category1)
session.add(item4)
session.commit()


# Items for Basketball
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

item5 = Items(user_id=1,
              name="Basketball",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category2)
session.add(item5)
session.commit()

item6 = Items(user_id=1,
              name="Basketball Hoops",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category2)
session.add(item6)
session.commit()

item7 = Items(user_id=1,
              name="Basketball Shoes",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category2)
session.add(item7)
session.commit()


# Items for Baseball
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

item8 = Items(user_id=1,
              name="Bat",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category3)
session.add(item8)
session.commit()

item9 = Items(user_id=1,
              name="Gloves",
              description=randomText[random.randint(0, len(randomText)-1)],
              category=category3)
session.add(item9)
session.commit()

item10 = Items(user_id=1,
               name="Hat",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category3)
session.add(item10)
session.commit()


# Items for Frisbee
category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

item11 = Items(user_id=1,
               name="Frisbee",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category4)
session.add(item11)
session.commit()


# Items for Snowboarding
category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

item12 = Items(user_id=1,
               name="Goggles",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category5)
session.add(item12)
session.commit()

item13 = Items(user_id=1,
               name="Snowboard",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category5)
session.add(item13)
session.commit()


# Items for Rock Climbing
category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

item14 = Items(user_id=1,
               name="Chalk",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category6)
session.add(item14)
session.commit()

item15 = Items(user_id=1,
               name="Rope",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category6)
session.add(item15)
session.commit()

item16 = Items(user_id=1,
               name="Carabiner",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category6)
session.add(item16)
session.commit()

item17 = Items(user_id=1,
               name="Chalk Bag",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category6)
session.add(item17)
session.commit()

item18 = Items(user_id=1,
               name="Sling",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category6)
session.add(item18)
session.commit()


# Items for Foosball
category7 = Category(name="Foosball")
session.add(category7)
session.commit()

item19 = Items(user_id=1,
               name="Foosball Table",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category7)
session.add(item19)
session.commit()


# Items for Skating
category8 = Category(name="Skating")
session.add(category8)
session.commit()

item20 = Items(user_id=1,
               name="Skateboard",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category8)
session.add(item20)
session.commit()

item21 = Items(user_id=1,
               name="Helmet",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category8)
session.add(item21)
session.commit()


# Items for Hockey
category9 = Category(name="Hockey")
session.add(category9)
session.commit()

item22 = Items(user_id=1,
               name="Stick",
               description=randomText[random.randint(0, len(randomText)-1)],
               category=category9)
session.add(item22)
session.commit()
