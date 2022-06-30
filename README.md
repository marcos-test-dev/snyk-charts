<h3 align="center">
    Snyk Charts: Generate interactive charts derived from the Snyk API
</h3>

  <img alt="Last commit" src="https://img.shields.io/github/last-commit/snyk-marcos/snyk-charts">
</p>

## :bar_chart: Snyk Charts

Please note this is not an official feature of Snyk. This was created as a hobby to be consumed and maintained by the community.

![Snyk Charts](https://github.com/snyk-marcos/repo-images/blob/main/snyk-charts/snyk-charts-logo.png?raw=true)

### Usage

To get started, clone the repository and install the necessary dependencies by running: `pip install -r requirements.txt`

:arrow_right: Create a new file named `parameters.txt` following the structure below:

- **`ORGID=your-org-id`**
- **`TOKEN=your-snyk-token`**
- **`START_DATE=yyyy-mm-dd`**
- **`END_DATE=yyyy-mm-dd`**

:arrow_right: Place your `parameters.txt` file in the root of the project

:arrow_right: Run the script: `python snyk-charts.py`

Please feel free to contribute or suggest features. This is a side-project I am looking forward to maintaining! :blush:

### Screenshots

<p align="center">
  <img alt="Issues over time graph" src="https://github.com/snyk-marcos/repo-images/blob/main/snyk-charts/16565355305053902issues_over_time_chart.png?raw=true" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Trending issues graph" src="https://github.com/snyk-marcos/repo-images/blob/main/snyk-charts/1656535539027444trending_issues_chart.png?raw=true" width="45%">
</p>

---

Made with :heart: by Marcos Bergami
