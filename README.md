# nsls2_badger_training (08/30/2024)

## Install Badger v1.0.2

### conda envs/pkgs directory locations

- We will create a new conda environment. Due to a very limited space under home (NFS), it is better to have this created under `/nsls2/data3`.

- First check to see where this env. will be created:
`$ conda config --show envs_dirs`
`$ conda config --show pkgs_dirs`

- If the top directory is NOT under `/nsls2/data3`, then do this:
`$ conda config --add envs_dirs /nsls2/data3/staff/<username>/.conda/envs`
`$ conda config --add pkgs_dirs /nsls2/data3/staff/<username>/.conda/pkgs`

### mamba (optional)

- `mamba` is practically the same as `conda`, but usually much faster. If you want to use `mamba`, add the following line your `~/.bashrc` to be able to use `mamba`:

  `alias mamba='/nsls2/software/ap/miniconda/py310_23.1.0-1/bin/mamba'`

### Set up a new conda/mamba environment for Badger in 2 steps

#### Step 1: `$ mamba create -n badger_training python=3.11 numpy=1 caproto -c conda-forge`
- Forcing NOT to install `numpy` v2. If `xopt` is included here, `numpy` may end up with v2.
- `caproto` is only needed to create temporary fake PVs for the training purpose.
- You can change "badger_training" if you want your environment named differently.

#### Step 2: Now install Badger and Xopt
`$ conda activate badger_training`
`(badger_training) $ mamba install xopt badger-opt pyepics debugpy matplotlib=3.8 h5py -c conda-forge`
- Only the frist 3 packages (up to `pyepics`) are required. The rest are optional.
- `debugpy` only useful if you are using Visual Studio Code (VSCode).
- `matplotlib` locked down to 3.8 due to a VSCode compatibility issue as of 7/11/2024.
- This installed Badger v1.0.2 and Xopt v2.3.0 as of 08/30/2024.
- This step will take a while to finish. So, let's move on to other prep tasks.

## Start a temporary IOC server for training

- Open a new terminal with the conda env activated. Then run the following commands:
  `(badger_training) $ cd <badger_training_git_folder>`
  `(badger_training) $ python ioc.py --list-pvs`

- Note `<badger_training_git_folder>` is the path to the folder where this README file is.
- Leave this terminal open. Now you have 4 PVs available:
  `<username>:knob_x`
  `<username>:knob_y`
  `<username>:obs_a`
  `<username>:obs_b`

- The knob PVs and observable PVs are related as follows:
  `obs_a := knob_x * 2`
  `obs_b := knob_y * (-1)`

- Our toy optimizatoin problem is to let Badger adjust the knob PV values such that `obs_a` and `obs_b` approach some user-specified target values.

- Try the following commands on a new separate terminal:
  `$ caget yhidaka:knob_x`
  `$ caput yhidaka:knob_x 4.2`
  (Replace `yhidaka` with your own username)

## Set up Badger plugins folder

- Go to a directory where you want to clone a `git` repository.

  `$ git clone https://github.com/SLAC-ML/Badger-Plugins.git my_badger_plugins`

- This will create a new folder named `my_badger_plugins`
  - Let `<path_to_my_badger_plugins>` denote the path to this newly created folder.

- Copy the test environment folder `nsls2_training` into this plugins folder:

  `$ cp -r <badger_training_git_folder>/nsls2_training <path_to_my_badger_plugins>/environments`

- You also need to copy the following (otherwise Badger will fail):

  `$ cp <badger_training_git_folder>/interfaces/epics/__init__.py <path_to_my_badger_plugins>/interfaces/epics`

### After Badger has been installed

- There is one more step before Badger GUI should be launched.

- The RCDS file for Xopt v2.3.0 is not be the latest version. Swap the file with the latest as follows:

  `(badger_training) $ cd <badger_training_git_folder>`
  `(badger_training) $ python update_rcds.py`

- Note that once you this manual modification, next time you try to create a separate conda/mamba environment, you may see a warning message like the following, though it'll be still functional:

  `# warning  libmamba Invalid package cache, file '/nsls2/data3/staff/yhidaka/.conda/pkgs/xopt-2.3.0-pyhd8ed1ab_0/site-packages/xopt/generators/rcds/rcds.py' has incorrect size`

## Launch Badger GUI

`(badger_training) $ badger -g`

- This should automatically create a new folder `~/.local/share/Badger` with sub-folders. Badger will use these folders to store their run data, etc.

- If you don't want to use up all the NFS quota, it is recommended to re-direct these to `/nsls2/data3`, as we did for conda/mamba environments. To do so, click on the gear button at the bottom right corner of the GUI. In the pop-up window, change as follows:

  `Plugin Root: <path_to_my_badger_plugins>`
  `Database Root: <badger_data_root>/db`
  `Logbook Root: <badger_data_root>/logbook`
  `Archive Root: <badger_data_root>/archive`

  - `<badger_data_root>` is wherever you decide to locate these folders (should be under `/nsls2/data3` though)

- "Routine Editor" => "Environment + VOCS"
  - "Name" should list `nsls2_training`. Select it.

- If you select `expected improvement` as an algorithm, you must add initial points. Otherwise, it will fail.

- Every time you modify something in the folder "nsls2_training", you probably need to re-launch Badger for the changes to take effect.
