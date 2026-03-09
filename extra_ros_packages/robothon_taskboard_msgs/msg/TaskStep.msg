uint8 TASK_STEP_TYPE_UNKNOWN = 0
uint8 TASK_STEP_TYPE_EQUAL = 1
uint8 TASK_STEP_TYPE_EQUAL_RANDOM = 2
uint8 TASK_STEP_TYPE_GREATER_EQUAL = 3
uint8 TASK_STEP_TYPE_TRACE_SHAPE = 4
uint8 TASK_STEP_TYPE_WAIT_RANDOM = 5
uint8 TASK_STEP_TYPE_ACTUATOR = 6

string sensor_name
uint8 type
SensorMeasurement target
string actuator_name
bool state
float32 tolerance
string clue_trigger_name
builtin_interfaces/Time clue_timeout
