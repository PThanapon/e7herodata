# Import necessary libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import base64

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    # Navigation and header
    
    # 'About' button with a link to the top-left corner of the page
    html.A(
        "About", 
        id='about-button',  # Unique identifier for the HTML element
        style={
            'position': 'absolute',  # Absolute positioning for custom placement
            'top': '10px',  # Distance from the top of the page
            'left': '10px',  # Distance from the left of the page
            'text-decoration': 'none',  # No underlining for the link
            'color': 'navy',  # Text color
            'font-weight': 'bold',  # Bold text
            'font-size': '20px',  # Font size
            'cursor': 'pointer'  # Cursor style (pointer indicates a clickable link)
        }
    ),
    
    # Header for the dashboard
    html.H1(
        "Character Data Dashboard", 
        style={
            'textAlign': 'center',  # Center-align text
            'color': 'navy',  # Text color
            'padding-top': '20px',  # Spacing from the top
            'cursor': 'pointer'  # Cursor style (pointer indicates a clickable link)
        }
    ),  
    
    # GitHub logo linking to the repository in the top-right corner of the page
    html.A(
        html.Img(src="assets/gh.webp", style={'width': '50px', 'height': '50px'}),
        href="https://github.com/PThanapon/e7herodata",  # GitHub repository URL
        target="_blank",  # Open link in a new tab
        style={
            'position': 'absolute',  # Absolute positioning for custom placement
            'top': '10px',  # Distance from the top of the page
            'right': '10px'  # Distance from the right of the page
        }
    ),
    
    # Dropdowns for selecting filter and statistics
    
    # Dropdown for selecting a character attribute filter
    dcc.Dropdown(
        id='filter-dropdown',  # Unique identifier for the dropdown
        options=[
            {'label': 'Rarity', 'value': 'rarity'},
            {'label': 'Class', 'value': 'class'},
            {'label': 'Horoscope', 'value': 'horoscope'},
            {'label': 'All', 'value': 'all'}  # Added 'All' option for selection
        ],
        value='rarity',  # Default selected value
        style={
            'width': '50%',  # Set the width of the dropdown
            'margin': '20px auto'  # Center-align the dropdown with margin
        }
    ),
    
    # Dropdown for selecting a character attribute statistic
    dcc.Dropdown(
        id='stat-dropdown',  # Unique identifier for the dropdown
        style={
            'width': '50%',  # Set the width of the dropdown
            'margin': '20px auto'  # Center-align the dropdown with margin
        }
    ),
    
    # Image and Comment display using a single div with display: flex
    
    # Div for displaying the character image and comment side by side
    html.Div([
        # Image display on the left
        html.Div([
            html.Img(
                id='character-image',  # Unique identifier for the image element
                src='',  # Image source (to be updated dynamically)
                style={'width': '100%'}  # Set the width of the image to 100%
            ),
        ], style={
            'width': '50%',  # Set the width of the left div
            'float': 'left'  # Float div to the left for side-by-side display
        }),
        
        # Comment display on the right
        html.Div([
            html.H3(
                "Comment",  # Header for the comment section
                style={'color': 'navy'}  # Text color
            ),
            html.Pre(
                id='character-comment',  # Unique identifier for the comment element
                style={'white-space': 'pre-wrap'}  # Preserve line breaks in text
            )
        ], style={
            'width': '50%',  # Set the width of the right div
            'float': 'right'  # Float div to the right for side-by-side display
        }),
    ], style={
        'display': 'flex'  # Use flexbox for side-by-side display of image and comment
    }),
    
    # Download image button
    
    # Button for downloading the character image
    html.Div([
        html.A(
            html.Button(
                "Download Image",  # Text for the button
                style={
                    'background-color': 'navy',  # Background color of the button
                    'color': 'white',  # Text color of the button
                    'border': 'none',  # No border for the button
                    'cursor': 'pointer',  # Cursor style (pointer indicates a clickable button)
                    'font-size': '16px',  # Font size of the button
                    'padding': '10px 20px'  # Padding for the button
                }
            ),
            id='download-link',  # Unique identifier for the download link
            download="image.png",  # File name for download
            href="",  # Download link URL (to be updated dynamically)
            target="_blank"  # Open link in a new tab
        ),
    ], style={
        'text-align': 'center',  # Center-align the button
        'margin-top': '10px'  # Margin from the top
    }),
    
    # About section
    
    # Section providing information about the dashboard
    html.Div([
        html.H2(
            "About",  # Header for the About section
            id='about-section',  # Unique identifier for the header element
            style={'color': 'navy', 'padding-top': '20px'}  # Text color and padding
        ),
        
        # Text describing the dashboard with a pointer cursor
        html.P(
            "Work in progress!",  # Text content
            id='about-content',  # Unique identifier for the text element
            style={'cursor': 'pointer'}  # Cursor style (pointer indicates a clickable text)
        ),
        
        # A placeholder div to adjust the height as needed
        html.Div(style={'height': '800px'})  # Adjust the height as needed
    ], style={
        'text-align': 'center'  # Center-align the About section
    }),
    
    # Back to top button
    
    # Button to scroll back to the top of the page
    html.A(
        "Back to Top",  # Text for the button
        id='back-to-top-button',  # Unique identifier for the button
        href="#",  # Link to the top of the page
        style={
            'position': 'fixed',  # Fixed positioning for the button
            'bottom': '10px',  # Distance from the bottom of the page
            'left': '10px',  # Distance from the left of the page
            'text-decoration': 'none',  # No underlining for the link
            'color': 'navy',  # Text color
            'font-weight': 'bold',  # Bold text
            'font-size': '16px'  # Font size
        }
    ),
    
    # Store for selected filter and stat
    
    # Data store to keep track of selected filter and statistic
    dcc.Store(id='filter-and-stat'),  # Unique identifier for the data store
])

# JavaScript code to scroll to the "about" section when the "About" button is clicked.

# Define a JavaScript callback function to scroll to the "about" section
app.clientside_callback(
    """
    function(clicks) {
        if (clicks > 0) {
            var aboutSection = document.getElementById('about-section');
            aboutSection.scrollIntoView({ behavior: 'smooth', block': 'start' });
        }
        return clicks;
    }
    """,
    Output('about-button', 'n_clicks'),  # Output to update the 'n_clicks' property of the 'about-button' element
    Input('about-button', 'n_clicks'),  # Input triggered by clicks on the 'about-button' element
    prevent_initial_call=True  # Add this line to prevent the initial call
)

# Callback to update character image and comment

# Define a callback to update the character image, comment, and download link
@app.callback(
    [Output('character-image', 'src'),  # Output to update the image source
     Output('character-comment', 'children'),  # Output to update the comment content
     Output('download-link', 'href')],  # Output to update the download link
    [Input('filter-dropdown', 'value'),  # Input for selected filter
     Input('stat-dropdown', 'value'),  # Input for selected statistic
     Input('filter-and-stat', 'data')]  # Input for filter and statistic data from the Store
)
def update_image(selected_filter, selected_stat, filter_and_stat_data):
    if filter_and_stat_data is not None:
        selected_filter, selected_stat = filter_and_stat_data.split('-')

    # Read and encode the character image file as base64
    with open(f'plots/png/{selected_stat}-{selected_filter}.png', 'rb') as f:
        image_binary = base64.b64encode(f.read()).decode('utf-8')

    # Define the file name for the character comment
    comment_filename = f'comments/{selected_stat}-{selected_filter}-comment.txt'

    try:
        # Try to open and read the character comment from a text file
        with open(comment_filename, 'r') as comment_file:
            comment = comment_file.read()
    except:
        # Handle the case where the comment file cannot be found
        comment = "Comment cannot be found"

    # Define the download link for the character image
    download_link = f'data:image/png;base64,{image_binary}'

    # Return updated image source, comment content, and download link
    return (
        f'data:image/png;base64,{image_binary}',  # Update the image source
        comment,  # Update the comment content
        download_link  # Update the download link
    )

# Callback to update stat dropdown options and value based on the filter dropdown

# Define a callback to update the statistic dropdown options and value based on the filter selection
@app.callback(
    [Output('stat-dropdown', 'options'),  # Output to update the dropdown options
     Output('stat-dropdown', 'value')],  # Output to update the selected value
    [Input('filter-dropdown', 'value')]  # Input for the selected filter
)
def update_stat_dropdown(selected_filter):
    if selected_filter == 'all':
        # When 'All' is selected, show 'Correlation' as the only statistic option
        stat_options = [{'label': 'Correlation', 'value': 'correlation'}]
        selected_stat = 'correlation'  # Set the selected statistic to 'Correlation'
    else:
        # When a specific filter is selected, show multiple statistic options
        stat_options = [
            {'label': 'Attack', 'value': 'attack'},
            {'label': 'Health', 'value': 'health'},
            {'label': 'Defense', 'value': 'defense'},
            {'label': 'Crit Chance', 'value': 'crit chance'},
            {'label': 'Crit Damage', 'value': 'crit damage'},
            {'label': 'Effectiveness', 'value': 'effectiveness'},
            {'label': 'Effectiveness Resistance', 'value': 'effectiveness resistance'},
            {'label': 'Speed', 'value': 'speed'},
        ]
        selected_stat = 'attack'  # Set the selected statistic to 'Attack'

    # Return updated dropdown options and selected value
    return stat_options, selected_stat

# Callback to store the selected filter and stat when 'All' is selected

# Define a callback to store the selected filter and statistic in the Store component when 'All' is selected
@app.callback(
    Output('filter-and-stat', 'data'),  # Output to update the data in the Store
    [Input('filter-dropdown', 'value'),  # Input for the selected filter
     Input('stat-dropdown', 'value')]  # Input for the selected statistic
)
def store_filter_and_stat(selected_filter, selected_stat):
    if selected_filter == 'all':
        # When 'All' is selected, store 'all-correlation' in the data
        return 'all-correlation'
    return f'{selected_filter}-{selected_stat}'  # Store the selected filter and statistic

