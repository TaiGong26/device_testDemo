from dataclasses import dataclass, field
from typing import List, Optional
import copy


@dataclass
class JointConfig:
    joint_name: str
    joint_limit: List[float]

@dataclass
class ArmConfig: