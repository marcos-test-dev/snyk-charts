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

    options = ["Issues over time", "Trending Issues"]
    cursor_style = ("fg_purple", "bold")
    terminal_menu = TerminalMenu(options, title="Please select your desired chart: \n", menu_cursor_style=cursor_style)
    menu_entry_index = terminal_menu.show()

    print("Loading   ", end="")

    # this logic could be turned into a function once chart options increase
    if (menu_entry_index == 0):
        endpoint = "https://snyk.io/api/v1/reporting/counts/issues?from=" + startDate + "&to=" + endDate + "&groupBy=severity"
    else:
        endpoint = "https://snyk.io/api/v1/reporting/issues/?from=" + startDate + "&to=" + endDate + "&page=1&perPage=100&sortBy=issueTitle&order=asc&groupBy=issue"

    response = api_request(apiToken, orgId, endpoint)

    if (menu_entry_index == 0):
        generate_issues_over_time(response)
    else:
        generate_issues_trending(response, startDate, endDate)


def generate_issues_over_time(obj):
    time_period = []

    low_count = []
    medium_count = [] 
    high_count = []
    critical_count = []

    print("\rLoading...", end="")

    while obj['results']:
        result = obj['results'].pop()
        date = result['day']
        time_period.append(date)
        severity = result['severity']
        critical_count.append(severity['critical'])
        high_count.append(severity['high'])
        medium_count.append(severity['medium'])
        low_count.append(severity['low'])
    
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

    # Edit the layout of the chart
    fig.update_layout(title='Issues over time',
                    xaxis_title='Month',
                    yaxis_title='Issues')


    print("Chart coming out of the oven!")

    saveChart = save_chart()

    # Save chart locally to images folder with unique name
    if (saveChart == 1):
        ts = str(time.time())
        ts = ts.replace(".","")
        fig.write_image("images/" + ts + "issues_over_time_chart.png")
    
    fig.show()

def generate_issues_trending(obj, startDate, endDate):
    issueList = []

    while obj['results']:
        result = obj['results'].pop()
        issue = result['issue']
        issueTitle = issue['title']
        issueList.append(issueTitle)
    
    df = pd.DataFrame(issueList, columns=["Issues"])

    issuesLabel = df["Issues"].value_counts().keys().tolist()
    issuesCount = df["Issues"].value_counts().tolist()

    fig = go.Figure([go.Bar(x=issuesLabel, y=issuesCount)])
    
    fig.update_layout(title="Trending issues " + startDate + " - " + endDate)
    
    saveChart = save_chart()

    # Save chart locally to images folder with unique name
    if (saveChart == 1):
        ts = str(time.time())
        ts = ts.replace(".","")
        fig.write_image("images/" + ts + "trending_issues_chart.png")
    
    fig.show()

def save_chart():
    options = ["No", "Yes"]
    cursor_style = ("fg_purple", "bold")
    terminal_menu = TerminalMenu(options, title="Would you like to save a copy of this chart now ? \n", menu_cursor_style=cursor_style)
    menu_entry_index = terminal_menu.show()
    
    # Save chart locally to images folder with unique name
    if (menu_entry_index == 1):
        return menu_entry_index

def api_request(apiToken, orgId, endpoint):
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

    return response

if __name__ == "__main__":
  main()