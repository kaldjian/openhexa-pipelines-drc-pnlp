import os
import pandas as pd
from datetime import datetime
import papermill as pm

from openhexa.sdk import current_run, pipeline, workspace
from openhexa.sdk.datasets.dataset import DatasetVersion


@pipeline(code="pnlp-tables-update", name="PNLP tables update")
def pnlp_tables_update():
    """
    In this pipeline we call a notebook launcher that executes the PNLP tables update
    
    """

    # Setup variables
    notebook_name = "DB_update"
    notebook_path = f"{workspace.files_path}/pipelines/pnlp_tables_update/code/"
    out_notebook_path = f"{workspace.files_path}/pipelines/pnlp_tables_update/notebook_outputs"

    # Run update notebook for PNLP tables    
    run_update_with(nb_name=notebook_name, nb_path=notebook_path, out_nb_path=out_notebook_path) 




@pnlp_tables_update.task
def run_update_with(nb_name:str, nb_path:str, out_nb_path:str):
    """
    Update a tables using the latest dataset version
    
    """         
    nb_full_path = os.path.join(nb_path, f"{nb_name}.ipynb")
        
    current_run.log_info(f"Executing notebook: {nb_full_path}")

    # out_nb_fname = os.path.basename(in_nb_dir.replace('.ipynb', ''))
    execution_timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H_%M_%S")   
    out_nb_fname = f"{nb_name}_OUTPUT_{execution_timestamp}.ipynb" 
    out_nb_full_path = os.path.join(out_nb_path, out_nb_fname)

    pm.execute_notebook(input_path = nb_full_path,
                        output_path = out_nb_full_path) 



if __name__ == "__main__":
    pnlp_tables_update()