<h3 align="center">
    Snyk Charts: Generate interactive charts derived from the Snyk API
</h3>

  <img alt="Last commit" src="https://img.shields.io/github/last-commit/snyk-marcos/snyk-charts">
</p>

## :bar_chart: Snyk Charts

Please note this is not an offical feature of Snyk. This was created as a hobby to be consumed and maintained by the community.

### Usage

To get started, clone the repository and install the necessary dependencies by running: `pip install -r requirements.txt`

Create a new file named `parameters.txt` following the structure below:

- **`ORGID=your-org-id`**
- **`TOKEN=your-snyk-token`**
- **`START_DATE=yyyy-mm-dd`**
- **`END_DATE=yyyy-mm-dd`**

Place your `parameters.txt` file in the root of the project

Run the script: `python snyk-charts.py`

Please feel free to contribute or suggest features. This is a side-project I am looking forward to maintaining! :blush:

---

Made with :heart: by Marcos Bergami