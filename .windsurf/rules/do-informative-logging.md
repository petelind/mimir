---
trigger: model_decision
description: When implementing a method or property - add extensive logging level.
---

Every service call or controller action must log to `app.log` at INFO level.
If logging is not yet configured - configure it. `app.log` is wiped on every restart for clean diagnosis.

## Logging Setup Pattern

```python
import logging
import io
from pprint import pformat
from tabulate import tabulate

logger = logging.getLogger(__name__)
buffer = io.StringIO()  # to collect structured info about data
```

## Core Logging Principles

When designing log messages, always ask:
- What information will I need to precisely pinpoint where the error is occurring?
- What context will I need in the logs to understand why it happened?
- What data transformations or validations occurred?
- Which decisions led to the current point?

## Required Logging Patterns

### 1. Method Entry with Context
```python
def method_name(self, param1, param2):
    logger.info(f'Starting {method_name} with param1={param1}, param2 shape: {param2.shape if hasattr(param2, "shape") else type(param2)}')
```

### 2. Data Structure Logging with Buffers
```python
# For DataFrames and complex structures
df.info(buf=buffer)
logger.info(f'Here is what I got for {dataset_name}: \n{buffer.getvalue()}')
buffer.truncate(0)

# For configuration objects
logger.info(f'Configuration loaded: \n{pformat(config_dict)}')

# For tabular data summaries
logger.info(f'Data preview: \n{tabulate(df.head(), headers=df.columns.tolist())}')
```

### 3. Conditional Logic Documentation
```python
if condition:
    logger.info(f'Column {column_name} present in df; attempting to process...')
    # processing logic
else:
    logger.warning(f'Column {column_name} missing; using default value: {default}')
```

### 4. Data Validation and Transformation Results
```python
# Before transformation
logger.debug(f'Input data types: {df.dtypes.to_dict()}')

# After transformation
detected_objects = df.dtypes == 'object'
if detected_objects.any():
    logger.warning(f'Object types still present in columns: {detected_objects[detected_objects].index.tolist()}')
else:
    logger.debug('All columns successfully converted to appropriate types')

# Statistical summaries
logger.info(f'Processing results for {operation_name}: \n{result.describe()}')
```

### 5. Error Context and Recovery
```python
try:
    # operation
    logger.info(f'Successfully completed {operation_name}')
except Exception as e:
    logger.error(f'Failed {operation_name} with error: {e}. Context: param1={param1}, data_shape={data.shape}')
    # recovery logic
    logger.info(f'Attempting recovery with fallback strategy')
```

## Minimum Logging Requirements

At minimum, our logging shall include:
- **Method entry**: Operation name, key parameters, data shapes/types
- **Configuration**: Setup decisions, rule books, parameters used
- **Data validation**: Input validation results, type conversions input and output, missing data handling warnings and errors
- **Processing steps**: Each major transformation with before/after summaries
- **Conditional logic**: Why certain paths were taken, what conditions triggered decisions
- **Results**: Statistical summaries, output shapes, success/failure indicators
- **Error context**: Full parameter context, data state, recovery attempts

## Log Level Guidelines

- **DEBUG**: Detailed flow control, type checking, internal state
- **INFO**: Method entry/exit, configuration, major processing steps, results
- **WARNING**: Concerning but recoverable conditions, substitutions, fallback usage, data quality issues
- **ERROR**: Failures requiring attention, unrecoverable conditions

## Buffer Management

When using StringIO buffers for structured logging:
```python
buffer = io.StringIO()
# ... collect data in buffer
logger.info(f'Structured data: \n{buffer.getvalue()}')
buffer.truncate(0)  # Clear for reuse
buffer.seek(0)      # Reset position if needed
```

## Data Summary Patterns

For complex data structures, always include:
- Shape/size information
- Data type summaries
- Statistical descriptions for numeric data
- Sample data (head/tail) for inspection
- Null/missing value counts


## On the INFO level, always include:

- Who triggered the action (user or agent)
- What the action did (inputs, affected models)
- Why the action occurred (based on intent, rule, or logic)
- The exact location (class, method/function, line if possible)
- Key input parameters or identifiers relevant to the operation
- The specific operation or action being attempted
- The error or unexpected condition encountered
- Relevant context or state (e.g., user ID, transaction ID, environment)
- (Optional) Next steps or hints if possible on how to investigate further

Design each log message so that if something fails, you can find the source and root cause without guessing or needing to reproduce the problem.

## On the DEBUG level, always include:

- The data we are operating on as real values, when feasible (we cannot show the entire dataframe, of course, but lets do head() and  tail() and describe())