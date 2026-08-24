from __future__ import annotations
from typing import BinaryIO
import numpy as np


class TimeEvents:
    def __init__(self, discrete: list[float], continuous: np.ndarray | None, infty: bool):
        self.discrete = discrete
        self.continuous = continuous
        self.infty = infty

    def clock(self, t: float) -> float:
        return min((s for s in self.discrete if s >= t), default=float("inf"))

class InteractingEntity:
    def __init__(self, id: str, proper_state_dim: int, states_description: list[str]):
        self.id = id
        self.proper_state_dim = proper_state_dim
        self.states_description = states_description
        
        # e.ac[i, t] is the activation of the interacting entity e for the interaction i at time t
        self.ac: dict[tuple[Interaction, float], float] = {} 
        
        # e.x[t] is the proper state of the interacting entity e at time t
        self.x: dict[float, np.ndarray] = {}


class Propagator(InteractingEntity):
    def __init__(self, id: str, proper_state_dim: int, states_description: list[str], type: str):

        super().__init__(id, proper_state_dim, states_description)

        self.interactions: list[Interaction] = []
        self.type = type
        self.gamma: dict[tuple[Interaction, float], object] = {}


class Patient(InteractingEntity):
    def __init__(self, id: str, proper_state_dim: int, states_description: list[str], Omega_type: str, P_density,f,
        Omega_discr_set: set | None = None,
        Omega_int_min: float | None = None,
        Omega_int_max: float | None = None):

        super().__init__(id, proper_state_dim, states_description)

        self.interactions: list[Interaction] = []
        self.I: dict[float, list[Interaction]] = {}
        self.Omega_type = Omega_type
        self.Omega_discr_set = Omega_discr_set
        self.Omega_int_min = Omega_int_min
        self.Omega_int_max = Omega_int_max
        self.P_density = P_density
        self.f = f

    def nx(self, s: float, t: float | None = None) -> dict[tuple[float, InteractingEntity], np.ndarray]:
        raise NotImplementedError


class Interaction:
    def __init__(self, id: str, agents: tuple[InteractingEntity, ...], pr: Propagator, pa: Patient, resources_type: type, resource_space_dim: int,
        T_s: TimeEvents,
        T_o: TimeEvents,
        T_a: TimeEvents,
        R=None,
        min_resource: float | None = None,
        max_resource: float | None = None):

        self.id = id
        self.agents = agents
        self.pr = pr
        self.pa = pa
        self.resources_type = resources_type
        self.resource_space_dim = resource_space_dim
        self.R = R
        self.min_resource = min_resource
        self.max_resource = max_resource

        self.T_s = T_s
        self.T_o = T_o
        self.T_a = T_a

        self.ts: dict[float, float] = {}
        self.to: dict[float, float] = {}
        self.ta: dict[float, float] = {}

        self.N: dict[float, list[InteractingEntity]] = {}

    def arity(self) -> int:
        return len(self.agents)

    def ag(self) -> tuple[InteractingEntity, ...]:
        return self.agents

    def a(self, j: int) -> InteractingEntity:
        return self.agents[j]

    def gamma(self, t: float | None = None) -> object:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Interaction(id={self.id})"

    def UML(self) -> BinaryIO:
        raise NotImplementedError

    def nx(self, t: float | None = None) -> dict[tuple[float, InteractingEntity], np.ndarray]:
        raise NotImplementedError

    def starting_times(self) -> list[float]:
        raise NotImplementedError

    def arrival_times(self) -> list[float]:
        raise NotImplementedError

    def ongoing_times(self) -> list[float]:
        raise NotImplementedError


class InteractionSpace:
    def __init__(self, id: str, t_st: float, t_end: float, Delta: float):
        self.id = id
        self.t_st = t_st
        self.t_end = t_end
        self.t = t_st
        self.E: dict[str, InteractingEntity] = {}
        self.I: dict[str, Interaction] = {}
        self.Delta = Delta

    def t_first_arrival(self, t: float | None = None) -> float:
        raise NotImplementedError

    def run(self) -> dict:
        raise NotImplementedError

    def execution_log(self, path: str) -> None:
        raise NotImplementedError

    def load_system_state(self, path: str) -> None:
        raise NotImplementedError