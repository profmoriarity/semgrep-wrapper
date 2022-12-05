# semgrep-wrapper - Generate Semgrep HTML Reports 
The purpose of this tool is to run semgrep and generate HTML templates. Semgrep has no option to produce HTML reports all by itself. The tool executes semgrep on give source directory using templates provided and generates a decent HTML report.

## Run

```
$ python3 parse-semgrep.py --input /mnt/d/Dev/dvja-master --output /mnt/d/Dev/dvja-master/out.html --templates /mnt/d/Dev/semgrep-rules-develop/semgrep-rules-develop/java/
```

### Requirements

```
pip3 install jinja2
```

## Example Report
![image](https://user-images.githubusercontent.com/35167539/205737643-562ec6dc-a6f4-4fe9-b35e-34b974513f1f.png)

