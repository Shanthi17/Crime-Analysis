from flask import Flask, render_template, request, redirect, session, flash, get_flashed_messages
from flask_mail import *
from random import *
import psycopg2
from psycopg2 import sql
import datetime
import re
import json
import dash
#import dash_core_components as dcc
import ssl
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from base64 import standard_b64encode

# except ImportError:
#     from urlparse import urlparse
# import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import altair as alt
import pandas as pd
from preprocess import *
import source.connector as ct
import source.docreader as dr
from source.queries import parse_input, add_crime_ids, add_geo_attr, rem_attrs, dict_match_on_crime
from source.mapping import plot_map
from bokeh.embed import components
import os
from dotenv import load_dotenv
load_dotenv()

# from kafka import KafkaProducer, KafkaConsumer
# import logging
# Kafka setup
# KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
# TOPIC = 'flask_error_logs'
# KAFKA_URL = os.environ.get('KAFKA_URL')
# port = str(int(float(9096)))
# KAFKA_URL = "kafka+ssl://ec2-35-168-34-44.compute-1.amazonaws.com:9096"
# producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
# producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
# logger = logging.getLogger(__name__)
# import config

# Set Kafka environment variables
# kafka_url = os.environ.get('KAFKA_URL')
# kafka_cafile = os.environ.get('KAFKA_CERT')
# kafka_certfile = os.environ.get('KAFKA_CLIENT_CERT')
# kafka_keyfile = os.environ.get('KAFKA_CLIENT_CERT_KEY')
# kafka_topic = os.environ.get('KAFKA_TOPIC')

# # Set SSL context
# ssl_context = ssl.create_default_context()
# ssl_context.load_cert_chain(kafka_certfile, keyfile=kafka_keyfile)
# ssl_context.load_verify_locations(cafile=kafka_cafile)

# Set Kafka producer and consumer
# producer = KafkaProducer(
#     bootstrap_servers=[kafka_url],
#     security_protocol="SSL",
#     ssl_context=ssl_context,
#     value_serializer=lambda x: json.dumps(x).encode('utf-8')
# )
# consumer = KafkaConsumer(
#     kafka_topic,
#     bootstrap_servers=[kafka_url],
#     security_protocol="SSL",
#     ssl_context=ssl_context,
#     auto_offset_reset='earliest',
#     enable_auto_commit=True,
#     group_id='my-group',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )


# Define the database connection parameters
conn = psycopg2.connect(
    dbname=os.environ['db_name'],
    user=os.environ['user'],
    password=os.environ['db_password'],
    host=os.environ['host'],
    port=os.environ['port']
)

alt.renderers.set_embed_options(actions=False)
query = "SELECT * FROM ucr_crime_1975_2015;"
data_raw = pd.read_sql(query, conn)
# data_raw = pd.read_csv("data/raw/ucr_crime_1975_2015.csv")

def data_processing(data):
    data['state'] = data['ORI'].str[:2]
    query = "SELECT * FROM states;"
    states = pd.read_sql(query, conn)
    data_with_state = pd.merge(data, states, how = 'left', left_on = 'state', right_on = 'Abbreviation')
    data_with_state = data_with_state.drop(['state', 'Abbreviation', 'url', 'source'], axis = 1)
    return data_with_state

data_crime = data_processing(data_raw)
state_list = data_crime['State'].unique().tolist()
state_list = [state for state in state_list if str(state) != 'nan']

color_discrete_map={'(?)':'#B22222',
                    "Homicide": "#9467bd",
                    "Rape": "#ff7f0e",
                    "Larceny": "#2ca02c",
                    "Aggravated Assault": "#1f77b4"}


button_style_white = {'background-color': 'white', 'width': '48%', 'height': '75px', 'margin': '0.5px 2px', 'font-size': '10px'}
hom_button = {'background-color': "#9467bd", 'width': '48%', 'height': '75px', 'margin': '0.5px 2px', 'font-size': '14px'}
larc_button = {'background-color': "#2ca02c",  'width': '48%', 'height': '75px', 'margin': '0.5px 2px', 'font-size': '14px'}
rape_button = {'background-color': "#ff7f0e",  'width': '48%', 'height': '75px', 'margin': '0.5px 2px', 'font-size': '14px'}
agg_button = {'background-color': "#1f77b4",  'width': '48%', 'height': '75px', 'margin': '0.5px 2px', 'font-size': '10px'}
# new code end

app = Flask(__name__)
app.secret_key = 'AppSecretKey'
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465     
app.config["MAIL_USERNAME"] = os.environ['mail_username'] 
app.config['MAIL_PASSWORD'] = os.environ['mail_password']
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  


# def get_kafka_ssl_context():
#     """
#     Returns an SSL context based on the certificate information in the Kafka config vars.
#     """
#     # NOTE: We assume that Kafka environment variables are present. If using
#     # Apache Kafka on Heroku, they will be available in your app configuration.
#     #
#     # 1. Write the PEM certificates necessary for connecting to the Kafka brokers to physical
#     # files.  The broker connection SSL certs are passed in environment/config variables and
#     # the python and ssl libraries require them in physical files.  The public keys are written
#     # to short lived NamedTemporaryFile files; the client key is encrypted before writing to
#     # the short lived NamedTemporaryFile
#     #
#     # 2. Create and return an SSLContext for connecting to the Kafka brokers referencing the
#     # PEM certificates written above
#     #

#     # stash the kafka certs in named temporary files for loading into SSLContext.  Initialize the
#     # SSLContext inside the with so when it goes out of scope the files are removed which has them
#     # existing for the shortest amount of time.  As extra caution password
#     # protect/encrypt the client key
#     with NamedTemporaryFile(suffix='.crt') as cert_file, \
#          NamedTemporaryFile(suffix='.key') as key_file, \
#          NamedTemporaryFile(suffix='.crt') as trust_file:
#         cert_file.write(os.environ['KAFKA_CLIENT_CERT'].encode('utf-8'))
#         cert_file.flush()

#         # setup cryptography to password encrypt/protect the client key so it's not in the clear on
#         # the filesystem.  Use the generated password in the call to load_cert_chain
#         passwd = standard_b64encode(os.urandom(33))
#         private_key = serialization.load_pem_private_key(
#             os.environ['KAFKA_CLIENT_CERT_KEY'].encode('utf-8'),
#             password=None,
#             backend=default_backend()
#         )
#         pem = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.BestAvailableEncryption(passwd)
#         )
#         key_file.write(pem)
#         key_file.flush()

#         trust_file.write(os.environ['KAFKA_TRUSTED_CERT'].encode('utf-8'))
#         trust_file.flush()

#         # create an SSLContext for passing into the kafka provider using the create_default_context
#         # function which creates an SSLContext with protocol set to PROTOCOL_SSLv23, OP_NO_SSLv2,
#         # and OP_NO_SSLv3 when purpose=SERVER_AUTH.
#         ssl_context = ssl.create_default_context(
#             purpose=ssl.Purpose.SERVER_AUTH, cafile=trust_file.name)
#         ssl_context.load_cert_chain(cert_file.name, keyfile=key_file.name, password=passwd)

#         # Intentionally disabling hostname checking.  The Kafka cluster runs in the cloud and Apache
#         # Kafka on Heroku doesn't currently provide stable hostnames.  We're pinned to a specific certificate
#         # for this connection even though the certificate doesn't include host information.  We rely
#         # on the ca trust_cert for this purpose.
#         ssl_context.check_hostname = False

#     return ssl_context


# def get_kafka_brokers():
#     """
#     Parses the KAKFA_URL and returns a list of hostname:port pairs in the format
#     that kafka-python expects.
#     """
#     # NOTE: The Kafka environment variables need to be present. If using
#     # Apache Kafka on Heroku, they will be available in your app configuration.
#     if not os.environ.get('KAFKA_URL'):
#         raise RuntimeError('The KAFKA_URL config variable is not set.')

#     return ['{}:{}'.format(parsedUrl.hostname, parsedUrl.port) for parsedUrl in
#             [urlparse(url) for url in os.environ.get('KAFKA_URL').split(',')]]


# producer = KafkaProducer(
#         bootstrap_servers=get_kafka_brokers(),
#         security_protocol='SSL',
#         ssl_context=get_kafka_ssl_context(),
#         acks=all
#     )
# new code start
def create_dashapp(app):
    app1 = dash.Dash(server=app, external_stylesheets=[dbc.themes.BOOTSTRAP], routes_pathname_prefix="/dash/")
    app1.title = "Crime in United States"
    server = app1.server
    tab_height = '5vh'
    # Set the layout  
    app1.layout = dbc.Container([
    html.H1("Crime in United States",
    style = {
        'padding' : 20,
        'color': 'firebrick',
        'margin-top': 20,
        'margin-bottom': 20,
        'text-align': 'center',
        'font-size': '48px',
        'border-radius': 3,
        'font-family':'Georgia, Times, serif'
    }),
    dbc.Row([
        dbc.Col([
            html.Div('State:'),
            html.Br(),
            dcc.Dropdown(
                id = 'state',
                options = [{'label': col, 'value': col} for col in state_list], 
                value = state_list,
                multi=True,
                style = {'border': '2px solid black'}),
            html.Br(),
            html.Br(),
            html.Div('Crime:'),
            html.Br(),
            html.Button('Homicide', id='hom_click', n_clicks=0, style = hom_button),
            html.Button('Rape', id='rape_click', n_clicks=0, style = rape_button),
            html.Br(),
            html.Br(),
            html.Button('Larceny', id='larc_click', n_clicks=0, style = larc_button),
            html.Button('Aggravated Assault', id='agg_click', n_clicks=0, style = agg_button),
            html.Br(),
            html.Br(),
            html.Div('Crime Metric:'),
            dcc.Dropdown(
                id = 'metric',
                options=[
                {'label': 'Rate (Crimes per 100k People)', 'value': 'Crime Rate (Crimes Committed Per 100,000 People)'},
                {'label': 'Number of Crimes Committed', 'value': 'Number of Crimes Committed'}
                ],
                value = 'Crime Rate (Crimes Committed Per 100,000 People)',
                clearable=False,
                style = {'border': '2px solid black'}
            ),
            html.Br(),
            html.Br(),
            html.Div('Year Range:'),
            html.Br(),
            dcc.RangeSlider(
                id = 'year_range',
                min=1975, 
                max=2015, 
                marks={1975: '1975', 1985: '1985', 1995: '1995', 2005: '2005', 2015: '2015'},
                value=[data_crime['year'].min(), data_crime['year'].max()]
                ),
        ], md= 3,
        style = {
            'background-color' : '#e6e6e6',
            'padding' : 15,
            'border' : '8px solid black'
        }),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Crime Rate/Crime Count By Region",
                style = {'background-color': '#B22222','textAlign': 'center', 'font-weight': 'bold'}),
                dbc.CardBody(
                    html.Iframe(
                        id = 'geochart',
                        style = {'border-width':'0', 'width': '125%', 'height': '400px', 'margin-top': '0', 'margin-left': '-5%'})
                )
            ], style={'border': 'none'}),
            html.Br(),
            dbc.Card([
                dbc.CardHeader("Crime Rate/Crime Count Over the Years",
                style = {'background-color': '#B22222','textAlign': 'center', 'font-weight': 'bold', 'font-size': '16px'}),
                dbc.CardBody(
                    html.Iframe(
                        id = 'trendchart',
                        style = {'border-width':'0', 'width': '125%', 'height': '400px'}),
                        style = {'margin-top': '0', 'margin-bottom' : '0', 'height': '400px'}
                )
            ], style={'border': 'none'})
        ], md = 6),
        dbc.Col([
            dbc.Card([dbc.CardHeader("Distribution of Crime Based On:",
                style = {'background-color': '#B22222','textAlign': 'center', 'font-weight': 'bold', 'font-size': '16px', 'border-bottom': 'none'}),
                dbc.CardBody(
                    dbc.Tabs(
                [
                    dbc.Tab(label="Crime Type", tab_id="tab-1",
                            tab_style={"width": "50%"}, label_style={"color": "black"}),
                    dbc.Tab(label="State", tab_id="tab-2",
                            tab_style={"width": "50%"}, label_style={"color": "black"}),
                ],
                id="card-tabs",

                # card=True,
                ##card=True,
                active_tab="tab-1",
                style={'border' : '0px', 'background-color': '#B22222', 'height':tab_height}
            ), style = {'background-color': '#B22222','textAlign': 'center', 'font-weight': 'bold', 'padding-top' : '0'}),
                dbc.CardBody(html.P(id="card-content", className="card-text"), style = {"padding": '0', 'height': '100%'}),
            ], style={'border': '2 px solid white'}),
        ], md = 3)
    ]), html.Hr()])
    # html.P([f'''
    # This dashboard was made by. ''',
    # ''' The city-crimes dataset collected as part of The Marshall Project has been used. Here is the link to the code: '''])
    # ], style = {'max-width': '90%'})
    # Registering callbacks
    @app1.callback(
        Output("card-content", "children"), [Input("card-tabs", "active_tab")]
    )
    def tab_content(active_tab):
        if active_tab == "tab-1":
            return dcc.Graph(id = "treemap",  style = {'border-width':'0', 'width': '125%', 'height': '1000px', 'margin-left':'-13%'})
        elif active_tab == "tab-2":
            return dcc.Graph(id = "treemap_2",  style = {'border-width':'0', 'width': '125%', 'height': '1000px', 'margin-left':'-13%'})

    @app1.callback(
        Output('geochart', 'srcDoc'),
        Input('state', 'value'),
        Input('year_range', 'value'),
        Input('metric', 'value'),
        Input('hom_click', 'n_clicks'),
        Input('rape_click', 'n_clicks'),
        Input('larc_click', 'n_clicks'),
        Input('agg_click', 'n_clicks')
    )
    def plot_geochart(state, year_range, metric, hom_click, rape_click, larc_click, agg_click):
        print('You have selected "{}"'.format(state))
        print('You have selected "{}"'.format(year_range))
        # print('You have selected "{}"'.format(crime))

        crime = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']
        if hom_click % 2  != 0:
            crime.remove('Homicide')
        if rape_click % 2  != 0:
            crime.remove('Rape')
        if larc_click % 2  != 0:
            crime.remove('Larceny')
        if agg_click % 2  != 0:
            crime.remove('Aggravated Assault')
        if not crime:
            crime = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']

        if not state:
            state = state_list

        results_df = data_filtering_geochart(state, crime, metric, year_range, data_crime)
        states = alt.topo_feature(data.us_10m.url, 'states')
        
        geo_chart = alt.Chart(states).mark_geoshape(stroke = 'black', tooltip = True).transform_lookup(
        lookup='id',
        from_=alt.LookupData(results_df, 'id', ['crime_count'])
        ).transform_calculate(
            crime_count = 'isValid(datum.crime_count) ? datum.crime_count : -1'
        ).encode(color = alt.condition(
            'datum.crime_count > 0',
            alt.Color('crime_count:Q', scale = alt.Scale(scheme = 'reds'), title = metric),
            alt.value('#dbe9f6')
        )).properties(width=500, height=300
        ).project(type='albersUsa'
        ).configure_view(strokeWidth = 0)
        geo_chart = geo_chart.configure_legend(orient='none', direction= "horizontal",
                                        legendX=45, legendY= 300, gradientVerticalMinLength = 400,
                                        titleAnchor= alt.TitleAnchor('middle'), titleLimit=350)
        return geo_chart.to_html()

    @app1.callback(
        Output('trendchart', 'srcDoc'),
        Input('state', 'value'),
        Input('year_range', 'value'),
        Input('metric', 'value'),
        Input('hom_click', 'n_clicks'),
        Input('rape_click', 'n_clicks'),
        Input('larc_click', 'n_clicks'),
        Input('agg_click', 'n_clicks')
    )

    def trend_chart(state, year_range, metric, hom_click, rape_click, larc_click, agg_click):
        crime = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']
        if hom_click % 2  != 0:
            crime.remove('Homicide')
        if rape_click % 2  != 0:
            crime.remove('Rape')
        if larc_click % 2  != 0:
            crime.remove('Larceny')
        if agg_click % 2  != 0:
            crime.remove('Aggravated Assault')
        if not crime:
            crime = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']

        if not state:
            state = state_list

        crime_metric = "Crime Rate"
        if metric == 'Number of Crimes Committed':
            crime_metric = "Crime Count"

        trend_chart_df = data_filtering_trendchart(state, crime, metric, year_range, data_crime)

        chart = alt.Chart(trend_chart_df).encode(
            alt.X('year', title = "Year", axis=alt.Axis(format="d", tickCount=10)),
            alt.Y('crime_count', title = metric),
            alt.Color('crime', title = 'Crime', legend = None,
                        scale = alt.Scale(
                            domain=crime,
                            range=[color_discrete_map[c] for c in crime])),
            tooltip=[alt.Tooltip('crime_count', title=crime_metric, formatType="number", format=".0f"),
                    alt.Tooltip('crime', title='Crime Type'),
                    alt.Tooltip('year', title='Year')])

        trend_plot = chart.mark_line(size=3) + chart.mark_circle(size=30)
        return trend_plot.to_html()

    @app1.callback(
        Output('treemap', 'figure'),
        Input('state', 'value'),
        Input('year_range', 'value'),
        Input('metric', 'value'),
        Input('hom_click', 'n_clicks'),
        Input('rape_click', 'n_clicks'),
        Input('larc_click', 'n_clicks'),
        Input('agg_click', 'n_clicks')
    )
    def tree_map(state, year_range, metric, hom_click, rape_click, larc_click, agg_click):

        crime_selected = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']
        if hom_click % 2  != 0:
            crime_selected.remove('Homicide')
        if rape_click % 2  != 0:
            crime_selected.remove('Rape')
        if larc_click % 2  != 0:
            crime_selected.remove('Larceny')
        if agg_click % 2  != 0:
            crime_selected.remove('Aggravated Assault')
        if not crime_selected:
            crime_selected = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']

        if not state:
            state = state_list
        tree_map = data_filtering_treemap(state, crime_selected, metric, year_range, data_crime)
        tree_map['more_crimes'] = tree_map['crime']
        fig = px.treemap(
            tree_map,
            path=['crime', 'State'],
            values = 'crime_count',
            color = 'crime',
            color_discrete_map=color_discrete_map
        )
        fig.update_layout(margin_l= 50, margin_r=50,margin_t=10)

        return fig

    @app1.callback(
        Output('treemap_2', 'figure'),
        Input('state', 'value'),
        Input('year_range', 'value'),
        Input('metric', 'value'),
        Input('hom_click', 'n_clicks'),
        Input('rape_click', 'n_clicks'),
        Input('larc_click', 'n_clicks'),
        Input('agg_click', 'n_clicks')
    )
    def tree_map_2(state, year_range, metric, hom_click, rape_click, larc_click, agg_click):

        crime_selected = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']
        if hom_click % 2  != 0:
            crime_selected.remove('Homicide')
        if rape_click % 2  != 0:
            crime_selected.remove('Rape')
        if larc_click % 2  != 0:
            crime_selected.remove('Larceny')
        if agg_click % 2  != 0:
            crime_selected.remove('Aggravated Assault')
        if not crime_selected:
            crime_selected = ['Homicide', 'Rape', 'Larceny', 'Aggravated Assault']

        if not state:
            state = state_list
        tree_map = data_filtering_treemap_2(state, crime_selected, metric, year_range, data_crime)
        tree_map['more_crimes'] = tree_map['crime']
        fig = px.treemap(
            tree_map,
            path=['State', 'crime'],
            values = 'crime_count',
            color = 'crime',
            color_discrete_map=color_discrete_map
        )
        fig.update_layout(margin_l= 50, margin_r=50, margin_t=10)
        return fig

    @app1.callback(
        Output('larc_click', 'style'),
        Output('hom_click', 'style'),
        Output('rape_click', 'style'),
        Output('agg_click', 'style'),
        Input('hom_click', 'n_clicks'),
        Input('rape_click', 'n_clicks'),
        Input('larc_click', 'n_clicks'),
        Input('agg_click', 'n_clicks'))
    def all_button_style(clicks_hom, clicks_rape, clicks_larc, clicks_agg):

        if (clicks_hom % 2  != 0):
            hom_but = button_style_white
        else:
            hom_but = hom_button

        if clicks_rape % 2  != 0:
            rape_but = button_style_white
        else:
            rape_but = rape_button

        if clicks_larc % 2  != 0:
            larc_but = button_style_white
        else:
            larc_but = larc_button

        if clicks_agg % 2  != 0:
            agg_but = button_style_white
        else:
            agg_but = agg_button

        if ((clicks_hom % 2  != 0) & (clicks_rape % 2  != 0) & (clicks_larc % 2  != 0) & (clicks_agg % 2  != 0)):
            return larc_button, hom_button, rape_button, agg_button
        
        return larc_but, hom_but, rape_but, agg_but
    return app1
# new code end

create_dashapp(app)
mail = Mail(app)  


# user = {"username": "admin", "password": "password"}

@app.route('/')
def index():
    #return render_template("verify.html")
    messages = get_flashed_messages()
    return redirect('/login')

@app.route('/forgot_password',methods = ["POST"])  
def verify():  
    email = request.form["email"]  
      
    msg = Message('OTP',sender = 'riso2414@gmail.com', recipients = [email])  
    otp = randint(000000,999999)
    session['otp'] = otp  # Store the OTP in the session
    msg.body = str(otp)
    try:
        mail.send(msg)
        return render_template('verify.html')  
    except Exception as e:
        print(str(e))
        return "<h3>Something went wrong while sending the email.</h3>"  
 

@app.route('/validate',methods=["POST"])  
def validate():  
    user_otp = request.form['otp']  
    if 'otp' in session and session['otp'] == int(user_otp):  
        return render_template("reset_password.html") 
    else:
        flash('Invalid OTP')
        return render_template("verify.html")

@app.route('/reset_password' , methods= ["POST", "GET"])
def reset_password_request():
    email_entered = request.form.get('password')
    confirm_email_entered = request.form.get('confirm_password')

    # check wether if email enteres is same
    if str(email_entered) == str(confirm_email_entered):

        ## write the SQL Code for inserting the password for user
        ##
        ##
        ## by @Shanthi

        flash("Your Password Has been reset")
        return redirect('/login')
    else :
        flash('Passwords do not match')
        return render_template("reset_password.html")  

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        # password = "mendak"
        '''
            Code for Searching in the database and delete the code below
        '''    
        # Create a cursor
        cur = conn.cursor()

        # Use the cursor to execute the SELECT statement
        cur.execute(
            sql.SQL("SELECT * FROM UserData WHERE username = %s AND password = %s"),
            [username, password]
        )

        # Fetch the result of the SELECT statement
        user = cur.fetchone()

        # Close the cursor
        cur.close()

        # If the result is not None, the login was successful
        if user is not None:
            # Set the session variable for the user
            session['username'] = user[1]
            # Redirect to the home page
            return redirect('/dashboard')
        else:
            # raise ValueError('Hiii!!!')
            return render_template("login.html", error="Invalid credentials") 

    return render_template("login.html")

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # Code for forgot password functionality goes here
    return render_template("forgot_password.html")



@app.route('/register', methods = ['POST', 'GET'])
def register():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')

        # Check for valid email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("register.html", error="Invalid email address")

        username = request.form.get('username')

        # Check for valid username
        if len(username) < 8 or len(username) > 12:
            return render_template("register.html", error="Length of username should be 8 to 12 characters")
        
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        ## check if the passwords are same
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")
        
        # Use datetime to create the current date and time
        now = datetime.datetime.now()

        # Format the current date and time as a string in the desired format
        created_on = now.strftime('%Y-%m-%d %H:%M:%S')

        # Create a cursor
        cur = conn.cursor()

        # Use the cursor to execute the INSERT statement
        cur.execute(
            sql.SQL("INSERT INTO UserData (username, name, password, email, created_on) VALUES (%s, %s, %s, %s, %s)"),
            [username, name, password, email, created_on]
        )

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cur.close()

        # Set the session variable for the user
        session['username'] = username
        return redirect('/dashboard')
    
    return render_template('register.html')



@app.route('/dashboard')
def dashboard():
    if('username' in session):
        return render_template('dashboard.html')
    return redirect('/login')

# Define dashapp route
@app.route('/dash/')
def redirect_to_dashapp():
    if('username' in session):
        return redirect('/dash/')
    return redirect('/login')

@app.route('/logout')
def logout():
    # Remove the session variable for the user
    if 'username' in session:
        session.pop('username', None)
    return redirect('/login')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('imp_contacts.html')


@app.route('/denver', methods=['GET', 'POST'])
def denver():
    if request.method == 'POST':
        form = request.form
        formfilters, queryfilters = parse_input(form)
        crime_db = ct.MongoConnector()
        mongo_db = crime_db.startup_db_client()
        crime_codes = dr.mongo_read()
        query = { '$and': [item for item in queryfilters] }
        #print(query)
        # query = { '$and': [{"GEO_LAT": 39.7616457} , {"GEO_LON": -105.0241665}] }
        # query = { 'OFFENSE_CODE': 3501, 'OFFENSE_CODE_EXTENSION': 0}
        query_attributes = formfilters
        query_attributes = add_crime_ids(query_attributes)
        query_attributes = add_geo_attr(query_attributes)
        # query_attributes = None
        # query = { 'incident_id': 2017421909} 

        query_list = crime_codes.db_find(mongo_db, 'Crime', 'Denver_Crime', query, query_attributes)
        query_list = dict_match_on_crime(mongo_db,query_list,query_attributes)
        
        remove_attributes = ['OFFENSE_CODE', 'OFFENSE_CODE_EXTENSION', 'OFFENSE_TYPE_ID']
        query_list = rem_attrs(query_list, remove_attributes)
        #print(query_list)

        if len(query_list) == 0:
            noquery = pd.DataFrame.from_dict([{'Welcome': 'queries.  Please enter a new query.'}])

            return render_template('index.html', tables = [noquery.to_html(classes="data")], titles=noquery.columns.values)
        # crime_codes.print_records(query_list)
        query_final = query_list
        df = pd.DataFrame(query_list)
        df.fillna('', inplace=True)
        
        map = plot_map(df, 1,1)
        script, div = components(map)

        query_final = rem_attrs(query_final, ['GEO_LON', 'GEO_LAT'])
        df = pd.DataFrame(query_final)
        df.fillna('', inplace=True)

        try:
            return render_template('index.html',  tables=[df.to_html(classes="data")], script=script, div=div)
        except:
            return render_template('index.html',  tables=[df.to_html(classes="data")])
    else:
        return render_template('index.html',  tables=[])

# @app.errorhandler(Exception)
# def log_and_render_error(e):
#     logger.exception(e)
#     # Send error message to Kafka topic
#     producer.send(TOPIC, str(e).encode('utf-8'))
#     # Render error message on webpage
#     return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Set the host to 0.0.0.0 to allow external connections
        port=int(os.environ.get("PORT", 8080)),  # Set the port to 8050 (or any other desired port)
        debug=True
    )