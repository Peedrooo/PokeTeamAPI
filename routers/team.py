import logging

from fastapi import APIRouter, status, Response
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import requests
import models
from database import get_db

router = APIRouter()


class Team(BaseModel):
    user: str
    team: list

    class Config:
        schema_extra = {
            "example": {
                "user": "ash",
                "team": ["pikachu", "blastoise"]
            }
        }


class TeamOut(BaseModel):
    owner: str
    pokemons: list


@router.post("/teams", tags=["Teams"], status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: Team,
    db: Session = Depends(get_db),
    response: Response = Response):
    logging.info(f"teams: {team_data}")
    try:
        trainer = db.query(models.Trainer).filter_by(
            name=team_data.user).first()
        if not trainer:
            trainer = models.Trainer(name=team_data.user)
            db.add(trainer)
            db.commit()
            db.refresh(trainer)
        pokemons = []

        if not team_data.team:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "message": "Error creating team, team is empty",
                "status": "error",
                "data": None
            }

        for pokemon_name in team_data.team:
            pokemon = db.query(models.Pokemon).filter_by(
                name=pokemon_name).first()
            if not pokemon:
                response_api = requests.get(
                    f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
                if response_api.status_code == 200:
                    pokemon_data = response_api.json()
                    pokemon = models.Pokemon(
                        name=pokemon_name,
                        weight=pokemon_data['weight'],
                        height=pokemon_data['height']
                    )
                    db.add(pokemon)
                    db.commit()
                    db.refresh(pokemon)
                else:
                    logging.error(
                        f"Error fetching data for {pokemon_name}. Status code: {response.status_code}")
                    db.rollback()

                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {
                        "message": f"Error creating team, pokemon {pokemon_name} not found",
                        "status": "error",
                        "data": None
                    }

            pokemons.append(pokemon)

        trainer.pokemons.extend(pokemons)
        db.commit()

        return {
            "message": "Team created successfully",
            "status": "success",
            "data": TeamOut(owner=trainer.name, pokemons=trainer.pokemons)
        }

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "Error creating team"}


@router.get("/teams/{user}", tags=["Teams"], status_code=status.HTTP_200_OK)
def get_team(
    user: str,
    db: Session = Depends(get_db),
    response: Response = Response
    ):
    try:
        trainer = db.query(models.Trainer).filter_by(
            name=user).first()
        if not trainer:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "message": f"Trainer {user} not found",
                "status": "error",
                "data": None
            }
        return TeamOut(owner=trainer.name, pokemons=trainer.pokemons)

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "Error fetching team"}


@router.get("/teams", tags=["Teams"], status_code=status.HTTP_200_OK)
def get_all_teams(db: Session = Depends(get_db)):
    try:
        trainers = db.query(models.Trainer).all()
        teams = {}
        for e, trainer in enumerate(trainers):
            teams[e+1] = TeamOut(owner=trainer.name, pokemons=trainer.pokemons)
        if not teams:
            return {
                "message": "No teams found",
                "status": "success",
                "data": None
            }
        return teams

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "Error fetching teams"}
