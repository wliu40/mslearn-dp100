from azureml.core import Run
import pandas as pd
import os

# Get the experiment run context
run = Run.get_context()

data = pd.DataFrame({'a':[1,2,4,5,6], 'b':[3,5,6,7,8]})

run.log(name="df_size", value=len(data))

run.tag('quality', 'good')

run.add_properties({"author": "wei"})

# Complete the run
run.complete()
