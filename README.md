# South King County Opportunity Youth

This project offers an updated estimate of the number of Opportunity Youth in South King County using the 2017 5-year American Community Survey [(ACS)](https://www.census.gov/programs-surveys/acs/about.html) Public Use Microdata Survey [(PUMS)](https://www.census.gov/programs-surveys/acs/technical-documentation/pums.html).

## THIS REPOSITORY

### Setup Instructions

If you are missing required software (e.g. Anaconda, PostgreSQL), please run the following command in Bash:
```bash
# installs necessary requirements
# note: this may take anywhere from 10-20 minutes
sh src/requirements/install.sh
```

### `oy-env` conda Environment

This project relies on you using the [`environment.yml`](environment.yml) file to recreate the `oy-env` conda environment. To do so, please run the following commands *in your terminal*:

```bash
# create the oy-env conda environment
conda env create -f environment.yml

# activate the oy-env conda environment
conda activate oy-env

# if needed, make oy-env available to you as a kernel in jupyter
python -m ipykernel install --user --name oy-env --display-name "Python 3 (oy-env)"
```

Note that this may take 10 or more minutes depending on internet speed.

**Catalina Note:** You may need to modify the `prefix` at the very bottom of `environment.yml` if you are on macOS Catalina.  Run `conda env list` in your terminal to determine the appropriate path by looking at the paths of your existing conda environment(s).  Modify `environment.yml` then try running the installation commands listed above again.

### Data Download

To download the relevant data, run the following command *in Python*:

```
data_collection.download_data_and_load_into_sql()
```

Note that this may take 10 or more minutes depending on internet speed.

There is an example notebook in the `notebooks/exploratory` directory with this code already added.

## BACKGROUND

Measuring the successes and barriers faced by our most vulnerable youth is a challenge in the South King County region<sup>1</sup>. While there is a lot of information gathered from K12 districts and colleges about student outcomes, few data exists among Opportunity Youth (OY): young folks between the age 16 through 24 who are disengaged from both work and school<sup>2</sup>. This population is of particular interest to The Seattle Region Partnership (SRP), a multi-sector initiative founded by the Seattle Metropolitan Chamber of Commerce, Seattle Foundation, City of Seattle, and King County<sup>3</sup>.

## PROJECT GOAL

The SRP would like an update on the estimated number of OY in South King County. According to a recent The Seattle Times article, the number of OY in South King County has remained steadfast at 19,000<sup>4</sup>. However, that estimation comes from a report that is over three years old. As Data Science Consultants, your task is to inform the SRP on the current status of OY in South King County using updated data.

## PROJECT REQUIREMENTS

At minimum, the SRP is expecting the following:

* A map that visualizes which parts of King County are a part of South King County;

* An update of the estimated number of OY in South King County. In addition the estimate, be sure to include a breakdown of the count of OY by Public Use Microdata Area (PUMA) within South King County;
    + _Note: your supervisor is very interested in these statistics. After the third day of project week, they will be conducting a code review to verify your results before you share these statistics with the SRP._


* An update of the table “Opportunity Youth Status by Age” located on page 2 of the 2016 report “Opportunity Youth in the Road Map Project Region”; and

* A visualization that highlights a trend between the 2016 report and current data.

The SRP has asked that any extra time remaining be used to create the following items:

* Create a choropleth map of the count of OY by PUMA within South King County;

* For South King County, create a choropleth map that shows the percentage of jobs for workers age 29 or younger out of the total number of jobs per census block; and

* Of the census blocks where jobs for workers age 29 or younger are the majority of employed people, what are a few of the industries that employ this group of people?

* Utilize additional data sources to support your recommendations, e.g. [Census Bureau APIs](https://www.census.gov/data/developers/data-sets.html), [King County Open Data](https://data.kingcounty.gov/browse?limitTo=datasets&provenance=official), or [King County GIS Open Data](https://gis-kingcounty.opendata.arcgis.com/)

## LEARNING GOALS
The goal of this project is to showcase your newfound Python and PostgreSQL skills to generate analytical insights and communicate the high level takeaways to a non-technical audience. This project will emphasize the following learning goals:

* Break down a question into small technical tasks;

* Query data from a PostgreSQL database;

* Produce descriptive statistics;

* Visualize descriptive statistics; and

* Tell a story from the descriptive statistics.

## DELIVERABLES

To complete this project, you will need to turn in the following deliverables:

1. A public GitHub repository.
2. An `environment.yml` file that contains all the necessary packages needed to recreate your conda environment.
    - Start with the provided `environment.yml`, then as you install any additional packages be sure to [export](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-the-environment-yml-file) the new version and commit the changes in git.
3. A standalone `src/` directory that stores all relevant source code.
    - All functions have docstrings that act as [professional-quality documentation](http://google.github.io/styleguide/pyguide.html#381-docstrings).
    - [Well documented](https://www.sqlstyle.guide/) SQL queries with appropriate single-line or multiline comments.
4. A user-focused `README.md` file that explains your process, methodology and findings.
    - Take the time to make sure that you craft your story well, and clearly explain your process and findings in a way that clearly shows both your technical expertise and your ability to communicate your results!
5. A record of your workflow stored in `notebooks/exploratory`.  Don't be afraid to leave in error messages, so you know what didn't work!
6. One final Jupyter Notebook file stored in `notebooks/report` that focuses on visualization and presentation.
    - The very beginning of the notebook contains a description of the purpose of the notebook.
       - This is helpful for your future self and anyone of your colleagues that needs to view your notebook. Without this context, you’re implicitly asking your peers to invest a lot of energy to help solve your problem. Help them by enabling them to jump into your project by providing them the purpose of this Jupyter Notebook.
    - Explanation of the data sources and where one can retrieve them
        - Whenever possible, link to the corresponding data dictionary
    - Custom functions and classes are imported from Python modules and are not created directly in the notebook.  As soon as you have a working function in one of your exploratory notebooks, copy it over to `src` so it is reusable.
7. A one-page memo stored in `reports/memo.md` written exclusively for a non-technical stakeholder.
    - This memo should describe:
       - A summary of the business problem you are trying to solve
       - Key takeaways from your solution
       - A section on next steps if you had more time (i.e. one additional week)
8. An "Executive Summary" Keynote/PowerPoint/Google Slide presentation (delivered as a PDF export) that explains what you have found for the SRP.
    - Make sure to also add and commit this file as presentation.pdf of your non-technical presentation to your repository with a file name of `reports/presentation.pdf`.
    - Contain between 5-10 professional quality slides detailing:
       - A high-level overview of your methodology
       - The results you’ve uncovered
       - Any real-world recommendations you would like to make based on your findings (ask yourself--why should the executive team care about what you found? How can your findings help the company/stakeholder?)
       - Avoid technical jargon and explain results in a clear, actionable way for non-technical audiences.
    - All visualizations included in this presentation should also be exported as image files (e.g. with `plt.savefig`, not by taking a screenshot) and saved under `reports/figures/`

## Citations

<sup>1</sup> Yohalem, N., Cooley, S. 2016. “Opportunity Youth in the Road Map Project Region”. Community Center for Education Results. Available at: https://bit.ly/2P2XRF3.

<sup>2</sup> Anderson, T., Braga, B., Derrick-Mills, T., Dodkowitz, A., Peters, E., Runes, C., and Winkler, M. 2019. “New Insights into the Back on Track Model’s Effects on Opportunity Youth Outcomes”. Urban Institute. Available at: https://bit.ly/2BuCLr1.

<sup>3</sup> Seattle Region Partnership. 2016. “King County Opportunity Youth Overview: Demographics of opportunity youth and systemic barriers to employment”. Available at: https://bit.ly/2oRGz37.

<sup>4</sup> Morton, N. 2019. “Nearly 19,000 youth in King County are neither working nor in school. How one Seattle nonprofit is changing that.” The Seattle Times. Available at: https://bit.ly/2W5EufR.
