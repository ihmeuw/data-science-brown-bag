import subprocess


locations = [6, 97, 102, 156]
years = [2000, 2005, 2010, 2015]
script = "/homes/tangkend/brownbag/run.py"
array_script = "/homes/tangkend/brownbag/run_array.py"
combined_script = "/homes/tangkend/brownbag/run_combined.py"


def submit_normal_jobs():
    """Submit a qsub for each location and year."""
    for location in locations:
        for year in years:
            qsub = "qsub -N notarray -b y python {script} {loc} {year}".format(
                    script=script, loc=location, year=year)
            print(qsub)
            subprocess.call(qsub, shell=True)


def submit_array_jobs():
    """Submit a single qsub as an array job over locations and years."""
    num_of_jobs = len(locations) * len(years)
    qsub = "qsub -N array -b y -t 1:{N} python {script}".format(
            script=array_script, N=num_of_jobs)
    print(qsub)
    subprocess.call(qsub, shell=True)


def try_combined_script():
    """Submit a qsub and an array job qsub on the script that can handle both
    cases."""

    # Try combined script with command line arguments
    qsub = "qsub -N combined-notarray -b y python {script} loc year".format(
                script=combined_script)
    print(qsub)
    subprocess.call(qsub, shell=True)

    # Try combined script with an array job
    num_of_jobs = len(locations) * len(years)
    qsub = "qsub -N combined-array -b y -t 1:{N} python {script}".format(
            script=combined_script, N=num_of_jobs)
    print(qsub)
    subprocess.call(qsub, shell=True)
