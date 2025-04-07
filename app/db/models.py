from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func


Base = declarative_base()

listing_categories = Table(
    'listing_categories',
    Base.metadata,
    Column('listing_id', Integer, ForeignKey('listings.listing_id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    listings = relationship("Listing", back_populates="user", cascade="all, delete-orphan")
    saved_listings = relationship("SavedListing", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    listings = relationship("Listing", secondary=listing_categories, back_populates="categories")

class Listing(Base):
    __tablename__ = 'listings'

    listing_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    description = Column(String, nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    property_type_id = Column(Integer, ForeignKey('property_types.property_type_id'))  
    city = Column(String)  
    street = Column(String) 
    house_number = Column(String)  
    apartment_number = Column(String, nullable=True) 
    area = Column(DECIMAL(10, 2), nullable=False)
    rooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(50), default='active')

    property_type = relationship("PropertyType")
    photos = relationship("ListingPhoto", back_populates="listing", cascade="all, delete-orphan")
    user = relationship("User", back_populates="listings")
    categories = relationship("Category", secondary=listing_categories, back_populates="listings")
    saved_listings = relationship("SavedListing", back_populates="listing", cascade="all, delete-orphan")

class SavedListing(Base):
    __tablename__ = 'saved_listings'

    saved_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    listing_id = Column(Integer, ForeignKey('listings.listing_id', ondelete='CASCADE'))

    user = relationship("User", back_populates="saved_listings")
    listing = relationship("Listing", back_populates="saved_listings")

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    receiver_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    listing_id = Column(Integer, ForeignKey('listings.listing_id', ondelete='CASCADE'))
    message = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP, default=func.now())
    chat_id = Column(Integer, ForeignKey('chats.chat_id', ondelete='CASCADE'))

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    chat = relationship("Chat", back_populates="messages")



class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(Integer, primary_key=True, index=True)
    user_1_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    user_2_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user_1 = relationship("User", foreign_keys=[user_1_id])
    user_2 = relationship("User", foreign_keys=[user_2_id])
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_1_id', 'user_2_id', name='_user_1_2_uc'),
    )


class ListingPhoto(Base):
    __tablename__ = "listing_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.listing_id", ondelete="CASCADE"))
    photo_url = Column(String, nullable=False) 

    listing = relationship("Listing", back_populates="photos")

class PropertyType(Base):
    __tablename__ = 'property_types'

    property_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)



