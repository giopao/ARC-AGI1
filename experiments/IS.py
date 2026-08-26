from __future__ import annotations
from typing import Any
from types import FunctionType
import numpy as np
import bisect


class TimeEvents:
    def __init__(self, IS: InteractionSpace, discrete: list[float], continuous: np.ndarray | None, infty: bool):
        self.IS = IS
        self.discrete = discrete
        self.continuous = continuous
        self.infty = infty

    def clock(self, t: float) -> float:
        
        # --- 1. DISCRETE COMPONENT ---
        # Filter discrete points that are greater than or equal to t
        valid_discrete = [s for s in self.discrete if s >= t]
        min_discrete = min(valid_discrete, default=float("inf"))
        
        # --- 2. CONTINUOUS COMPONENT (INTERVALS) ---
        # Extract lower bounds T.continuous[k, 0] and and upper bounds T.continuous[k, 1]
        t_k1 = self.continuous[:, 0]
        t_k2 = self.continuous[:, 1]
        
        # An interval can contain a valid s >= t only if its upper bound is >= t
        valid_intervals_mask = t <= t_k2
        
        if np.any(valid_intervals_mask):
            # For each valid interval, the local minimum >= t is max(t, t_k^1)
            local_minima = np.maximum(t, t_k1[valid_intervals_mask])
            min_continuous = np.min(local_minima)
        else:
            min_continuous = float("inf")

        # --- 3. GLOBAL MINIMUM ---
        # The minimum of the union is the minimum of the individual components
        return min(min_discrete, min_continuous)
    
    
class InteractingEntity:
    def __init__(self, id: str, IS: InteractionSpace, proper_state_dim: int, states_description: list[str]):
        self.id = id
        self.IS = IS
        self.proper_state_dim = proper_state_dim
        self.states_description = states_description
        
        # e.ac[i, t] is the activation of the interacting entity e for the interaction i at time t
        # in case of static IS, we use e.ac[i]
        self.ac: dict[tuple[Interaction, float], float] | dict[Interaction, float] = {} 
        
        # e.x[t] is the proper state of the interacting entity e at time t
        # in case of static IS, we use e.x
        self.x: dict[float, np.ndarray] | np.ndarray = {}


class Propagator(InteractingEntity):
    def __init__(self, id: str, IS: InteractionSpace, proper_state_dim: int, states_description: list[str], type: str):

        super().__init__(id, IS, proper_state_dim, states_description)

        self.interactions: list[Interaction] = []
        self.type = type
        self.gamma: dict[tuple[Interaction, float], Any] | dict[Interaction, Any] = {}


class Patient(InteractingEntity):
    def __init__(self, id: str, IS: InteractionSpace, proper_state_dim: int, states_description: list[str], 
        Omega_type: str | None = None,
        Omega_discr_set: set | None = None,
        Omega_int_min: float | None = None,
        Omega_int_max: float | None = None,
        P_density: FunctionType | None = None, 
        f: FunctionType | None = None):

        super().__init__(id, IS, proper_state_dim, states_description)

        self.interactions: list[Interaction] = []
        
        # Implementation of p.I following the def.
        self.I: dict[float, list[Interaction]] | list[Interaction]
        if self.IS.is_static == False:
            t1 = self.IS.t_first_arrival(self.IS.t)
            self.I[self.IS.t] = [i for i in self.interactions if 
                                 t1 <= i.ta[self.IS.t] <= t1 + self.IS.Delta]
        else:
            self.I = self.interactions
        
        self.Omega_type = Omega_type
        self.Omega_discr_set = Omega_discr_set
        self.Omega_int_min = Omega_int_min
        self.Omega_int_max = Omega_int_max
        self.P_density = P_density
        self.f = f

    def nx(self, t: float | None = None, s: float | None = None) -> dict[tuple[float, InteractingEntity], np.ndarray]:
        raise NotImplementedError


class Interaction:
    def __init__(self, id: str, IS: InteractionSpace, agents: tuple[InteractingEntity, ...], 
        pr: Propagator, 
        pa: Patient, 
        resources_type: Any, 
        resource_space_dim: int,
        R: tuple(Any, FunctionType) | None = None,
        min_resource: float | None = None,
        max_resource: float | None = None,
        T_s: TimeEvents | None = None,
        T_o: TimeEvents | None = None,
        T_a: TimeEvents | None = None):

        self.id = id
        self.IS = IS
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
        
        # current time
        t = self.IS.t

        self.ts: dict[float, float]
        self.ts[t] = self.T_s.clock(t)
        
        self.to: dict[float, float]
        self.to[t] = self.T_o.clock(t)
        
        self.ta: dict[float, float]
        if len(self.T_a) < 2:
            self.ta[t] = self.T_a[0]
            
        # Find the insertion index using binary search
        idx = bisect.bisect_right(self.T_a, t)
        
        # Case 1: t is less than the first element
        if idx == 0:
            self.ta[t] = float("-inf")
            
        # Case 2: t is greater than or equal to the last element
        if idx == len(self.T_a):
            self.ta[t] = self.T_a[-1]
            
        # Case 3: t falls exactly between two elements
        self.ta[t] = self.T_a[idx - 1]

        self.N: dict[t: float, list[InteractingEntity]] = {}

    def arity(self) -> int:
        return len(self.agents)

    def ag(self) -> tuple[InteractingEntity, ...]:
        return self.agents

    def a(self, j: int) -> InteractingEntity:
        return self.agents[j]
      
    def gamma(self, t: float | None = None) -> Any:
        if self.IS.is_static == False:
            return self.pr.gamma[self, t]
        else:
            return self.pr.gamma[self]

    def UML(self) -> None:
        raise NotImplementedError

    def nx(self, t: float) -> dict[tuple[float, InteractingEntity], np.ndarray]:
        raise NotImplementedError

    def starting_times(self) -> list[float]:
        return sorted(self.T_s.discrete + self.T_s.continuous.flatten())

    def arrival_times(self) -> list[float]:
        return self.T_a.discrete

    def ongoing_times(self) -> list[float]:
        return sorted(self.T_o.discrete + self.T_o.continuous.flatten())


class InteractionSpace:
    def __init__(self, id: str, t_st: float, t_end: float, Delta: float, is_static: bool):
        self.id = id
        self.t_st = t_st
        self.t_end = t_end
        self.t = t_st
        self.E: dict[str, InteractingEntity] = {}
        self.I: dict[str, Interaction] = {}
        self.Delta = Delta
        self.is_static = is_static

    def t_first_arrival(self, t: float) -> float:
        return min((i.ta[t] for i in self.I.values() if i.ts[t] == t), default = float('inf'))

    def run(self) -> dict:
        raise NotImplementedError

    def execution_log(self, path: str) -> None:
        raise NotImplementedError

    def load_system_state(self, path: str) -> None:
        raise NotImplementedError