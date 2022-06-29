import os
import requests
import time
import json
import pandas as pd
from getpass import getpass
import plotly.graph_objects as go
import pyfiglet
from simple_term_menu import TerminalMenu
from rich import print as rprint



def main():
    if not os.path.exists("images"):
        os.mkdir("images")
    
    with open("parameters.txt") as f:
        data = {}
        for line in f:
            key, value = line.strip().split("=")
            data[key] = value
    f.close()

    orgId = data['ORGID']
    apiToken = data['TOKEN']
    startDate = data['START_DATE']
    endDate = data['END_DATE']

    title = pyfiglet.figlet_format("Snyk Charts", font="slant")
    rprint("[bold magenta]" + title)
    rprint("[cyan]GENERATE INTERACTIVE CHARTS DERIVED FROM THE SNYK API[/cyan] \n \n")

    print("Loading   ", end="")

    selection = input("Which endpoint to follow ?")

    if selection == "old":
        endpoint = "https://snyk.io/api/v1/reporting/counts/issues?from=2022-05-01&to=2022-06-27&groupBy=severity"
    else:
        endpoint = "https://snyk.io/api/v1/reporting/issues/?from=2022-05-01&to=2022-06-27&page=1&perPage=100&sortBy=issueTitle&order=asc&groupBy=issue"

    # endpoint = "https://snyk.io/api/v1/reporting/counts/issues?from=" + 2017-07-01 + "&to=" + 2017-07-03 + "&groupBy=severity"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + apiToken
    }

    print("\rLoading.  ", end="")

    values = json.dumps({
        "filters": {
            "orgs": [orgId],
            "severity": [
            "critical",
            "high",
            "medium",
            "low"
            ],
            "types": [
            "vuln"
            # "license",
            # "configuration"
            ],
            "languages": [
            "node",
            "javascript",
            "ruby",
            "java",
            "scala",
            "python",
            "golang",
            "php",
            "dotnet",
            "swift-objective-c",
            "elixir",
            "docker",
            "linux",
            "dockerfile",
            "terraform",
            "kubernetes",
            "helm",
            "cloudformation"
            ],
            "projects": [],
            "ignored": False,
            "patched": False,
            "fixable": False,
            "isUpgradable": False,
            "isPatchable": False,
            "isPinnable": False,
            "priorityScore": {
            "min": 0,
            "max": 1000
            }
        }
    }, indent=4)

    print("\rLoading.. \n", end="")

    request = requests.request("POST", endpoint, headers=headers, data=values)
    response = request.json()

    if selection == "old":
        time_period = []

        low_count = []
        medium_count = [] 
        high_count = []
        critical_count = []

        print("\rLoading...", end="")

        while response['results']:
            result = response['results'].pop()
            date = result['day']
            time_period.append(date)
            severity = result['severity']
            critical_count.append(severity['critical'])
            high_count.append(severity['high'])
            medium_count.append(severity['medium'])
            low_count.append(severity['low'])

        print("Chart coming out of the oven!")
        fig = go.Figure()
        # Create and style traces
        fig.add_trace(go.Scatter(x=time_period, y=low_count, name='Low',
                                line=dict(color='gray', width=4)))
        fig.add_trace(go.Scatter(x=time_period, y=medium_count, name = 'Medium',
                                line=dict(color='burlywood', width=4)))
        fig.add_trace(go.Scatter(x=time_period, y=high_count, name = 'High',
                                line=dict(color='coral', width=4)))
        fig.add_trace(go.Scatter(x=time_period, y=critical_count, name = 'Critical',
                                line=dict(color='crimson', width=4)))

        # Edit the layout
        fig.update_layout(title='Issues over time',
                        xaxis_title='Month',
                        yaxis_title='Issues')

        ts = str(time.time())
        ts = ts.replace(".","")

        fig.write_image("images/" + ts + "chart.png")
        fig.show()
    else:
        issueList = []

        while response['results']:
            result = response['results'].pop()
            issue = result['issue']
            issueTitle = issue['title']
            issueList.append(issueTitle)
        
        df = pd.DataFrame(issueList, columns=["Issues"])

        issuesLabel = df["Issues"].value_counts().keys().tolist()
        issuesCount = df["Issues"].value_counts().tolist()

        fig = go.Figure([go.Bar(x=issuesLabel, y=issuesCount)])
        
        fig.update_layout(title="Trending issues " + startDate + " - " + endDate)

        fig.show()

        
        

if __name__ == "__main__":
  main()