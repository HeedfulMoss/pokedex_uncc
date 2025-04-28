from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association tables for many-to-many relationships
pokemon_weak_against = Table(
    'pokemon_weak_against', 
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
    Column('type_id', Integer, ForeignKey('type.id'))
)

pokemon_strong_against = Table(
    'pokemon_strong_against', 
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
    Column('type_id', Integer, ForeignKey('type.id'))
)

pokemon_types = Table(
    'pokemon_types', 
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
    Column('type_id', Integer, ForeignKey('type.id'))
)

class Pokemon(Base):
    __tablename__ = 'pokemon'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    types = relationship("Type", secondary=pokemon_types, backref="pokemon_with_type")
    weak_against = relationship("Type", secondary=pokemon_weak_against, backref="pokemon_weak_to")
    strong_against = relationship("Type", secondary=pokemon_strong_against, backref="pokemon_strong_against")

class Type(Base):
    __tablename__ = 'type'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)