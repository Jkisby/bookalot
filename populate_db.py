from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Product

engine = create_engine('sqlite:///catalog.db')
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
User1 = User(name="James Kisby", email="james.kisby@hotmail.com",
             picture='')
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Category(user_id=1, name="J.K. Rowling")

session.add(category1)
session.commit()

item1 = Product(user_id=1,
                name="Harry Potter and the Philosopher's Stone",
                description="Harry Potter's life is miserable. His parents are"
                            " dead and he's stuck with his heartless relatives"
                            ", who force him to live in a tiny closet under "
                            "the stairs. But his fortune changes when he "
                            "receives a letter that tells him the truth about "
                            "himself: he's a wizard. A mysterious visitor "
                            "rescues him from his relatives and takes him to "
                            "his new home, Hogwarts School of Witchcraft and "
                            "Wizardry.",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1474154022l/3.jpg")

session.add(item1)
session.commit()

item2 = Product(user_id=1,
                name="Harry Potter and the Chamber of Secrets",
                description="The Dursleys were so mean and hideous that summer"
                            " that all Harry Potter wanted was to get back to "
                            "the Hogwarts School for Witchcraft and Wizardry. "
                            "But just as he's packing his bags, Harry receives"
                            " a warning from a strange, impish creature named "
                            "Dobby who says that if Harry Potter returns to "
                            "Hogwarts, disaster will strike.",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1474169725l/15881"
                        ".jpg")

session.add(item2)
session.commit()

item3 = Product(user_id=1,
                name="Harry Potter and the Prisoner of Azkaban",
                description="Harry Potter is lucky to reach the age of "
                            "thirteen, since he has already survived the "
                            "murderous attacks of the feared Dark Lord on more"
                            " than one occasion. But his hopes for a quiet "
                            "term concentrating on Quidditch are dashed when a"
                            " maniacal mass-murderer escapes from Azkaban, "
                            "pursued by the soul-sucking Dementors who guard "
                            "the prison.",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1362278317l/5.jpg")

session.add(item3)
session.commit()

item4 = Product(user_id=1,
                name="Harry Potter and the Goblet of Fire",
                description="Harry Potter is midway through both his training "
                            "as a wizard and his coming of age. Harry wants to"
                            " get away from the pernicious Dursleys and go to "
                            "the International Quidditch Cup with Hermione, "
                            "Ron, and the Weasleys. He wants to dream about "
                            "Cho Chang, his crush (and maybe do more than "
                            "dream). He wants to find out about the mysterious"
                            " event that supposed to take place at Hogwarts "
                            "this year, an event involving two other rival "
                            "schools of magic, and a competition that hasn't "
                            "happened for hundreds of years. He wants to be a "
                            "normal, fourteen-year-old wizard. But "
                            "unfortunately for Harry Potter, he's not normal "
                            "- even by wizarding standards.  ",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1361482611l/6.jpg")
session.add(item4)
session.commit()

item5 = Product(user_id=1,
                name="Harry Potter and the Order of the Phoenix",
                description="Harry Potter is due to start his fifth year at "
                            "Hogwarts School of Witchcraft and Wizardry. His "
                            "best friends Ron and Hermione have been very "
                            "secretive all summer and he is desperate to get "
                            "back to school and find out what has been going "
                            "on. However, what Harry discovers is far more "
                            "devastating than he could ever have expected..."
                            "And in his case, different can be deadly.       ",
                price="$7.50",
                category=category1,
                picture="https://upload.wikimedia.org/wikipedia/en/7/70/Harry"
                        "_Potter_and_the_Order_of_the_Phoenix.jpg")

session.add(item5)
session.commit()

item6 = Product(user_id=1,
                name="Harry Potter and the Half-Blood Prince",
                description="It is the middle of the summer, but there is an "
                            "unseasonal mist pressing against the windowpanes."
                            " Harry Potter is waiting nervously in his bedroom"
                            " at the Dursleys' house in Privet Drive for a "
                            "visit from Professor Dumbledore himself. One of "
                            "the last times he saw the Headmaster was in a "
                            "fierce one-to-one duel with Lord Voldemort, and "
                            "Harry can't quite believe that Professor "
                            "Dumbledore will actually appear at the Dursleys'"
                            " of all places. Why is the Professor coming to "
                            "visit him now? What is it that cannot wait until"
                            " Harry returns to Hogwarts in a few weeks' time?"
                            " Harry's sixth year at Hogwarts has already got "
                            "off to an unusual start, as the worlds of Muggle"
                            " and magic start to intertwine...",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1361039191l/1.jpg")

session.add(item6)
session.commit()

item7 = Product(user_id=1,
                name="Harry Potter and the Deathly Hallows",
                description="It's no longer safe for Harry at Hogwarts, so he"
                            " and his best friends, Ron and Hermione, are on "
                            "the run. Professor Dumbledore has given them "
                            "clues about what they need to do to defeat the "
                            "dark wizard, Lord Voldemort, once and for all, "
                            "but it's up to them to figure out what these "
                            "hints and suggestions really mean.",
                price="$7.50",
                category=category1,
                picture="https://images.gr-assets.com/books/1474171184l/"
                        "136251.jpg")

session.add(item7)
session.commit()


# Menu for UrbanBurger
category2 = Category(user_id=1, name="Stephen King")

session.add(category2)
session.commit()

item1 = Product(user_id=1,
                name="The Green Mile",
                description="At Cold Mountain Penitentiary, along the lonely "
                            "stretch of cells known as the Green Mile, "
                            "killers are depraved as the psychopathic 'Billy "
                            "the Kid' Wharton and the possessed Eduard "
                            "Delacroix await death strapped in 'Old Sparky.'",
                price="$7.50",
                category=category2,
                picture="https://images.gr-assets.com/books/1373903563l/"
                        "11566.jpg")

session.add(item1)
session.commit()

item2 = Product(user_id=1,
                name="The Shining",
                description="Danny was only five years old but in the words of"
                            " old Mr Halloran he was a 'shiner', aglow with "
                            "psychic voltage. When his father became caretaker"
                            " of the Overlook Hotel his visions grew "
                            "frighteningly out of control. ",
                price="$7.50",
                category=category2,
                picture="https://images.gr-assets.com/books/1353277730l/"
                        "11588.jpg")

session.add(item2)
session.commit()

item3 = Product(user_id=1,
                name="The Stand",
                description="This is the way the world ends: with a nanosecond"
                            " of computer error in a Defense Department "
                            "laboratory and a million casual contacts that "
                            "form the links in a chain letter of death.",
                price="$7.50",
                category=category2,
                picture="https://images.gr-assets.com/books/1213131305l/"
                        "149267.jpg")

session.add(item3)
session.commit()

item4 = Product(user_id=1,
                name="Carrie",
                description="Carrie knew she should not use the terrifying "
                            "power she possessed... But one night at her "
                            "senior prom, Carrie was scorned and humiliated "
                            "just one time too many, and in a fit of "
                            "uncontrollable fury she turned her clandestine "
                            "game into a weapon of horror and destruction...",
                price="$7.50",
                category=category2,
                picture="https://images.gr-assets.com/books/1166254258l/"
                        "10592.jpg")
session.add(item4)
session.commit()

item5 = Product(user_id=1,
                name="IT",
                description="To the children, the town was their whole world."
                            " To the adults, knowing better, Derry, Maine was"
                            " just their home town: familiar, well-ordered for"
                            " the most part. A good place to live.",
                price="$7.50",
                category=category2,
                picture="https://images.gr-assets.com/books/1334416842l/"
                        "830502.jpg")

session.add(item5)
session.commit()


# Menu for UrbanBurger
category3 = Category(user_id=1, name="Charles Dickens")

session.add(category3)
session.commit()

item1 = Product(user_id=1,
                name="A Tale of Two Cities",
                description="After eighteen years as a political prisoner in "
                            "the Bastille, the ageing Doctor Manette is "
                            "finally released and reunited with his daughter "
                            "in England. There the lives of two very different"
                            " men, Charles Darnay, an exiled French "
                            "aristocrat, and Sydney Carton, a disreputable but"
                            " brilliant English lawyer, become enmeshed "
                            "through their love for Lucie Manette. From the "
                            "tranquil roads of London, they are drawn against"
                            " their will to the vengeful, bloodstained streets"
                            " of Paris at the height of the Reign of Terror, "
                            "and they soon fall under the lethal shadow of La"
                            " Guillotine.",
                price="$7.50",
                category=category3,
                picture="https://images.gr-assets.com/books/1344922523l/"
                        "1953.jpg")

session.add(item1)
session.commit()

item2 = Product(user_id=1,
                name="Oliver Twist",
                description="",
                price="$7.50",
                category=category3,
                picture="https://images.gr-assets.com/books/1327868529l/"
                        "18254.jpg")

session.add(item2)
session.commit()

item3 = Product(user_id=1,
                name="Great Expectations",
                description="In what may be Dickens's best novel, humble, "
                            "orphaned Pip is apprenticed to the dirty work of"
                            " the forge but dares to dream of becoming a "
                            "gentleman - and one day, under sudden and "
                            "enigmatic circumstances, he finds himself in "
                            "possession of 'great expectations. In this "
                            "gripping tale of crime and guilt, revenge and "
                            "reward, the compelling characters include "
                            "Magwitch, the fearful and fearsome convict; "
                            "Estella, whose beauty is excelled only by her "
                            "haughtiness; and the embittered Miss Havisham, "
                            "an eccentric jilted bride.",
                price="$7.50",
                category=category3,
                picture="https://images.gr-assets.com/books/1327920219l/"
                        "2623.jpg")

session.add(item3)
session.commit()

item4 = Product(user_id=1,
                name="A Christmas Carol",
                description="",
                price="$7.50",
                category=category3,
                picture="https://images.gr-assets.com/books/1406512317l/"
                        "5326.jpg")
session.add(item4)
session.commit()

item5 = Product(user_id=1,
                name="David Copperfield",
                description="",
                price="$7.50",
                category=category3,
                picture="https://images.gr-assets.com/books/1461452762l/"
                        "58696.jpg")

session.add(item5)
session.commit()

print "added menu items!"
