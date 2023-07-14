class HTMLTableGenerationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


async def generate_html_table(data):
    # Create the HTML table header
    html = """
    <html>
        <head>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                
                th, td {
                    text-align: left;
                    padding: 8px;
                }
                
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
    """
    
    html += "<p style='text-align: center; font-weight: bold;'>Daily Employee Activities</p>"
    
    html += "<table>"
    html += "<thead><tr><th>Employees</th><th>Projects</th><th>Time Spent</th></tr></thead>"
    
    # Create the HTML table body
    html += "<tbody>"
    
    try:
        username = data['username']
        projects = data['projects']
        num_projects = len(projects)
        
        # Add a row for each project
        for i, project in enumerate(projects):
            if i == 0:
                # Only display the employee name in the first row
                html += f"<tr><td rowspan='{num_projects}'>{username}</td>"
            else:
                html += "<tr>"
            
            html += f"<td>{project['project_name']}</td>"
            html += f"<td>{project['tracked_time']}</td>"
            html += "</tr>"
        
        html += "</tbody>"
        html += "</table>"
        
        # Close the HTML tags
        html += "</body></html>"
        
        return html
    
    except Exception as e:
        raise HTMLTableGenerationError("Error occurred during HTML table generation.") from e
