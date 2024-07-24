from dataclasses import dataclass
from typing import Dict, Optional, Type


@dataclass
class FilmWork:
    id: str
    title: str
    description: Optional[str]
    creation_date: str
    file_path: Optional[str]
    rating: float
    type: str
    created_at: str
    updated_at: str


@dataclass
class Genre:
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Person:
    id: str
    full_name: str
    created_at: str
    updated_at: str


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: str


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: str


TABLE_TO_CLASS: Dict[str, Type[dataclass]] = {
    'film_work': FilmWork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork,
}
