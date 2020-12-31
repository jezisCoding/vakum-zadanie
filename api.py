import connexion
import parser

# Create a swagger app with specification in ./
app = connexion.App(__name__, specification_dir="./")

# Add API from swagger yaml file definition.
# Resource routes are defined in the swagger file
app.add_api("swagger.yml")

# Home  
@app.route('/')
def home():
    return 'ahoj sanko'

if __name__ == "__main__":
    #data = parser.parse_dir("data")
    stromec = parser.parse_file("data/004/018004927.xml")
    stromec.write("stromec.xml")
    #app.run(host='localhost', port=5000, debug=True)
