# Classes

## Organism
- pop_size: int
- low_pheno: int
- high_pheno: int
- emitted: int
- bin_length: int
+ init_population
+ emit

## Schedule(ABC)
- current_count_requirement: float
- count: int
+ in_response_class
+ update_counter
+ get_availability
+ set_count_requirement
+ run

### Info:
The schedule class can be used for reinforcement or punishment; however, it **cannot** be used for both at the same time. The ScheduleData class has a flag `is_reinforcement_schedule` where if this is `True` then the schedule is a reinforcement schedule, otherwise it is a punishment schedule.

### 