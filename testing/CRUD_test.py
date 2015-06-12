from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine(
        'sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# add an entry into 'Restaurant' table
#restaurantQuery = session.query(Restaurant).filter_by(name="Sheraton Waikiki").one()

# add an entry into 'Restaurant' table
restaurantObj = Restaurant(name = "Sheraton Waikiki")
session.add(restaurantObj)
session.commit()

# add an entry into 'MenuItem' table
menuObj = MenuItem(name = "Chinese noodles",course="Dinner",description="Asian wok tossed noodles",price="$6",restaurant=restaurantObj)
session.add(menuObj)
session.commit()

# add an entry into 'MenuItem' table
menuObj = MenuItem(name = "Lau Lau",course="Dinner",description="Hawaiian pork and butterfish lau lau",price="$9",restaurant=restaurantObj)
session.add(menuObj)
session.commit()
"""
# add an entry into 'Restaurant' table
restaurantObj = Restaurant(name = "The French room")
session.add(restaurantObj)
session.commit()

# add an entry into 'Restaurant' table
restaurantObj = Restaurant(name = "Highlands Bar & Grill")
session.add(restaurantObj)
session.commit()

# add an entry into 'Restaurant' table
restaurantObj = Restaurant(name = "Sushi Nakazawa")
session.add(restaurantObj)
session.commit()
"""
