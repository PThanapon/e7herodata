import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import base64

app = dash.Dash(__name__)

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
        "E7 Hero Data Dashboard", 
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
            'width': '50%',  # Set the width of the left div to 50%
            'display': 'flex',  # Use flexbox for centering
            'justify-content': 'flex-end'  # Align the right edge to the center
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
            'width': '50%',  # Set the width of the right div to 50%
            'display': 'flex',  # Use flexbox for centering
            'justify-content': 'flex-start',  # Align the content to the left
            'flex-direction': 'column'  # Display content in a column layout
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
            aboutSection.scrollIntoView({ behavior: 'smooth', 'block': 'start' });
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
# Callback to update character image and comment
@app.callback(
    [Output('character-image', 'src'),  # Output to update the image source
     Output('character-comment', 'children'),  # Output to update the comment content
     Output('download-link', 'href'),  # Output to update the download link
     Output('character-image', 'style')],  # Output to update the image style
    [Input('filter-dropdown', 'value'),  # Input for selected filter
     Input('stat-dropdown', 'value'),  # Input for selected statistic
     Input('filter-and-stat', 'data')]  # Input for filter and statistic data from the Store
)
def update_image(selected_filter, selected_stat, filter_and_stat_data):
    if filter_and_stat_data is not None:
        selected_filter, selected_stat = filter_and_stat_data.split('-')

    if selected_filter == 'all':
        # When "All" is selected, display the default graph (e.g., "attack_averages.png")
        if selected_stat == "correlation":
            with open('plots/png/correlation.png', 'rb') as f:
                image_binary = base64.b64encode(f.read()).decode('utf-8')

            comment_filename = f'comments/correlation-comment.txt'
            image_style = {'width': '85%'}
        else:
            with open(f'plots/png/{selected_stat}_averages.png', 'rb') as f:
                image_binary = base64.b64encode(f.read()).decode('utf-8')

            comment_filename = f'comments/{selected_stat}-averages-comment.txt'
            image_style = {'width': '50%'}
        try:
            with open(comment_filename, 'r') as comment_file:
                comment = comment_file.read()
        except:
            comment = "Comment cannot be found"

        download_link = f'data:image/png;base64,{image_binary}'

        # Set the image style for 50% width using CSS
    else:
        # When other filters are selected, display the corresponding graph
        with open(f'plots/png/{selected_stat}-{selected_filter}.png', 'rb') as f:
            image_binary = base64.b64encode(f.read()).decode('utf-8')

        comment_filename = f'comments/{selected_stat}-{selected_filter}-comment.txt'

        try:
            with open(comment_filename, 'r') as comment_file:
                comment = comment_file.read()
        except:
            comment = "Comment cannot be found"

        download_link = f'data:image/png;base64,{image_binary}'

        # Reset the image style (remove the width property)
        image_style = {'width': '105%'}

    return (
        f'data:image/png;base64,{image_binary}',
        comment,
        download_link,
        image_style  # Pass the image style to the output
    )


# Callback to store the selected filter and stat when 'All' is selected

# Define a callback to update the statistic dropdown options and value based on the filter selection
@app.callback(
    [Output('stat-dropdown', 'options'),  # Output to update the dropdown options
     Output('stat-dropdown', 'value')],  # Output to update the selected value
    [Input('filter-dropdown', 'value')]  # Input for the selected filter
)
def update_stat_dropdown(selected_filter):
    if selected_filter == 'all':
        # When 'All' is selected, show 'Correlation' plus all eight stat options
        stat_options = [
            {'label': 'Attack', 'value': 'attack'},
            {'label': 'Health', 'value': 'health'},
            {'label': 'Defense', 'value': 'defense'},
            {'label': 'Crit Chance', 'value': 'crit chance'},
            {'label': 'Crit Damage', 'value': 'crit damage'},
            {'label': 'Effectiveness', 'value': 'effectiveness'},
            {'label': 'Effectiveness Resistance', 'value': 'effectiveness resistance'},
            {'label': 'Speed', 'value': 'speed'},
            {'label': 'Correlation', 'value': 'correlation'}  # Add 'Correlation' option
        ]
        selected_stat = 'correlation'  # Set the selected statistic to 'Correlation'
    else:
        # When a specific filter is selected, show only the eight stat options
        stat_options = [
            {'label': 'Attack', 'value': 'attack'},
            {'label': 'Health', 'value': 'health'},
            {'label': 'Defense', 'value': 'defense'},
            {'label': 'Crit Chance', 'value': 'crit chance'},
            {'label': 'Crit Damage', 'value': 'crit damage'},
            {'label': 'Effectiveness', 'value': 'effectiveness'},
            {'label': 'Effectiveness Resistance', 'value': 'effectiveness resistance'},
            {'label': 'Speed', 'value': 'speed'}
        ]
        selected_stat = 'attack'  # Set the selected statistic to 'Attack' as default

    # Return updated dropdown options and selected value
    return stat_options, selected_stat

if __name__ == "__main__":
    app.run_server(debug = True)
