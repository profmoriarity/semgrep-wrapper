import argparse
import json
from jinja2 import Template
import os

# Define a command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Path to the input JSON file')
parser.add_argument('--output', required=True, help='Path to the output file')
parser.add_argument('--templates', required=True, help='Path to the template location')

# Parse the command-line arguments
args = parser.parse_args()


template = """
<!DOCTYPE html>
<html>
<head>
    <title>
        Semgrep - output
    </title>
    <style>
    body{
    background: lightgrey;
    }
    pre {
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
} 
pre, code {
        font-family: Consolas, monospace;
        font-size: 12px;
    }

    /* Set the background and border for the code snippet */
    pre {
        background-color: #f5f5f5;
        border: 1px solid #ccc;
        border-radius: 3px;
        padding: 16px;
    }

</style>
    <!-- CSS only -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>

</head>
<body>
<div class="container">
    <br><br>
    <h3> Semgrep Report ( {{ count }} potential vulnerabilties found)</h3>
    <hr>

    {% for result in results %}

<h4> Check for  {{ result.check_id }} </h4>

<p><strong>Description :</strong> {{ result['extra']['message']  }} </p>

<p> <strong>Source File :</strong> {{ result.path }} </p>
<p> Line<strong> start :</strong> {{ result.start.line }} </p>
<pre><code class="java">
    {{ result['extra']['lines'] | replace("\n","<br>") }}
    </code></pre>


{% if result['extra']['severity'] == "ERROR" %}
    <button type="button" class="btn btn-outline-danger">Severity: Critical</button>
{% elif result['extra']['severity'] == "WARNING" %}
    <button type="button" class="btn btn-outline-warning">Severity: High</button>
{% elif result['extra']['severity'] == "INFO" %}
    <button type="button" class="btn btn-outline-success">Severity: Low</button>
{% endif %}

 <button type="button" class="btn btn-danger">Tags: {{ result['extra']['metadata']['technology'] | join(', ') }}</button>
<br><br>
{% if result['extra']['metadata']['docs'] %}
Docs:  <a href="{{ result['extra']['metadata']['docs'] }}">  {{ result['extra']['metadata']['docs'] }}</a>
{% endif %}


{% if result['extra']['metadata']['references'] %}
<strong>References: </strong>
<ol>
{% for x in result['extra']['metadata']['references'] %}
<li><a href="{{ x }}">  {{ x }}</a></li>
{% endfor %}
</ol>
{% endif %}


{% if result['extra']['metadata']['cwe'] %}
<strong>CWE: </strong>
<ol>
{% for x in result['extra']['metadata']['cwe'] %}
<li> {{ x }}</li>
{% endfor %}
</ol>
{% endif %}

<hr>


{% endfor %}

</div>
</body>
</html>
"""




cmd = "semgrep -f {} --output {} --json {}".format(args.templates, args.output+".json", args.input)
print(cmd)
os.system(cmd)


with open(args.output+".json", 'r') as f:
    data = json.load(f)
    jdata = data['results']
    t = Template(template)
    count = len(jdata)
    output = t.render(data, count=count)
    with open(args.output, 'w') as f:
        f.write(output)

