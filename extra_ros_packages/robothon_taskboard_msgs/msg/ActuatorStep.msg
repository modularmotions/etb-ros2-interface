uint8 ACTUATOR_VALUE_TYPE_UNKNOWN = 0
uint8 ACTUATOR_VALUE_TYPE_BOOL = 1
#uint8 ACTUATOR_VALUE_TYPE_ANALOG = 2
#uint8 ACTUATOR_VALUE_TYPE_INTEGER = 3

string actuator_name
uint8 type
bool target

# To emulate a union, we use all fields as vectors and only one is filled
#bool[<=1] bool_value
#float32[<=1] analog_value
#int64[<=1] integer_value
